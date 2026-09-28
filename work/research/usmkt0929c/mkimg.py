import sys,json,urllib.request,datetime
sys.path.insert(0,'work');import blogimg
P='work/research/usmkt0929c/pkg/img/'
blogimg.table(P+'01.png','9월 28일 미국 증시 마감',['지수','종가','전일 대비'],
 [['다우','51,481.51','-0.67%'],['S&P 500','7,683.69','-0.77%'],['나스닥','26,820.38','-0.92%'],['러셀2000','2,817.91','-0.69%'],['VIX(변동성)','16.07','+8.07%']],
 hl_col=2,src='야후 파이낸스 종가(2026-09-28 뉴욕 기준)')
blogimg.table(P+'02.png','업종별 등락 (업종 ETF 기준)',['업종','ETF','등락'],
 [['헬스케어','XLV','+0.33%'],['필수소비재','XLP','+0.27%'],['에너지','XLE','+0.10%'],['기술','XLK','-0.89%'],['금융','XLF','-1.19%'],['경기소비재','XLY','-1.41%'],['통신','XLC','-1.58%']],
 hl_col=2,src='야후 파이낸스, 스테이트스트리트 SPDR 업종 ETF 종가')
u="https://query1.finance.yahoo.com/v8/finance/chart/^TNX?range=3mo&interval=1d"
r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0"}),timeout=20))["chart"]["result"][0]
xs=[];ys=[]
for t,c in zip(r["timestamp"],r["indicators"]["quote"][0]["close"]):
    if c: xs.append(datetime.datetime.fromtimestamp(t).strftime("%m/%d"));ys.append(round(c,2))
blogimg.line(P+'03.png','미국 10년 국채 금리, 최근 석 달',xs,ys,marks=[(xs[0],ys[0],f'{ys[0]}%','ink'),(xs[-1],ys[-1],f'{ys[-1]}%','red')],unit='%',src='야후 파이낸스 ^TNX')
print(xs[0],ys[0],xs[-1],ys[-1])
