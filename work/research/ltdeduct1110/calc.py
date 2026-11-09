# 장기보유특별공제 현행·정부안(2028·2029) 양도세 계산 — 11/10 write ltdeduct1110
# 근거: 소득세법 제95조②·표2(nts_ltd), 제55조 세율(nts_rate), 시행령 제160조(12억 초과분), 제103조 기본공제 250만, 지방소득세 10%
# 정부안: 재정경제부 2026 세제개편안 상세본 p.57·59·68, 문답 p.37, 정부 법안 2221042 제95조·제103조 (raw/) — 문답 p.37 사례 ①② 여섯 값 그대로 나옴(아래 check)
import sys; sys.stdout.reconfigure(encoding='utf-8')
BR=[(1400e4,.06,0),(5000e4,.15,84e4),(8800e4,.24,624e4),(1.5e8,.35,1536e4),(3e8,.38,3706e4),(5e8,.40,9406e4),(10e8,.42,17406e4),(9e99,.45,38406e4)]
def tax(base):
    lo=0
    for hi,r,acc in BR:
        if base<=hi: return acc+(base-lo)*r
        lo=hi
def ltd_rate(rule,hold,live):
    if live<2:  # 1세대1주택 표2 못 받음(시행령 제159조의4 2년 거주) → 표1(주택)
        if rule in ('2026','현행'): return (min(2*hold,30) if hold>=3 else 0), None   # 현행 표1 연2% 최대30
        if rule=='2028': return (min(hold,15) if hold>=3 else 0), 20e8            # 법안 표1 2028 보유 연1%(거주 2년 미만 0)
        return 0, 10e8                                                             # 법안 표1 2029 거주 2년 미만 0
    if rule in ('2026','현행'):   # 표2: 보유 3년+ 연4% 최대40, 거주 2~3년 8%(보유3년+), 3년+ 연4% 최대40
        h=min(hold*4,40) if hold>=3 else 0
        l=8 if 2<=live<3 else (min(live*4,40) if live>=3 else 0)
        return h+l, None
    if rule=='2028':
        h=min(hold*2,20) if hold>=3 else 0
        l=min(live*6,60) if live>=2 else 0
        return h+l, 20e8
    if rule=='2029':
        l=min(live*8,80) if live>=2 else 0
        return l, 10e8
def case(buy,sell,hold,live,rule,year=None):
    gain=sell-buy
    taxable_gain=gain*(sell-12e8)/sell if sell>12e8 else 0
    r,cap=ltd_rate(rule,hold,live)
    ded=taxable_gain*r/100
    if cap: ded=min(ded,cap)
    year=year or {'현행':2026,'2026':2026,'2028':2028,'2029':2029}[rule]
    basic=2500e4 if (year>=2027 and live>=10 and sell<=30e8) else 250e4   # 법안 제103조① 단서, 2027.1.1 양도분부터(상세본 p.68)
    base=max(taxable_gain-ded-basic,0)
    t=tax(base); return dict(rate=r,taxable_gain=taxable_gain,ded=ded,base=base,tax=t,total=round(t*1.1))
if __name__=='__main__':
    print('== 정부 문답 p.37 사례 확인(기본공제 250만, 산출세액 억)')
    for r in ('현행','2028','2029'):
        a=case(12e8,32e8,10,2,r,2026); b=case(25e8,75e8,10,10,r,2026)
        print(f' {r}: ① {a["rate"]}% 공제{a["ded"]/1e8:.2f}억 세액{a["tax"]/1e8:.2f}억 | ② {b["rate"]}% 공제{b["ded"]/1e8:.2f}억 세액{b["tax"]/1e8:.2f}억')
    for buy,sell in [(8e8,20e8),(10e8,30e8)]:
        print(f'== 취득 {buy/1e8:.0f}억 → 양도 {sell/1e8:.0f}억, 10년 보유, 지방소득세 포함')
        for live in (10,2,1.5):
            for y,r in ((2026,'현행'),(2027,'현행'),(2028,'2028'),(2029,'2029')):
                c=case(buy,sell,10,live,r,y)
                print(f' 거주{live:>4}년 {y}양도 공제율{c["rate"]:>3}% 공제{c["ded"]/1e4:,.0f}만 과표{c["base"]/1e4:,.0f}만 세금{c["total"]/1e4:,.0f}만')
