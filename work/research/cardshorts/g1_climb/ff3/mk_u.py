# g1_climb 첫 프레임 문구 시험 3차(copywriter 2026-10-10 18시대, 운영실장 11:18 막힘 ①): visual r1 틀(4회 평균 6.13) 그대로, '산 값까지' → '산 값 회복까지'만 바꿈.
# 판단: '회복'은 '산 값'을 목적어로 붙일 때만 허용(가격 산수, 전망 아님) · '본전'·'원금'은 계속 금지(KRX 매매 수수료가 빠져 실제 본전은 +50.7%보다 큼).
# 숫자: ep/G-1/raw/calc_2026-10-06.json 269,810(1/29)→179,000(10/6) = -33.66% · +50.73%.
import sys,os,json,math
sys.path.insert(0,r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.stdout.reconfigure(encoding='utf-8')
import cardshort as C
from PIL import Image,ImageDraw,ImageEnhance
H=os.path.dirname(os.path.abspath(__file__)); G=os.path.join(H,'..')
W,HH=1080,1920
K=json.load(open(os.path.join(G,'..','..','longform','ep','G-1','raw','calc_2026-10-06.json'),encoding='utf-8'))['KRX_M04020000_won_per_g']
PK,NOW=K['2026-01-29'],K['2026-10-06']; assert PK==max(K.values()) and NOW==179000
assert round((NOW/PK-1)*100)==-34 and round((PK/NOW-1)*100)==51
RED,YEL,WHITE=(235,40,40),(255,214,0),(255,255,255)
def bright(top=170,b=1.05):
    bg=Image.open(os.path.join(G,'v8','gold_photo.jpg')).convert('RGB').resize((W,HH),Image.LANCZOS)
    bg=ImageEnhance.Brightness(ImageEnhance.Contrast(bg).enhance(1.25)).enhance(b)
    sh=Image.new('L',(W,HH)); ds=ImageDraw.Draw(sh)
    for y in range(HH): ds.line([(0,y),(W,y)],fill=int(top*max(0,1-y/1000)))
    return Image.composite(Image.new('RGB',(W,HH),(8,8,10)),bg,sh)
def arrow(d,p0,p1,w,head,col,ol=14):
    x0,y0=p0;x1,y1=p1;L=math.hypot(x1-x0,y1-y0);ux,uy=(x1-x0)/L,(y1-y0)/L;nx,ny=-uy,ux
    bx,by=x1-ux*head,y1-uy*head
    poly=[(x0+nx*w/2,y0+ny*w/2),(bx+nx*w/2,by+ny*w/2),(bx+nx*head*.75,by+ny*head*.75),(x1,y1),(bx-nx*head*.75,by-ny*head*.75),(bx-nx*w/2,by-ny*w/2),(x0-nx*w/2,y0-ny*w/2)]
    d.polygon(poly,outline=(0,0,0),width=ol); d.polygon(poly,fill=col); d.line(poly+[poly[0]],fill=(0,0,0),width=ol,joint='curve')
def txt(d,xy,s,f,fill,sw=12):
    d.text(xy,s,font=f,fill=fill,stroke_width=sw,stroke_fill=(0,0,0))
def u(bg,top,mid):
    d=ImageDraw.Draw(bg)
    txt(d,(60,130),top,C.BHS(150),WHITE,14)
    txt(d,(60,330),mid,C.BHS(118),WHITE,12)
    assert d.textbbox((60,330),mid,font=C.BHS(118))[2]<930
    txt(d,(30,480),'+51%',C.BHS(330),YEL,20)
    arrow(d,(470,1450),(470,880),150,260,YEL,16)
    return bg
for k,top,mid in [('u1','고점에 샀다면?','산 값 회복까지'),('u2','금 -34%','산 값 회복까지')]:
    u(bright(),top,mid).save(os.path.join(H,k+'.png')); print(k)
