# 썸네일 생성 — 경쟁 채널 459편(쇼츠 80·롱폼 379) 실측에서 뽑은 규칙으로 우리 디자인을 만든다(2026-09-23).
# 규칙(실측 근거):
#  - 제목 2줄, 윗줄 흰색 / 아랫줄은 앞에서부터 일부만 노란색(yellow_frac). 굵은 제목체(Black Han Sans, OFL 무료).
#  - 글자가 가로폭 88% 이상을 채운다(폰트 크기를 폭에 맞춰 자동 조정).
#  - 검은 외곽선 + 그림자로 어떤 배경에서도 읽히게.
#  - 배경 사진은 어둡게 깔고(밝기 45%) 글자 뒤는 더 어둡게.
#  - 좌상단에 채널 표시 한 줄. 숫자는 본문 색과 다르게(노란 줄은 그대로 노랑).
#  - 조회 상위 제목 패턴: 따옴표 인용 25%(조회 +27%), 지역명 28%(+30%), 경고·부정 8%(+38%). 숫자 43%.
#   py -3.12 work/thumb.py "윗줄" "아랫줄" <출력.png> [배경이미지] [--short]
import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
try: import numpy as np
except Exception: np = None
HERE = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(HERE, 'fonts')
YELLOW = (255, 214, 10); WHITE = (255, 255, 255); BLACK = (0, 0, 0)
# 흰 면적 손잡이 2 — 글자를 '작게' 말고 '흰색이 아니게' 만든다(2026-09-24 step39 막힘에서 나옴).
# 측정에서 흰색은 (채도<40 & 명도>205)인 픽셀이다. text_scale 은 white 와 text_bot 이 같은 손잡이를 놓고 싸워
# 하한 0.9 에 붙어 버렸다(loop step38~39 "한계에 붙어 더 못 감").
# 글자 전체를 한 색으로 아이보리로 바꿔 보니(실측 2026-09-24) 0.25→0.5 사이에서 white 0.0224 → 0.0003 으로
# 한 칸에 뛰어넘어 목표 0.0107 에 설 자리가 없었다. 그래서 '색의 세기'가 아니라 '아이보리로 칠하는 넓이'로 바꿨다.
# 줄마다 아래쪽 text_tint 만큼을 강조색으로 칠한다(위는 흰색 그대로) — 글자 크기는 1픽셀도 안 줄어든다.
# 색은 차갑게 간다. 처음에 아이보리(255,214,130)로 뒀더니 그 색의 색상각이 20도라 측정의 노랑 띠(20~35)에
# 그대로 들어가서, tint 를 올릴수록 yellow 가 같이 올라가고 루프가 yellow_frac 을 0까지 깎아 버렸다
# (step40→41 실측: yellow 0.0086 → 0.0154, yellow_frac 0.3978 → 0.3009 → 0.0). 두 손잡이가 서로를 망친다.
# 얼음빛 파랑은 색상각이 파랑 쪽이라 노랑·빨강 띠 어디에도 안 걸리고, 채도 70 으로 흰색 기준(채도<40)도 벗어난다.
TINT = (185, 222, 255)

def tint_rgb():
    return TINT

def cfg(kind):
    """loop.py가 매 회차 갱신하는 design.json. 없으면 첫 측정값(2026-09-23 경쟁 상위 중앙값)"""
    try: d = json.load(open(os.path.join(HERE, 'design.json'), encoding='utf-8'))
    except Exception: d = {}
    base = {'long': {'text_y': 0.72, 'bg_bright': 0.45, 'panel_alpha': 150, 'yellow_bottom': 1, 'yellow_frac': 1.0, 'num_yellow': 1, 'stroke_ratio': 16, 'text_scale': 1.0, 'text_spread': 0.0, 'bg_sat': 0.8, 'text_tint': 0.0},
            'short': {'text_y': 0.52, 'bg_bright': 0.30, 'panel_alpha': 150, 'yellow_bottom': 0, 'yellow_frac': 0.0, 'num_yellow': 1, 'stroke_ratio': 16, 'text_scale': 1.0, 'text_spread': 0.0, 'bg_sat': 0.8, 'text_tint': 0.0}}[kind]
    base.update(d.get(kind, {})); return base

def disp(sz):
    for n in ('BlackHanSans.ttf', 'pd700.ttf'):
        p = os.path.join(FD, n)
        if os.path.exists(p): return ImageFont.truetype(p, sz)
    return ImageFont.truetype(r'C:\Windows\Fonts\malgunbd.ttf', sz)

def body(sz):
    p = os.path.join(FD, 'pd500.ttf')
    return ImageFont.truetype(p, sz) if os.path.exists(p) else ImageFont.truetype(r'C:\Windows\Fonts\malgun.ttf', sz)

def fit(dr, text, maxw, lo=40, hi=260):
    """글자가 maxw를 꽉 채우는 최대 크기"""
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if dr.textlength(text, font=disp(mid)) <= maxw: lo = mid
        else: hi = mid - 1
    return disp(lo)

def snap(text, n):
    """노랑/흰색 경계가 숫자·영문 한 덩어리 안을 가르지 않게 가까운 쪽 끝으로 민다('2|5개' → '25|개')"""
    run = lambda ch: ch.isdigit() or ch.isascii() and ch.isalpha() or ch == '%'
    if not (0 < n < len(text)) or not (run(text[n - 1]) and run(text[n])): return n
    a = n
    while a > 0 and run(text[a - 1]): a -= 1
    b = n
    while b < len(text) and run(text[b]): b += 1
    return a if n - a <= b - n else b

def stroked(dr, xy, text, f, fill, sw):
    x, y = xy
    dr.text((x, y), text, font=f, fill=fill, stroke_width=sw, stroke_fill=BLACK)

def make(top, bottom, out, bg=None, short=False, brand='파이어맵'):
    c = cfg('short' if short else 'long')
    W, H = (1080, 1920) if short else (1280, 720)
    if bg and os.path.exists(bg):
        im = Image.open(bg).convert('RGB')
        r = max(W / im.width, H / im.height)
        im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1)).crop((0, 0, W, H))
        im = ImageEnhance.Brightness(im).enhance(max(0.12, min(1.8, c['bg_bright'])))
        # 배경 채도. 0.8로 박아 두었던 값을 손잡이로 바꿨다 — 쇼츠 채도가 우리 0.187 vs 경쟁 0.399로
        # 여섯 회차 연속 "그리기 손잡이 없음"으로 막혀 있었다(2026-09-23 step25~30).
        im = ImageEnhance.Color(im).enhance(max(0.0, min(3.0, float(c.get('bg_sat', 0.8)))))
    else:
        v = int(255 * c['bg_bright'] * 0.35)
        im = Image.new('RGB', (W, H), (max(8, v - 6), max(9, v - 4), max(14, v + 6)))
        g = Image.new('L', (1, H)); [g.putpixel((0, y), int(30 + 50 * y / H)) for y in range(H)]
        im = Image.composite(Image.new('RGB', (W, H), (v + 14, v + 18, v + 34)), im, g.resize((W, H)))
    dr = ImageDraw.Draw(im)
    pad = int(W * 0.05); maxw = W - pad * 2
    f1 = fit(dr, top, maxw); f2 = fit(dr, bottom, maxw)
    sz = min(f1.size, f2.size)
    # 흰 면적은 흰 글자 픽셀에서 나온다. 외곽선(검정)으로는 줄지 않아 글자 크기를 손잡이로 뒀다(2026-09-23).
    sz = max(int(W * 0.055), int(sz * min(max(float(c.get('text_scale', 1.0)), 0.66), 1.0)))
    f1 = disp(sz); f2 = disp(sz)
    lh = int(sz * 1.18); block = lh * 2
    y0 = int(min(max(c['text_y'], 0.15), 0.80) * H) - block // 2   # 글자 세로 위치. loop.py가 실측 차이를 보고 움직인다
    # 두 줄을 위·아래로 벌린다(text_spread 0~1). 쇼츠(1080x1920)는 두 줄을 붙여 놓으면 세로 셋 중 한 칸에만 글자가 들어가
    # text_y를 어디로 옮겨도 top·bot 두 칸을 동시에 채울 수 없었다(2026-09-23 step19~23 "듣지 않는 손잡이" 5회차).
    # 경쟁 쇼츠 상위는 top 0.2748 · mid 0.4241 · bot 0.3093 으로 세 칸에 다 글자가 있다 — 훅을 위, 답을 아래에 두는 판형.
    spread = min(max(float(c.get('text_spread', 0.0)), 0.0), 1.0)
    off = int(spread * H * 0.30)
    ya = max(int(H * 0.04), y0 - off)                        # 윗줄
    yb = min(H - lh - int(H * 0.05), y0 + lh + off)           # 아랫줄
    # 글자 뒤 어둡게 — 벌어졌으면 줄마다 따로, 붙어 있으면 한 덩이로
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dsh = ImageDraw.Draw(sh)
    if off > lh * 0.4:
        for y in (ya, yb): dsh.rectangle([0, y - int(lh * 0.35), W, y + lh + int(lh * 0.3)], fill=(0, 0, 0, int(c['panel_alpha'])))
    else:
        dsh.rectangle([0, ya - int(lh * 0.35), W, yb + lh + int(lh * 0.3)], fill=(0, 0, 0, int(c['panel_alpha'])))
    im = Image.alpha_composite(im.convert('RGBA'), sh.filter(ImageFilter.GaussianBlur(28))).convert('RGB'); dr = ImageDraw.Draw(im)
    sw = max(3, int(sz // max(6, c['stroke_ratio'])))
    tx = (W - dr.textlength(top, font=f1)) / 2
    stroked(dr, (tx, ya), top, f1, WHITE, sw)
    # 아랫줄 노랑: 켜고 끄는 스위치가 아니라 '앞에서부터 몇 글자까지 노랑인가'(yellow_frac 0~1).
    # 경쟁 상위 노랑 면적은 롱폼 0.0258 · 쇼츠 0.0067 인데 한 줄 통째 노랑은 0.0526 이라 늘 넘어갔다 — 그래서 연속 손잡이로 바꿨다(2026-09-23).
    fr = c.get('yellow_frac')
    if fr is None: fr = 1.0 if c.get('yellow_bottom', 1) else 0.0
    fr = min(max(float(fr), 0.0), 1.0)
    bx = (W - dr.textlength(bottom, font=f2)) / 2
    stroked(dr, (bx, yb), bottom, f2, WHITE, sw)          # 외곽선은 줄 전체에 한 번만
    # 흰 면적 손잡이 2: 두 줄 모두 아래쪽 text_tint 만큼을 아이보리로 덮는다(노랑보다 먼저 — 노랑이 위에 온다)
    tt = min(max(float(c.get('text_tint', 0.0)), 0.0), 1.0)
    if tt > 0.001:
        gl = Image.new('L', (W, H), 0); gd = ImageDraw.Draw(gl)
        gd.text((tx, ya), top, font=f1, fill=255)
        gd.text((bx, yb), bottom, font=f2, fill=255)
        col = Image.new('L', (1, H), 0)                      # 줄마다 아래 tt 만큼만 1
        for ly in (ya, yb):
            top_of_tint = int(ly + lh * (1.0 - tt))
            for y in range(max(0, top_of_tint), min(H, ly + lh + 1)): col.putpixel((0, y), 255)
        col = col.resize((W, H)).filter(ImageFilter.GaussianBlur(max(1, sz // 24)))   # 경계를 부드럽게
        mask = Image.fromarray(
            (np.asarray(gl, dtype=np.uint16) * np.asarray(col, dtype=np.uint16) // 255).astype(np.uint8)
        ) if np is not None else Image.composite(gl, Image.new('L', (W, H), 0), col.point(lambda v: 255 if v > 127 else 0))
        im.paste(Image.new('RGB', (W, H), TINT), (0, 0), mask); dr = ImageDraw.Draw(im)
    n = snap(bottom, int(round(len(bottom) * fr)))
    if n: dr.text((bx, yb), bottom[:n], font=f2, fill=YELLOW)   # 같은 자리에 같은 글자를 덮어 칠해 앞부분만 노랑
    fb = body(int(W * 0.028))
    dr.rectangle([pad, pad, pad + 10, pad + int(W * 0.045)], fill=YELLOW)
    dr.text((pad + 24, pad), brand, font=fb, fill=(235, 235, 240))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True); im.save(out)
    print('썸네일', out, f'{W}x{H}', '글자크기', sz)
    return out

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if x != '--short']
    make(a[0], a[1], a[2], a[3] if len(a) > 3 else None, short='--short' in sys.argv)
