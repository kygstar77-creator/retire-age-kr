import json,urllib.request,datetime,re
H={'User-Agent':'Mozilla/5.0','Accept':'application/json'}
out=[]
d=datetime.date(2026,10,1)
while d<=datetime.date(2026,10,31):
    if d.weekday()<5:
        u=f'https://api.nasdaq.com/api/calendar/earnings?date={d}'
        try:
            j=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=20))
            rows=(j.get('data') or {}).get('rows') or []
            for r in rows:
                mc=re.sub(r'[^0-9]','',r.get('marketCap') or '') or '0'
                out.append(dict(date=str(d),sym=r['symbol'],name=r['name'],mc=int(mc),time=r.get('time'),eps=r.get('epsForecast'),fq=r.get('fiscalQuarterEnding'),last=r.get('lastYearEPS'),lastd=r.get('lastYearRptDt')))
            print(d,len(rows))
        except Exception as e: print(d,'ERR',e)
    d+=datetime.timedelta(1)
json.dump(out,open('work/research/q3season0929/cal.json','w',encoding='utf-8'),ensure_ascii=False)
top=sorted(out,key=lambda x:-x['mc'])[:40]
for r in top: print(r['date'],r['sym'],r['name'][:30],round(r['mc']/1e9),r['time'],r['eps'],r['fq'],r['last'])
