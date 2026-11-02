# pen600_1102 계산 — 소득세법 제59조의3①(15%/12%, 연금저축 600만원·합계 900만원), 지방세특례제한법 제167조의2①(소득세 공제액의 10%)
import sys; sys.stdout.reconfigure(encoding='utf-8')
def credit(pension, irp, rate):
    base = min(min(pension, 600) + irp, 900)
    tax = base * rate; local = tax * 0.1
    return base, tax, local, tax + local
for rate in (0.15, 0.12):
    for p, i in ((900, 0), (600, 0), (900, 300), (600, 300)):
        b, t, l, s = credit(p, i, rate)
        print(f'공제율 {rate:.0%} 연금저축 {p} + IRP {i} → 인정 {b}만원 · 소득세 {t:.1f} · 지방소득세 {l:.2f} · 합 {s:.2f}만원')
    print(f'  IRP 새 돈 300만원 더 넣을 때 늘어나는 합: {credit(900,300,rate)[3]-credit(900,0,rate)[3]:.2f}만원')
    print(f'  연금저축 초과 300만원을 IRP로 이전(제59조의3①2호 제외) → 늘어나는 합 0만원')
