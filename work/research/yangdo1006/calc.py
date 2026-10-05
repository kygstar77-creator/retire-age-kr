# yangdo1006 계산 — 소득세법 제92·95·103·104·55조, 시행령 제160·159조의4 원문 식 그대로
import sys; sys.stdout.reconfigure(encoding='utf-8')
def basic(t):  # 제55조① 기본세율 (제104조①1호)
    br=[(14e6,0,.06,0),(50e6,0.84e6,.15,14e6),(88e6,6.24e6,.24,50e6),(150e6,15.36e6,.35,88e6),(300e6,37.06e6,.38,150e6),(500e6,94.06e6,.40,300e6),(1e9,174.06e6,.42,500e6),(9e99,384.06e6,.45,1e9)]
    for top,base,r,lo in br:
        if t<=top: return base+(t-lo)*r
def tax(sell,buy,rate):
    gain=sell-buy; ratio=(sell-1.2e9)/sell
    g=gain*ratio; ltd=g*rate  # 시행령 160조① 1·2호
    inc=g-ltd; base=max(inc-2.5e6,0)  # 제103조 250만원
    t=basic(base); local=t*0.1
    return dict(과세양도차익=g,장특=ltd,과표=base,양도세=t,지방=local,합계=t+local)
SELL,BUY=1.5e9,0.6e9
rows=[('거주 1년(2년 미만) → 표1 보유 15년',0.30),('거주 2년 → 표2 40%+8%',0.48),('거주 5년 → 표2 40%+20%',0.60),('거주 10년 이상 → 표2 40%+40%',0.80)]
for name,r in rows:
    d=tax(SELL,BUY,r)
    print(name, f'공제율 {r:.0%}', ' · '.join(f'{k} {v/1e4:,.1f}만원' for k,v in d.items()))
print('비과세 판정: 12억 이하 부분 비과세 비율', f'{1.2e9/SELL:.0%}', '과세 비율', f'{(SELL-1.2e9)/SELL:.0%}')
