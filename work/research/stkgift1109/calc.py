# 상증법 제63조①1가: 평가기준일 이전·이후 각 2개월 종가 평균 — 하락한 날 증여하면 평가액은 그날 종가와 얼마나 다른가
import json, datetime as dt, sys
sys.stdout.reconfigure(encoding='utf-8')
def load(t):
    return [(dt.date.fromisoformat(a), c) for a, c in json.load(open(f'raw/px_{t}.json', encoding='utf-8'))['rows']]
def addm(d, m):
    y, mo = d.year, d.month + m
    while mo > 12: y += 1; mo -= 12
    while mo < 1: y -= 1; mo += 12
    import calendar
    return dt.date(y, mo, min(d.day, calendar.monthrange(y, mo)[1]))
def val(rows, day):
    a, b = addm(day, -2), addm(day, 2)
    w = [c for d, c in rows if a <= d <= b]
    close = dict(rows)[day]
    return close, sum(w) / len(w), len(w), a, b
LAST = dt.date(2026, 11, 9)
k = load('^KS11'); s = load('005930.KS'); e = load('069500.KS')
kd = dict(k)
drops = []
for i in range(1, len(k)):
    d, c = k[i]; p = k[i-1][1]
    drops.append(((c/p-1)*100, d))
drops.sort()
print('코스피 하루 하락 상위(평가 기간이 끝난 날만 = 증여일+2개월 <= 2026-11-09)')
for r, d in drops[:15]:
    done = addm(d, 2) <= LAST
    if not done: print(f'  {d} {r:.2f}% (아직 평가 기간 안 끝남)'); continue
    for name, rows in (('삼성전자', s), ('KODEX 200', e)):
        if d not in dict(rows): continue
        c, av, n, a, b = val(rows, d)
        print(f'  {d} 코스피 {r:.2f}% | {name} 종가 {c:,.0f} · {a}~{b} {n}일 평균 {av:,.0f} · 평균/종가 {av/c*100:.1f}%')
# 예시: 5천만원어치를 그날 종가로 계산해 넘겼을 때 신고할 증여재산가액
def tax(base):
    t = base
    if t <= 0: return 0
    if t <= 1e8: return t*0.1
    if t <= 5e8: return 1e7 + (t-1e8)*0.2
    if t <= 1e9: return 9e7 + (t-5e8)*0.3
    if t <= 3e9: return 2.4e8 + (t-1e9)*0.4
    return 1.04e9 + (t-3e9)*0.5
print()
for day in [dt.date(2025,4,7)]:
    for name, rows in (('삼성전자', s), ('KODEX 200', e)):
        c, av, n, a, b = val(rows, day)
        sh = int(5e7 // c)
        v_close = sh*c; v_avg = sh*av
        for ded, who in ((5e7,'성인 자녀'), (2e7,'미성년 자녀')):
            base = max(0, v_avg-ded); t = tax(base); t2 = t*0.97
            print(f'{day} {name} {sh}주 종가 가치 {v_close:,.0f} · 평가액(평균) {v_avg:,.0f} | {who} 공제 {ded:,.0f} 과표 {base:,.0f} 산출 {t:,.0f} 신고공제 3% 뒤 {t2:,.0f}')

print('\n== 2026년 코스피 5% 넘게 빠진 날(평가 기간 끝난 날) — 그날 증여했다면 평가액(4개월 평균)이 종가보다 높았나')
for name, rows in (('KODEX 200', e), ('삼성전자', s)):
    hi = lo = 0; lst = []
    for r, d in drops:
        if r > -5 or d.year != 2026 or addm(d, 2) > LAST or d not in dict(rows): continue
        c, av, n, a, b = val(rows, d)
        lst.append((d, round(av/c*100, 1)))
        if av > c: hi += 1
        else: lo += 1
    lst.sort()
    print(f'  {name}: {hi+lo}일 중 평균>종가 {hi}일 · 평균<=종가 {lo}일 · 범위 {min(x for _,x in lst)}%~{max(x for _,x in lst)}%')
    print('   ', lst)
print('\n== 11월 6일에 넘겼다면(평가 기간 9/6~1/6, 아직 진행 중)')
d = dt.date(2026, 11, 6)
for name, rows in (('삼성전자', s), ('KODEX 200', e)):
    R = dict(rows); c = R[d]
    pre = [x for dd, x in rows if addm(d, -2) <= dd < d]
    post_known = [x for dd, x in rows if d < dd <= LAST]
    # 4개월 거래일 수를 앞 2개월 거래일 수의 2배쯤으로 보고(+그날), 평균이 그날 종가와 같아지려면 남은 날 평균이 얼마여야 하나
    n_pre = len(pre); n_post_total = n_pre  # 근사: 뒤 2개월 거래일 수 = 앞 2개월 거래일 수
    need = (c*(n_pre + 1 + n_post_total) - sum(pre) - c - sum(post_known)) / (n_post_total - len(post_known))
    print(f'  {name}: 11/6 종가 {c:,.0f} · 앞 2개월({addm(d,-2)}~11/5) {n_pre}일 평균 {sum(pre)/n_pre:,.0f} · 11/9까지 뒤 {len(post_known)}일 평균 {sum(post_known)/max(1,len(post_known)):,.0f} · 평가액이 11/6 종가와 같아지려면 남은 약 {n_post_total-len(post_known)}일 평균 {need:,.0f}({need/c*100:.0f}%)')
# 7/28 예시 상세
d = dt.date(2026, 7, 28)
c, av, n, a, b = val(s, d); sh = int(5e7 // c)
print(f'\n== 예시 7/28 삼성전자: 종가 {c:,.0f}, {sh}주 = {sh*c:,.0f}원 · 평가액 {sh*av:,.0f}원({a}~{b} {n}일 평균 {av:,.0f})')
for ded, who in ((5e7, '성인'), (2e7, '미성년')):
    base = max(0, sh*av - ded); t = tax(base)
    print(f'   {who}: 과표 {base:,.0f} · 산출 {t:,.0f} · 신고 3% 공제 뒤 {t*0.97:,.0f} | 종가로 셌다면 과표 {max(0,sh*c-ded):,.0f} 세금 {tax(max(0,sh*c-ded))*0.97:,.0f}')
d = dt.date(2026, 6, 26)
c, av, n, a, b = val(s, d); sh = int(5e7 // c)
print(f'== 반대 예시 6/26 삼성전자: 종가 {c:,.0f}, {sh}주 = {sh*c:,.0f} · 평가액 {sh*av:,.0f}({a}~{b} {n}일 평균 {av:,.0f})')
print('신고기한: 7/28 증여 → 7월 31일부터 3개월 = 10월 31일 · 평가 기간 끝 9/28 · 11/6 증여 → 11/30+3개월 = 2027-02-28(일) · 평가 기간 끝 2027-01-06')
