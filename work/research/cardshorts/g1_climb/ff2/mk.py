# g1_climb 새 첫 프레임 틀(visual-designer 2026-10-10 11시대, 운영실장 배차): 글자 카드 천장 6.5(copywriter 07:52) → 사진·화살표가 주인공.
# 숫자: ep/G-1/raw/calc_2026-10-06.json KRX 1g 고점 269,810(1/29) → 179,000(10/6) = -33.66% · 산 값까지 +50.7%. 문구 n3 축('고점에 산 금'·'산 값까지 +51%'), '본전·회복' 안 씀.
# 사진 = v8/gold_photo.jpg(제미나이 생성, 실제 인물 없음). 글자는 쇼츠 가림 안전선 x<930·y<1540 안.
import sys,os,json,math
sys.path.insert(0,r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.stdout.reconfigure(encoding='utf-8')
import cardshort as C
from PIL import Image,ImageDraw,ImageFilter,ImageEnhance
H=os.path.dirname(os.path.abspath(__file__)); G=os.path.join(H,'..')
W,HH=1080,1920
K=json.load(open(os.path.join(G,'..','..','longform','ep','G-1','raw','calc_2026-10-06.json'),encoding='utf-8'))['KRX_M04020000_won_per_g']
PK,NOW=K['2026-01-29'],K['2026-10-06']; assert PK==max(K.values()) and NOW==179000
DN=(NOW/PK-1)*100; UP=(PK/NOW-1)*100; assert round(DN)==-34 and round(UP)==51
RED,YEL,WHITE=(235,40,40),(255,214,0),(255,255,255)
def photo(dark):
    bg=Image.open(os.path.join(G,'v8','gold_photo.jpg')).convert('RGB').resize((W,HH),Image.LANCZOS)
    bg=ImageEnhance.Contrast(bg).enhance(1.15); bg=ImageEnhance.Brightness(bg).enhance(dark)
    sh=Image.new('L',(W,HH)); ds=ImageDraw.Draw(sh)
    for y in range(HH): ds.line([(0,y),(W,y)],fill=int(200*max(0,1-y/1100)))  # 위쪽 어둡게(글자 자리)
    return Image.composite(Image.new('RGB',(W,HH),(8,8,10)),bg,sh)
def plain():
    bg=Image.new('RGB',(W,HH),(14,15,18)); d=ImageDraw.Draw(bg)
    for y in range(1100,HH): d.line([(0,y),(W,y)],fill=(14+int(60*(y-1100)/820),15+int(45*(y-1100)/820),18))
    return bg
def arrow(d,p0,p1,w,head,col,ol=14):
    x0,y0=p0;x1,y1=p1;L=math.hypot(x1-x0,y1-y0);ux,uy=(x1-x0)/L,(y1-y0)/L;nx,ny=-uy,ux
    bx,by=x1-ux*head,y1-uy*head
    poly=[(x0+nx*w/2,y0+ny*w/2),(bx+nx*w/2,by+ny*w/2),(bx+nx*head*.75,by+ny*head*.75),(x1,y1),(bx-nx*head*.75,by-ny*head*.75),(bx-nx*w/2,by-ny*w/2),(x0-nx*w/2,y0-ny*w/2)]
    if ol: d.polygon(poly,outline=(0,0,0),width=ol)
    d.polygon(poly,fill=col)
    if ol: d.line(poly+[poly[0]],fill=(0,0,0),width=ol,joint='curve')
def txt(d,xy,s,f,fill,sw=12,anchor='la'):
    d.text(xy,s,font=f,fill=fill,stroke_width=sw,stroke_fill=(0,0,0),anchor=anchor)
def line(d,x0,y0,w,h):  # 실제 KRX 1g 일별 종가(얇게, 화살표 밑그림)
    ks=sorted(K); vs=[K[k] for k in ks]; lo,hi=min(vs),max(vs); n=len(vs)-1
    pts=[(x0+w*i/n,y0+h*(1-(v-lo)/(hi-lo))) for i,v in enumerate(vs)]; ip=vs.index(hi)
    d.line(pts[:ip+1],fill=(230,190,90),width=10,joint='curve'); d.line(pts[ip:],fill=(255,140,140),width=10,joint='curve')
    return pts[ip],pts[-1]
def p1(bg):  # 사진 + 큰 화살표 둘(빨강 내려감 -34%, 노랑 올라가야 +51%)
    d=ImageDraw.Draw(bg)
    txt(d,(60,150),'고점에 산 금',C.BHS(170),WHITE,14)
    pk=(150,560); nw=(470,1130)
    d.line([(pk[0]-60,pk[1]),(880,pk[1])],fill=WHITE,width=8)  # 고점 = 산 값 높이
    txt(d,(560,pk[1]-92),'산 값',C.BHS(80),WHITE,8)
    arrow(d,pk,nw,95,210,RED)
    arrow(d,(nw[0]+150,nw[1]),(nw[0]+150+260,pk[1]+20),95,210,YEL)
    txt(d,(20,1200),'-34%',C.BHS(175),RED,12)
    txt(d,(520,1200),'+51%',C.BHS(175),YEL,12)
    return bg
def p2(bg):  # 사진 + 실제 KRX 선 위에 빨강 화살표 하나 + 아래 큰 질문
    d=ImageDraw.Draw(bg)
    txt(d,(60,140),'고점에 산 금',C.BHS(170),WHITE,14)
    pk,nw=line(d,60,520,860,520)
    arrow(d,(pk[0]+20,pk[1]+30),(nw[0]-30,nw[1]-10),80,190,RED)
    txt(d,(pk[0]+60,pk[1]-20),'-34%',C.BHS(200),RED,14)
    txt(d,(60,1150),'산 값까지',C.BHS(150),WHITE,12)
    txt(d,(40,1300),'+51%',C.BHS(300),YEL,18)
    return bg
def p3(bg):  # 사진 + 거대 노랑 위 화살표 하나(+51%가 주인공)
    d=ImageDraw.Draw(bg)
    txt(d,(60,140),'금 -34%',C.BHS(210),RED,16)
    txt(d,(60,380),'산 값까지',C.BHS(150),WHITE,12)
    arrow(d,(820,1480),(820,620),140,280,YEL,16)
    txt(d,(40,700),'+51%',C.BHS(300),YEL,18)
    return bg
for k,f,b in [('p1',p1,lambda:photo(.85)),('p2',p2,lambda:photo(.8)),('p3',p3,lambda:photo(.85)),('q1',p1,plain)]:
    f(b()).save(os.path.join(H,k+'.png')); print(k)
print('DN %.2f UP %.2f'%(DN,UP))
# ── 2차(11시대): 심사 공통 지적 = 숫자 둘이 다투고 사진이 어둡다 → +51% 하나를 주인공, 질문형 머리, 밝은 금 사진.
def bright(top=170,b=1.05):
    bg=Image.open(os.path.join(G,'v8','gold_photo.jpg')).convert('RGB').resize((W,HH),Image.LANCZOS)
    bg=ImageEnhance.Brightness(ImageEnhance.Contrast(bg).enhance(1.25)).enhance(b)
    sh=Image.new('L',(W,HH)); ds=ImageDraw.Draw(sh)
    for y in range(HH): ds.line([(0,y),(W,y)],fill=int(top*max(0,1-y/1000)))
    return Image.composite(Image.new('RGB',(W,HH),(8,8,10)),bg,sh)
def r1(bg):  # 질문 + 거대 +51% + 위 화살표
    d=ImageDraw.Draw(bg)
    txt(d,(60,130),'고점에 샀다면?',C.BHS(150),WHITE,14)
    txt(d,(60,330),'산 값까지',C.BHS(130),WHITE,12)
    txt(d,(30,480),'+51%',C.BHS(330),YEL,20)
    arrow(d,(470,1450),(470,880),150,260,YEL,16)
    return bg
def r2(bg):  # 작은 빨강 -34% 화살표 → 거대 +51%
    d=ImageDraw.Draw(bg)
    txt(d,(60,130),'고점에 산 금',C.BHS(150),WHITE,14)
    arrow(d,(80,360),(260,560),60,130,RED,12); txt(d,(290,380),'-34%',C.BHS(150),RED,12)
    txt(d,(60,640),'산 값까지',C.BHS(130),WHITE,12)
    txt(d,(30,790),'+51%',C.BHS(285),YEL,18)
    arrow(d,(800,1480),(800,1060),120,220,YEL,14)
    return bg
def r3(bg):  # p2(실제 선) 밝게 + 숫자 위계(+51% 크게, -34% 작게)
    d=ImageDraw.Draw(bg)
    txt(d,(60,130),'고점에 산 금',C.BHS(150),WHITE,14)
    pk,nw=line(d,60,420,860,380)
    arrow(d,(pk[0]+20,pk[1]+30),(nw[0]-30,nw[1]-10),60,150,RED,12)
    txt(d,(pk[0]+70,pk[1]-10),'-34%',C.BHS(130),RED,10)
    txt(d,(60,900),'산 값까지',C.BHS(130),WHITE,12)
    txt(d,(30,1040),'+51%',C.BHS(285),YEL,18)
    return bg
for k,f in [('r1',r1),('r2',r2),('r3',r3)]:
    f(bright()).save(os.path.join(H,k+'.png')); print(k)
# ── 3차: r1(6.25)이 최고. 지적 = '+51%'가 수익률로 오독·금 사진 더 밝게·하락 선이 사진 위를 가로질러야. → 질문 머리 + 실제 KRX 선 굵게 사진 위 + '+51% 올라야 산 값'.
def bigline(d,x0,y0,w,h,lw=26):
    ks=sorted(K); vs=[K[k] for k in ks]; lo,hi=min(vs),max(vs); n=len(vs)-1
    pts=[(x0+w*i/n,y0+h*(1-(v-lo)/(hi-lo))) for i,v in enumerate(vs)]; ip=vs.index(hi)
    d.line(pts[:ip+1],fill=(0,0,0),width=lw+14,joint='curve'); d.line(pts[ip:],fill=(0,0,0),width=lw+14,joint='curve')
    d.line(pts[:ip+1],fill=(255,225,120),width=lw,joint='curve'); d.line(pts[ip:],fill=RED,width=lw+6,joint='curve')
    e=pts[-1]; arrow(d,(e[0]-60,e[1]-40),(e[0]+25,e[1]+45),1,120,RED,12)
    return pts[ip],e
def s1(bg,box=False,small=False):
    d=ImageDraw.Draw(bg,'RGBA')
    if box: d.rectangle([0,1020,1080,1520],fill=(0,0,0,170))
    txt(d,(60,120),'고점에 샀다면?',C.BHS(148),WHITE,14)
    pk,e=bigline(d,60,420,800,480)
    if small: txt(d,(e[0]-330,e[1]+40),'-34%',C.BHS(120),RED,10)
    txt(d,(30,1040),'+51%',C.BHS(290),YEL,18)
    txt(d,(60,1340),'올라야 산 값',C.BHS(140),WHITE,12)
    return bg
for k,f in [('s1',lambda b:s1(b)),('s2',lambda b:s1(b,box=True)),('s3',lambda b:s1(b,small=True))]:
    f(bright(170,1.2)).save(os.path.join(H,k+'.png')); print(k)
# ── 4차: 3차(선 크게)는 5로 떨어짐 → 최고 r1 틀(질문+산 값까지+거대 +51%+위 화살표)로 돌아가 하나씩만 바꿈.
def t(bg,band=False,down=False):
    d=ImageDraw.Draw(bg,'RGBA')
    if band: d.rectangle([0,0,1080,860],fill=(0,0,0,150))
    txt(d,(60,130),'고점에 샀다면?',C.BHS(148),WHITE,14)
    if down:
        txt(d,(60,330),'금 -34%',C.BHS(130),RED,12); y0=500
    else: y0=330
    txt(d,(60,y0),'산 값까지',C.BHS(130),WHITE,12)
    txt(d,(20,y0+140),'+51%',C.BHS(330),YEL,20)
    arrow(d,(470,1480),(470,y0+590),150,260,YEL,16)
    return bg
for k,f in [('t1',lambda b:t(b,down=True)),('t2',lambda b:t(b,band=True)),('t3',lambda b:t(b,band=True,down=True))]:
    f(bright(170,1.05)).save(os.path.join(H,k+'.png')); print(k)
