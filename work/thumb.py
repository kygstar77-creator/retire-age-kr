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

def fit_bg(im, W, H):
    """자료 화면은 통째로 보이게 넣는다 — 잘라 채우지 않는다(사장님 2026-09-23 "자료 화면이 보여야 한다").
    2026-09-24 실측: chartimg --short 는 1080x1350 인데 1080x1920 에 max 배율로 맞춰 (0,0) 에서 자르면
    가로가 1536 으로 늘어나 오른쪽 30%가 잘려 나간다. 막대와 값이 통째로 사라지고 단지 이름만 남아서
    자료 화면이 장식이 돼 버렸다(영상 프레임·썸네일 둘 다 확인). 그래서 '덮기'가 아니라 '안에 맞추기'다.
    남는 자리는 원본 가장자리 색으로 채워 이어 붙인 티가 안 나게 한다."""
    # 0.92 는 천천히 확대(design.json video.zoom)가 먹는 자리다 — 딱 맞춰 넣으면 확대되면서 다시 가장자리 값이 잘린다
    r = min(W / im.width, H / im.height) * 0.92
    nw, nh = max(1, int(im.width * r)), max(1, int(im.height * r))
    sm = im.resize((nw, nh))
    if nw >= W and nh >= H: return sm.crop((0, 0, W, H))
    edge = im.resize((1, 1)).getpixel((0, 0))          # 원본 평균색 — 차트 바탕이 어두우면 어둡게 채워진다
    out = Image.new('RGB', (W, H), edge)
    out.paste(sm, ((W - nw) // 2, (H - nh) // 2))
    return out


def tint_rgb():
    return TINT

def cfg(kind):
    """loop.py가 매 회차 갱신하는 design.json. 없으면 첫 측정값(2026-09-23 경쟁 상위 중앙값)"""
    try: d = json.load(open(os.path.join(HERE, 'design.json'), encoding='utf-8'))
    except Exception: d = {}
    base = {'long': {'text_y': 0.72, 'bg_bright': 0.45, 'panel_alpha': 150, 'yellow_bottom': 1, 'yellow_frac': 1.0, 'num_yellow': 1, 'stroke_ratio': 16, 'text_scale': 1.0, 'text_spread': 0.0, 'bg_sat': 0.8, 'text_tint': 0.0, 'yellow_tint': 0.0, 'tint_v': 1.0, 'tint_v': 1.0},
            'short': {'text_y': 0.52, 'bg_bright': 0.30, 'panel_alpha': 150, 'yellow_bottom': 0, 'yellow_frac': 0.0, 'num_yellow': 1, 'stroke_ratio': 16, 'text_scale': 1.0, 'text_spread': 0.0, 'bg_sat': 0.8, 'text_tint': 0.0, 'yellow_tint': 0.0, 'tint_v': 1.0, 'lines': 3, 'split_scale': 2.0}}[kind]
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

def clip_words(t, n):
    """글자 수로 뚝 자르면 '월세 50만원'이 '월세 50만'이 된다(2026-09-24 썸네일에서 확인).
    넘치면 띄어쓰기 앞에서 자른다 — 말이 깨지지 않게."""
    t = (t or '').strip()
    if len(t) <= n: return t
    cut = t[:n]
    sp = cut.rfind(' ')
    return (cut[:sp].strip() if sp >= n // 2 else cut).strip()

def split2(t):
    """한 줄을 띄어쓰기 중 가운데에 가장 가까운 곳에서 둘로 나눈다. 말은 그대로, 순서도 그대로."""
    sp = [i for i, ch in enumerate(t) if ch == ' ']
    if not sp: return None
    i = min(sp, key=lambda x: abs(x - len(t) / 2))
    a, b = t[:i].strip(), t[i + 1:].strip()
    return (a, b) if a and b else None

def make(top, bottom, out, bg=None, short=False, brand='파이어맵'):
    c = cfg('short' if short else 'long')
    W, H = (1080, 1920) if short else (1280, 720)
    if bg and os.path.exists(bg):
        im = fit_bg(Image.open(bg).convert('RGB'), W, H)
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
    # --- 몇 줄로 쓸 것인가 (쇼츠 3줄 판형, 2026-09-24) -------------------------------------
    # 경쟁 쇼츠 상위는 세로 세 칸에 글자가 골고루 있다(top 0.2748 · mid 0.4241 · bot 0.3093, 296장 측정).
    # 우리는 두 줄뿐이라 text_spread 를 한계 1.0 까지 올려도 text_bot 0.203 에서 멈췄다(loop 45회차 실측).
    # 두 줄로는 칸이 둘뿐이라 구조적으로 못 닿는다 — 아랫줄을 띄어쓰기에서 둘로 나눠 세 칸을 채운다.
    # 글자를 새로 짓지 않는다: 주어진 말 그대로, 순서 그대로, 줄만 바꾼다.
    parts = [top, bottom]
    if short and int(c.get('lines', 2)) >= 3:
        sp = split2(bottom)
        if sp: parts = [top, sp[0], sp[1]]
    fs = [fit(dr, t, maxw) for t in parts]
    sz = min(f.size for f in fs)
    # 흰 면적은 흰 글자 픽셀에서 나온다. 외곽선(검정)으로는 줄지 않아 글자 크기를 손잡이로 뒀다(2026-09-23).
    sz = max(int(W * 0.055), int(sz * min(max(float(c.get('text_scale', 1.0)), 0.66), 1.0)))
    szs = [sz] * len(parts)
    if len(parts) == 3:
        # 나눈 두 줄은 짧아져서 폭에 여유가 생긴다 — 그 여유만큼 키운다(split_scale, 1.0이면 안 키움).
        # 윗한계 2.0은 임의로 박아 둔 값이었다 — loop 72회차까지 격자 최선이 늘 끝점 2.0 에 붙어
        # "유지(가장 작다)"로 보고되며 short 판형 오차가 0.2653 에 얼어 있었다(2026-09-24 확인).
        # 진짜 한계는 아래 fit(...) 폭 맞춤이므로 판을 넘치게 하지 않는다. 그래서 윗한계를 3.2 로 넓힌다.
        ss = min(max(float(c.get('split_scale', 1.0)), 1.0), 3.2)
        for i in (1, 2): szs[i] = max(sz, min(fit(dr, parts[i], maxw).size, int(sz * ss)))
    fonts = [disp(x) for x in szs]; lhs = [int(x * 1.18) for x in szs]
    cy = int(min(max(c['text_y'], 0.15), 0.80) * H)   # 글자 세로 가운데. loop.py가 실측 차이를 보고 움직인다
    # 줄을 위·아래로 벌린다(text_spread 0~1).
    spread = min(max(float(c.get('text_spread', 0.0)), 0.0), 1.0)
    if len(parts) == 2:
        off = int(spread * H * 0.30)
        y0 = cy - lhs[0]
        ys = [max(int(H * 0.04), y0 - off), min(H - lhs[1] - int(H * 0.05), y0 + lhs[0] + off)]
    else:
        off = int(spread * H * 0.26)
        m0 = cy - lhs[1] // 2
        ys = [max(int(H * 0.04), m0 - lhs[0] - off), m0, min(H - lhs[2] - int(H * 0.05), m0 + lhs[1] + off)]
    # 글자 뒤 어둡게 — 벌어졌으면 줄마다 따로, 붙어 있으면 한 덩이로
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dsh = ImageDraw.Draw(sh)
    if off > lhs[0] * 0.4:
        for y, l in zip(ys, lhs): dsh.rectangle([0, y - int(l * 0.35), W, y + l + int(l * 0.3)], fill=(0, 0, 0, int(c['panel_alpha'])))
    else:
        dsh.rectangle([0, ys[0] - int(lhs[0] * 0.35), W, ys[-1] + lhs[-1] + int(lhs[-1] * 0.3)], fill=(0, 0, 0, int(c['panel_alpha'])))
    im = Image.alpha_composite(im.convert('RGBA'), sh.filter(ImageFilter.GaussianBlur(28))).convert('RGB'); dr = ImageDraw.Draw(im)
    xs = [(W - dr.textlength(t, font=f)) / 2 for t, f in zip(parts, fonts)]
    for t, f, x, y, z in zip(parts, fonts, xs, ys, szs):
        stroked(dr, (x, y), t, f, WHITE, max(3, int(z // max(6, c['stroke_ratio']))))   # 외곽선은 줄마다 한 번만
    # 흰 면적 손잡이 2: 줄마다 아래쪽 text_tint 만큼을 얼음빛 파랑으로 덮는다(노랑보다 먼저 — 노랑이 위에 온다)
    tt = min(max(float(c.get('text_tint', 0.0)), 0.0), 1.0)
    if tt > 0.001:
        gl = Image.new('L', (W, H), 0); gd = ImageDraw.Draw(gl)
        for t, f, x, y in zip(parts, fonts, xs, ys): gd.text((x, y), t, font=f, fill=255)
        col = Image.new('L', (1, H), 0)                      # 줄마다 아래 tt 만큼만 1
        for y, l in zip(ys, lhs):
            for yy in range(max(0, int(y + l * (1.0 - tt))), min(H, y + l + 1)): col.putpixel((0, yy), 255)
        col = col.resize((W, H)).filter(ImageFilter.GaussianBlur(max(1, sz // 24)))   # 경계를 부드럽게
        mask = Image.fromarray(
            (np.asarray(gl, dtype=np.uint16) * np.asarray(col, dtype=np.uint16) // 255).astype(np.uint8)
        ) if np is not None else Image.composite(gl, Image.new('L', (W, H), 0), col.point(lambda v: 255 if v > 127 else 0))
        # 대비 손잡이(tint_v): 강조색의 밝기. 쇼츠 대비가 우리 0.2638 vs 경쟁 0.1791 로 여러 회차 막혀 있었다.
        # 2026-09-24 갈라 재 보니 넘치는 대비는 배경이 아니라 글자 자리에서 온다(경쟁 상위 10장 vs 우리 3장):
        #   배경만 대비  우리 0.0531 < 경쟁 0.0734   ← 우리 배경은 이미 경쟁보다 평평하다
        #   글자자리 대비 우리 0.4063 > 경쟁 0.2732 · 아주 밝은 픽셀(V>0.80) 우리 0.0913 vs 경쟁 0.0235
        # 얼음빛 파랑(185,222,255)은 V가 255라, text_tint 를 0.88 까지 올려 흰 면적을 맞춘 대신
        # 글자의 절반 이상이 '아주 밝은' 픽셀이 됐다. 그래서 배경을 누르는 손잡이(bg_flat)가 아니라
        # 강조색을 낮추는 손잡이를 단다 — 자료 화면은 1픽셀도 안 건드린다(사장님 "자료가 보여야 한다").
        tv = min(max(float(c.get('tint_v', 1.0)), 0.75), 1.0)   # 0.75 하한: 더 낮추면 글자가 회색으로 죽는다(화면 검증 2026-09-24)
        im.paste(Image.new('RGB', (W, H), tuple(int(v * tv) for v in TINT)), (0, 0), mask); dr = ImageDraw.Draw(im)
    # 마지막 줄 노랑: 켜고 끄는 스위치가 아니라 '앞에서부터 몇 글자까지 노랑인가'(yellow_frac 0~1).
    # 경쟁 상위 노랑 면적은 롱폼 0.0258 · 쇼츠 0.0067 인데 한 줄 통째 노랑은 0.0526 이라 늘 넘어갔다 — 그래서 연속 손잡이로 바꿨다(2026-09-23).
    fr = c.get('yellow_frac')
    if fr is None: fr = 1.0 if c.get('yellow_bottom', 1) else 0.0
    fr = min(max(float(fr), 0.0), 1.0)
    last = parts[-1]
    n = snap(last, int(round(len(last) * fr)))
    if n: dr.text((xs[-1], ys[-1]), last[:n], font=fonts[-1], fill=YELLOW)   # 같은 자리에 같은 글자를 덮어 칠해 앞부분만 노랑
    # 노랑 손잡이 2: 마지막 줄 글자의 아래쪽 yellow_tint 만큼만 노랑으로 칠한다(0~1).
    # yellow_frac 은 '글자 몇 개'라 계단이다 — 쇼츠 실측(2026-09-24, 배경 3종 중앙값):
    #   0/0.0997 → 0.0003 · 0.1088~0.2 → 0.0099 · 0.3~0.6 → 0.0169 · 1.0 → 0.0345.
    # 경쟁 상위 쇼츠 목표 0.0067 은 '글자 0개'와 '1개' 사이에 있어 어떤 값으로도 못 맞춘다(루프 53~61회차 막힘).
    # 밑줄(형광펜)도 대 봤지만 못 쓴다: 실측 yellow_bar 0.15 에서 노랑 0.0051 로 잘 듣는 대신
    # text_bot 이 0.3009 → 0.3894 로 뛴다(목표 0.3093 에서 +26%, 새 차이가 생긴다).
    # 측정의 글자 지도가 Canny 가장자리를 25x9 로 두 번 부풀리기 때문에, 가로로 긴 줄 하나가
    # 아래 칸 전체를 글자로 칠해 버린다. 그래서 '새 잉크를 안 더하는' 쪽으로 간다 —
    # text_tint 와 같은 방식으로 이미 있는 글자 픽셀의 아래쪽만 노랑으로 바꾼다. 글자량·대비는 그대로다.
    yt = min(max(float(c.get('yellow_tint', 0.0)), 0.0), 1.0)
    if yt > 0.001:
        gl = Image.new('L', (W, H), 0); gd = ImageDraw.Draw(gl)
        gd.text((xs[-1], ys[-1]), last, font=fonts[-1], fill=255)
        col = Image.new('L', (1, H), 0)
        for yy in range(max(0, int(ys[-1] + lhs[-1] * (1.0 - yt))), min(H, ys[-1] + lhs[-1] + 1)):
            col.putpixel((0, yy), 255)
        col = col.resize((W, H)).filter(ImageFilter.GaussianBlur(max(1, szs[-1] // 24)))
        mask = Image.fromarray(
            (np.asarray(gl, dtype=np.uint16) * np.asarray(col, dtype=np.uint16) // 255).astype(np.uint8)
        ) if np is not None else Image.composite(gl, Image.new('L', (W, H), 0), col.point(lambda v: 255 if v > 127 else 0))
        im.paste(Image.new('RGB', (W, H), YELLOW), (0, 0), mask); dr = ImageDraw.Draw(im)
    fb = body(int(W * 0.028))
    dr.rectangle([pad, pad, pad + 10, pad + int(W * 0.045)], fill=YELLOW)
    dr.text((pad + 24, pad), brand, font=fb, fill=(235, 235, 240))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True); im.save(out)
    print('썸네일', out, f'{W}x{H}', '글자크기', sz)
    return out

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if x != '--short']
    make(a[0], a[1], a[2], a[3] if len(a) > 3 else None, short='--short' in sys.argv)
