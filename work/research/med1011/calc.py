# med1011 부모님 의료비 세액공제 — 소득세법 제59조의4 ②(법령 API 2026-10-10 조회 law_act.xml), 시행령 제118조의5(law_dec.xml)
# 계산 틀은 cardded1011/calc.py 재사용: 소득세법 제47조 근로소득공제·제55조 세율·제59조 근로소득세액공제
# 가정: 1인 가구(본인 기본공제 150만원), 연봉=총급여, 비과세 없음, 4대보험 근로자 몫만 공제, 그 밖 공제 없음,
#       부모님 65세 이상(제2호 다목), 본인 의료비 0원, 표준세액공제 13만원(제59조의4 ⑨1호) 대신 특별세액공제 신청
import sys; sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'../cardded1011')
MAN = 10_000
def earn_ded(p):
    for top, base, lo, r in [(500e4, 0, 0, .7), (1500e4, 350e4, 500e4, .4), (4500e4, 750e4, 1500e4, .15), (1e8, 1200e4, 4500e4, .05)]:
        if p <= top: return min(base + (p - lo) * r, 2000e4)
    return min(1475e4 + (p - 1e8) * .02, 2000e4)
def calc_tax(base):
    for top, b, lo, r in [(1400e4, 0, 0, .06), (5000e4, 84e4, 1400e4, .15), (8800e4, 624e4, 5000e4, .24), (1.5e8, 1536e4, 8800e4, .35)]:
        if base <= top: return b + (base - lo) * r
    raise ValueError
def credit59(tax, pay):
    c = tax * .55 if tax <= 130e4 else 71.5e4 + (tax - 130e4) * .3
    if pay <= 3300e4: lim = 74e4
    elif pay <= 7000e4: lim = max(74e4 - (pay - 3300e4) * 8 / 1000, 66e4)
    elif pay <= 1.2e8: lim = max(66e4 - (pay - 7000e4) / 2, 50e4)
    else: lim = max(50e4 - (pay - 1.2e8) / 2, 20e4)
    return min(c, lim)
def pre_tax(pay):
    """의료비 공제 전 산출세액에서 근로소득세액공제까지 뺀 세액(소득세)"""
    m = pay / 12
    nps = min(int(m // 1000 * 1000), 659e4) * .0475 * 12
    hi = m * .03595 * 12; ltc = hi * .1314; emp = m * .009 * 12
    base = max(0, pay - earn_ded(pay) - 150e4 - nps - hi - ltc - emp)
    t = calc_tax(base); return t, max(0, t - credit59(t, pay)), base
def med_credit(pay, paid):
    """제59조의4 ②2호(65세 이상 부모님 의료비): 지급액 − 총급여 3% 문턱(본인 의료비 0원이라 미달분 전부), ×15%"""
    th = pay * .03
    return max(0, paid - th) * .15, th
def won(x): return f'{round(x):,}원'
def mw(x): return f'{x/MAN:,.1f}만원'
if __name__ == '__main__':
    PAID = 600 * MAN
    print('[표1] 부모님 병원비 600만원(65세 이상) 한 사람이 다 냈을 때 — 연봉별 문턱·공제액')
    for p in [3000, 4000, 6000, 8000, 10000]:
        pay = p * MAN; c, th = med_credit(pay, PAID); t0, t1, b = pre_tax(pay)
        eff = min(c, t1)  # 결정세액이 0 아래로는 못 내려감
        net = max(0, eff - 13e4)
        print(f'  연봉 {p:,}만원: 문턱 {th/MAN:,.0f}만원 · 공제대상 {(PAID-th)/MAN:,.0f}만원 · 세액공제 {won(c)} · 낼 세금(의료비 전, 근로소득세액공제 후) {won(t1)} · 실제 줄어드는 소득세 {won(eff)} · 표준세액공제 13만 대신 신청해 늘어나는 몫 {won(net)} (+지방소득세 10% {won(net*.1)})')
    print('\n[표2] 형(연봉 8,000만원)·동생(연봉 4,000만원) 600만원 병원비 — 누가 내서 신청하나')
    for name, a, b in [('동생이 600만원 다 냄', 600, 0), ('형이 600만원 다 냄', 0, 600), ('반반 300만원씩 냄', 300, 300)]:
        s = 0; row = []
        for pay, paid in [(4000*MAN, a*MAN), (8000*MAN, b*MAN)]:
            c, th = med_credit(pay, paid) if paid else (0, pay*.03)
            row.append(c)
        tot = sum(row); print(f'  {name}: 동생 {won(row[0])} + 형 {won(row[1])} = {won(tot)}')
    print('\n[표3] 동생 연봉이 낮으면 — 낼 세금이 공제보다 적을 때')
    for p in [2000, 2500, 3000, 3500, 4000]:
        pay = p * MAN; c, th = med_credit(pay, PAID); t0, t1, b = pre_tax(pay)
        print(f'  연봉 {p:,}만원: 세액공제 {won(c)} / 낼 세금 {won(t1)} → 줄어드는 세금 {won(min(c,t1))}, 못 쓰는 공제 {won(max(0,c-t1))}')
    print('\n[문턱 순서 확인] 법 ②2호 단서 — 제1호 의료비가 문턱에 미달하면 그 미달액을 뺌')
    pay=4000*MAN
    print('  본인 의료비 100만원 + 부모님 500만원, 연봉 4,000만원: 본인 100만원이 문턱 120만원에 20만원 모자람 →', won(max(0,(500*MAN-(pay*.03-100*MAN)))*.15))
    print('  본인 의료비 0원 + 부모님 600만원:', won((600*MAN-pay*.03)*.15), '(위 두 경우 합이 같음: 의료비 총액 600만원에서 문턱 120만원을 한 번 뺌)')
