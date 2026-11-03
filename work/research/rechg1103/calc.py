# 재건축부담금 — 재건축초과이익 환수에 관한 법률 제12조(부과율)·제14조의2(1세대 1주택 감경) 원문 식 (raw/law_제12조.txt, raw/law_제14조의2.txt, 2026-11-03 받음)
# 조합원 1인당 평균이익 A(원) → 1인당 평균 부담금. 실제 개인 몫은 제6조③ 조합원별 분담기준으로 달라진다(이 식은 평균).
import sys
sys.stdout.reconfigure(encoding='utf-8')
M = 10_000
def charge(a):
    if a <= 8000*M: return 0
    if a <= 13000*M: return (a-8000*M)*0.10
    if a <= 18000*M: return 500*M + (a-13000*M)*0.20
    if a <= 23000*M: return 1500*M + (a-18000*M)*0.30
    if a <= 28000*M: return 3000*M + (a-23000*M)*0.40
    return 5000*M + (a-28000*M)*0.50
CUT = [(6,0.10),(7,0.20),(8,0.30),(9,0.40),(10,0.50),(15,0.60),(20,0.70)]
def cut(years):
    r = 0
    for y, p in CUT:
        if years >= y: r = p
    return r
for a in [8000, 10000, 13000, 15000, 20000, 30000, 50000]:
    c = charge(a*M)
    print(f"평균이익 {a/10000:g}억: 부담금 {c/M:,.0f}만원 (이익의 {c/(a*M)*100:.1f}%) | 1주택 6년 {c*(1-cut(6))/M:,.0f} · 10년 {c*(1-cut(10))/M:,.0f} · 15년 {c*(1-cut(15))/M:,.0f} · 20년 {c*(1-cut(20))/M:,.0f}만원")
# 경계 확인
for a in [13000, 18000, 23000, 28000]:
    print('경계', a, charge(a*M)/M)
