# fxdepfee1026 계산 — 달러 정기예금 1년, 환전 수수료(전신환 스프레드)까지 넣은 본전 환율
# 입력: KB국민은행 2026-10-26 15:18:11 고시(256회차, obank.kbstar.com C101423) 매매기준율 1,323.70·송금 보내실 때 1,336.50·받으실 때 1,310.90
#       KB국민은행 거주자 USD 정기예금 12개월이상~18개월미만 연 3.60740%(조회기준일 2026-10-26, 주 표·KB국민UP외화정기예금 12개월 3.6074 같음 — 3.55169는 9개월이상~12개월미만 칸), 이자 세금 15.4%(소득세 14%+지방소득세 1.4%)
import sys; sys.stdout.reconfigure(encoding='utf-8')
P = 100_000_000
base, send, recv = 1323.70, 1336.50, 1310.90
sb, ss = (send - base) / base, (base - recv) / base   # 살 때·팔 때 스프레드 비율
spread = sb
rate, tax = 0.0360740, 0.154
net = rate * (1 - tax)
print(f'한쪽 스프레드 {spread*100:.3f}%  세후 이자율 {net*100:.4f}%')
rows = []
for u in (0.0, 0.5, 0.9):
    buy = base * (1 + sb * (1 - u))
    usd = P / buy
    end = usd * (1 + net)
    be_base = P / (end * (1 - ss * (1 - u)))       # 1년 뒤 매매기준율이 이 값 밑이면 원화로 손해
    drop = (base - be_base) / base * 100
    rows.append((u, buy, usd, end, be_base, drop))
    print(f'우대 {u*100:.0f}%: 살 때 {buy:,.2f}원 → {usd:,.2f}달러 → 1년 뒤 {end:,.2f}달러 · 본전 기준율 {be_base:,.1f}원 (지금보다 {drop:.2f}% 아래)')
# 수수료 없이(기준율로 사고팔 때)
usd0 = P / base; end0 = usd0 * (1 + net); be0 = P / end0
print(f'수수료 없음: 본전 기준율 {be0:,.1f}원 (지금보다 {(base-be0)/base*100:.2f}% 아래)')
# 환율 그대로일 때 1년 뒤 원화(우대별)
for u, buy, usd, end, be, d in rows:
    won = end * base * (1 - ss * (1 - u))
    print(f'우대 {u*100:.0f}%: 환율 그대로면 1년 뒤 {won:,.0f}원 (이자 몫 {won-P:,.0f}원)')
print(f'환율 그대로·수수료 없음: {end0*base:,.0f}원 (이자 {end0*base-P:,.0f}원)')
# 수수료(우대 0%)로 바로 사고 팔면 드는 돈
print(f'바로 사고 팔면(우대 0%) 1억이 {P/send*recv:,.0f}원 → 차이 {P - P/send*recv:,.0f}원')
