import json,urllib.request,sys
H={'User-Agent':'Mozilla/5.0','Accept':'application/json'}
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=20))
out={}
import time
for t in sys.argv[1:]:
    time.sleep(1.5)
    try:
        d=get(f'https://api.nasdaq.com/api/quote/{t}/dividends?assetclass=stocks')
        rows=d['data']['dividends']['rows'][:6]
        s=get(f'https://api.nasdaq.com/api/quote/{t}/info?assetclass=stocks')['data']
        out[t]={'rows':[{k:r[k] for k in ('exOrEffDate','amount','declarationDate','recordDate','paymentDate')} for r in rows],
                'yield':d['data'].get('yield'),'annual':d['data'].get('annualizedDividend'),'name':s.get('companyName'),'last':s['primaryData'].get('lastSalePrice')}
        print(t,out[t]['name'],out[t]['last'],out[t]['yield'],out[t]['annual']);[print('  ',r) for r in out[t]['rows'][:3]]
    except Exception as e: print(t,'ERR',e)
json.dump(out,open(sys.argv[0].replace('nasdaq.py','nasdaq_%s.json'%sys.argv[1]),'w',encoding='utf-8'),ensure_ascii=False,indent=1)
