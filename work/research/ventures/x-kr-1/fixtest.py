# X-KR-1 10/12 고침 검산: 고친 파일에 값을 넣고 실제 Excel로 다시 계산 ↔ 같은 식을 파이썬으로 재현 → out/fixtest.json
#   py -3.12 fixtest.py        (make_xlsx.py 로 out/가계부_은퇴나이_2026.xlsx 를 먼저 만든다. 파일은 읽기 전용으로 열고 저장하지 않는다)
# 웹 식과의 대조(국민연금 포함)는 verify.py(checks.md)가 한다. 여기는 오류 5개(T5·T6·T8·+N일·연금)를 시험한다.
import os, sys, json, math, re, datetime, subprocess
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
sys.path.insert(0, HERE)
import make_xlsx as mx  # noqa: E402

TODAY = datetime.date.today()
S1, CALC = '월 가계부', '계산'

# ── 시나리오: 예시 파일(8월 3~11행, 9월 12~20행)에 넣을 것
SEP_TXT = ['2026.09.01', '2026. 9. 2.', '2026/09/03', '2026년 9월 4일', '20260905', '26.09.06', '2026-09-07 14:22', '2026.9.8', '2026-09-09']
SCEN = {
    'S0 예시 그대로': [],
    'T5 이번 달(10/3) 커피 5,000원 추가': [('A21', '2026-10-03', 'date'), ('B21', '커피'), ('C21', 5000), ('D21', '음식·숙박')],
    'T5b 11/3 커피 5,000원 추가(옛 시험 그대로)': [('A21', '2026-11-03', 'date'), ('B21', '커피'), ('C21', 5000), ('D21', '음식·숙박')],
    'T5c 새로 쓰는 사람: 이번 달 1줄뿐': [('clear', 'A3:D20'), ('A3', '2026-10-03', 'date'), ('B3', '커피'), ('C3', 5000), ('D3', '음식·숙박')],
    'T6 9월 날짜 9줄을 글자 9가지 모양으로': [(f'A{12 + i}', t, 'text') for i, t in enumerate(SEP_TXT)],
    'T6b 9월 날짜 글자 2026.09.0N(옛 시험 그대로)': [(f'A{12 + i}', f'2026.09.0{1 + i}', 'text') for i in range(9)],
    'T6c 못 읽는 날짜 9/10 한 줄': [('A21', '9/10', 'text'), ('B21', '커피'), ('C21', 50000), ('D21', '음식·숙박')],
    'T6d 금액 글자 100,000원': [('C16', '100,000원', 'text')],
    'T8 3003행에 100만원(3,000줄 밖)': [('A3003', '2026-09-15', 'date'), ('B3003', '가전'), ('C3003', 1000000), ('D3003', '가정용품·가사서비스')],
    'T8b 2500행에 100만원(3,000줄 안)': [('A2500', '2026-09-15', 'date'), ('B2500', '가전'), ('C2500', 1000000), ('D2500', '가정용품·가사서비스')],
    'T9 예시 줄 전부 삭제': [('clear', 'A3:D20')],
    'P0 국민연금 0원': [('s2:D16', 0)],
    'P1 58세·4억·연금 120만': [('s2:D12', 58), ('s2:D13', 400000000), ('s2:D16', 1200000)],
}

PS = r'''
$ErrorActionPreference = "Stop"
$sc = Get-Content -Raw -Encoding UTF8 "%(dir)s\fixtest_in.json" | ConvertFrom-Json
$x = New-Object -ComObject Excel.Application; $x.DisplayAlerts = $false
$res = @{}
try {
foreach ($p in $sc.PSObject.Properties) {
  $wb = $x.Workbooks.Open("%(dir)s\가계부_은퇴나이_2026.xlsx", 0, $true)
  $s1 = $wb.Worksheets.Item("월 가계부"); $s2 = $wb.Worksheets.Item("은퇴 나이"); $c = $wb.Worksheets.Item("계산")
  foreach ($op in $p.Value) {
    $a = $op[0]
    if ($a -eq "clear") { $s1.Range($op[1]).ClearContents() | Out-Null; continue }
    $ws = $s1; if ($a.StartsWith("s2:")) { $ws = $s2; $a = $a.Substring(3) }
    $r = $ws.Range($a)
    if ($op.Count -gt 2 -and $op[2] -eq "text") { $r.NumberFormat = "@"; $r.Value2 = [string]$op[1] }
    elseif ($op.Count -gt 2 -and $op[2] -eq "date") { $d = [datetime]::ParseExact($op[1], "yyyy-MM-dd", $null); $r.Value2 = $d.ToOADate() }
    elseif ($op[1] -is [string]) { $r.Value2 = [string]$op[1] }
    else { $r.Value2 = [double]$op[1] }
  }
  $sw = [Diagnostics.Stopwatch]::StartNew(); $x.CalculateFull(); $ms = $sw.ElapsedMilliseconds
  $o = @{ ms = $ms }
  foreach ($k in "B5","B6","B7","B8","B9","B14","B16","B17","B18","B19","B22","B23","B30","B31","B32","B33","B34","B35","B37","B93","B149") { $o["c_$k"] = $c.Range($k).Value2 }
  foreach ($k in "B2","B3","B4","B7","B8","B10","D10") { $o["s2_$k"] = $s2.Range($k).Text }
  $o["E"] = @(); foreach ($rr in 3..21) { $o["E"] += ,@($rr, [string]$s1.Range("E$rr").Text) }
  $o["err"] = @(); foreach ($k in "B2","B3","B4","B7","B8","B10","D10","F10") { if ($s2.Range($k).Text -like "#*") { $o["err"] += $k } }
  $res[$p.Name] = $o; $wb.Close($false)
}
} finally { $x.Quit(); [void][Runtime.InteropServices.Marshal]::ReleaseComObject($x) }
$res | ConvertTo-Json -Depth 6 | Out-File -Encoding utf8 "%(dir)s\fixtest_excel.json"
'''


# ── 파이썬 재현(엑셀 식과 같은 규칙, 웹 retirementSimulator.js와 같은 시뮬레이션)
def parse_date(v):
    if v is None or v == '':
        return None
    if isinstance(v, datetime.date):
        return v
    if isinstance(v, (int, float)):
        if 19000101 <= v <= 21001231:
            y, m, d = int(v // 10000), int(v // 100) % 100, int(v) % 100
            try: return datetime.date(y, m, d)
            except ValueError: return None
        return None
    s = str(v).strip()
    for a, b in (('년', '-'), ('월', '-'), ('일', ''), ('.', '-'), ('/', '-'), (' ', '-')):
        s = s.replace(a, b)
    for _ in range(3):
        s = s.replace('--', '-')
    t = s + '-'
    try:
        if len(t) == 9 and '-' not in t[:8] and t[:8].isdigit():
            y, m, d = int(t[:4]), int(t[4:6]), int(t[6:8])
        else:
            p = t.split('-')
            y, m, d = int(p[0]), int(p[1]), int(p[2])
        if y < 100: y += 2000
        if not (2000 <= y <= 2099): return None
        return datetime.date(y, m, d)
    except (ValueError, IndexError):
        return None


def parse_amt(v):
    if v is None or v == '': return None
    if isinstance(v, (int, float)): return v
    try: return float(str(v).strip().replace(',', '').replace('원', '').replace(' ', '').replace('−', '-'))
    except ValueError: return None


def pension_age(age):
    by = TODAY.year - age
    return 60 if by <= 1952 else 61 if by <= 1956 else 62 if by <= 1960 else 63 if by <= 1964 else 64 if by <= 1968 else 65


def grid_final(age, asset, r, i, S, M, R, P, PA):
    a = asset
    for y in range(1, mx.YMAX + 1):
        if age + y > mx.UNTIL: break
        flow = 12 * S if age + y <= R else -12 * max(0, M - (P if age + y >= PA else 0)) * (1 + i) ** y
        a = a + flow
        if a > 0: a *= 1 + r
        # 엑셀 격자와 같이 마지막(90세) 값만 본다. 은퇴 뒤 인출이 0 이상이면 자산은 줄기만 하므로 웹의 '도중에 0 이하'와 같다
    return a


def earliest(age, asset, r, i, S, M, P, PA):
    finals = []
    for k in range(mx.KMAX + 1):
        finals.append(grid_final(age, asset, r, i, S, M, age + k, P, PA))
    ok = [age + k for k in range(mx.KMAX + 1) if age + k <= mx.MAXR and finals[k] > 0]
    if not ok: return None, None
    R = min(ok)
    if R == age: return R, age
    f0, f1 = finals[R - age - 1], finals[R - age]
    return R, R - 1 + (-f0) / (f1 - f0)


def required(age, r, i, M, P, PA):
    s = 0
    for y in range(1, mx.YMAX + 1):
        if age + y > mx.UNTIL: continue
        s += 12 * max(0, M - (P if age + y >= PA else 0)) * (1 + i) ** y / (1 + r) ** (y - 1)
    return math.ceil(s)


def replica(ops):
    rows = {mx.FIRST + k: [d, n, a, c] for k, (d, n, a, c) in enumerate(mx.ledger_rows(None))}
    inp = {'D12': 30, 'D13': 30000000, 'D14': 5, 'D15': 3, 'D16': mx.PENSION}
    for op in ops:
        if op[0] == 'clear':
            rows = {k: v for k, v in rows.items() if not (3 <= k <= 20)}; continue
        if op[0].startswith('s2:'):
            inp[op[0][3:]] = op[1]; continue
        col, rr = op[0][0], int(op[0][1:])
        val = op[1]
        if len(op) > 2 and op[2] == 'date': val = datetime.date.fromisoformat(val)
        rows.setdefault(rr, [None, None, None, None])['ABCD'.index(col)] = val
    first = datetime.date(TODAY.year, TODAY.month, 1)
    ok_rows, bad, over, cur_n = [], 0, 0, 0
    for rr, (d, n, a, c) in rows.items():
        if rr > mx.LAST:
            over += 1; continue
        dd, aa = parse_date(d), parse_amt(a)
        if a not in (None, '') and (dd is None or aa is None): bad += 1
        if dd and dd >= first: cur_n += 1
        if dd and aa is not None: ok_rows.append((dd, aa, c))
    done = [d for d, _, _ in ok_rows if d < first]
    alld = [d for d, _, _ in ok_rows]
    out = {'bad': bad, 'over': over, 'cur_n': cur_n}
    if not alld:
        out['big'] = '가계부를 넣어 주세요'; return out
    base_d = max(done) if done else max(alld)
    out['fallback'] = not done
    base = datetime.date(base_d.year, base_d.month, 1)
    prev = datetime.date(base.year - (base.month == 1), 12 if base.month == 1 else base.month - 1, 1)

    def month(m0):
        inc = sum(a for d, a, c in ok_rows if (d.year, d.month) == (m0.year, m0.month) and c == mx.INCOME)
        tot = sum(a for d, a, c in ok_rows if (d.year, d.month) == (m0.year, m0.month))
        return inc, tot - inc
    inc0, sp0 = month(base)
    inc1, sp1 = month(prev)
    age, asset, r, i, P = inp['D12'], inp['D13'], inp['D14'] / 100, inp['D15'] / 100, inp['D16']
    PA = pension_age(age)
    R0, a0 = earliest(age, asset, r, i, inc0 - sp0, sp0, P, PA)
    R1, a1 = earliest(age, asset, r, i, inc0 - sp0 - 100000, sp0 + 100000, P, PA)
    R2, a2 = earliest(age, asset, r, i, inc1 - sp1, sp1, P, PA)
    out.update(base=base.isoformat(), spend=sp0, R=R0, big=('70세 넘음' if R0 is None else '지금' if R0 == age else f'{R0}세'),
               required=required(age, r, i, sp0, P, PA), PA=PA)
    m0 = None if a0 is None else round(a0 * 12)
    m1 = None if a1 is None else round(a1 * 12)
    m2 = None if a2 is None else round(a2 * 12)
    out['plus100k_months'] = (m1 - m0) if (m0 is not None and m1 is not None and m1 - m0 > 0) else None
    out['vs_prev_months'] = None if (sp1 == 0 or m0 is None or m2 is None) else m2 - m0
    return out


def main():
    json.dump({k: [list(o) for o in v] for k, v in SCEN.items()}, open(os.path.join(OUT, 'fixtest_in.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    ps1 = os.path.join(OUT, 'fixtest.ps1')
    open(ps1, 'w', encoding='utf-8-sig').write(PS % {'dir': OUT})
    subprocess.run(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', ps1], check=True)
    xl = json.load(open(os.path.join(OUT, 'fixtest_excel.json'), encoding='utf-8-sig'))
    res, allok = {}, True
    for name, ops in SCEN.items():
        e, p = xl[name], replica(ops)
        checks = []
        checks.append(('큰 숫자', e['s2_B4'], p['big']))
        if 'R' in p:
            checks.append(('필요 자산', round(e['c_B32']), p['required']))
            want10 = '' if p['plus100k_months'] is None else f'월 지출이 10만원 늘면 은퇴가 약 {p["plus100k_months"]}개월 늦어져요'
            checks.append(('10만원 줄', e['s2_B8'], want10))
            checks.append(('이번 달 지출', round(e['c_B6']), round(p['spend'])))
            v = p['vs_prev_months']
            want7 = '' if v is None else '지난달과 같음' if v == 0 else f'이번 달 지출대로면 지난달보다 {abs(v)}개월 {"빨라져요" if v > 0 else "늦어져요"}'
            checks.append(('지난달 비교', e['s2_B7'], want7))
        else:
            checks.append(('10만원 줄(빈칸)', e['s2_B8'], ''))
        checks.append(('못 읽은 줄', int(e['c_B18']), p['bad']))
        checks.append(('3,000줄 밖', int(e['c_B19']), p['over']))
        checks.append(('화면 오류(#)', ','.join(e['err']) or '없음', '없음'))
        ok = True
        for lab, a, b in checks:
            good = (abs(a - b) <= max(1000, abs(b) * 1e-6)) if isinstance(b, (int, float)) and isinstance(a, (int, float)) else a == b
            ok &= good
        allok &= ok
        res[name] = {'ok': ok, 'checks': checks, 'excel': {k: e[k] for k in ('s2_B2', 's2_B3', 's2_B4', 's2_B7', 's2_B8', 's2_B10', 's2_D10', 'ms')},
                     'E': [x for x in e['E'] if x[1]], 'python': p}
        print(f'{"통과" if ok else "다름"} | {name} | 큰 숫자 {e["s2_B4"]} (파이썬 {p["big"]}) | {e["s2_B3"]} | {e["s2_B2"] or "(경고 없음)"} | {e["s2_B8"]} | 재계산 {e["ms"]}ms')
        for lab, a, b in checks:
            print(f'      {lab}: 엑셀 {a} / 파이썬 {b}')
    json.dump({'today': TODAY.isoformat(), 'all_ok': allok, 'res': res}, open(os.path.join(OUT, 'fixtest.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    print('전부 통과' if allok else '다름 있음')
    sys.exit(0 if allok else 1)


if __name__ == '__main__':
    main()
