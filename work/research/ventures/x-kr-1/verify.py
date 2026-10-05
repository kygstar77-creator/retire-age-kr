# X-KR-1 검산: 엑셀(실제 Excel로 재계산) ↔ firemap 운영 식(node, src/utils/retirementSimulator.js) 나란히 → checks.md
#   py -3.12 verify.py      (make_xlsx.py 로 out/ 파일을 먼저 만든다. 미리보기 PDF도 여기서 뽑는다)
import os, sys, json, subprocess
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
sys.path.insert(0, HERE)
from make_xlsx import CASES  # noqa: E402

PS = r'''
$dir = "%s"
$x = New-Object -ComObject Excel.Application; $x.DisplayAlerts = $false
$res = @{}
foreach ($f in "case_1","case_2","case_3","가계부_은퇴나이_2026") {
  $wb = $x.Workbooks.Open("$dir\$f.xlsx", 0, $true); Start-Sleep -Seconds 2
  $c = $wb.Worksheets.Item("계산"); $s1 = $wb.Worksheets.Item("월 가계부"); $s2 = $wb.Worksheets.Item("은퇴 나이")
  $o = @{}; foreach ($a in "B6","B7","B8","B9","B37","C37","D37","B93","C93","B149","D149","B20","B30","B31","B32") { $o[$a] = $c.Range($a).Value2 }
  $o["lines"] = @(); foreach ($r in 3..22) { if ($s1.Range("B$r").Value2) { $o["lines"] += ,@($s1.Range("B$r").Value2, $s1.Range("C$r").Value2, $s1.Range("E$r").Text) } }
  $o["s2"] = @{ B4 = $s2.Range("B4").Text; B7 = $s2.Range("B7").Text; B10 = $s2.Range("B10").Text; D10 = $s2.Range("D10").Text; F10 = $s2.Range("F10").Text }
  if ($f -like "가계부*") { $s2.ExportAsFixedFormat(0, "$dir\preview_sheet2.pdf"); $s1.ExportAsFixedFormat(0, "$dir\check_sheet1.pdf")
    # 대표 이미지 2장째(실제 시트 화면, 순돌이 10/5 ③): 시트 2 B2:H50을 그림으로 복사 → 빈 차트에 붙여 PNG
    foreach ($pair in @(@("은퇴 나이","A1:H50","sheet2.png"), @("월 가계부","A1:K16","sheet1.png"))) {
      $ws = $wb.Worksheets.Item($pair[0]); $ws.Activate() | Out-Null; $rg = $ws.Range($pair[1])
      $rg.CopyPicture(1, 2) | Out-Null
      $co = $ws.ChartObjects().Add(0, 0, $rg.Width, $rg.Height); $co.Activate() | Out-Null; Start-Sleep -Milliseconds 500
      $co.Chart.Paste() | Out-Null; $co.Chart.Export("$dir\" + $pair[2]) | Out-Null; $co.Delete() | Out-Null }
  }
  $res[$f] = $o; $wb.Close($false)
}
$x.Quit()
$res | ConvertTo-Json -Depth 6 | Out-File -Encoding utf8 "$dir\excel_raw.json"
'''


def excel():
    ps1 = os.path.join(OUT, 'excel_read.ps1')
    open(ps1, 'w', encoding='utf-8-sig').write(PS % OUT)  # BOM 있어야 PowerShell 5.1이 한글 경로를 읽는다
    subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ps1], check=True)
    return json.load(open(os.path.join(OUT, 'excel_raw.json'), encoding='utf-8-sig'))


def main():
    ref = json.loads(subprocess.run(['node', os.path.join(HERE, 'ref.mjs')], capture_output=True, text=True, check=True).stdout)
    xl = excel()
    json.dump(xl, open(os.path.join(OUT, 'excel_values.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    rows, ok = [], True
    for n in (1, 2, 3):
        e, w = xl[f'case_{n}'], ref[str(n)]
        age, asset, r, i, inc, m, mp = CASES[n]
        checks = [('은퇴 나이(해 단위)', e['B37'], w['earliest']), ('월 지출 +10만', e['B93'], w['earliest_plus100k']),
                  ('지난달 지출로', e['B149'], w['earliest_prev'])]
        for lab, a, b in checks:
            good = a == b
            ok &= good
            rows.append(f'| {n} | {lab} | {a}세 | {b}세 | {a - b} | {"통과" if good else "다름"} |')
        diff = e['B32'] - w['required']
        good = abs(diff) <= max(1000, w['required'] * 1e-6)
        ok &= good
        rows.append(f'| {n} | 필요 자산 | {e["B32"]:,.0f}원 | {w["required"]:,.0f}원 | {diff:+,.0f}원 | {"통과" if good else "다름"} |')
        good = e['B30'] == f'{w["earliest"]}세'  # 큰 숫자 = 웹과 같은 해 단위(본부장 판정 10/1)
        ok &= good
        rows.append(f'| {n} | 엑셀 큰 숫자(해 단위) | {e["B30"]} | {w["earliest"]}세 | {"0" if good else "다름"} | {"통과" if good else "다름"} |')
    ex = xl['가계부_은퇴나이_2026']
    md = [
        '# X-KR-1 검산 — 엑셀 ↔ 파이어맵 운영 식 (firemap-venture-builder, verify.py 자동 생성)',
        '',
        '- 엑셀 값: Microsoft Excel 16(COM)으로 파일을 열어 재계산한 값. 웹 값: `node ref.mjs` — `src/utils/retirementSimulator.js` 의 `findEarliestRetirementAge()`·`findRequiredAssetNow()` 를 그대로 불러 씀.',
        '- 같은 조건: 국민연금 0 · 국내 투자(세금 0) · 부업·임대 0 · 급여 상승 0 · 90세까지 · 월 저축 = 최근 달 수입 − 지출.',
        '- 통과 기준(brief): 1년 안. 해 단위 나이는 **같아야** 통과로 더 세게 잡았다.',
        '',
        '| 예시 | 항목 | 엑셀 | 웹 식 | 차이 | 판정 |',
        '|---|---|---|---|---|---|',
        *rows,
        '',
        '예시 입력: ' + ' / '.join(f'{n}) {a}세·자산 {s / 1e4:,.0f}만·수익 {r}%·물가 {i}%·월 수입 {inc / 1e4:,.0f}만·지출 {m / 1e4:,.0f}만(지난달 {mp / 1e4:,.0f}만)'
                                   for n, (a, s, r, i, inc, m, mp) in CASES.items()),
        '',
        f'- 참고: 웹 계산기 기본값(국민연금 월 100만원)을 켜면 예시 1·2·3은 {ref["1"]["earliest_webdefault_pension"]}·{ref["2"]["earliest_webdefault_pension"]}·{ref["3"]["earliest_webdefault_pension"]}세. 엑셀은 연금을 넣지 않아 그보다 늦다 → 시트 3 \'계산 가정\'에 적음.',
        f'- 판매 파일(예시 줄 9·10월) 큰 숫자 \'{ex["B30"]}\' · {ex["B31"]} · 필요 자산 {ex["B32"]:,.0f}원 · +N일 기울기 {ex["B20"]:.6f}일/원',
        '- 예시 줄 +N일: ' + ', '.join(f'{a} {int(b):,}원 {c}' for a, b, c in ex['lines'][9:] if c),
        '',
        f'**결과: {"전부 통과" if ok else "다름 있음 — 식을 다시 본다"}**',
    ]
    open(os.path.join(HERE, 'checks.md'), 'w', encoding='utf-8').write('\n'.join(md) + '\n')
    print('\n'.join(md))
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
