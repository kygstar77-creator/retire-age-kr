import sys, os, json; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from blogimg import F, INK, SUB, LINE, BG, ACC, WARN
GRAY=(178,186,200); GREEN=(22,140,90)
# 01: 1억 넣었다면 1년 뒤 — 1억 대비 늘고 준 돈(0 기준 막대)
rows=[('KIWOOM 국고채10년','국고채 10년물',-595,'약 9,405만원','-595만원'),
      ('TIGER 국채3년','국고채 3년물',-20,'약 9,980만원','-20만원'),
      ('TIGER 단기통안채','만기 9개월 이하 통안채',234,'약 1억 234만원','+234만원')]
W,H=900,620; im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.text((40,32),'1억 넣었다면 1년 뒤',font=F(38,True),fill=INK)
d.text((40,84),'2025년 10월 17일 → 2026년 10월 19일 종가 · 분배금 포함 · 세전',font=F(21),fill=SUB)
zero=600; sc=330/600
y=150
for n,s2,v,t,dv in rows:
    d.text((40,y),n,font=F(28,True),fill=INK); d.text((40+d.textlength(n,font=F(28,True))+12,y+6),s2,font=F(20),fill=SUB)
    c=WARN if v<-100 else (GRAY if v<0 else GREEN)
    x1=zero+v*sc
    d.rectangle((min(zero,x1),y+46,max(zero,x1)+ (2 if v==0 else 0),y+96),fill=c)
    f=F(28,True)
    if v<0:
        tw=d.textlength(dv,font=f); d.text((min(zero,x1)-tw-12,y+54),dv,font=f,fill=c if v<-100 else SUB)
    else:
        d.text((x1+12,y+54),dv,font=f,fill=GREEN)
    d.text((zero+14 if v<0 else 40,y+56) if False else (W-40-d.textlength(t,font=F(22)),y+10),t,font=F(22),fill=SUB)
    y+=130
d.line((zero,140,zero,y-20),fill=INK,width=2); d.text((zero-58,y-14),'넣은 돈 1억',font=F(20,True),fill=INK)
d.text((40,H-40),'한국거래소 종가 · 운용사 분배금 공시로 직접 계산(분배금은 받은 그대로 더함)',font=F(18),fill=SUB)
im.save('pkg/img/01.png')
# 02: 듀레이션과 1년 값 변화
rows2=[('10년물 ETF','7.7년','약 -6%','약 770만원'),('3년물 ETF','2.8년','-0.2%','약 280만원'),('단기통안채','0.4년','약 +2%','약 40만원')]
W,H=900,560; im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.text((40,32),'듀레이션이 길수록 가격이 더 흔들린다',font=F(36,True),fill=INK)
d.text((40,84),'3년·10년 금리 1년 새 약 1.3%p 오를 때 · 채권 ETF 셋',font=F(21),fill=SUB)
cols=[(40,'ETF'),(290,'듀레이션'),(470,'1년 손익'),(680,'1억·금리 1%p')]
for cx,ct in cols: d.text((cx,140),ct,font=F(22,True),fill=SUB)
d.line((40,178,W-40,178),fill=LINE,width=2)
y=196
for i,(a,b,c,e) in enumerate(rows2):
    d.rounded_rectangle((40,y,W-40,y+84),radius=12,fill=(244,246,250))
    d.text((60,y+24),a,font=F(30,True),fill=INK)
    d.text((290,y+22),b,font=F(32,True),fill=ACC)
    d.text((470,y+22),c,font=F(32,True),fill=WARN if '-' in c else GREEN)
    d.text((680,y+24),e,font=F(28,True),fill=INK)
    y+=98
d.text((40,y+10),'듀레이션: 키움투자자산운용(10/19)·미래에셋자산운용(10/16) 공시',font=F(18),fill=SUB)
d.text((40,y+38),'1년 손익은 분배금 포함 · 오른쪽은 금리 1%p에 늘거나 주는 돈 어림셈',font=F(18),fill=SUB)
im.save('pkg/img/02.png')
json.dump({'01.png':{'rows':[[n,t,dv] for n,s2,v,t,dv in rows]},'02.png':{'rows':[list(r) for r in rows2]}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
