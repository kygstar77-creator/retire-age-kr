# pendec1118 계산 — 소득세법 제59조의3(공제율·한도)·금감원 금융상품통합비교공시 정기예금(오늘 받은 것) · firemap-write-b 11/18
import json, statistics as st, sys, os
sys.path.insert(0, os.path.abspath('../..'))
sys.stdout.reconfigure(encoding='utf-8')
import apis
if not os.path.exists('raw/finlife_deposit_1118.json'):
    d = apis.finlife('deposit')
    json.dump(d, open('raw/finlife_deposit_1118.json','w',encoding='utf-8'), ensure_ascii=False)
d = json.load(open('raw/finlife_deposit_1118.json',encoding='utf-8'))
print(type(d), (list(d[0].keys()) if isinstance(d,list) else list(d.keys()))[:20])
r12=[x['금리'] for x in d if str(x['기간'])=='12' and x['금리']]
rate=st.median(r12)/100
print('정기예금 12개월 기본금리', len(r12),'개 상품 중앙', round(rate*100,3),'% · 공시월', sorted({x['공시월'] for x in d})[-1])
# 세액공제(지방소득세 10% 포함): 소득세법 59조의3 — 15%(종합소득 4,500만원 이하·근로만 총급여 5,500만원 이하)·12%
for amt in (600, 900):
    for r in (0.15, 0.12):
        print(f'납입 {amt}만원 공제율 {r*100:.0f}% → 소득세 {amt*r:.1f}만원 · 지방세 포함 {amt*r*1.1:.2f}만원')
# 매달 1일 75만원(1~12월) vs 12월 말 900만원 한 번 — 12월 31일까지 붙는 예금 이자(단리, 같은 금리 가정)
monthly = sum(75*rate*(12-m+1)/12 for m in range(1,13))
print(f'매달 75만원: 12월 말까지 이자 {monthly:.2f}만원 · 12월 말 한 번: 0원 · 차이 {monthly:.2f}만원')
print(f'공제 148.5만원 대비 이자 차이 비율 {monthly/148.5*100:.1f}%')
