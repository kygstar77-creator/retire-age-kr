# 블로그용 표 이미지(직접 만든 이미지). 900px 폭, 밝은 배경 — 네이버 블로그 본문 폭에 맞춤. 파이어맵 브랜드 표시 없음(블로그는 파이어맵과 분리).
import sys, os
from PIL import Image, ImageDraw, ImageFont
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
def F(sz, bold=False):
    p = os.path.join(FD, 'pd700.ttf' if bold else 'pd500.ttf')
    return ImageFont.truetype(p, sz) if os.path.exists(p) else ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf' if bold else r'C:\Windows\Fonts\malgun.ttf', sz)
INK=(24,28,38); SUB=(98,106,122); LINE=(226,230,238); BG=(255,255,255); HEAD=(244,246,250); ACC=(32,96,224); WARN=(214,69,65)
def table(path, title, cols, rows, widths, note=None, hl_col=None, src=None):
    W=900; pad=36; rh=58; th=54
    H=pad+56+18+th+rh*len(rows)+(34 if note else 0)+(30 if src else 0)+pad
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.text((pad,pad),title,font=F(30,True),fill=INK)
    y=pad+56+18; x0=pad; tw=W-pad*2
    xs=[x0]; 
    for w in widths: xs.append(xs[-1]+int(tw*w))
    d.rounded_rectangle((x0,y,x0+tw,y+th),10,fill=HEAD)
    for i,c in enumerate(cols): d.text((xs[i]+14,y+15),c,font=F(20,True),fill=SUB)
    y+=th
    for r in rows:
        for i,c in enumerate(r):
            col = ACC if (hl_col is not None and i==hl_col) else INK
            d.text((xs[i]+14,y+16),str(c),font=F(22, i==0 or i==hl_col),fill=col)
        y+=rh; d.line((x0,y,x0+tw,y),fill=LINE,width=1)
    if note: d.text((pad,y+12),note,font=F(18),fill=SUB); y+=34
    if src: d.text((pad,y+10),src,font=F(16),fill=(150,156,168))
    im.save(path); return path

def steps(path, title, items, note=None, src=None):
    """번호가 붙은 절차 카드. 표와 달리 순서를 보여 줄 때."""
    W=900; pad=36; rh=86
    H=pad+56+18+rh*len(items)+(34 if note else 0)+(30 if src else 0)+pad
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.text((pad,pad),title,font=F(30,True),fill=INK)
    y=pad+56+18
    for i,(head,desc) in enumerate(items,1):
        d.rounded_rectangle((pad,y+10,pad+44,y+54),22,fill=ACC)
        w=d.textlength(str(i),font=F(22,True))
        d.text((pad+22-w/2,y+21),str(i),font=F(22,True),fill=(255,255,255))
        d.text((pad+62,y+12),head,font=F(23,True),fill=INK)
        if desc: d.text((pad+62,y+44),desc,font=F(19),fill=SUB)
        y+=rh
        if i<len(items): d.line((pad+62,y-6,W-pad,y-6),fill=LINE,width=1)
    if note: d.text((pad,y+12),note,font=F(18),fill=SUB); y+=34
    if src: d.text((pad,y+10),src,font=F(16),fill=(150,156,168))
    im.save(path); return path
