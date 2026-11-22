# H-6 은마 썸네일 시안(visual 2026-11-21 09시) — KOSPI-1 make_kospi1.py 복사(N-2 thumb_A 꼴, 큰 글 아래 40~45% C-02), 사진·문구만 바꿈.
#   문구 research/copy/h6/titles.md '썸네일 문구 (가운데 값 기준)' 그대로: 흰 줄 '은마아파트 84㎡ · 실거래 가운데 값' / 큰 흰 '같은 평형 43억이' / 큰 주황 '1년 뒤 34억으로' · 알약 없음
#   사실 ep/H-6/calc2_out.txt: 84㎡ 2025.10~12 계약 가운데 42.80억(3건) → 2026.10~11 계약 34.30억(9건) — 43·34는 대본 말 '43억 가까이'·'34억을 조금 넘어요'와 같음
#   사진 Pexels(photo/sources.json) — 사람 없음, 실제 은마 사진 아님(낡은 판상형 아파트 외벽·단지)
import os, sys, json
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.abspath(__file__)); H = os.path.join(O, 'photo'); WORK = os.path.abspath(os.path.join(O, '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts'); W, HH = 1920, 1080; X0 = 80
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)
BIG = ['같은 평형 43억이', '1년 뒤 34억으로']   # 11/18 copywriter 1초 시험 2차: '하루 5% 하락'은 딱 5%로 읽힘 → 첫 줄 고침(11자, 합 19자)
TOP = '은마아파트 84㎡ · 실거래 가운데 값'
PILL = None   # copywriter 11/20: 알약 생략(큰 글이 답 숫자를 품음, C-10)


def f(size, w='700'):
    if w == 'black':
        ft = ImageFont.truetype(os.path.join(FONT, 'NotoSansKR-Black.ttf'), size); ft.set_variation_by_name('Black'); return ft
    return ImageFont.truetype(os.path.join(FONT, f'pd{w}.ttf'), size)


def photo(name, y_anchor=0.0, x_anchor=0.5, zoom=1.0):
    im = Image.open(os.path.join(H, name)).convert('RGB'); r = max(W / im.width, HH / im.height) * zoom
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = int((im.width - W) * x_anchor); y = int((im.height - HH) * y_anchor); return im.crop((x, y, x + W, y + HH))


def shade(im, y0, y1, alpha, top=False):
    m = Image.new('L', im.size, 0); d = ImageDraw.Draw(m)
    for y in range(y0, y1):
        t = (y - y0) / max(1, (y1 - y0) * 0.45) if not top else (y1 - y) / max(1, (y1 - y0) * 0.45)
        d.line([(0, y), (W, y)], fill=int(alpha * min(1, t)))
    return Image.composite(Image.new('RGB', im.size, INK), im, m)


def fit(d, t, size, w, maxw, floor=40):
    while size > floor and d.textlength(t, font=f(size, w)) > maxw: size -= 2
    return size


def make(out, pic, ya, xa=0.5, zoom=1.0, band=235, tshade=(380, 210), targets=(0.86, 0.80), ls=1.10, hmax=0.45, top_size=104, sw=6, tsw=5, pk=1.15):
    im = photo(pic, y_anchor=ya, x_anchor=xa, zoom=zoom); d0 = ImageDraw.Draw(im)
    sizes = [fit(d0, t, 320, 'black', maxw=int(W * tg)) for t, tg in zip(BIG, targets)]
    hb = sum(int(s * ls) for s in sizes)
    if hb > HH * hmax: k = HH * hmax / hb; sizes = [int(s * k) for s in sizes]; hb = sum(int(s * ls) for s in sizes)
    y = HH - 30 - hb
    ts = fit(d0, TOP, top_size, '700', maxw=int(W * 0.88))
    im = shade(im, max(0, y - 160), HH, band); im = shade(im, 0, tshade[0], tshade[1], top=True); d = ImageDraw.Draw(im)
    ty = 36
    d.text((X0, ty), TOP, font=f(ts, '700'), fill=WHITE, stroke_width=tsw, stroke_fill=INK); ty += int(ts * 1.30)
    if PILL:
        ps = int(ts * pk); pf = f(ps, '700'); tw = d.textlength(PILL, font=pf); px, py = 28, 12
        d.rounded_rectangle((X0, ty, X0 + tw + 2 * px, ty + ps + 2 * py + 6), radius=(ps + 2 * py) // 2, fill=ORANGE)
        d.text((X0 + px, ty + py - int(ps * 0.08)), PILL, font=pf, fill=WHITE)
    else: ps = 0
    widths = []
    for k, (t, s) in enumerate(zip(BIG, sizes)):
        bb = d.textbbox((X0, y - int(s * 0.12)), t, font=f(s, 'black'), stroke_width=sw); widths.append((bb[2] - bb[0]) / W)
        d.text((X0, y - int(s * 0.12)), t, font=f(s, 'black'), fill=WHITE if k == 0 else ORANGE, stroke_width=sw, stroke_fill=INK); y += int(s * ls)
    sm = im.resize((1280, 720), Image.LANCZOS); sm.save(os.path.join(O, out))
    for p in (412, 168): sm.resize((p, p * 9 // 16), Image.LANCZOS).save(os.path.join(O, out.replace('.png', f'_{p}.png')))
    print(out, f'흰 줄 {ts}px · 알약 {ps}px · 큰 글 {sizes}px · 줄별 폭 ' + '·'.join(f'{w:.0%}' for w in widths) + f' · 높이 {hb / HH:.0%}')



if __name__ == '__main__':
    kw = dict(band=190, tshade=(330, 160), sw=13, tsw=8)
    make('h6_a.png', 'p_3736898.jpg', 0.3, **kw)      # 낡은 판상형 외벽 정면(경쟁 다수가 은마 외벽)
    make('h6_b.png', 'p_41136594.jpg', 0.2, **kw)     # 고층 단지 내려다봄
    make('h6_c.png', 'p_41136598.jpg', 0.0, **kw)     # 아래서 올려다본 고층 아파트(벽 단지 이름 '후곡 906' 보임 → 1안은 nosign)
    # 11/21 짝 비교 c가 a·b 둘 다 2:0 → 1안. 왼쪽 동 벽의 실제 단지 이름('후곡 906')이 은마 영상에 다른 단지로 읽히므로 그 자리만 흐림
    from PIL import ImageFilter
    import numpy as np, cv2   # 글자 화소만 골라 벽으로 메움(cv2.inpaint) — 흐림 상자는 하늘까지 번져 티 남(11/21 첫 시도 버림)
    a = np.array(Image.open(os.path.join(H, 'p_41136598.jpg')).convert('RGB'))[..., ::-1].copy();   # cv2.imread는 한글 경로 못 읽음
    x0, y0, x1, y1 = 420, 590, 600, 800
    g = cv2.cvtColor(a[y0:y1, x0:x1], cv2.COLOR_BGR2HSV); m = np.zeros(a.shape[:2], np.uint8)
    sub = ((g[..., 2] < 150) | ((g[..., 1] > 90) & (g[..., 2] > 60))).astype(np.uint8) * 255   # 어두운 글자·붉은 로고
    m[y0:y1, x0:x1] = cv2.dilate(sub, np.ones((7, 7), np.uint8))
    Image.fromarray(cv2.inpaint(a, m, 9, cv2.INPAINT_TELEA)[..., ::-1]).save(os.path.join(H, 'p_41136598_nosign.jpg'), quality=95)
    make('h6_c2.png', 'p_41136598_nosign.jpg', 0.0, **kw)
    json.dump({
      'p_3736898.jpg': {'site': 'Pexels', 'id': 3736898, 'by': '형길 장', 'url': 'https://www.pexels.com/photo/modern-multistory-building-with-windows-and-balconies-in-city-3736898/', 'license': 'Pexels License', 'face': '없음'},
      'p_41136594.jpg': {'site': 'Pexels', 'id': 41136594, 'by': 'FREE VIDEO HAPPY', 'url': 'https://www.pexels.com/photo/high-rise-apartment-view-in-goyang-si-41136594/', 'license': 'Pexels License', 'face': '없음'},
      'p_41136598.jpg': {'site': 'Pexels', 'id': 41136598, 'by': 'FREE VIDEO HAPPY', 'url': 'https://www.pexels.com/photo/high-rise-residential-apartments-in-goyang-si-41136598/', 'license': 'Pexels License', 'face': '없음'},
    }, open(os.path.join(H, 'sources.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


# 11/22 copywriter 1초 시험 1차: '43억이/34억으로'가 3명 모두 '9억'으로 읽힘(실제 가운데 값 차 8.50억) → BIG만 정밀 숫자로(소수점판은 aitell A31) · TOP·사진 a 그대로
def make_a2():
    global BIG
    BIG = ['같은 평형 42억 8천이', '1년 뒤 34억 3천으로']
    make('h6_a2.png', 'p_3736898.jpg', 0.3, band=190, tshade=(330, 160), sw=13, tsw=8)
