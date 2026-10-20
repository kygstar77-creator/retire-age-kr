import sys, os, json; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
from blogimg import F, INK, SUB, LINE, BG, ACC
import calc
def table(path, title, head, rows, foot, widths, hl_col=None):
    W=1040; rh=64; H=150+rh*(len(rows)+1)+90
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.text((40,30),title,font=F(32,True),fill=INK)
    x0=40; y=110
    xs=[x0]
    for w in widths: xs.append(xs[-1]+w)
    d.rectangle((x0,y,xs[-1],y+rh),fill=(232,238,252))
    for i,h in enumerate(head):
        d.text((xs[i]+14,y+16),h,font=F(24,True),fill=INK)
    for r,row in enumerate(rows):
        yy=y+rh*(r+1)
        d.line((x0,yy,xs[-1],yy),fill=LINE,width=1)
        for i,c in enumerate(row):
            col = ACC if (hl_col is not None and i in hl_col) else INK
            d.text((xs[i]+14,yy+16),c,font=F(24,i==0 or (hl_col and i in hl_col)),fill=col)
    d.text((40,H-70),foot[0],font=F(18),fill=SUB); d.text((40,H-40),foot[1],font=F(17),fill=(150,156,168))
    im.save(path)
rows=[]
for G in (3000,4000,5000,6000,7000,8000,9000):
    r=[f'{G:,}만원']
    for k in (0,1,2): r.append(f'{round(calc.reach(G,"c",k)):,}만원')
    rows.append(r)
table('pkg/img/01.png','신용카드만 쓸 때 한도에 닿는 카드값',['총급여','자녀 없음','자녀 1명','자녀 2명 이상'],rows,
  ['총급여 7천만원 이하 한도 300·350·400만원, 초과 250·275·300만원 · 2026년 사용분','자료: 조세특례제한법 제126조의2 · 직접 계산 · 2026년 10월 20일 조회'],[210,240,240,270],hl_col=None)
def fmt(x): return f'{x:g}'
def case(**kw):
    out=[]
    for k in (0,1,2):
        d,o,c=calc.ded(5000,kids=k,**kw); out.append(fmt(round(o,1))+'만원')
    return out
a=case(credit=3600); b=case(credit=3000,debit=1500,market=200,transit=200)
rows=[['신용카드 3,600만원']+a,['신용 3,000·체크 1,500\n전통시장 200·대중교통 200'.replace('\n',' ')]+b]
rows[1][0]='섞어 쓴 4,900만원'
table('pkg/img/02.png','총급여 5천만원, 공제받는 금액',['카드 사용','자녀 없음','자녀 1명','자녀 2명 이상'],rows,
  ['섞어 쓴 경우=신용 3,000·체크·현금영수증 1,500·전통시장 200·대중교통 200(만원) · 2026년 사용분','자료: 조세특례제한법 제126조의2 · 직접 계산 · 2026년 10월 20일 조회'],[360,190,190,240])
json.dump({'01.png':rows}, open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False)
print(a,b)
