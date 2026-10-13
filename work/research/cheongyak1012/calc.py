# cheongyak1012 계산 — 조특법 87조 ②③⑦(facts L3·L7·L8) · 소득세법 55조 세율(facts L10)
# 소득세만 센다(지방소득세 빼고). 세율 한 구간 안에 공제 120만원이 다 들어간다고 본 단순 계산.
import sys; sys.stdout.reconfigure(encoding='utf-8')
PAY = 3_000_000          # 연 납입 인정 한도(L3)
DED = PAY * 40 // 100    # 소득공제액 120만원
YEARS = 3
claw = PAY * YEARS * 6 // 100   # 추징 = 공제 뒤 납입 누계 × 6% (L7)
print(f'공제액/년 {DED:,} · {YEARS}년 납입 누계 {PAY*YEARS:,} · 추징(6%) {claw:,}')
for rate in (6, 15, 24):
    save1 = DED * rate // 100
    save = save1 * YEARS
    pay = min(save, claw)                    # L8: 실제 감면이 적으면 그만큼만
    print(f'세율 {rate}%: 1년 감면 {save1:,} · {YEARS}년 감면 {save:,} · 추징 {claw:,} · 증명하면 {pay:,} · 남는 돈 {save-pay:,} · 증명 안 하면 차이 {save-claw:,}')
print('15% 구간: 공제율 40% × 세율 15% = 6% = 추징률')
