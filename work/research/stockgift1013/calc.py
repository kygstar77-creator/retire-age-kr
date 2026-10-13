# stockgift1013 — 상장주식 증여 평가: 증여일 앞뒤 각 2개월 종가 평균(상증법 제63조①1가)
# 시세: 다음 금융 일별 시세 API(finance.daum.net/api/quote/A005930/days, 한국거래소 정규장 종가, 2026-10-13 18:3x 조회) daum_005930.json
#   네이버 일봉은 장 마감 뒤 넥스트레이드 거래까지 묶은 값이라(10/13 18:28 236,500원·거래량 계속 증가) 법이 말하는 '거래소 최종 시세'와 다르다.
#   Yahoo chart API 10/13 232,000원은 다음 값과 같지만 10/12가 비어 있다.
# 세율 제26조(제56조 준용) · 직계존속→성인 자녀 공제 5천만원(제53조, 10년 합산 — 그 전 10년 증여 없다고 가정)
# 신고세액공제 3%(제69조②) · 최대주주 할증(제63조③)은 일반 개인 소액주주라 없음
import sys, re, datetime as D
sys.stdout.reconfigure(encoding='utf-8')
import json
rows = {D.date.fromisoformat(k): int(v) for k, v in json.load(open('daum_005930.json', encoding='utf-8'))}
def addm(d, k):
    y, mo = d.year, d.month + k
    while mo > 12: y += 1; mo -= 12
    while mo < 1: y -= 1; mo += 12
    return D.date(y, mo, min(d.day, 28 if mo == 2 else 30 if mo in (4, 6, 9, 11) else 31))
def tax(base):
    if base <= 0: return 0
    if base <= 1e8: return base * 0.10
    if base <= 5e8: return 1e7 + (base - 1e8) * 0.20
    return 9e7 + (base - 5e8) * 0.30
def pay(value):
    t = tax(value - 5e7)
    return t * 0.97
def w(x): return f'{round(x):,}원'

g = D.date(2026, 7, 28)
p0 = rows[g]; prev = rows[max(d for d in rows if d < g)]
n = int(1e8 // p0)
print(f'증여일 {g} 종가 {p0:,}원 (전일 {prev:,}원, {p0/prev*100-100:.1f}%) · 1억원어치 = {n}주 = {w(n*p0)}')
before = [rows[d] for d in sorted(rows) if addm(g, -2) <= d <= g]
after = [rows[d] for d in sorted(rows) if g < d <= addm(g, 2)]
print(f'앞 2개월 {addm(g,-2)}~{g} {len(before)}일 평균 {sum(before)/len(before):,.0f}원 · 뒤 2개월 ~{addm(g,2)} {len(after)}일 평균 {sum(after)/len(after):,.0f}원')
def show(label, after_prices):
    allp = before + after_prices
    avg = sum(allp) / len(allp)
    val = avg * n
    print(f'[{label}] 4개월 평균 {avg:,.0f}원 · 평가액 {w(val)} · 과세표준 {w(val-5e7)} · 신고 시 납부 {w(pay(val))}')
    return avg, val, pay(val)
show('앞 2개월만(참고)', [])
v0 = n * p0
print(f'[당일 종가 기준이라면] 평가액 {w(v0)} · 납부 {w(pay(v0))}')
na = len(after)
A = show('(가) 뒤 2개월 그대로', [p0] * na)
B = show('(나) 뒤 2개월 +20%', [p0 * 1.2] * na)
C = show('(다) 뒤 2개월 −10%', [p0 * 0.9] * na)
R = show('실제(뒤 2개월 실제 종가)', after)
# 다른 셈법(앞쪽 경계 하루 뒤)으로 해도 거의 같은지
b2 = [rows[d] for d in sorted(rows) if addm(g, -2) < d <= g]
print(f'경계 하루 바꾼 셈: 실제 평균 {(sum(b2)+sum(after))/(len(b2)+len(after)):,.0f}원')
# 신고기한: 증여일이 속하는 달 말일부터 3개월 — 7월 28일 증여면 10월 31일
print('신고기한(7/28 증여): 2026-10-31 · 4개월 평균이 다 나오는 날: 2026-09-28 무렵')
print('오늘 급락 예: 10/13 종가', f"{rows[D.date(2026,10,13)]:,}", '전일', f"{rows[D.date(2026,10,12)]:,}", '10/8', f"{rows[D.date(2026,10,8)]:,}")
# 오늘(10/13) 급락일에 증여한다면: 앞 2개월(8/13~10/13) 평균은 이미 정해져 있다
t = D.date(2026, 10, 13)
bt = [rows[d] for d in sorted(rows) if addm(t, -2) <= d <= t]
print(f'10/13 증여라면 앞 2개월 {addm(t,-2)}~{t} {len(bt)}일 평균 {sum(bt)/len(bt):,.0f}원 (당일 {rows[t]:,}원보다 {sum(bt)/len(bt)/rows[t]*100-100:.1f}% 높음) · 신고기한 2027-01-31 · 평균 확정 12/13 무렵')
print(f'7/28 사례 평가액/증여일 시가 = {R[1]/v0:.3f} · 세금 차이(실제-당일가) {w(R[2]-pay(v0))}')
# 10/13 증여, 뒤 2개월이 당일 종가에 머문다면(가정): 뒤 2개월 거래일 수는 7/28 사례와 같은 41일로 둔다
avg13 = (sum(bt) + rows[t] * 41) / (len(bt) + 41)
print(f'10/13 증여·뒤 2개월 {rows[t]:,}원 유지 가정: 4개월 평균 {avg13:,.0f}원 · 당일보다 {avg13/rows[t]*100-100:.1f}% 높음')
