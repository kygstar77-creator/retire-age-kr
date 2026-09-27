import json,urllib.request,datetime,sys
sys.path.insert(0,'../..')
import blogimg as B
H={'User-Agent':'Mozilla/5.0'}
d=json.load(urllib.request.urlopen(urllib.request.Request("https://query1.finance.yahoo.com/v8/finance/chart/PLTR?range=1y&interval=1d",headers=H)))['chart']['result'][0]
rows=[(str(datetime.datetime.utcfromtimestamp(a).date()),x) for a,x in zip(d['timestamp'],d['indicators']['quote'][0]['close']) if x]
xs=[r[0][5:].replace('-','/') for r in rows]; ys=[round(r[1],2) for r in rows]
i_hi=max(range(len(ys)),key=lambda i:ys[i]); i_lo=min(range(len(ys)),key=lambda i:ys[i])
B.line('pkg/img/01.png','팔란티어(PLTR) 1년 종가',xs,ys,marks=[(xs[i_hi],ys[i_hi],f'최고 {ys[i_hi]}','ink'),(xs[i_lo],ys[i_lo],f'최저 {ys[i_lo]}','red'),(xs[-1],ys[-1],f'9/25 {ys[-1]}','ink')],unit='달러',src='야후 파이낸스 일별 종가')
B.table('pkg/img/02.png','팔란티어 2분기 매출 (2026년 4~6월)',['구분','매출','1년 전보다'],
 [['미국 정부','8억 900만 달러','+90%'],['미국 기업','7억 6,400만 달러','+149%'],['미국 밖','3억 6,200만 달러','-'],['합계','19억 3,500만 달러','+93%']],
 src='팔란티어 2분기 실적 발표(2026-08-03, SEC 8-K)',note='미국 밖 = 합계에서 미국 매출 15억 7,300만 달러를 뺀 값')
peers=[('팔란티어','PLTR'),('세일즈포스','CRM'),('마이크로소프트','MSFT'),('서비스나우','NOW'),('어도비','ADBE'),('오라클','ORCL')]
out=[]
for n,t in peers:
    d=json.load(urllib.request.urlopen(urllib.request.Request(f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=1y&interval=1d",headers=H)))['chart']['result'][0]
    r=[(str(datetime.datetime.utcfromtimestamp(a).date()),x) for a,x in zip(d['timestamp'],d['indicators']['quote'][0]['close']) if x]
    last=r[-1];q=[x for x in r if x[0]<='2026-06-30'][-1];ye=[x for x in r if x[0]<='2025-12-31'][-1]
    out.append([f'{n}({t})',f'{(last[1]/q[1]-1)*100:+.1f}%',f'{(last[1]/ye[1]-1)*100:+.1f}%'])
print(out)
B.table('pkg/img/03.png','미국 소프트웨어 대형주, 3분기와 올해 등락',['종목','3분기','올해'],out,hl_col=1,src='야후 파이낸스 종가 · 3분기=6/30→9/25, 올해=2025/12/31→9/25')
