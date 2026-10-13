# T-1 1세대 1주택 고가주택 양도세 — 현행(~'27) vs 정부안('28 중간·'29 본격). 원문: raw/law_55·95·103·104, dec_160, J-1/raw/mofe_0803_8.txt p.37~38
# 가정: 필요경비 0(취득세·중개수수료 빼지 않음), 2년 이상 보유(기본세율 §104①1), 조정지역 다주택 아님. 지방소득세(10%)는 따로 표시.
import sys
sys.stdout.reconfigure(encoding='utf-8')
EOK = 1e8
def rate(regime, hold, live):
    if hold < 3 or live < 2: return None  # 표2 요건 밖 — 이 편에서 안 다룸(비거주 1주택 정부안 처리 확인 필요)
    if regime == '2027':
        h = min(40, 4*hold) if hold >= 3 else 0  # 표2 보유 3년 12%…10년 40%
        l = 8 if live < 3 else min(40, 4*live)
        return h, l, None
    if regime == '2028':
        h = min(20, 2*hold); l = min(60, 6*live); return h, l, 20*EOK
    if regime == '2029':
        return 0, min(80, 8*live), 10*EOK
def tax55(base):
    t = [(14e6,.06,0),(50e6,.15,84e4),(88e6,.24,624e4),(150e6,.35,1536e4),(300e6,.38,3706e4),(500e6,.40,9406e4),(1e9,.42,17406e4),(float('inf'),.45,38406e4)]
    lo = 0
    for i,(hi,r,b) in enumerate(t):
        if base <= hi: return b + (base - lo)*r
        lo = hi
def calc(sell, buy, hold, live, regime):
    gain = sell - buy
    part = (sell - 12*EOK)/sell if sell > 12*EOK else 0
    tg = gain*part                                  # 시행령 §160 ①1
    h, l, cap = rate(regime, hold, live)
    ded = gain*(h+l)/100*part                       # §160 ①2
    if cap: ded = min(ded, cap)                     # 정부안 공제 한도(물건별)
    base = max(0, tg - ded - 250e4)                 # §103 기본공제
    t = tax55(base)
    return dict(tg=tg, rate=h+l, ded=ded, base=base, tax=t, total=t*1.1)
CASES = [  # (이름, 양도가, 취득가, 보유, 거주, 정부 표 산출세액 '27·'28·'29 억원)
 ('정부 사례①', 32*EOK, 12*EOK, 10, 2, (2.36, 3.20, 4.05)),
 ('정부 사례②', 75*EOK, 25*EOK, 10, 10, (3.16, 9.23, 13.73)),
 ('A 15억·10년 거주', 15*EOK, 6*EOK, 10, 10, None),
 ('B 20억·10년 보유 2년 거주', 20*EOK, 8*EOK, 10, 2, None),
 ('C 20억·10년 거주', 20*EOK, 8*EOK, 10, 10, None),
 ('D 25억·5년 보유 5년 거주', 25*EOK, 15*EOK, 5, 5, None),
 ('E 30억·15년 보유 5년 거주', 30*EOK, 10*EOK, 15, 5, None),
]
if __name__ == '__main__':
    for name, s, b, h, l, gov in CASES:
        print(f'== {name}: 양도 {s/EOK:g}억 취득 {b/EOK:g}억 보유 {h}년 거주 {l}년')
        for i, rg in enumerate(('2027', '2028', '2029')):
            r = calc(s, b, h, l, rg)
            chk = ''
            if gov: chk = f" | 정부 {gov[i]:.2f}억 차 {r['tax']/EOK-gov[i]:+.3f}"
            print(f"  {rg}: 공제율 {r['rate']}% 공제 {r['ded']/EOK:.3f}억 과표 {r['base']/EOK:.3f}억 산출 {r['tax']/1e4:,.0f}만원 (지방세 포함 {r['total']/1e4:,.0f}만원){chk}")
