import sys, os, json; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from blogimg import F, INK, SUB, LINE, BG, ACC
GRAY=(178,186,200)
# 01: 뉴스에 나오는 '평균 월급' 세 가지와 한가운데(중위)
rows=[('한가운데(중위)','2024년 12월 · 국가데이터처',288,True),('평균','2024년 12월 · 국가데이터처',375,False),
      ('평균','2026년 4월 · 고용노동부',403.1,False),('평균','2026년 7월 · 고용노동부',431.6,False)]
W,H=900,600; im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.text((40,30),'뉴스 속 평균 월급과 줄 한가운데 월급 (세전)',font=F(32,True),fill=INK)
y=110; mx=460.0; x0=330
for n,s,v,hl in rows:
    d.text((40,y+4),n,font=F(25,True),fill=ACC if hl else INK); d.text((40,y+40),s,font=F(16),fill=SUB)
    bw=(W-x0-150)*v/mx; d.rectangle((x0,y+6,x0+bw,y+56),fill=ACC if hl else GRAY)
    t=(f'{v:g}만원' if v==int(v) else f'{int(v)}만 {int(round((v-int(v))*10))}천원'); d.text((x0+bw+12,y+14),t,font=F(26,True),fill=ACC if hl else INK)
    y+=105
d.text((40,H-62),'평균은 많이 받는 사람 쪽으로 끌려 올라간 값 · 노동부는 사업체 조사, 데이터처는 일자리 기준',font=F(18),fill=SUB)
d.text((40,H-34),'출처: 국가데이터처 2024년 임금근로일자리 소득(2026.2.23) · 고용노동부 사업체노동력조사(2026.9.30)',font=F(16),fill=(150,156,168))
im.save('pkg/img/01.png')
# 02: 나이대별 평균과 한가운데 차이
ages=[('30~34세',368,333),('40~44세',464,389),('50~54세',464,324),('60~64세',319,230)]
W,H=900,640; im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.text((40,30),'나이대별 평균과 한가운데 월급 차이 (세전)',font=F(32,True),fill=INK)
d.rectangle((40,94,62,116),fill=GRAY); d.text((70,90),'평균',font=F(22,True),fill=INK)
d.rectangle((170,94,192,116),fill=ACC); d.text((200,90),'한가운데(중위)',font=F(22,True),fill=INK)
base=520; top=170; scale=(base-top)/500.0; gw=(W-80)/4
for i,(n,a,m) in enumerate(ages):
    x=40+i*gw+gw*0.14; bw=gw*0.33
    for j,(v,c) in enumerate([(a,GRAY),(m,ACC)]):
        xx=x+j*(bw+8); yy=base-v*scale; d.rectangle((xx,yy,xx+bw,base),fill=c)
        t=f'{v}'; f=F(22,True); tw=d.textlength(t,font=f); d.text((xx+bw/2-tw/2,yy-30),t,font=f,fill=SUB if j==0 else ACC)
    f=F(23,True); tw=d.textlength(n,font=f); d.text((40+i*gw+gw/2-tw/2,base+12),n,font=f,fill=INK)
    g=f'차이 {a-m}만원'; f=F(21,True); tw=d.textlength(g,font=f); d.text((40+i*gw+gw/2-tw/2,base+44),g,font=f,fill=(214,69,65) if a-m>=100 else SUB)
d.line((40,base,W-40,base),fill=LINE,width=2)
d.text((40,H-34),'단위 만원 · 2024년 12월 세전 월 보수 · 국가데이터처 임금근로일자리 소득(2026.2.23)',font=F(16),fill=(150,156,168))
im.save('pkg/img/02.png')
json.dump({'01.png':{'rows':[[n,s,(f'{v:g}만원' if v==int(v) else f'{int(v)}만 {int(round((v-int(v))*10))}천원')] for n,s,v,h in rows]},'02.png':{'rows':[[n,f'평균 {a}',f'중위 {m}'] for n,a,m in ages]}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
