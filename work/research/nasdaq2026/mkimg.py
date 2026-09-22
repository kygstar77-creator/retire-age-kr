import json,datetime as D,os,sys
from blogimg import table, F, INK, SUB, LINE, BG, ACC, wrap
from PIL import Image, ImageDraw
O=r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\research\nasdaq2026\img'
SRC='자료: Nasdaq 지수 일별 시세(종가), FRED NASDAQCOM·NASDAQ100 교차확인'
table(os.path.join(O,'b2.png'),'나스닥 지수, 작년 말과 9월 21일 종가',
  ['지수','2025.12.31','2026.9.21','오른 폭','상승률'],
  [['나스닥 종합','23,241.99','27,122.09','+3,880.10','+16.69%'],
   ['나스닥100','25,249.85','30,482.35','+5,232.50','+20.72%']],
  [0.22,0.2,0.2,0.2,0.18], hl_col=4, note='9월 21일은 미국 날짜, 한국 시간 9월 22일 새벽 5시 마감', src=SRC)
table(os.path.join(O,'b4.png'),'나스닥 종합지수 2026년 월말 종가',
  ['월','월말 종가','전월 말 대비'],
  [['2025년 12월','23,241.99','-'],['1월','23,461.82','+0.95%'],['2월','22,668.21','-3.38%'],['3월','21,590.63','-4.75%'],
   ['4월','24,892.31','+15.29%'],['5월','26,972.62','+8.36%'],['6월','26,213.72','-2.81%'],['7월','25,373.85','-3.20%'],
   ['8월','26,370.89','+3.93%'],['9월(21일까지)','27,122.09','+2.85%']],
  [0.36,0.34,0.30], hl_col=2, note='각 달 마지막 거래일 종가 기준', src=SRC)
table(os.path.join(O,'b5.png'),'최근 52주 최고·최저 종가',
  ['지수','최고 종가','최저 종가','9월 21일'],
  [['나스닥 종합','27,122.09\n(9월 21일)','20,794.64\n(3월 30일)','27,122.09'],
   ['나스닥100','30,660.60\n(6월 2일)','22,953.38\n(3월 30일)','30,482.35']],
  [0.22,0.27,0.27,0.24], note='기간: 2025년 9월 22일~2026년 9월 21일(251거래일), 종가 기준', src=SRC)
table(os.path.join(O,'b6.png'),'나스닥 거래 시간, 한국 시간 기준',
  ['구분','미국 동부시간','지금(서머타임)','11월 2일부터'],
  [['정규장','9:30~16:00','22:30~다음날 5:00','23:30~다음날 6:00'],
   ['프리마켓','4:00~9:30','17:00~22:30','18:00~23:30'],
   ['애프터마켓','16:00~20:00','5:00~9:00','6:00~10:00']],
  [0.2,0.24,0.28,0.28], hl_col=2, note='미국 서머타임 11월 1일(일) 종료. 프리·애프터마켓은 증권사마다 다를 수 있음',
  src='자료: NYSE 거래시간, nasdaq.com, Nasdaq Trader 캘린더, 15 U.S.C. §260a')
# line chart
r=json.load(open(r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\research\nasdaq2026\raw\COMP.json'))['data']['tradesTable']['rows']
pts=sorted((D.datetime.strptime(x['date'],'%m/%d/%Y').date(),float(x['close'].replace(',',''))) for x in r)
pts=[p for p in pts if p[0]>=D.date(2025,12,31)]
W,H=900,560; pad=36; im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.text((pad,pad),'나스닥 종합지수 일별 종가',font=F(30,True),fill=INK)
d.text((pad,pad+44),'2025년 12월 31일 ~ 2026년 9월 21일',font=F(18),fill=SUB)
L,R,T,B=pad+70,W-pad-20,150,H-90
lo,hi=20000,28000
X=lambda dt:L+(dt-pts[0][0]).days/(pts[-1][0]-pts[0][0]).days*(R-L)
Y=lambda v:B-(v-lo)/(hi-lo)*(B-T)
for v in range(lo,hi+1,2000):
    d.line((L,Y(v),R,Y(v)),fill=LINE); s=f'{v:,}'; d.text((L-10-d.textlength(s,font=F(16)),Y(v)-10),s,font=F(16),fill=SUB)
for m in range(1,10):
    x=X(D.date(2026,m,1)); d.text((x-8,B+10),f'{m}월',font=F(16),fill=SUB)
yv=pts[0][1]
d.line([(X(a),Y(b)) for a,b in pts],fill=ACC,width=3)
def lab(dt,v,txt,dx,dy):
    x,y=X(dt),Y(v); d.ellipse((x-6,y-6,x+6,y+6),fill=ACC)
    f=F(18,True); d.text((x+dx,y+dy),txt,font=f,fill=INK)
x0,y0=X(pts[0][0]),Y(pts[0][1]); d.line((x0,y0,x0,y0-70),fill=SUB,width=1); lab(pts[0][0],pts[0][1],'12월 31일 23,241.99',6,-98)
lab(D.date(2026,3,30),20794.64,'3월 30일 20,794.64',12,6)
lab(pts[-1][0],pts[-1][1],'9월 21일 27,122.09',-190,-38)
d.text((pad,H-40),SRC,font=F(16),fill=(150,156,168))
im.save(os.path.join(O,'b3.png'))
print('ok')
