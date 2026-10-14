# pencap1015 연금계좌세액공제가 결정세액에 막히는 지점 — 소득세법(2026.1.1 시행본, 법령 API 2026-10-14 15:26 조회 law_sodeuk.xml)
# 제47조 근로소득공제·제55조 세율·제59조 근로소득세액공제·제59조의3 연금계좌세액공제(12%/15%, 600·900만원)
# 제59조의4⑨ 표준세액공제 13만원(제52조 보험료 특별소득공제를 신청하지 않은 경우)·제61조③ 초과분은 연금계좌세액공제를 받지 않은 것으로 봄
# 가정: 1인 가구(본인 기본공제 150만원), 연봉=총급여(비과세 없음), 다른 공제·세액공제 없음
#   4대보험 근로자 몫: 국민연금 4.75%(제51조의3 연금보험료공제) · 건강 3.595% · 장기요양 = 건강×13.14% · 고용 0.9%
#   보험료 특별소득공제(건강·장기요양·고용)를 받는 경우와 표준세액공제 13만원을 받는 경우 중 세금이 적은 쪽
import sys; sys.stdout.reconfigure(encoding='utf-8')
MAN = 10_000
def earn_ded(p):
    for top, base, lo, r in [(500e4,0,0,.7),(1500e4,350e4,500e4,.4),(4500e4,750e4,1500e4,.15),(1e8,1200e4,4500e4,.05)]:
        if p <= top: return min(base+(p-lo)*r, 2000e4)
    return min(1475e4+(p-1e8)*.02, 2000e4)
def calc_tax(b):
    for top, base, lo, r in [(1400e4,0,0,.06),(5000e4,84e4,1400e4,.15),(8800e4,624e4,5000e4,.24),(1.5e8,1536e4,8800e4,.35)]:
        if b <= top: return base+(b-lo)*r
def credit59(t, pay):
    c = t*.55 if t <= 130e4 else 71.5e4+(t-130e4)*.3
    if pay <= 3300e4: lim = 74e4
    elif pay <= 7000e4: lim = max(74e4-(pay-3300e4)*8/1000, 66e4)
    elif pay <= 1.2e8: lim = max(66e4-(pay-7000e4)/2, 50e4)
    else: lim = max(50e4-(pay-1.2e8)/2, 20e4)
    return min(c, lim)
def before_pension(pay):
    m = pay/12
    nps = min(int(m//1000*1000), 659e4)*.0475*12
    hi = m*.03595*12; ltc = hi*.1314; emp = m*.009*12
    out = {}
    for opt, ins, std in [('보험료공제', hi+ltc+emp, 0), ('표준13만', 0, 13e4)]:
        base = max(0, pay-earn_ded(pay)-150e4-nps-ins)
        t = calc_tax(base); c59 = credit59(t, pay)
        out[opt] = (base, t, c59, max(0, t-c59-std))
    return out
def won(x): return f'{round(x):,}원'
print('연봉 | 과표 | 산출세액 | 근로소득세액공제 | 남은 소득세(연금 넣기 전) | 공제율 | 세금 줄이는 납입 상한 | 900만원 넣을 때 실제 환급(지방세 포함) | 900만원 중 공제 못 받는 몫')
for p in [2500, 3000, 3500, 4000, 4500, 5000, 5500, 7000]:
    pay = p*MAN; o = before_pension(pay)
    opt = min(o, key=lambda k: o[k][3]); base, t, c59, rest = o[opt]
    rate = .15 if pay <= 5500*MAN else .12
    cap = min(900*MAN, rest/rate)
    refund = min(rest, 900*MAN*rate)*1.1
    print(f'{p:,}만원 | {won(base)} | {won(t)} | {won(c59)} | {won(rest)} ({opt}; 다른 쪽 {won(o["표준13만" if opt=="보험료공제" else "보험료공제"][3])}) | {rate*110:.1f}% | {won(cap)} | {won(refund)} | {won(900*MAN-cap)}')

print('\n[예시] 납입액별 줄어드는 세금(소득세+지방소득세 10%)')
for p in [3000, 3500]:
    pay = p*MAN; o = before_pension(pay); rest = min(v[3] for v in o.values())
    for x in [300, 600, 900]:
        cut = min(rest, x*MAN*.15)
        print(f'  연봉 {p:,}만원 · {x}만원 납입: 소득세 {won(cut)} 줄고 지방세 포함 {won(cut*1.1)} · 공제 못 받은 납입액 {won(x*MAN - cut/.15)}')

print('\n[부양가족] 소득 없는 배우자 1명 기본공제(150만원) 더할 때 — 자녀 없음')
def before_pension_n(pay, extra):
    m = pay/12
    nps = min(int(m//1000*1000), 659e4)*.0475*12
    hi = m*.03595*12; ltc = hi*.1314; emp = m*.009*12
    best = None
    for ins, std in [(hi+ltc+emp, 0), (0, 13e4)]:
        base = max(0, pay-earn_ded(pay)-150e4-extra-nps-ins)
        t = calc_tax(base); r = max(0, t-credit59(t, pay)-std)
        best = r if best is None else min(best, r)
    return best
for p in [3000, 3500, 4000]:
    pay = p*MAN; r = before_pension_n(pay, 150e4)
    print(f'  연봉 {p:,}만원 + 배우자: 남는 소득세 {won(r)} → 상한 {won(min(900*MAN, r/.15))}')
