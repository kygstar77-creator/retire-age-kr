# 결산배당 회사마다 배당락일(기준일 직전 거래일) 전날·당일 종가 — 야후 일별 종가(대조용 2차). 코스피 지수(^KS11)도 같이.
import sys,json,urllib.request,time,os,datetime
sys.stdout.reconfigure(encoding='utf-8')
rows=[r for r in json.load(open('raw/dart_divrows.json',encoding='utf-8')) if r['kind']=='결산배당' and r['rec'] and r['stock_code']]
os.makedirs('raw/yahoo',exist_ok=True)
def get(t):
    fn=f'raw/yahoo/{t}.json'
    if os.path.exists(fn): return json.load(open(fn,encoding='utf-8'))
    u=f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?period1=1764547200&period2=1775001600&interval=1d'
    try: d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=20))['chart']['result'][0]
    except Exception as e: return None
    s={datetime.datetime.fromtimestamp(ts,datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d'):c for ts,c in zip(d['timestamp'],d['indicators']['quote'][0]['close']) if c}
    json.dump(s,open(fn,'w')); time.sleep(0.2); return s
ks=get('^KS11')
out=[]
for r in rows:
    s=get(r['stock_code']+'.KS')
    if not s: print('no',r['corp_name']); continue
    # 결제일 S = 기준일 이하 마지막 거래일(12/31 휴장·주말이면 앞당김), 배당락일 = S 직전 거래일 (T+2, 2025.12.29 사례와 맞춤)
    days=sorted(d for d in s if d<=r['rec'])
    if len(days)<3: continue
    ex,prev=days[-2],days[-3]
    out.append(dict(name=r['corp_name'],code=r['stock_code'],rec=r['rec'],dec=r['dec'],dps=r['dps'],yld=r['yld'],ex=ex,prev=prev,p0=s[prev],p1=s[ex],k0=ks.get(prev),k1=ks.get(ex)))
json.dump(out,open('raw/exday.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
print(len(out))
