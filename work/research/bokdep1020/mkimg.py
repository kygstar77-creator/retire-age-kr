import sys, os, json; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from blogimg import F, INK, SUB, LINE, BG, ACC, WARN
GRAY=(150,158,172)
e=json.load(open('raw/ecos_1020.json',encoding='utf-8'))
months=['202512','202601','202602','202603','202604','202605','202606','202607','202608']
base=dict((a,float(b)) for a,b,c in e['base']); dep=dict((a,float(b)) for a,b,c in e['dep12'])
# 01: 기준금리(계단) vs 은행 1~2년 정기예금 신규 금리
W,H=900,640; im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.text((40,30),'예금 금리는 기준금리보다 먼저 올랐다',font=F(36,True),fill=INK)
d.text((40,82),'은행이 그 달 새로 받은 1~2년 정기예금 평균 · 2025년 12월~2026년 8월',font=F(21),fill=SUB)
x0,x1,y0,y1=90,820,150,540; lo,hi=2.3,3.7
X=lambda i:x0+(x1-x0)*i/(len(months)-1); Y=lambda v:y1-(y1-y0)*(v-lo)/(hi-lo)
for v in (2.5,3.0,3.5):
    d.line((x0,Y(v),x1,Y(v)),fill=LINE,width=1); d.text((40,Y(v)-12),f'{v:.1f}%',font=F(18),fill=SUB)
pts=[]
for i,m in enumerate(months):
    pts+= [(X(i),Y(base[m]))] if i==0 else [(X(i),Y(base[months[i-1]])),(X(i),Y(base[m]))]
d.line(pts,fill=GRAY,width=5)
dp=[(X(i),Y(dep[m])) for i,m in enumerate(months)]; d.line(dp,fill=ACC,width=6)
for (x,y),m in zip(dp,months):
    d.ellipse((x-7,y-7,x+7,y+7),fill=ACC)
for i,m in enumerate(months):
    lab=f"{int(m[4:])}월"; d.text((X(i)-d.textlength(lab,font=F(18))/2,y1+12),lab,font=F(18),fill=SUB)
for m,dy in (('202601',-44),('202606',-44),('202607',-44),('202608',22)):
    i=months.index(m); t=f'{dep[m]:.2f}%'; d.text((X(i)-d.textlength(t,font=F(24,True))/2,Y(dep[m])+dy),t,font=F(24,True),fill=ACC)
d.text((X(6)+8,Y(2.5)+8),'기준금리 2.5%',font=F(20,True),fill=GRAY)
d.text((X(8)-60,Y(3.0)-30),'3.00%',font=F(20,True),fill=GRAY); d.text((X(7)+6,Y(2.75)-28),'2.75%',font=F(20,True),fill=GRAY)
d.rectangle((x0,y1+48,x0+28,y1+56),fill=ACC); d.text((x0+38,y1+40),'예금 금리',font=F(20,True),fill=INK)
d.rectangle((x0+180,y1+48,x0+208,y1+56),fill=GRAY); d.text((x0+218,y1+40),'기준금리(7/16·8/27 인상, 8월은 27일부터 3%)',font=F(20,True),fill=INK)
d.text((40,H-34),'자료: 한국은행 경제통계시스템(2026-10-20 조회) · 8월분이 가장 최근',font=F(18),fill=SUB)
im.save('pkg/img/01.png')
# 02: 국고채 3년 일별
k=[(a,float(b)) for a,b,c in json.load(open('raw/ecos_ktb3_daily.json',encoding='utf-8'))]
W,H=900,600; im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.text((40,30),'국고채 3년물도 올리기 전에 올랐다',font=F(36,True),fill=INK)
d.text((40,82),'국고채 3년 금리(매일) · 2025년 12월~2026년 10월 19일',font=F(21),fill=SUB)
x0,x1,y0,y1=90,840,140,500; lo,hi=2.8,4.2
n=len(k); X=lambda i:x0+(x1-x0)*i/(n-1); Y=lambda v:y1-(y1-y0)*(v-lo)/(hi-lo)
for v in (3.0,3.5,4.0):
    d.line((x0,Y(v),x1,Y(v)),fill=LINE,width=1); d.text((40,Y(v)-12),f'{v:.1f}%',font=F(18),fill=SUB)
idx={a:i for i,(a,v) in enumerate(k)}
for day,lab in (('20260716','7/16 인상'),('20260827','8/27 인상')):
    i=idx[day]; d.line((X(i),y0,X(i),y1),fill=GRAY,width=2); d.text((X(i)-d.textlength(lab,font=F(19,True))-6,y0),lab,font=F(19,True),fill=GRAY)
d.line([(X(i),Y(v)) for i,(a,v) in enumerate(k)],fill=ACC,width=4)
for day,t,dy in (('20251230','12/30 2.95%',14),('20260630','6/30 3.70%',14),('20261019','10/19 3.88%',22)):
    i=idx[day]; v=dict(k)[day]; d.ellipse((X(i)-7,Y(v)-7,X(i)+7,Y(v)+7),fill=INK)
    tx=min(X(i)-20,x1-140); d.text((tx,Y(v)+dy),t,font=F(24,True),fill=INK)
for mlab,day in (('2026년 1월','20260102'),('4월','20260401'),('7월','20260701'),('10월','20261001')):
    i=min(i for a,i in idx.items() if a>=day); d.text((X(i)-d.textlength(mlab,font=F(18))/2,y1+12),mlab,font=F(18),fill=SUB)
d.rounded_rectangle((110,150,420,206),radius=10,fill=(255,243,224)); d.text((126,160),'첫 인상 전까지 +0.75%p',font=F(26,True),fill=WARN)
d.text((40,H-34),'자료: 한국은행 경제통계시스템 시장금리(일별), 2026-10-20 조회',font=F(18),fill=SUB)
im.save('pkg/img/02.png')
json.dump({'01.png':{'rows':[[f'{int(m[4:])}월',base[m],dep[m]] for m in months]},'02.png':{'rows':[['2025-12-30',2.952],['2026-06-30',3.703],['2026-10-19',3.877]]}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
