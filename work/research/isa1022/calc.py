# isa1022 계산 — PLUS 고배당주(161510) 최근 12회 분배금으로 일반계좌 vs ISA(중개형) 세금
# 근거: 조세특례제한법 제91조의18①②⑤(raw/jotuk91_18.txt) · 소득세법 제129조①2나 14%(raw/sotax129.txt)
#       지방세법 제103조의13① 소득세의 10%(raw/localtax103_13.txt)
#       분배금: 한화자산운용 리포트(raw/plus_report1910.txt) + 야후 161510.KS(raw/y161510.json) · 종가 네이버(raw/n161510_basic.json)
import json, os, datetime, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
y = json.load(open(H + '/raw/y161510.json'))['chart']['result'][0]['events']['dividends']
divs = sorted((datetime.datetime.fromtimestamp(int(k)).date(), v['amount']) for k, v in y.items())
last12 = divs[-12:]
print('최근 12회 분배금(분배락 기준):')
for d, a in last12: print(' ', d, int(a))
D = int(sum(a for _, a in last12))
PRICE = 23060  # 2026-10-21 종가(네이버)
print('12회 합', D, '원 · 10/21 종가', PRICE, '원 · 분배율 %.2f%%' % (D / PRICE * 100))
GEN = 0.154   # 14% + 지방 1.4%
ISA_OVER = 0.099  # 9% + 지방 0.9%
def shares(won): return won // PRICE
def gen_tax(div): return round(div * GEN)
def isa_tax(total, limit): return round(max(0, total - limit) * ISA_OVER)
print()
s1 = shares(10_000_000); d1 = s1 * D
print(f'[1천만원] {s1}주({s1*PRICE:,}원) · 1년 분배금 {d1:,}원 · 일반계좌 세금 {gen_tax(d1):,}원')
s = shares(20_000_000); dy = s * D
print(f'[2천만원 1년] {s}주({s*PRICE:,}원) · 분배금 {dy:,}원 · 일반계좌 세금 {gen_tax(dy):,}원 · ISA 0원(3년 채울 때)')
print()
print('[3년 — 해마다 초에 2천만원씩 더 삼, 값·분배금 그대로, 분배금은 재투자 안 함]')
tot = 0; gtot = 0
for yr in (1, 2, 3):
    sh = s * yr; dv = sh * D; tot += dv; g = gen_tax(dv); gtot += g
    print(f'  {yr}년차 {sh}주 · 분배금 {dv:,}원 · 일반계좌 세금 {g:,}원')
print(f'  3년 분배금 합 {tot:,}원 · 일반계좌 세금 합 {gtot:,}원 (15.4%)')
for name, lim in (('일반형', 2_000_000), ('서민형·농어민', 4_000_000)):
    t = isa_tax(tot, lim)
    print(f'  ISA {name} 한도 {lim:,} → 넘는 {max(0,tot-lim):,}원 × 9.9% = {t:,}원 · 차이 {gtot-t:,}원')
# 한도를 3년 동안 '매년 200만원'으로 착각했을 때
wrong = sum(isa_tax(s*yr*D, 2_000_000) for yr in (1,2,3))
print(f'  (참고) 한도를 해마다 200만원으로 잘못 알면 세금 {wrong:,}원으로 셈 — 실제 일반형 {isa_tax(tot,2_000_000):,}원')
# 일반형 200만원을 분배금만으로 채우는 원금
need = 2_000_000 / (D / PRICE)
print(f'  분배금 200만원(일반형 한도)이 1년에 나오려면 약 {need:,.0f}원어치')
print(f'  분배금 400만원(서민형 한도)이 1년에 나오려면 약 {2*need:,.0f}원어치')
print(f'  재투자 분배금은 납입한도에 안 셈(시행령 제93조의4⑫)')
print(f'  1천만원만 3년: 분배금 {s1*D*3:,}원 — 일반형 한도 안, ISA 세금 {isa_tax(s1*D*3, 2_000_000):,}원 · 일반계좌 {gen_tax(s1*D)*3:,}원')
