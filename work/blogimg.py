# 블로그용 표 이미지(직접 만든 이미지). 900px 폭, 밝은 배경 — 네이버 블로그 본문 폭에 맞춤. 파이어맵 브랜드 표시 없음(블로그는 파이어맵과 분리).
import sys, os
from PIL import Image, ImageDraw, ImageFont
FD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
def F(sz, bold=False):
    p = os.path.join(FD, 'pd700.ttf' if bold else 'pd500.ttf')
    return ImageFont.truetype(p, sz) if os.path.exists(p) else ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf' if bold else r'C:\Windows\Fonts\malgun.ttf', sz)
INK=(24,28,38); SUB=(98,106,122); LINE=(226,230,238); BG=(255,255,255); HEAD=(244,246,250); ACC=(32,96,224); WARN=(214,69,65)
_M = ImageDraw.Draw(Image.new('RGB',(8,8)))   # 글자 폭만 재는 용도
def wrap(text, font, maxw):
    """maxw 픽셀 안에 들어가도록 줄을 나눈다. 띄어쓰기에서 먼저 끊고,
    한 덩어리가 통째로 넘치면 글자 단위로 자른다(한국어는 단어가 길게 붙는다)."""
    text = str(text)
    out = []
    for para in text.split('\n'):
        cur = ''
        for w in para.split(' '):
            t = (cur + ' ' + w).strip()
            if _M.textlength(t, font=font) <= maxw:
                cur = t; continue
            if cur: out.append(cur); cur = ''
            while _M.textlength(w, font=font) > maxw:
                i = 1
                while i < len(w) and _M.textlength(w[:i+1], font=font) <= maxw: i += 1
                out.append(w[:i]); w = w[i:]
            cur = w
        out.append(cur)
    return out or ['']

def table(path, title, cols, rows, widths, note=None, hl_col=None, src=None):
    W=900; pad=36; th=54; lh=30; vpad=15
    x0=pad; tw=W-pad*2
    xs=[x0]
    for w in widths: xs.append(xs[-1]+int(tw*w))
    cw=[xs[i+1]-xs[i]-28 for i in range(len(widths))]      # 셀 안쪽 폭(좌우 여백 14씩)
    # 1차: 각 셀을 줄바꿈해서 행 높이를 먼저 구한다
    wrapped=[]; heights=[]
    for r in rows:
        cells=[wrap(c, F(22, i==0 or i==hl_col), cw[i]) for i,c in enumerate(r)]
        wrapped.append(cells)
        heights.append(max(len(c) for c in cells)*lh + vpad*2)
    tf=F(30,True); nf=F(18); sf=F(16)
    tl=wrap(title, tf, tw); nl=wrap(note, nf, tw) if note else []; sl=wrap(src, sf, tw) if src else []
    H=pad+len(tl)*42+18+th+sum(heights)+(len(nl)*26+12 if nl else 0)+(len(sl)*22+10 if sl else 0)+pad
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    y=pad
    for ln in tl: d.text((pad,y),ln,font=tf,fill=INK); y+=42
    y+=18
    d.rounded_rectangle((x0,y,x0+tw,y+th),10,fill=HEAD)
    for i,c in enumerate(cols): d.text((xs[i]+14,y+15),c,font=F(20,True),fill=SUB)
    y+=th
    for cells,rh in zip(wrapped,heights):
        for i,lines in enumerate(cells):
            col = ACC if (hl_col is not None and i==hl_col) else INK
            f=F(22, i==0 or i==hl_col)
            ty=y+vpad
            for ln in lines: d.text((xs[i]+14,ty),ln,font=f,fill=col); ty+=lh
        y+=rh; d.line((x0,y,x0+tw,y),fill=LINE,width=1)
    if nl:
        y+=12
        for ln in nl: d.text((pad,y),ln,font=nf,fill=SUB); y+=26
    if sl:
        y+=10
        for ln in sl: d.text((pad,y),ln,font=sf,fill=(150,156,168)); y+=22
    im.save(path); return path

def steps(path, title, items, note=None, src=None):
    """번호가 붙은 절차 카드. 표와 달리 순서를 보여 줄 때."""
    W=900; pad=36; tx=pad+62; iw=W-pad-tx
    hf=F(23,True); df=F(19); tf=F(30,True); nf=F(18); sf=F(16)
    body=[(wrap(h,hf,iw), wrap(dsc,df,iw) if dsc else []) for h,dsc in items]
    heights=[max(86, 22+len(hl)*30+(len(dl)*26 if dl else 0)+18) for hl,dl in body]
    tl=wrap(title,tf,W-pad*2); nl=wrap(note,nf,W-pad*2) if note else []; sl=wrap(src,sf,W-pad*2) if src else []
    H=pad+len(tl)*42+18+sum(heights)+(len(nl)*26+12 if nl else 0)+(len(sl)*22+10 if sl else 0)+pad
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    y=pad
    for ln in tl: d.text((pad,y),ln,font=tf,fill=INK); y+=42
    y+=18
    for i,((hl,dl),rh) in enumerate(zip(body,heights),1):
        d.rounded_rectangle((pad,y+10,pad+44,y+54),22,fill=ACC)
        w=d.textlength(str(i),font=F(22,True))
        d.text((pad+22-w/2,y+21),str(i),font=F(22,True),fill=(255,255,255))
        ty=y+12
        for ln in hl: d.text((tx,ty),ln,font=hf,fill=INK); ty+=30
        if dl:
            ty+=4
            for ln in dl: d.text((tx,ty),ln,font=df,fill=SUB); ty+=26
        y+=rh
        if i<len(items): d.line((tx,y-6,W-pad,y-6),fill=LINE,width=1)
    if nl:
        y+=12
        for ln in nl: d.text((pad,y),ln,font=nf,fill=SUB); y+=26
    if sl:
        y+=10
        for ln in sl: d.text((pad,y),ln,font=sf,fill=(150,156,168)); y+=22
    im.save(path); return path
