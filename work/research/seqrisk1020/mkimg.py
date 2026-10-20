import sys, os, json, re; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from blogimg import F, INK, SUB, LINE, BG, ACC, WARN
txt=open('calc_out.txt',encoding='utf-8').read()
# 01 순서
W,H=900,520; im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.text((40,32),'같은 28년 수익률, 순서만 바꾸면',font=F(38,True),fill=INK)
d.text((40,86),'3억원 · 매달 200만원 꺼내 씀 · S&P500 배당 포함(원화) · 1998~2025년',font=F(21),fill=SUB)
rows=[('실제 순서 (1998년 수익률부터)','14년째(2011년 1월) 바닥 — 1년 치를 못 꺼냄',0.012,WARN),('순서만 거꾸로 (2025년 수익률부터)','28년 뒤 13억 4,500만원 남음',13.45,ACC)]
y=150; maxw=W-80
for n,lab,v,c in rows:
    d.text((40,y),n,font=F(27,True),fill=INK)
    w=max(10,int(v/14*maxw)); d.rectangle((40,y+46,40+w,y+96),fill=c)
    tx=40+w+14 if w<500 else 56; d.text((tx,y+54),lab,font=F(28,True),fill=c if w<500 else (255,255,255))
    y+=150
d.text((40,H-46),'안 꺼냈다면 두 순서 모두 3억 → 35억 6,500만원 · 해마다 1월 1년 치 매도 · 물가 반영 안 함 · 파이어맵 계산',font=F(18),fill=SUB)
im.save('pkg/img/01.png')
# 02 37명
pts=[(int(a),float(b),c) for a,b,c in re.findall(r'  (\d{4}): 첫5년 ([+-][\d.]+)% · (\S+)',txt) if int(a)<=2008]
W,H=900,640; im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
d.text((40,28),'시작한 해별 첫 5년 연평균 수익률 (원화)',font=F(36,True),fill=INK)
d.text((40,80),'3억에서 매년 2,400만원(8%) 꺼냈을 때 · 빨간 막대 = 그해 시작한 계좌가 바닥난 경우',font=F(23,True),fill=WARN)
top,bot=150,560; zero=top+int((bot-top)*40/50); sc=(bot-top)/50
L=60; bw=(W-L-30)/len(pts)
d.line((L,zero,W-30,zero),fill=LINE,width=2)
for v in (-10,0,10,20,30,40):
    yy=zero-v*sc; d.text((8,yy-12),f'{v}%'.replace('-','−'),font=F(16),fill=SUB)
for i,(yr,v,res) in enumerate(pts):
    x0=L+i*bw+2; x1=L+(i+1)*bw-2; yy=zero-v*sc
    c=WARN if res=='바닥' else (ACC if yr<=2012 else (170,190,220))
    d.rectangle((x0,min(yy,zero),x1,max(yy,zero)),fill=c)
    if yr%5==0 or yr==2008: d.text((x0-6,bot+8),str(yr),font=F(15),fill=SUB)
d.text((40,H-40),'1989~2008년 1월 시작(18년 넘게 지켜본 경우만) · 3억 · 월 200만원 · 파이어맵 계산',font=F(17),fill=SUB)
im.save('pkg/img/02.png')
json.dump({'01.png':{'rows':[[n,l] for n,l,v,c in rows]},'02.png':{'rows':[[str(a),f'{b:+.1f}%',c] for a,b,c in pts]}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(pts))
