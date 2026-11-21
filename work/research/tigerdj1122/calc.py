# tigerdj1122 — TIGER 미국배당다우존스(458730) vs SCHD 직접(원화) 상장 뒤 총수익, 2026-11-21
# 원자료: raw/*_chart_20261121.json(야후), raw/fred_DEXKOUS_20261121.json, raw/tiger_dist_page_1121.txt(미래에셋 연간 합)
import json, datetime as dt
def load(t):
    d = json.load(open(f'raw/{t}_chart_20261121.json'))['chart']['result'][0]
    ts = [dt.datetime.fromtimestamp(x, dt.UTC).date() for x in d['timestamp']]
    c = d['indicators']['quote'][0]['close']
    px = {a: b for a, b in zip(ts, c) if b}
    ev = {dt.datetime.fromtimestamp(int(k), dt.UTC).date(): v['amount'] for k, v in d.get('events', {}).get('dividends', {}).items()}
    return px, ev
T, Tev = load('458730.KS'); S, Sev = load('SCHD'); FX, _ = load('KRW=X')
Tev[dt.date(2023, 9, 26)] = 33.0   # 야후에 빠짐 — 미래에셋 2023년 합 202 - 야후 169 = 33
fred = {dt.date.fromisoformat(a): float(b) for a, b in json.load(open('raw/fred_DEXKOUS_20261121.json'))}
def prev(dic, d):
    k = [x for x in dic if x <= d]; return max(k)
def fxat(d): return FX[prev(FX, d)]
print('TIGER 분배 연도별 합', {y: sum(v for k, v in Tev.items() if k.year == y) for y in (2023, 2024, 2025, 2026)})
print('TIGER 분배 횟수', len(Tev), '최근 12번 합', sum(v for k, v in sorted(Tev.items())[-12:]))
def tr_kr(start, end):   # TIGER 총수익: 분배락일 종가로 재투자(세전)
    days = sorted(d for d in T if start <= d <= end); u = 1.0
    for d in days:
        if d in Tev and d != days[0]: u += u * Tev[d] / T[d]
    return u * T[days[-1]] / T[days[0]], days[0], days[-1]
def us_day(kd):  # 한국 날짜 kd 종가에 반영된 미국 종가 = kd 이전 미국 거래일
    return max(x for x in S if x < kd)
def tr_us(kstart, kend, wh=0.15):  # SCHD 직접: 미국 종가 × 그날 환율, 배당은 15% 떼고 재투자
    s0, s1 = us_day(kstart), us_day(kend); u = 1.0
    for d in sorted(x for x in S if s0 < x <= s1):
        if d in Sev: u += u * Sev[d] * (1 - wh) / S[d]
    usd = u * S[s1] / S[s0]; f0, f1 = fxat(kstart), fxat(kend)
    return usd * f1 / f0, usd, f0, f1, s0, s1
def show(a, b, tag):
    t, d0, d1 = tr_kr(a, b); k, usd, f0, f1, s0, s1 = tr_us(d0, d1); k0 = tr_us(d0, d1, 0)[0]
    print(f'{tag} {d0}~{d1} TIGER {100*(t-1):.1f}% | SCHD원화(15%뗌) {100*(k-1):.1f}% (달러 {100*(usd-1):.1f}%, 환율 {f0:.1f}->{f1:.1f}, 미국 {s0}~{s1}) | 안 뗌 {100*(k0-1):.1f}% | 차이 {100*(t-k):.2f}%p | 1억: {1e8*t/1e4:,.0f}만 vs {1e8*k/1e4:,.0f}만')
first = min(T); last = max(T)
show(first, last, '상장 뒤')
for y in (2024, 2025):
    show(dt.date(y, 1, 1), dt.date(y, 12, 31), f'{y}년')
show(dt.date(2026, 1, 1), last, '2026년')
show(last - dt.timedelta(days=365), last, '최근 1년')
# 환율 대조: 시작·끝 야후 vs FRED
for d in (first, last):
    fd = prev(fred, d); print('환율', d, '야후', round(fxat(d), 2), 'FRED', fd, fred[fd])
print('TIGER 종가', first, T[first], last, T[last]); print('SCHD 종가', us_day(first), S[us_day(first)], us_day(last), S[us_day(last)])
print('SCHD 배당 횟수(기간)', len([d for d in Sev if us_day(first) < d <= us_day(last)]))
# 네이버 Y3(연평균으로 보임) 대조용: 3년 누적·연평균
t3, a3, b3 = tr_kr(dt.date(2023, 11, 20), dt.date(2026, 11, 19))
print(f'3년 {a3}~{b3} TIGER 누적 {100*(t3-1):.2f}% 연평균 {100*(t3**(1/3)-1):.2f}%')
t1, a1, b1 = tr_kr(dt.date(2025, 11, 19), dt.date(2026, 11, 19)); print(f'1년 {a1}~{b1} TIGER {100*(t1-1):.2f}%')
# 분배 1억 예: 최근 12번 합 ÷ 11/20 종가
ttm = sum(v for k, v in sorted(Tev.items())[-12:]); y = ttm / T[last]
print(f'TIGER 최근 12번 {ttm}원 ÷ {T[last]} = {100*y:.2f}% → 1억 세전 연 {1e8*y/1e4:.0f}만 월 {1e8*y/12/1e4:.1f}만')
s4 = sorted(Sev.items())[-4:]; sy = sum(v for k, v in s4) / S[us_day(last)]
print('SCHD 최근 4번', [(str(k), v) for k, v in s4], f'합 {sum(v for k,v in s4):.4f} ÷ {S[us_day(last)]:.2f} = {100*sy:.2f}%')
# 같은 날 원화 1억으로 시작한 두 계좌 3년 5개월 동안 가장 크게 벌어진 날
days = sorted(d for d in T if d >= first); mx = (0, None)
for d in days[20:]:
    a = tr_kr(first, d)[0]; b = tr_us(first, d)[0]
    if abs(a - b) > abs(mx[0]): mx = (a - b, d)
print(f'가장 크게 벌어진 날 {mx[1]} 차이 {100*mx[0]:.2f}%p(1억이면 {mx[0]*1e8/1e4:.0f}만)')
