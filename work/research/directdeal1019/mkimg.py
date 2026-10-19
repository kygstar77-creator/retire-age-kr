import sys, os, json; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from blogimg import F, INK, SUB, LINE, BG, ACC
GRAY=(178,186,200); YEL=(255,236,170); RED=(214,69,65)
# 01: 직거래 vs 중개거래 — 같은 단지 중개 가운데 값보다 얼마나 쌌나(구간별 비율)
rows=[('30% 넘게 쌈',33.4,0.3),('5~30% 쌈',48.8,14.7),('비슷(±5%)',15.0,None),('5% 넘게 비쌈',2.8,None)]
rows=[('30% 이상 쌈',33.4,0.3),('5~30% 쌈',48.8,14.7),('비슷 (위아래 5%)',15.0,69.7),('5% 이상 비쌈',2.8,15.3)]
W,H=900,640; im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.text((40,30),'같은 단지·같은 면적 중개거래 중간값과 비교',font=F(32,True),fill=INK)
d.rectangle((40,94,62,116),fill=ACC); d.text((70,90),'개인끼리 직거래 742건',font=F(22,True),fill=INK)
d.rectangle((340,94,362,116),fill=GRAY); d.text((370,90),'중개거래 4만 1,571건(같은 방법)',font=F(22,True),fill=INK)
base=520; top=170; scale=(base-top)/75.0; gw=(W-80)/4
for i,(n,a,b) in enumerate(rows):
    x=40+i*gw+gw*0.14; bw=gw*0.33
    for j,(v,c) in enumerate([(a,ACC),(b,GRAY)]):
        x0=x+j*(bw+8); y0=base-v*scale
        d.rectangle((x0,y0,x0+bw,base),fill=c)
        t=f'{v:g}%'; f=F(23,True); tw=d.textlength(t,font=f)
        d.text((x0+bw/2-tw/2,y0-32),t,font=f,fill=ACC if j==0 else SUB)
    f=F(23,True); tw=d.textlength(n,font=f); d.text((40+i*gw+gw/2-tw/2,base+14),n,font=f,fill=INK)
d.line((40,base,W-40,base),fill=LINE,width=2)
d.text((40,H-62),'서울 아파트 매매 · 2025년 10월~2026년 9월 계약 · 취소 거래 뺌 · 앞뒤 석 달 중개 3건 이상',font=F(18),fill=SUB)
d.text((40,H-34),'국토교통부 실거래가(공공데이터포털, 10월 19일 받음)로 직접 계산',font=F(17),fill=(150,156,168))
im.save('pkg/img/01.png')
items=[('시세 10억 집을 7억에','깎은 3억 = 기준금액 3억','0원',True),
       ('시세 10억 집을 6억에','증여로 보는 돈 1억','약 485만원',False),
       ('시세 20억 집을 15억에','증여로 보는 돈 2억','약 1,940만원',False),
       ('시세 20억 집을 14억에','증여로 보는 돈 3억','약 3,880만원',False)]
W=900; rh=100; H=110+len(items)*(rh+12)+96
im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.text((40,34),'부모 집을 싸게 산 성년 자녀의 증여세 (양도세·취득세는 따로)',font=F(34,True),fill=INK)
y=100
for t,s,v,hl in items:
    d.rounded_rectangle((40,y,W-40,y+rh),radius=14,fill=YEL if hl else (244,246,250))
    d.text((64,y+14),t,font=F(28,True),fill=INK); d.text((64,y+58),s,font=F(21),fill=SUB)
    f=F(36,True); tw=d.textlength(v,font=f); d.text((W-64-tw,y+28),v,font=f,fill=RED if hl else ACC)
    y+=rh+12
d.text((40,y+12),'기준금액 = 시가 30%와 3억원 중 적은 금액 · 증여로 보는 돈에서 5천만원 뺌 · 신고하면 3% 덜 냄',font=F(18),fill=SUB)
d.text((40,y+44),'부모 양도세·자녀 취득세는 따로(5% 이상 깎으면 시가로) · 시세는 예시 값',font=F(17),fill=(150,156,168))
im.save('pkg/img/02.png')
json.dump({'01.png':{'rows':[[n,f'{a:g}%',f'{b:g}%'] for n,a,b in rows]},'02.png':{'rows':[[t,s,v] for t,s,v,h in items]}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
