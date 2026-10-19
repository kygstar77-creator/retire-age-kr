import sys, os, json; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from blogimg import F, INK, SUB, LINE, BG, ACC
GRAY=(178,186,200); YEL=(255,236,170)
# 01: 은행별 1년·3년 막대
rows=[('KB국민',3.6,2.6),('신한',3.5,2.6),('하나',3.6,2.7),('우리',3.6,2.7),('농협',3.65,2.7)]
W,H=900,620; im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.text((40,32),'5대 은행 정기예금 최고금리, 1년이 3년보다 높다',font=F(34,True),fill=INK)
d.rectangle((40,96,62,118),fill=ACC); d.text((70,92),'1년',font=F(24,True),fill=INK)
d.rectangle((140,96,162,118),fill=GRAY); d.text((170,92),'3년',font=F(24,True),fill=INK)
base=520; top=150; scale=(base-top)/4.0
gw=(W-80)/5
for i,(n,a,b) in enumerate(rows):
    x=40+i*gw+gw*0.12; bw=gw*0.34
    for j,(v,c) in enumerate([(a,ACC),(b,GRAY)]):
        x0=x+j*(bw+8); y0=base-v*scale
        d.rectangle((x0,y0,x0+bw,base),fill=c)
        t=f'{v:g}%'; f=F(24,True); tw=d.textlength(t,font=f)
        d.text((x0+bw/2-tw/2,y0-34),t,font=f,fill=ACC if j==0 else SUB)
    f=F(26,True); tw=d.textlength(n,font=f); d.text((40+i*gw+gw/2-tw/2,base+14),n,font=f,fill=INK)
d.line((40,base,W-40,base),fill=LINE,width=2)
d.text((40,H-46),'최고금리(우대 포함) · 2026년 9월 공시 · 10월 19일 조회 · 금융감독원 금융상품 통합비교공시',font=F(18),fill=SUB)
im.save('pkg/img/01.png')
# 02: 1억 3년 세후 이자 카드(강조 줄)
items=[('3년짜리 2.7%에 한 번','우리은행 WON플러스예금','약 685만원',False),
       ('1년짜리 3.6%로 세 번','금리가 그대로라면','약 942만원',True),
       ('1년짜리, 2년째부터 3.0%','','약 834만원',False),
       ('1년짜리, 2년째부터 2.5%','','약 745만원',False),
       ('1년짜리, 2년째부터 2.16%','여기서 3년짜리와 같아짐','약 685만원',False)]
W=900; rh=96; H=110+len(items)*(rh+12)+90
im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.text((40,34),'1억을 3년 맡기면 세후 이자',font=F(34,True),fill=INK)
y=100
for t,s,v,hl in items:
    d.rounded_rectangle((40,y,W-40,y+rh),radius=14,fill=YEL if hl else (244,246,250))
    d.text((64,y+(14 if s else 30)),t,font=F(28,True),fill=INK)
    if s: d.text((64,y+56),s,font=F(20),fill=SUB)
    f=F(34,True); tw=d.textlength(v,font=f); d.text((W-64-tw,y+26),v,font=f,fill=(214,69,65) if hl else ACC)
    y+=rh+12
d.text((40,y+12),'이자소득세 15.4% 뗀 금액 · 1년짜리는 만기마다 원금+이자를 다시 넣는다고 계산',font=F(19),fill=SUB)
d.text((40,y+42),'금융감독원 공시 금리(9월)로 직접 계산',font=F(17),fill=(150,156,168))
im.save('pkg/img/02.png')
json.dump({'01.png':{'rows':[[n,f'{a:g}%',f'{b:g}%'] for n,a,b in rows]},'02.png':{'rows':[[t,v] for t,s,v,h in items]}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
