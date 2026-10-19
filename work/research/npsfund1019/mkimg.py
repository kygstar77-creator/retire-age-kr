import sys, os, json; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from blogimg import F, INK, SUB, LINE, BG, ACC
RED=(214,69,65); GRAY=(178,186,200); YEL=(255,236,170)
rows=json.load(open('returns.json'))
# 01: 연도별 수익률 막대 (2026은 7월 말까지)
W,H=1000,640; im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.text((40,30),'국민연금 기금 연도별 수익률, 마이너스는 세 번',font=F(34,True),fill=INK)
L,R=70,W-30; top=120; bot=510; sc=(bot-top)/30.0; zero=top+20*sc
for v in (-10,-5,0,5,10,15,20):
    y=zero-v*sc; d.line((L,y,R,y),fill=(232,235,240) if v else LINE,width=1 if v else 2)
    d.text((22,y-12),f'{v}%',font=F(18),fill=SUB)
n=len(rows); gw=(R-L)/n
for i,(y,amt,r) in enumerate(rows):
    x0=L+i*gw+2; x1=x0+gw-4
    c=RED if r<0 else (ACC if y==2026 else GRAY)
    if y==2026: d.rectangle((x0,zero-r*sc,x1,zero),fill=(214,226,252),outline=ACC,width=3)
    elif r>=0: d.rectangle((x0,zero-r*sc,x1,zero),fill=c)
    else: d.rectangle((x0,zero,x1,zero-r*sc),fill=c)
    if r<0:
        t=f'{y}\n{r:g}%'; f=F(19,True)
        d.multiline_text(((x0+gw+4, zero+40) if y==2022 else (x0+gw/2-24, zero-r*sc+8)),t,font=f,fill=RED,spacing=2,align='center')
    if y in (1988,2000,2010,2020):
        d.text((x0-6,bot+12),str(y),font=F(18),fill=SUB)
    if y==2026:
        t='2026년(파란 테두리)은 1~7월만, 14.84%'; f=F(20,True); d.text((R-d.textlength(t,font=f),84),t,font=f,fill=ACC)
d.text((40,H-58),'기금 전체 수익률 · 2026년은 1~7월 잠정 · 2026년 10월 19일 조회',font=F(18),fill=SUB)
d.text((40,H-32),'자료: 국민연금 기금운용본부 운용성과',font=F(17),fill=(150,156,168))
im.save('pkg/img/01.png')
# 02: 손실 난 해 → 다음 해
items=[('2008년','-0.18%','10.39%'),('2018년','-0.92%','11.31%'),('2022년','-8.22%','13.59%')]
W=900; rh=104; H=170+len(items)*(rh+14)+80
im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.text((40,34),'기금이 손실 난 해, 그다음 해 수익률',font=F(34,True),fill=INK)
d.text((300,104),'손실 난 해',font=F(22,True),fill=SUB); d.text((610,104),'다음 해',font=F(22,True),fill=SUB)
y=146
for yr,a,b in items:
    d.rounded_rectangle((40,y,W-40,y+rh),radius=14,fill=(244,246,250))
    d.text((70,y+32),yr,font=F(32,True),fill=INK)
    d.text((290,y+28),a,font=F(38,True),fill=RED)
    d.text((480,y+30),'→',font=F(34,True),fill=SUB)
    d.text((600,y+28),b,font=F(38,True),fill=ACC)
    y+=rh+14
d.text((40,y+10),'1988~2025년 38년 중 마이너스는 이 세 해뿐 · 기금 전체 수익률',font=F(19),fill=SUB)
d.text((40,y+40),'자료: 국민연금 기금운용본부 운용성과(2026년 10월 19일 조회)',font=F(17),fill=(150,156,168))
im.save('pkg/img/02.png')
json.dump({'01.png':{'rows':[[y,f'{r:g}%'] for y,a,r in rows]},'02.png':{'rows':[list(t) for t in items]}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
