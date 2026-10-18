# '내 연봉 상위 몇 %' 엑셀 검산 (firemap-write, 2026-10-18)
#   py -3.12 verify.py
# 1) make_xlsx.py로 파일을 다시 만든다.
# 2) Microsoft Excel(COM, PowerShell)로 열어 입력 칸(C4)을 바꿔 가며 다시 계산한 값을 읽는다. 이 스크립트가 띄운 Excel만 닫는다.
# 3) 같은 입력을 파이썬으로 원자료 CSV에서 따로 계산해 맞춘다. 원자료 합계는 N-1 nts_pct.json(영상 사실표)과도 맞춘다.
# 4) 결과를 out/check.md 에 쓴다.
import os, sys, json, subprocess
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
sys.path.insert(0, HERE)
import make_xlsx as M  # noqa: E402

CASES = [0, 20, 21, 1000, 3358, 3400, 3417, 3418, 5000, 9117, 10000, 19953, 50000, 99936, 99937, 150000]


def py_expect(x):
    asc = [dict(k=r['k'], a=round(r['g'] * 10000 / r['n'])) for r in reversed(M.ROWS)]
    a = [r['a'] for r in asc]
    if x < min(a):
        return dict(lo='맨 아래 구간 평균보다 적음', lo_a='', hi=asc[0]['k'], hi_a=asc[0]['a'])
    i = max(j for j, v in enumerate(a) if v <= x)
    if x >= max(a):
        return dict(lo=asc[i]['k'], lo_a=asc[i]['a'], hi='위 구간 없음(상위 0.1% 평균 이상)', hi_a='')
    return dict(lo=asc[i]['k'], lo_a=asc[i]['a'], hi=asc[i + 1]['k'], hi_a=asc[i + 1]['a'])


PS = r'''
$cases = Get-Content -Raw -Encoding UTF8 "%(cases)s" | ConvertFrom-Json
$before = @((Get-Process EXCEL -ErrorAction SilentlyContinue).Id)
$x = New-Object -ComObject Excel.Application
Start-Sleep -Seconds 8
$mine = @((Get-Process EXCEL -ErrorAction SilentlyContinue).Id | Where-Object { $before -notcontains $_ })
$res = @{ pid = ($mine -join ",") }
try {
  $wb = $null
  foreach ($k in 1..20) { try { $wb = $x.Workbooks.Open("%(file)s"); break } catch { Start-Sleep -Seconds 2 } }
  if ($wb -eq $null) { throw "파일을 열지 못함" }
  $res["excel_version"] = $x.Version
  $s = $wb.Worksheets.Item("내 연봉 넣기")
  $d = $wb.Worksheets.Item("원자료")
  foreach ($c in $cases) {
    $s.Range("C4").Value2 = [double]$c
    $x.CalculateFull()
    $o = @{}
    foreach ($a in "C6","C7","C8","C9","A12") { $o[$a] = $s.Range($a).Text }
    $res["x" + $c] = $o
  }
  $res["sumN"] = $d.Range("B%(tot)s").Value2
  $res["sumG"] = $d.Range("C%(tot)s").Value2
  $res["avg"] = $d.Range("D%(tot)s").Value2
  $res["top_share_first"] = $d.Range("E%(first)s").Text
  $t = $wb.Worksheets.Item("주요 구간")
  $kv = @{}
  foreach ($y in 4..13) { $kv[$t.Range("A$y").Text] = $t.Range("B$y").Value2 }
  $res["keys"] = $kv
  $wb.Close($false)
} catch {
  $res["error"] = "$_ @ $($_.InvocationInfo.ScriptLineNumber)"
} finally {
  try { $x.Quit() } catch {}
  try { [System.Runtime.InteropServices.Marshal]::ReleaseComObject($x) | Out-Null } catch {}
  Start-Sleep -Seconds 3
  foreach ($p in $mine) { if (Get-Process -Id $p -ErrorAction SilentlyContinue) { Stop-Process -Id $p -Force } }
}
$res | ConvertTo-Json -Depth 5 | Out-File -Encoding utf8 "%(out)s"
'''


def excel():
    cj, oj, ps1 = (os.path.join(OUT, n) for n in ('_cases.json', '_excel_raw.json', '_excel_read.ps1'))
    json.dump(CASES, open(cj, 'w', encoding='utf-8'))
    open(ps1, 'w', encoding='utf-8-sig').write(PS % dict(cases=cj, file=M.FILE, out=oj, tot=M.LAST + 2, first=M.FIRST))
    subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ps1], check=True)
    res = json.load(open(oj, encoding='utf-8-sig'))
    if 'error' in res:
        raise SystemExit('Excel: ' + res['error'])
    return res


def fmt(v):
    return f'{v:,}' if isinstance(v, int) else str(v)


def main():
    M.build()
    R = excel()
    ref = json.load(open(os.path.join(HERE, '..', 'longform', 'ep', 'N-1', 'nts_pct.json'), encoding='utf-8'))
    N = sum(r['n'] for r in M.ROWS); G = sum(r['g'] for r in M.ROWS)
    lines = ['# 회원 자료 2호 엑셀 검산 (verify.py 자동)', '',
             f"- Excel {R.get('excel_version')} 로 열어 다시 계산 · 파일 {os.path.basename(M.FILE)}", '',
             '## 원자료 합계', '| 항목 | 파이썬(CSV) | N-1 사실표(nts_pct.json) | Excel | 일치 |', '|---|---|---|---|---|']
    bad = 0
    for name, p, r, e in (('인원(명)', N, ref['N'], R['sumN']), ('총급여(억원)', G, ref['G_eok'], R['sumG'])):
        ok = p == r == int(e)
        bad += not ok
        lines.append(f'| {name} | {p:,} | {r:,} | {int(e):,} | {"O" if ok else "X"} |')
    lines += ['', f"- 평균 총급여(만원): Excel {int(R['avg']):,} · 파이썬 {round(G * 10000 / N):,}",
              f"- 맨 아래 구간 '위에 있는 사람 비율': Excel {R['top_share_first']} (99%여야 함)", '',
              '## 입력값별 결과', '| 넣은 총급여(만원) | 아래 구간(Excel) | 평균 | 위 구간(Excel) | 평균 | 파이썬과 일치 |', '|---|---|---|---|---|---|']
    for c in CASES:
        e = R['x' + str(c)]; p = py_expect(c)
        ok = (e['C6'] == p['lo'] and e['C7'].replace(',', '') == str(p['lo_a']) and e['C8'] == p['hi'] and e['C9'].replace(',', '') == str(p['hi_a']))
        bad += not ok
        lines.append(f"| {c:,} | {e['C6']} | {e['C7']} | {e['C8']} | {e['C9']} | {'O' if ok else 'X (파이썬 ' + json.dumps(p, ensure_ascii=False) + ')'} |")
    lines += ['', '## 한 줄 결과 예(5,000만원)', '- ' + R['x5000']['A12'], '', '## 주요 구간(Excel 값)']
    for k, v in R['keys'].items():
        lines.append(f'- {k}: {int(v):,}만원')
    lines += ['', f'판정: {"통과" if bad == 0 else "불일치 " + str(bad) + "건"}']
    open(os.path.join(OUT, 'check.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
