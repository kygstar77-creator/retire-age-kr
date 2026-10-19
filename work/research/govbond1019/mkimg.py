import sys, os, json; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from blogimg import F, INK, SUB, LINE, BG, ACC
GRAY=(178,186,200); YEL=(255,236,170); RED=(214,69,65)
P=10_000_000; c=4.510; a=0.28
yrs=list(range(1,11))
simple=[P*c/100*y/10000 for y in yrs]                 # 만원
comp=[P*((1+(c+a)/100)**y-1)/10000 for y in yrs]
# 01: 해마다 중도환매 이자 vs 끝까지 들고 갔을 때 그해까지 붙은 이자
W,H=900,660; im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.text((40,28),'10년물 1천만원, 몇 년 차에 빼면 이자가 얼마일까',font=F(32,True),fill=INK)
d.rectangle((40,92,62,114),fill=ACC); d.text((70,88),'만기 금리 4.79% 복리로 계산(비교용)',font=F(21,True),fill=INK)
d.rectangle((470,92,492,114),fill=GRAY); d.text((500,88),'중도환매로 받는 이자(4.51% 단리)',font=F(21,True),fill=INK)
base=540; top=160; mx=620; sc=(base-top)/mx; gw=(W-80)/10
for i,y in enumerate(yrs):
    x=40+i*gw+gw*0.12; bw=gw*0.36
    for j,(v,col) in enumerate([(comp[i],ACC),(simple[i],GRAY)]):
        if y==10 and j==1: continue
        x0=x+j*(bw+3); d.rectangle((x0,base-v*sc,x0+bw,base),fill=col)
    if y in (3,5,10):
        for j,(v,col) in enumerate([(comp[i],ACC),(simple[i],SUB)]):
            if y==10 and j==1: continue
            t=f'{v:,.0f}'; f=F(19,True); tw=d.textlength(t,font=f)
            d.text((x+bw/2+j*(bw+3)-tw/2, base-v*sc-26-(j*0)), t, font=f, fill=col)
    t=f'{y}년'; f=F(20,True); tw=d.textlength(t,font=f); d.text((40+i*gw+gw/2-tw/2,base+12),t,font=f,fill=INK)
d.line((40,base,W-40,base),fill=LINE,width=2)
d.text((40,base+50),'단위: 만원, 세전 · 파란 막대는 비교용 계산, 만기 전엔 이 돈으로 못 뺌',font=F(21,True),fill=SUB)
d.text((40,H-34),'2026년 10월 발행분 금리(재정경제부 9월 30일 발표)로 직접 계산',font=F(17),fill=(150,156,168))
im.save('pkg/img/01.png')
# 02: 쓸 날이 정해져 있으면 — 처음부터 그 만기 vs 10년물 사고 중간에 빼기
items=[('3년 뒤 쓸 돈','3년물 복리 만기 약 121만원','10년물 3년 차 환매 약 135만원',False),
       ('5년 뒤 쓸 돈','5년물 만기 약 236만원','10년물 5년 차 환매 약 226만원',True),
       ('10년 넘게 안 쓸 돈','10년물 만기 약 597만원','세금은 분리과세 15.4%',False)]
W=900; rh=118; H=110+len(items)*(rh+12)+100
im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.text((40,34),'1천만원, 쓸 날에 따라 이자 비교 (세전)',font=F(34,True),fill=INK)
y=100
for t,s1,s2,hl in items:
    d.rounded_rectangle((40,y,W-40,y+rh),radius=14,fill=YEL if hl else (244,246,250))
    d.text((64,y+14),t,font=F(28,True),fill=INK)
    d.text((64,y+56),s1,font=F(23,True),fill=ACC); d.text((64,y+86),s2,font=F(21),fill=SUB)
    y+=rh+12
d.text((40,y+12),'중도환매는 발행 1년 뒤부터 · 달마다 신청 기간과 한도 · 가산금리·분리과세 빠짐',font=F(18),fill=SUB)
d.text((40,y+44),'2026년 10월 발행분 금리 기준 · 다음 달 금리는 달라짐 · 정보 제공용',font=F(17),fill=(150,156,168))
im.save('pkg/img/02.png')
json.dump({'01.png':{'rows':[[f'{y}년',f'{s:,.1f}',f'{cc:,.1f}'] for y,s,cc in zip(yrs,simple,comp)]},
           '02.png':{'rows':[[t,s1,s2] for t,s1,s2,h in items]}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
