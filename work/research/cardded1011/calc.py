# cardded1011 신용카드 소득공제 계산 — 조세특례제한법 제126조의2(2026.1.1 시행본, 법령 API 2026-10-10 조회 law_jotuk.xml)
# 세금 차이: 소득세법 제47조(근로소득공제)·제55조(세율)·제59조(근로소득세액공제) + 지방소득세 10%
# 가정: 1인 가구(본인 기본공제 150만원), 연봉=총급여, 식대 등 비과세 없음, 4대보험 근로자 몫만 소득공제
#       (국민연금 4.75%·상한 월 659만원 / 건강 3.595% / 장기요양 = 건강×13.14% / 고용 0.9%), 그 밖 공제·세액공제 없음
#       카드 사용은 전부 일반 가맹점(전통시장·대중교통·문화 없음), 자녀 없음, 1~9월은 신용카드
import sys; sys.stdout.reconfigure(encoding='utf-8')
MAN = 10_000

def card_ded(pay, credit, debit, trad=0, bus=0, kids=0):
    """제126조의2 ②·⑥·⑩·⑪ (문화체육 0)"""
    low = pay * 0.25
    c1, c2 = trad * 0.40, bus * 0.40
    c4, c5 = debit * 0.30, credit * 0.15
    gross = c1 + c2 + c4 + c5
    if low <= credit: sub = low * 0.15
    elif low <= credit + debit: sub = credit * 0.15 + (low - credit) * 0.30
    else: sub = credit * 0.15 + debit * 0.30 + (low - credit - debit) * 0.40
    d = max(0, gross - sub)
    if pay <= 7000 * MAN: lim = {0: 300, 1: 350}.get(kids, 400) * MAN; extra = 300 * MAN
    else: lim = {0: 250, 1: 275}.get(kids, 300) * MAN; extra = 200 * MAN
    if d <= lim: return d
    return lim + min(d - lim, min(c1 + c2, extra))

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

def final_tax(pay, cardd):
    m = pay / 12
    nps = min(int(m // 1000 * 1000), 659e4) * .0475 * 12
    hi = m * .03595 * 12; ltc = hi * .1314; emp = m * .009 * 12
    base = max(0, pay - earn_ded(pay) - 150e4 - nps - hi - ltc - emp - cardd)
    t = calc_tax(base); t = max(0, t - credit59(t, pay))
    return t * 1.1, base

def won(x): return f'{round(x):,}원'

print('[표1] 연봉별 문턱(총급여 25%)과 기본한도까지 필요한 연간 사용액(자녀 없음, 일반 가맹점)')
for p in [3000, 5000, 7000, 9000]:
    pay = p * MAN; low = pay * .25; lim = (300 if pay <= 7000 * MAN else 250) * MAN
    print(f'  연봉 {p:,}만원: 문턱 {low/MAN:,.0f}만원 · 신용카드만 쓰면 {(low + lim/.15)/MAN:,.1f}만원 · 체크카드만 쓰면 {(low + lim/.30)/MAN:,.1f}만원에서 한도 {lim/MAN:,.0f}만원')

print('\n[표2] 1~9월 신용카드, 10~12월 같은 금액을 신용카드로 계속 vs 체크카드로 바꿈')
rows = []
for p, mon in [(3000, 150), (5000, 150), (5000, 300), (7000, 150), (9000, 150)]:
    pay = p * MAN; m = mon * MAN
    a = card_ded(pay, 12 * m, 0); b = card_ded(pay, 9 * m, 3 * m)
    ta, ba = final_tax(pay, a); tb, bb = final_tax(pay, b)
    rows.append((p, mon, a, b, ta - tb))
    print(f'  연봉 {p:,}만원·월 {mon}만원: 공제 {won(a)} → {won(b)} (+{won(b-a)}) · 결정세액+지방세 {won(ta)} → {won(tb)} (−{won(ta-tb)}) · 과표 {won(ba)}')

print('\n[검증] 순서 무관 — 연봉 5,000만원, 신용 1,000만·체크 800만: 산식(나목) 공제', won(card_ded(5000*MAN, 1000*MAN, 800*MAN)))
print('[검증] 같은 1,800만원을 전부 신용카드:', won(card_ded(5000*MAN, 1800*MAN, 0)), ' 전부 체크카드:', won(card_ded(5000*MAN, 0, 1800*MAN)))
print('\n[자녀] 연봉 5,000만원·월 300만원(연 3,600만원) 신용→10~12월 체크 전환: 자녀 0/1/2명')
for k in (0, 1, 2):
    a = card_ded(5000*MAN, 3600*MAN, 0, kids=k); b = card_ded(5000*MAN, 2700*MAN, 900*MAN, kids=k)
    print(f'  자녀 {k}명: 공제 {won(a)} → {won(b)} (+{won(b-a)}) · 세금 −{won(final_tax(5000*MAN,a)[0]-final_tax(5000*MAN,b)[0])}')
print('\n[추가한도] 연봉 5,000만원·신용 3,600만원 + 대중교통 체크 120만·전통시장 체크 60만원:',
      won(card_ded(5000*MAN, 3600*MAN, 0, trad=60*MAN, bus=120*MAN)))
