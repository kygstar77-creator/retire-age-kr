# 코스피200 ETF(KODEX 200) 1년: 한 번에 산 경우 vs 매달 나눠 산 경우 — 종가는 Yahoo chart(069500.KS), 분배금은 같은 자료 events(삼성 S1과 대조)
import json, datetime as dt, sys
sys.stdout.reconfigure(encoding='utf-8')
c = sys.argv[1] if len(sys.argv) > 1 else '069500'
d = json.load(open(f'raw/yh_{c}.json', encoding='utf-8'))['chart']['result'][0]
ts = [dt.datetime.fromtimestamp(t).date() for t in d['timestamp']]
cl = d['indicators']['quote'][0]['close']
px = {t: p for t, p in zip(ts, cl) if p}
divs = sorted((dt.datetime.fromtimestamp(v['date']).date(), v['amount']) for v in d['events']['dividends'].values())
days = sorted(px)
START, END = dt.date(2025, 11, 12), dt.date(2026, 11, 12)
def on_or_after(day): return next(x for x in days if x >= day)
end = max(x for x in days if x <= END); pend = px[end]
MONTHLY = 500_000
# 매달 나눠 사기: 2025-11-12부터 매달 12일(휴장이면 다음 거래일) 50만원, 12번 — 마지막 2026-10-12
buys = []
for i in range(12):
    y, m = 2025 + (10 + i) // 12, (10 + i) % 12 + 1
    day = on_or_after(dt.date(y, m, 12)); buys.append((day, px[day]))
sh = 0.0; cash_div = 0.0; out = []
for day, p in buys:
    sh += MONTHLY / p; out.append(f'  {day} 종가 {p:,.0f}원 → 누적 {sh:.2f}주')
for dday, amt in divs:
    if START < dday <= END:
        held = sum(MONTHLY / p for b, p in buys if b < dday)
        cash_div += held * amt
paid = MONTHLY * 12
val = sh * pend
print(f'[{c}] 끝 {end} 종가 {pend:,.0f}원')
print('\n'.join(out))
print(f'나눠 사기: 넣은 돈 {paid:,}원 · 평가 {val:,.0f}원 · 분배금(세전) {cash_div:,.0f}원 · 합 {val+cash_div:,.0f}원 · 수익률 {(val+cash_div)/paid*100-100:.2f}%')
avg = paid / sh
print(f'  평균 매입가 {avg:,.0f}원 (끝 종가 대비 {pend/avg*100-100:.2f}%)')
s0 = on_or_after(START); p0 = px[s0]; sh1 = paid / p0
div1 = sum(sh1 * a for dd, a in divs if START < dd <= END)
print(f'한 번에 사기: {s0} 종가 {p0:,.0f}원 {paid:,}원 → 평가 {sh1*pend:,.0f}원 · 분배금(세전) {div1:,.0f}원 · 합 {sh1*pend+div1:,.0f}원 · 수익률 {(sh1*pend+div1)/paid*100-100:.2f}%')
hi = max((px[x], x) for x in days if START <= x <= END)
print(f'1년 중 가장 높은 종가 {hi[1]} {hi[0]:,.0f}원 → 끝 종가 {pend/hi[0]*100-100:.2f}%')
print('분배금:', [(str(a), b) for a, b in divs if START < a <= END])
mo = [(x, px[x]) for x in days if x >= dt.date(2026, 10, 12)]
print('한 달 전(10/12 다음 거래일) → 끝:', mo[0], f'{pend/mo[0][1]*100-100:.2f}%')

# 대조: 네이버 일별 시세(수정주가, 분배금 반영) — raw/nv_sise_069500.txt
import re
t = open('raw/nv_sise_069500.txt', encoding='utf-8', errors='ignore').read()
nv = {dt.datetime.strptime(r[0], '%Y%m%d').date(): float(r[1]) for r in re.findall(r'\["(\d{8})",\s*[\d.]+,\s*[\d.]+,\s*[\d.]+,\s*([\d.]+)', t)}
nb = [(b, nv[b]) for b, _ in buys]
shn = sum(MONTHLY / p for _, p in nb); ne = nv[end]
print(f'[대조·네이버 수정주가] 나눠 사기 {shn*ne:,.0f}원({shn*ne/paid*100-100:.2f}%) · 한 번에 사기 {paid/nv[s0]*ne:,.0f}원({ne/nv[s0]*100-100:.2f}%)')
# 50만원씩이면 매달 산 주수 (1주 단위가 아니라 소수 — 실제로는 1주 단위)
print('매달 50만원으로 살 수 있는 주수(1주 단위):', [int(MONTHLY // p) for _, p in buys])

# 같은 12번 산 몫을 10월 30일 종가로 매기면(2주 전 시점)
for dd in [dt.date(2026, 10, 30), dt.date(2026, 11, 2)]:
    if dd in px:
        print(f'{dd} 종가 {px[dd]:,.0f}원으로 매기면 나눠 사기 평가 {sh*px[dd]:,.0f}원({sh*px[dd]/paid*100-100:.2f}%, 분배금 빼고)')
# 산 달별 지금 손익
print('달별 50만원의 지금 값(분배금 빼고):', [(str(b), round(MONTHLY / p * pend)) for b, p in buys])
print('11월 종가들:', [(str(x), px[x]) for x in days if x >= dt.date(2026, 10, 28)])
