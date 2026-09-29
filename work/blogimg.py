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

def auto_widths(cols, rows, hl_col=None, cap=0.34):
    """열 폭을 내용에 맞춰 정한다. 각 열에서 가장 긴 글자의 실제 픽셀 폭을 재고,
    한 열이 전체의 cap(기본 34%)을 넘지 않게 눌러 비율로 돌려준다.
    2026-09-24: 손으로 폭을 주면 '94,120주'가 '94,120 / 주'로 갈리는 일이 회차마다 반복돼 넣었다."""
    need=[]
    for i,c in enumerate(cols):
        f=F(22, i==0 or i==hl_col)
        w=_M.textlength(str(c), font=F(20,True))
        for r in rows:
            if i < len(r): w=max(w, _M.textlength(str(r[i]), font=f))
        need.append(w+28)
    tot=sum(need) or 1.0
    auto_widths.need_px=tot            # 줄바꿈 없이 담으려면 몇 픽셀이 필요한지
    ws=[n/tot for n in need]
    over=[i for i,w in enumerate(ws) if w>cap]
    if over:                                  # 한 열이 너무 넓으면 깎아 나머지에 나눠 준다
        spare=sum(ws[i]-cap for i in over)
        rest=sum(w for i,w in enumerate(ws) if i not in over) or 1.0
        ws=[cap if i in over else w+spare*w/rest for i,w in enumerate(ws)]
    return ws

def table(path, title, cols, rows, widths=None, note=None, hl_col=None, src=None):
    W=900; pad=36; th=54; lh=30; vpad=15
    x0=pad; tw=W-pad*2
    # widths를 안 주면 내용을 재서 자동으로 정한다.
    fs=22
    if not widths:
        widths=auto_widths(cols, rows, hl_col)
        # 열이 많아 가용폭(tw)에 다 못 담으면 글자를 한 단계씩 줄인다.
        # 안 줄이면 '94,120주'가 '94,120 / 주'로 갈린다(2026-09-24).
        gap=28*len(cols)                               # 셀 여백은 글자를 줄여도 그대로다
        while fs>17 and (auto_widths.need_px-gap)*(fs/22.0)+gap > tw:
            fs-=1
    # widths는 비율(합 1)로 받는다. 픽셀 값(합이 1보다 훨씬 큰 경우)으로 줘도
    # 열이 화면 밖으로 밀리지 않도록 합으로 나눠 비율로 맞춘다.
    tot=float(sum(widths)) or 1.0
    ws=[w/tot for w in widths]
    xs=[x0]
    for w in ws: xs.append(xs[-1]+int(tw*w))
    cw=[xs[i+1]-xs[i]-28 for i in range(len(widths))]      # 셀 안쪽 폭(좌우 여백 14씩)
    # 1차: 각 셀을 줄바꿈해서 행 높이를 먼저 구한다
    wrapped=[]; heights=[]
    for r in rows:
        cells=[wrap(c, F(fs, i==0 or i==hl_col), cw[i]) for i,c in enumerate(r)]
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
    for i,c in enumerate(cols): d.text((xs[i]+14,y+15),c,font=F(min(20,fs-1),True),fill=SUB)
    y+=th
    for cells,rh in zip(wrapped,heights):
        for i,lines in enumerate(cells):
            col = ACC if (hl_col is not None and i==hl_col) else INK
            f=F(fs, i==0 or i==hl_col)
            ty=y+vpad
            for ln in lines: d.text((xs[i]+14,ty),ln,font=f,fill=col); ty+=lh
        y+=rh; d.line((x0,y,x0+tw,y),fill=LINE,width=1)
    if nl:
        y+=12
        for ln in nl: d.text((pad,y),ln,font=nf,fill=SUB); y+=26
    if sl:
        y+=10
        for ln in sl: d.text((pad,y),ln,font=sf,fill=(150,156,168)); y+=22
    im.save(path); _keep_table(path, title, cols, rows); return path

def _keep_table(path, title, cols, rows):
    """표 칸을 pkg/tables.json 에 남긴다 — selfcheck가 '표에만 있고 본문에 없는 숫자'를 찾는다.
    2026-09-29 report: pltr0929 표의 7억 6,400만달러·8억 900만달러가 본문에 없었는데
    selfcheck는 본문→사실표 방향만 봐서 못 잡았다. img/ 안에 두면 사진 수를 세는 스크립트(bodystudy)가 틀리니 pkg 에 둔다."""
    try:
        import json
        d = os.path.dirname(os.path.abspath(path))
        if os.path.basename(d) != 'img': return
        tp = os.path.join(os.path.dirname(d), 'tables.json')
        cur = json.load(open(tp, encoding='utf-8')) if os.path.exists(tp) else {}
        cur[os.path.basename(path)] = {'title': title, 'cols': list(cols), 'rows': [[str(c) for c in r] for r in rows]}
        json.dump(cur, open(tp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    except Exception:
        pass

def steps(path, title, items, note=None, src=None):
    """번호가 붙은 절차 카드. 표와 달리 순서를 보여 줄 때."""
    W=900; pad=36; tx=pad+62; iw=W-pad-tx
    hf=F(23,True); df=F(19); tf=F(30,True); nf=F(18); sf=F(16)
    # 2026-09-25: items 에 (제목, 설명) 쌍이 아니라 문자열만 넘기면 "too many values to unpack"
    # 으로 죽었다. 이미 그린 장수만 남고 나머지가 안 그려져, 회차가 원인을 찾느라 시간을 썼다.
    # 문자열 한 줄만 넘겨도 설명 없는 항목으로 받아 준다.
    items = [(it, '') if isinstance(it, str) else (tuple(it) + ('',))[:2] for it in items]
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

def line(path, title, xs, ys, marks=(), unit='', src=None):
    """주가·금리 같은 시계열 선 그래프. marks=[(x, y, '글자', 'red'|'ink'), ...] 로 점과 글자를 찍는다.
    2026-09-27: 종목 글마다 주가 차트를 회차가 즉석 스크립트로 그리고 있었고, matplotlib 이 안 깔려 있어
    그 자리에서 설치했다. 한 곳에 모아 둔다. (pip install matplotlib)"""
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib import font_manager as fm
    fp = fm.FontProperties(fname=os.path.join(FD, 'pd500.ttf')); fb = fm.FontProperties(fname=os.path.join(FD, 'pd700.ttf'))
    fig, ax = plt.subplots(figsize=(9, 5.2), dpi=100)
    # 글자 축은 위치(0,1,2…)로 그린다. 2026-09-27 JEPQ 분배금: 12월에 두 번 받은 달이 같은 이름이라
    # 한 칸에 겹쳐 선이 수직으로 튀었고, 36개 눈금 글자가 서로 덮였다. 눈금은 8개 안팎만 찍는다.
    lab = [str(x) for x in xs]; pos = list(range(len(lab)))
    ax.plot(pos, ys, color='#2060e0', lw=2)
    step = max(1, len(lab) // 8)
    ax.set_xticks(pos[::step]); ax.set_xticklabels(lab[::step], fontproperties=fp, fontsize=11)
    for i, (x, y, t, c) in enumerate(marks):
        col = '#d64541' if c == 'red' else '#181c26'
        x = x if isinstance(x, int) else (len(lab) - 1 - lab[::-1].index(str(x)) if str(x) in lab else 0)
        ax.scatter([x], [y], color=col, zorder=5)
        # 2026-09-28 노령연금 수급자 추이: 첫 점 글자가 바닥 아래로 내려가 x축 '2020'과 겹쳤다.
        # 바닥 15% 안쪽 점은 글자를 위로, 왼쪽 끝 점은 글자를 오른쪽으로 민다.
        y0, y1 = ax.get_ylim(); low = (y - y0) / ((y1 - y0) or 1) < 0.15
        dy = 12 if (i % 2 or low) else -22
        left = x <= (len(lab) - 1) * 0.1
        ax.annotate(t, (x, y), xytext=(12 if left else -12, dy), textcoords='offset points', ha='left' if left else 'right',
                    fontproperties=fb, fontsize=13, color=col)
    ax.set_title(title, fontproperties=fb, fontsize=19, loc='left', pad=14)
    for s in ('top', 'right'): ax.spines[s].set_visible(False)
    ax.grid(axis='y', color='#e2e6ee')
    if unit: ax.set_ylabel(unit, fontproperties=fp, fontsize=12)
    if src: fig.text(0.01, 0.01, src, fontproperties=fp, fontsize=11, color='#626a7a')
    plt.tight_layout(rect=(0, 0.03, 1, 1)); plt.savefig(path); plt.close(fig)
