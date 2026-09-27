import sys, json, time, urllib.request, datetime
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.stdout.reconfigure(encoding='utf-8')
import apis
UA={'User-Agent':'Mozilla/5.0'}
out={'fetched':time.strftime('%Y-%m-%d %H:%M'), 'yahoo':{}}
for s in ['^TNX','KRW=X','CL=F','GC=F']:
    u='https://query1.finance.yahoo.com/v8/finance/chart/'+urllib.parse.quote(s) if False else 'https://query1.finance.yahoo.com/v8/finance/chart/'+s.replace('^','%5E').replace('=','%3D')+'?range=1mo&interval=1d'
    d=json.loads(urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=25).read())
    r=d['chart']['result'][0]; m=r['meta']; tz=m.get('exchangeTimezoneName')
    rows=[]
    for t,c in zip(r['timestamp'], r['indicators']['quote'][0]['close']):
        dt=datetime.datetime.utcfromtimestamp(t+m.get('gmtoffset',0)).strftime('%Y-%m-%d %H:%M')
        rows.append((dt,c))
    out['yahoo'][s]={'url':u,'tz':tz,'currency':m.get('currency'),'rows':rows,'regularMarketPrice':m.get('regularMarketPrice')}
    print(s,tz,m.get('currency'))
    for x in rows[-10:]: print('  ',x)
for s in ['FEDFUNDS','DFEDTARU','DFEDTARL','DGS10']:
    try: out[s]=apis.fred(s,8); print(s,out[s])
    except Exception as e: print(s,'ERR',e)
try:
    out['ecos']=apis.ecos(n=6); print('ecos',out['ecos'])
except Exception as e: print('ecos ERR',e)
json.dump(out,open('data.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
