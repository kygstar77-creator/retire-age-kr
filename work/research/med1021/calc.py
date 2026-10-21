# 의료비 세액공제 예시 계산(소득세법 59조의4②·시행령 118조의5) — firemap-write 2026-10-21
import sys; sys.stdout.reconfigure(encoding='utf-8')
def credit(pay, general=0, special=0):
    th = pay*0.03
    g_over = general - th
    if g_over >= 0:
        base = min(g_over, 7_000_000) + special
    else:
        base = max(0, special + g_over)  # 2호: 1호가 문턱에 못 미치면 그 미달액을 뺌
    return th, base, base*0.15
pay = 50_000_000
for name, g, s in [('A 어머니 70세 1,000만원(65세 이상=2호, 한도 없음)',0,10_000_000),
                   ('B 어머니 63세 1,000만원(1호, 700만원 한도)',10_000_000,0),
                   ('C 어머니 70세 1,000만원 중 실손 400만원 받음 → 600만원',0,6_000_000),
                   ('D 어머니 70세 140만원',0,1_400_000),
                   ('E 어머니 63세 3,000만원(1호)',30_000_000,0),
                   ('F 어머니 70세 3,000만원(2호)',0,30_000_000)]:
    th, base, c = credit(pay, g, s)
    print(f'{name}: 문턱 {th:,.0f} · 공제 대상 {base:,.0f} · 세액공제 {c:,.0f}')
for p in [30_000_000, 50_000_000, 70_000_000, 100_000_000]:
    print(f'총급여 {p:,} → 문턱(3%) {p*0.03:,.0f}')
