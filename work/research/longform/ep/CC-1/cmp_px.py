# CC-1 종가 원문 대조 — 삼성 product-earning(상장일~, 주 단위 + 최근 12개월 일 단위) PRICE ↔ 야후 441640.KS 종가 (youtube-loop 2026-11-22)
import json, datetime
def load(p): return {x['GIJUN_YMD']:x for x in json.load(open(p,encoding='utf-8'))}
S=load('raw/kodex_earning_all_1122.json'); S.update(load('raw/kodex_earning_12m_1122.json'))
r=json.load(open('raw/441640.KS_chart_20261122.json'))['chart']['result'][0]
Y={datetime.datetime.utcfromtimestamp(a+9*3600).strftime('%Y%m%d'):c for a,c in zip(r['timestamp'],r['indicators']['quote'][0]['close']) if c}
both=[d for d in S if d in Y]; bad=[(d,S[d]['PRICE'],Y[d]) for d in both if abs(S[d]['PRICE']-Y[d])>0.5]
print('삼성 날짜',len(S),'겹침',len(both),'다른 종가',len(bad),bad[:10])
for d in ['20220927','20230620','20251119','20251120','20261120']: print(d,'삼성',S.get(d,{}).get('PRICE'),'NAV',S.get(d,{}).get('NAV'),'야후',Y.get(d))
