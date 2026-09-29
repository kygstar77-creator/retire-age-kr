import sys,json,urllib.request,datetime
sys.path.insert(0,'work');import blogimg
P='work/research/usmkt0930/pkg/img/'
def ch(t,rng='10d'):
    u=f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range={rng}&interval=1d"
    r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=20))["chart"]["result"][0]
    return [(datetime.datetime.fromtimestamp(a,datetime.UTC).strftime("%m/%d"),b) for a,b in zip(r["timestamp"],r["indicators"]["quote"][0]["close"]) if b]
def pct(t):
    d=ch(t);return d[-1][1],(d[-1][1]/d[-2][1]-1)*100,d[-1][0]
rows=[]
for n,t in [('다우','^DJI'),('S&P 500','^GSPC'),('나스닥','^IXIC'),('러셀2000','^RUT')]:
    p,c,dd=pct(t);rows.append([n,f'{p:,.2f}',f'{c:+.2f}%']);print(t,dd,p,c)
blogimg.table(P+'01.png','9월 29일 미국 증시 마감',['지수','종가','전일 대비'],rows,hl_col=2,src='야후 파이낸스 종가(2026-09-29 뉴욕 기준)')
rows=[]
for n,t in [('메타','META'),('마이크론','MU'),('엔비디아','NVDA'),('테슬라','TSLA'),('애플','AAPL')]:
    p,c,dd=pct(t);rows.append([n,t,f'{p:,.2f}달러',f'{c:+.2f}%']);print(t,dd,p,c)
blogimg.table(P+'02.png','큰 종목은 이렇게 갈렸어요',['종목','티커','종가','등락'],rows,hl_col=3,src='야후 파이낸스 종가(2026-09-29 뉴욕 기준)')
d=ch('^TYX','3mo');xs=[a for a,b in d];ys=[round(b,2) for a,b in d]
blogimg.line(P+'03.png','미국 30년 국채 금리, 최근 석 달',xs,ys,marks=[(xs[0],ys[0],f'{ys[0]}%','ink'),(xs[-1],ys[-1],f'{ys[-1]}%','red')],unit='%',src='야후 파이낸스 ^TYX')
print(xs[0],ys[0],xs[-1],ys[-1],max(ys))
