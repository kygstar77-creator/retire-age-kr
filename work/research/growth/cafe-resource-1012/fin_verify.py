# 금융소득·건보료 판정 엑셀 검산 (자료 담당, 2026-10-12)
#   py -3.12 fin_verify.py
# 1) make_fin_xlsx.py로 파일을 다시 만든다.
# 2) Microsoft Excel(COM)로 파일을 열어 예시마다 입력 칸을 바꾸고 다시 계산한 값을 읽는다. 이 스크립트가 띄운 Excel만 닫는다.
# 3) 같은 예시를 파이썬으로 따로 계산(법 원문대로 새로 짠 식)하고, 건보 부분은 사이트 식(node fin_site_ref.mjs)과도 맞춘다.
# 4) 결과를 fin-excel-check.md 의 '자동 검산' 칸(표시 줄 사이)에 넣는다.
import os, sys, json, subprocess, re
from decimal import Decimal, ROUND_HALF_UP
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
sys.path.insert(0, HERE)
import make_fin_xlsx as M  # noqa: E402

KV = {r[0]: r[2] for r in M.K_ROWS}
DEP, LOC = M.DEP, M.LOC
# (id, 이자, 국내 상장주식 배당, 그 밖의 배당, 자격, 공적연금·근로, 그 밖의 종합소득금액, 재산 과표, 메모)
CASES = [
    ('EX', 8000000, 10000000, 6000000, DEP, 12000000, 0, 300000000, '배포 파일 기본 예시 = 안내 글 표'),
    ('S01', 0, 0, 0, DEP, 0, 0, 0, '아무 소득 없음'),
    ('S02', 9000000, 0, 0, DEP, 0, 0, 0, '금융 900만'),
    ('S03', 10000000, 0, 0, LOC, 0, 0, 0, '금융 딱 1천만'),
    ('S04', 10010000, 0, 0, LOC, 0, 0, 0, '금융 1,001만'),
    ('S05', 6000000, 5000000, 4000000, DEP, 12000000, 0, 300000000, '금융 1,500만·연금 1,200만·재산 3억'),
    ('S06', 15000000, 0, 10000000, LOC, 0, 0, 0, '금융 2,500만'),
    ('S07', 10000000, 15000000, 5000000, DEP, 18000000, 0, 600000000, '금융 3천만·연금 1,800만·재산 6억'),
    ('S08', 8000000, 0, 0, DEP, 15000000, 0, 200000000, '금융 800만·연금 1,500만 — 1천만 규칙에 따라 갈림'),
    ('S09', 5000000, 0, 0, DEP, 6000000, 0, 600000000, '재산 6억·금융 500만·연금 600만 — 갈림'),
    ('S10', 12000000, 0, 0, DEP, 0, 0, 1000000000, '재산 10억'),
    ('S11', 20000000, 30000000, 10000000, LOC, 24000000, 0, 1500000000, '금융 6천만·연금 2,400만·재산 15억'),
    ('S12', 50000000, 50000000, 50000000, LOC, 0, 0, 3000000000, '금융 1억5천만·재산 30억'),
    ('S13', 0, 0, 0, LOC, 24000000, 0, 105000000, '연금만 2,400만·재산 1.05억'),
    ('S14', 0, 0, 0, LOC, 6720000, 0, 0, '소득월액 딱 28만원'),
    ('S15', 0, 0, 0, LOC, 6730000, 0, 0, '소득월액 28만원 조금 넘음'),
    ('S16', 1000000000, 0, 0, LOC, 0, 0, 0, '금융 10억 — 상한'),
    ('S17', 0, 0, 0, LOC, 6725000, 0, 200000000, '소득월액 280,208원(28만원 바로 위)·재산 2억'),
    ('H1', 30000000, 0, 0, LOC, 0, 0, 0, '손 계산 1: 이자 3천만'),
    ('H2', 0, 50000000, 0, LOC, 0, 100000000, 0, '손 계산 2: 국내 배당 5천만 + 다른 소득금액 1억'),
    ('H3', 20000000, 20000000, 10000000, LOC, 0, 50000000, 0, '손 계산 3: 이자 2천만·국내 배당 2천만·ETF 1천만 + 다른 소득금액 5천만'),
]
HAND = {  # 손으로 원문 계산한 값(fin-excel-check.md 3장): 종합과세 시 세액 ①, 분리과세 시 세액 ②, 배당가산액, 더 내는 소득세
    'H1': dict(TAX1=3310000, TAX2=4200000, G=0, ADD=0),
    'H2': dict(TAX1=33385000, TAX2=26035000, G=3000000, ADD=4350000),
    'H3': dict(TAX1=16360000, TAX2=13015000, G=2000000, ADD=1345000),
}
KEYS = ['F', 'OVER', 'GUB', 'G', 'BASE1', 'TAX1', 'TAX2', 'CR', 'DET', 'ADD', 'FH', 'SUMA', 'SUMB', 'LIM', 'JA', 'JB', 'JD',
        'INCY', 'INCM', 'PI', 'PB', 'PP', 'PR', 'HI', 'LT', 'TOT', 'TOT0', 'DIFF']


def rnd(x):
    return int(Decimal(str(x)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


def tax(x):
    if x <= 0:
        return 0
    lo, base, rate = [t for t in M.TAX_TABLE if t[0] < x][-1]
    return base + (x - lo) * rate


def points(v):
    if v <= 0:
        return 0
    lowers = [0] + [u * 10000 for u in M.PROP_UPPER_MAN]
    return M.PROP_POINTS[sum(1 for lo in lowers if lo < v) - 1]


def py_calc(i, dk, de, st, pen, oth, prop):
    """법 원문대로 다시 짠 식(엑셀 식을 옮기지 않았다)."""
    o = {}
    T, ded = KV['T'], KV['DED']
    F = i + dk + de
    o['F'] = F
    over = max(0, F - T)
    o['OVER'] = over
    # 시행령 제116조의2: 이자 → 그 밖의 배당 → 배당가산 대상 배당 순으로 2천만원을 채운다
    room = T
    used_i = min(i, room); room -= used_i
    used_de = min(de, room); room -= used_de
    used_dk = min(dk, room)
    o['GUB'] = dk - used_dk
    o['G'] = rnd(o['GUB'] * KV['GU'])
    t2 = rnd(i * KV['WI'] + (dk + de) * KV['WD'] + tax(max(0, oth - ded)))
    o['TAX2'] = t2
    if F > T:
        o['BASE1'] = max(0, over + o['G'] + oth - ded)
        o['TAX1'] = rnd(T * KV['WI'] + tax(o['BASE1']))
        o['CR'] = o['G']
        o['DET'] = max(o['TAX1'] - o['CR'], t2)
    else:
        o['BASE1'] = o['TAX1'] = ''
        o['CR'] = 0
        o['DET'] = t2
    o['ADD'] = o['DET'] - t2
    fh = F if F > KV['FT'] else 0
    o['FH'] = fh
    o['SUMA'], o['SUMB'] = F + pen, fh + pen
    lim = KV['DEPINC2'] if prop > KV['DEPP1'] else KV['DEPINC']
    o['LIM'] = lim
    judge = lambda s: '탈락' if prop > KV['DEPP2'] else ('유지' if s <= lim else '탈락')  # noqa: E731
    o['JA'], o['JB'] = judge(o['SUMA']), judge(o['SUMB'])
    o['JD'] = o['JA'] if o['JA'] == o['JB'] else '확인 필요'
    ltc = round(KV['LTCR'] / KV['HR'], 4)

    def prem(fin):
        incm = (fin + pen * KV['HALF']) / 12
        pi = KV['FLOOR'] if incm <= KV['FLOORM'] else incm * KV['HR']
        pb = max(0, prop - KV['PDED'])
        pp = points(pb)
        pr = pp * KV['PT']
        hi = min(max(pi + pr, KV['FLOOR']), KV['CAP'])
        return incm, pi, pb, pp, pr, hi, hi * ltc, rnd(hi * (1 + ltc))
    o['INCY'] = fh + pen * KV['HALF']
    o['INCM'], o['PI'], o['PB'], o['PP'], o['PR'], o['HI'], o['LT'], o['TOT'] = prem(fh)
    o['TOT0'] = prem(0)[-1]
    o['DIFF'] = o['TOT'] - o['TOT0']
    return o


PS = r'''
$cases = Get-Content -Raw -Encoding UTF8 "%(cases)s" | ConvertFrom-Json
$cells = Get-Content -Raw -Encoding UTF8 "%(cells)s" | ConvertFrom-Json
$before = @((Get-Process EXCEL -ErrorAction SilentlyContinue).Id)
$x = New-Object -ComObject Excel.Application
Start-Sleep -Seconds 8
$mine = @((Get-Process EXCEL -ErrorAction SilentlyContinue).Id | Where-Object { $before -notcontains $_ })   # 이 스크립트가 띄운 Excel
$res = @{ pid = ($mine -join ",") }
try {
  $wb = $null
  foreach ($k in 1..20) { try { $wb = $x.Workbooks.Open("%(file)s"); break } catch { Start-Sleep -Seconds 2 } }
  if ($wb -eq $null) { throw "파일을 열지 못함" }
  $res["excel_version"] = $x.Version
  $s = $wb.Worksheets.Item("판정")
  foreach ($c in $cases) {
    $s.Range("C12").Value2 = [double]$c.i; $s.Range("C13").Value2 = [double]$c.dk; $s.Range("C14").Value2 = [double]$c.de
    $s.Range("C15").Value2 = [string]$c.st; $s.Range("C16").Value2 = [double]$c.pen; $s.Range("C17").Value2 = [double]$c.oth; $s.Range("C18").Value2 = [double]$c.prop
    $x.CalculateFull()
    $o = @{}
    foreach ($p in $cells.PSObject.Properties) { $o[$p.Name] = $s.Range($p.Value).Value2 }
    foreach ($a in "B2","B3","B4","B7","B8") { $o[$a] = $s.Range($a).Text }
    $res[$c.id] = $o
  }
  $wb.Close($false)
} catch {
  $res["error"] = "$_ @ $($_.InvocationInfo.ScriptLineNumber)"
} finally {
  try { $x.Quit() } catch {}
  try { [System.Runtime.InteropServices.Marshal]::ReleaseComObject($x) | Out-Null } catch {}
  Start-Sleep -Seconds 3
  foreach ($p in $mine) { if (Get-Process -Id $p -ErrorAction SilentlyContinue) { Stop-Process -Id $p -Force } }   # 내가 띄운 것만 닫는다
}
$res | ConvertTo-Json -Depth 5 | Out-File -Encoding utf8 "%(out)s"
'''


def excel(R):
    cj, kj, oj, ps1 = (os.path.join(OUT, n) for n in ('_cases.json', '_cells.json', '_excel_raw.json', '_excel_read.ps1'))
    json.dump([dict(id=c[0], i=c[1], dk=c[2], de=c[3], st=c[4], pen=c[5], oth=c[6], prop=c[7]) for c in CASES],
              open(cj, 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump({k: R[k] for k in KEYS}, open(kj, 'w', encoding='utf-8'))
    open(ps1, 'w', encoding='utf-8-sig').write(PS % dict(cases=cj, cells=kj, file=M.FILE, out=oj))
    subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ps1], check=True)
    res = json.load(open(oj, encoding='utf-8-sig'))
    if 'error' in res:
        raise SystemExit('Excel: ' + res['error'])
    return res


def site():
    cj = os.path.join(OUT, '_site_cases.json')
    json.dump([dict(id=c[0], fin=c[1] + c[2] + c[3], pension=c[5], prop=c[7]) for c in CASES], open(cj, 'w', encoding='utf-8'))
    r = subprocess.run(['node', os.path.join(HERE, 'fin_site_ref.mjs'), cj], capture_output=True, text=True, encoding='utf-8', check=True, cwd=HERE)
    return json.loads(r.stdout)


def same(a, b):
    if isinstance(b, str) or isinstance(a, str):
        return (a or '') == (b or '')
    return abs((a or 0) - (b or 0)) < 0.01


def main():
    _, R, _ = M.build()
    xl = excel(R)
    web = site()
    py = {c[0]: py_calc(*c[1:8]) for c in CASES}
    lines = []
    # A. 엑셀 ↔ 파이썬(모든 칸)
    bad = []
    for c in CASES:
        e, p = xl[c[0]], py[c[0]]
        for k in KEYS:
            if not same(e.get(k), p[k]):
                bad.append(f'{c[0]} {k}: 엑셀 {e.get(k)} · 파이썬 {p[k]}')
    lines += ['### A. 엑셀(Excel 재계산) ↔ 파이썬 재현 — 예시 %d개 × 칸 %d개' % (len(CASES), len(KEYS)), '',
              f'- Excel {xl["excel_version"]}(COM)로 연 파일에 입력을 바꿔 넣고 CalculateFull 한 값과, 법 원문대로 따로 짠 파이썬 식(fin_verify.py py_calc)을 칸마다 비교했다.',
              f'- 다른 칸: **{len(bad)}개**' + ('' if not bad else ' — ' + ' / '.join(bad[:20])), '']
    # B. 손 계산 ↔ 엑셀
    lines += ['### B. 손 계산(3장) ↔ 엑셀', '', '| 예시 | 항목 | 손 계산 | 엑셀 | 판정 |', '|---|---|---|---|---|']
    hand_ok = True
    for cid, exp in HAND.items():
        for k, v in exp.items():
            got = xl[cid][k]
            ok = same(got, v); hand_ok &= ok
            lines.append(f'| {cid} | {dict(TAX1="종합과세 시 세액 ①", TAX2="분리과세 시 세액 ②", G="배당가산액", ADD="더 내는 소득세")[k]} | {v:,.0f}원 | {got:,.0f}원 | {"같음" if ok else "다름"} |')
    lines.append('')
    # C. 사이트 식 ↔ 엑셀(건보)
    lines += ['### C. 사이트 /health-insurance 식 ↔ 엑셀(건보) — 예시 %d개' % len(CASES), '',
              '| 예시 | 입력(금융·연금근로·재산 과표) | 피부양자: 사이트 | 엑셀 판정(A/B) | 지역 월 합계: 사이트 | 엑셀 | 차이 | 금융소득 0일 때: 사이트 | 엑셀 | 원인 |',
              '|---|---|---|---|---|---|---|---|---|---|']
    nd = nm = 0
    for c in CASES:
        e, w = xl[c[0]], web[c[0]]
        fin = c[1] + c[2] + c[3]
        sj = '유지' if w['eligible'] else '탈락'
        why = []
        if sj != e['JD']:
            nd += 1
            why.append('피부양자: 사이트는 B(1천만원 이하 금융소득 뺌)만 본다. 엑셀은 A·B가 다르면 확인 필요' if e['JD'] == '확인 필요' else '피부양자 판정 다름')
        d = e['TOT'] - w['monthly']
        if abs(d) >= 1:
            nm += 1
            if (fin % 10000) or (c[5] % 10000):
                why.append('사이트는 금액을 만원 단위로 반올림해 넣는다(연금·근로 672.5만 → 673만). 엑셀은 소득월액 280,208원으로 28만원 바로 위 구간 규칙(2장)이 걸린다')
            elif e['HI'] >= KV['CAP']:
                why.append('상한 4,591,740원(고시 제2조) — 사이트 식에 상한 없음')
            elif abs(d + (rnd(e['HI'] * (1 + 0.9448 / 7.19)) - e['TOT'])) <= 1:
                why.append(f'장기요양 비율: 엑셀 0.1314(제9조 다섯째자리 반올림·복지부 13.14%), 사이트 0.9448/7.19 그대로 → {abs(d):.0f}원')
            else:
                why.append('확인 필요')
        lines.append(f'| {c[0]} | {fin / 1e4:,.0f}만·{c[5] / 1e4:,.0f}만·{c[7] / 1e8:g}억 | {sj} | {e["JD"]}({e["JA"]}/{e["JB"]}) | {w["monthly"]:,} | {e["TOT"]:,.0f} | {d:+,.0f} | '
                     f'{w["monthly0"]:,} | {e["TOT0"]:,.0f} | {"; ".join(why) or "같음"} |')
    lines += ['', f'- 피부양자 판정이 다른 예시 {nd}개, 지역 월 합계가 1원 이상 다른 예시 {nm}개(원인은 표 오른쪽 칸).', '']
    # D. 큰 숫자 문장
    lines += ['### D. 화면 문장(엑셀이 그린 글자 그대로)', '', '| 예시 | 메모 | 큰 숫자(B4) | 아래 줄(B7) | 세금 줄(B8) | 경고(B2) |', '|---|---|---|---|---|---|']
    for c in CASES:
        e = xl[c[0]]
        lines.append(f'| {c[0]} | {c[8]} | {e["B4"]} | {e["B7"]} | {e["B8"]} | {e["B2"] or "-"} |')
    lines.append('')
    verdict = f'A {len(bad)}칸 다름 · B {"전부 같음" if hand_ok else "다름 있음"} · C 피부양자 {nd}개·월 보험료 {nm}개 다름(원인 표기)'
    md_path = os.path.join(HERE, 'fin-excel-check.md')
    md = open(md_path, encoding='utf-8').read()
    block = '<!-- auto:start -->\n' + f'자동 검산 결과({verdict}). `py -3.12 fin_verify.py`가 이 칸을 다시 쓴다.\n\n' + '\n'.join(lines) + '\n<!-- auto:end -->'
    md = re.sub(r'<!-- auto:start -->.*?<!-- auto:end -->', lambda m: block, md, flags=re.S)
    open(md_path, 'w', encoding='utf-8').write(md)
    json.dump(dict(excel=xl, site=web, py=py), open(os.path.join(OUT, '_verify_values.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    for n in ('_cases.json', '_cells.json', '_excel_raw.json', '_excel_read.ps1', '_site_cases.json'):
        try:
            os.remove(os.path.join(OUT, n))
        except OSError:
            pass
    print(verdict)


if __name__ == '__main__':
    main()
