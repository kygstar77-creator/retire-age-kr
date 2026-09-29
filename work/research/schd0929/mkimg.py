import sys; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import os, json, urllib.request, datetime; os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
d='pkg/img/'; SRC='stockanalysis.com·야후 파이낸스 (2026-09-29 조회)'
xs=['24.12','25.03','25.06','25.09','25.12','26.03','26.06','26.09']
ys=[0.2645,0.2488,0.2602,0.2604,0.2782,0.2569,0.2525,0.2665]
B.line(d+'00.png','SCHD 분기 배당금 (주당, 달러)',xs,ys,marks=[(7,0.2665,'9월 0.2665','red'),(4,0.2782,'12월 0.2782','ink')],unit='달러',src=SRC+' · 배당락월 기준')
B.table(d+'01.png','SCHD는 어떤 ETF인가',['항목','내용'],
 [['운용사','찰스 슈왑'],['따라가는 지수','다우존스 미국 배당 100'],['담은 종목 수','102개'],['총보수','연 0.06%'],['운용자산','1,096억 달러'],['상장','2011년 10월'],['배당 주기','분기(3·6·9·12월)']],hl_col=1,src=SRC)
B.table(d+'02.png','1년 전과 지금',['','1년 전','지금','변화'],
 [['주가','27.10달러','33.01달러','+21.8%'],['최근 4번 배당 합','1.0339달러','1.0541달러','+2.0%'],['배당률','3.81%','3.19%','-0.62%p']],hl_col=3,
 note='1년 전 = 2025-09-29 종가와 그 전 4번 배당 · 지금 = 2026-09-28 종가',src=SRC)
B.table(d+'03.png','미국 배당 ETF 셋 견주기',['ETF','배당률','배당 증가(1년)','주가(1년)','총보수'],
 [['SCHD','3.19%','+2.0%','+21.8%','0.06%'],['VYM','2.35%','+4.5%','+11.6%','0.04%'],['DGRO','1.96%','+8.1%','+12.5%','0.08%']],hl_col=1,
 note='배당 증가 = 최근 4번 합계와 그 전 4번 합계 비교',src=SRC)
B.steps(d+'04.png','1억원으로 SCHD를 사면',[('2,232주','1달러 1,357원, 주가 33.01달러 기준'),('세전 연 2,353달러','최근 1년 배당이 그대로 나온다고 칠 때'),('세후 약 271만원','미국 원천징수 15%를 뗀 뒤 원화로'),('9월분 약 68만 6천원','주당 0.2665달러, 세후')],note='환율·주가·배당이 바뀌면 달라진다',src=SRC)
c=json.load(urllib.request.urlopen(urllib.request.Request('https://query1.finance.yahoo.com/v8/finance/chart/SCHD?range=1y&interval=1wk',headers={'User-Agent':'Mozilla/5.0'}),timeout=20))
r=c['chart']['result'][0]; q=r['indicators']['quote'][0]['close']
pts=[(datetime.date.fromtimestamp(t).strftime('%y.%m'),v) for t,v in zip(r['timestamp'],q) if v]
B.line(d+'05.png','SCHD 주가 1년 (주간 종가, 달러)',[p[0] for p in pts],[round(p[1],2) for p in pts],unit='달러',src='야후 파이낸스 (2026-09-29 조회)')
print('ok',len(pts),pts[0],pts[-1])
