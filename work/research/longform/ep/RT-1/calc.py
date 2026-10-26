# RT-1 일시금 vs IRP 연금수령 세금 (youtube-loop 2026-10-26) — 퇴직소득세는 rettax1022/calc.py(홈택스 모의계산 5건 원 단위 일치) 그대로 가져옴
# 연금수령 세율: 소득세법 129조①5의3 — 실제 수령연차 10년 이하 70% · 10년 초과~20년 60% · 20년 초과 50% (연금외수령 원천징수세율 대비)
# 운용수익은 빼고 퇴직금 원금 부분만 본다(운용수익 세율 129조①5의2 나이별은 research에서 따로 확인).
import sys; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\research\rettax1022')
sys.stdout.reconfigure(encoding='utf-8')
from calc import ret
for P in (5e7, 1e8, 2e8, 3e8):
    for n in (5, 10, 15, 20, 25, 30):
        r = ret(P, n); L = r['total']
        a70, a60, a50 = int(L*.7), int(L*.6), int(L*.5)
        print(f"{P/1e4:>6.0f}만 근속{n:>2}년 | 일시금 {L:>11,} ({r['eff']:.2f}%) | 연금 1~10년차 {a70:>11,} (아낌 {L-a70:>10,}) | 11~20년차 {a60:>11,} (아낌 {L-a60:>10,}) | 21년차~ {a50:>11,} (아낌 {L-a50:>10,})")
# 연금수령한도(시행령 40조의2③3): 평가액 ÷ (11 − 연금수령연차) × 120%. 1년차 평가액 1억이면
for y in (1, 2, 5, 10):
    print(f"한도 {y}년차, 평가액 1억 → {1e8/(11-y)*1.2:,.0f}원")
# 경쟁 qh3a_fsRgzU [02:34] '퇴직금 4억이면 세금 4,000만원(10%)' — 근속 없이 말함. 근속별로 보면:
for n in (5, 10, 15, 20, 25, 30):
    r = ret(4e8, n); print(f"4억 근속{n:>2}년 일시금 {r['total']:,} ({r['eff']:.2f}%)")
