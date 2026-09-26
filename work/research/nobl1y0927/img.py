import json,sys
sys.path.insert(0,'../..')
import blogimg
from PIL import Image, ImageDraw
D=json.load(open('data.json'))
KO={'ERIE':'이리 인뎀니티','ROP':'로퍼 테크놀로지','IBM':'IBM','ADP':'ADP','MDT':'메드트로닉','GPC':'제뉴인 파츠','FDS':'팩트셋','SHW':'셔윈윌리엄스'}
# yield using last 4 divs
for o in D:
    o['y4']=round(sum(a for d,a in o['divs'][-4:])/o['p1']*100,2)
json.dump(D,open('data.json','w'),ensure_ascii=False,indent=1)
dn=sorted([o for o in D if o['ret']<0],key=lambda x:x['ret'])
rows=[[KO[o['t']]+' ('+o['t']+')','%.1f%%'%o['ret'],'%.1f%%'%o['fromhi'],'%.2f%%'%o['y4']] for o in dn]
blogimg.table('pkg/img/02.png','배당귀족 중 1년 새 주가가 내린 8곳',['종목','1년 등락','1년 최고가 대비','배당률(최근 4회)'],rows,
  note='2025-09-26 종가 → 2026-09-25 종가. 배당률 = 최근 4회 배당 합 ÷ 9월 25일 종가',src='야후 파이낸스 차트 API · NOBL 비중 상위 25종목')
# bar chart
S=sorted(D,key=lambda x:x['ret'])
W,H=900,40+len(S)*30+70
im=Image.new('RGB',(W,H),(255,255,255));d=ImageDraw.Draw(im)
d.text((30,14),'배당귀족 25종목 1년 주가 등락',font=blogimg.F(28,True),fill=blogimg.INK)
x0=450;sc=4.0
for i,o in enumerate(S):
    y=64+i*30; v=o['ret']; c=(214,69,65) if v<0 else (32,150,90)
    x1=x0+v*sc
    d.rectangle([min(x0,x1),y,max(x0,x1),y+20],fill=c)
    d.text((x0+ (8 if v<0 else -8), y+1),o['t'],font=blogimg.F(16,True),fill=blogimg.INK,anchor='la' if v<0 else 'ra')
    lab='%+.1f%%'%v
    d.text((x1-6 if v<0 else x1+6,y+1),lab,font=blogimg.F(15),fill=blogimg.SUB,anchor='ra' if v<0 else 'la')
d.line([x0,58,x0,H-50],fill=blogimg.LINE,width=2)
d.text((30,H-36),'2025-09-26 → 2026-09-25 종가 · 출처 야후 파이낸스 · 종목은 NOBL 비중 상위 25',font=blogimg.F(15),fill=blogimg.SUB)
im.save('pkg/img/01.png')
for o in S: print(o['t'],o['ret'],o['y4'])
