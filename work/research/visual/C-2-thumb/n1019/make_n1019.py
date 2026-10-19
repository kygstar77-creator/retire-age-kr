# C-2 새 썸네일 2안(10/19, 사장님 "두 번째(N-2 thumb_A) 게 좋네. 첫 번째는 클로드 디자인 티 난다") — N-2 pilot/compose7.py thumb() 꼴 그대로.
#   꽉 찬 실사 1장 + 글자 3층(작은 흰 줄 1 · 큰 주황 · 주황 알약 1). 머리띠·꼬리표·날짜·카드 상자·출처 줄 없음.
#   숫자는 ep/C-2/calc_n1_out.txt만: 1998년 1월 시작 → 2011년 바닥(35행), 2003년 1월 시작 → 2025년 말 2.72억(52행), 3억·월 200만원.
#   py -3.12 make_n1019.py → ep/C-2/thumb_n1a.png, thumb_n1b.png (1280×720)
import os, sys, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(H, '..', '..', '..', '..'))
PH = os.path.join(H, 'photo'); FONT = os.path.join(WORK, 'fonts')
EP = os.path.join(WORK, 'research', 'longform', 'ep', 'C-2')
W, HH = 1920, 1080
ORANGE, WHITE = (255, 90, 0), (255, 255, 255)


def f(size, w='700'):
    if w == 'black':
        ft = ImageFont.truetype(os.path.join(FONT, 'NotoSansKR-Black.ttf'), size); ft.set_variation_by_name('Black'); return ft
    return ImageFont.truetype(os.path.join(FONT, f'pd{w}.ttf'), size)


def photo(name, y_anchor=0.5, x_anchor=0.5, dark=1.0, flip=False, zoom=1.0):
    im = Image.open(os.path.join(PH, name)).convert('RGB')
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    r = max(W / im.width, HH / im.height) * zoom
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = int((im.width - W) * x_anchor); y = int((im.height - HH) * y_anchor)
    im = im.crop((x, y, x + W, y + HH))
    return ImageEnhance.Brightness(im).enhance(dark) if dark != 1.0 else im


def shade_top(im, h, alpha=225):
    """위쪽 h 높이를 위→아래로 옅어지게 어둡힌다(글자 바탕, 상자 아님)."""
    m = Image.new('L', im.size, 0); d = ImageDraw.Draw(m)
    for y in range(h):
        d.line([(0, y), (W, y)], fill=int(alpha * min(1, (h - y) / (h * 0.45))))
    return Image.composite(Image.new('RGB', im.size, (10, 11, 14)), im, m)


def thumb(name, photo_name, lines, pill, y_anchor=0.5, x_anchor=0.5, dark=1.0, shade_h=640, flip=False, zoom=1.0):
    im = photo(photo_name, y_anchor, x_anchor, dark, flip, zoom)
    im = shade_top(im, shade_h)
    d = ImageDraw.Draw(im)
    for t, size, col, w, y in lines:
        d.text((80, y), t, font=f(size, w), fill=col, stroke_width=6 if size > 150 else 0, stroke_fill=(0, 0, 0))
    tag, py = pill
    ft = f(64, '700'); tw = d.textlength(tag, font=ft)
    d.rounded_rectangle((80, py, 80 + tw + 52, py + 90), 18, fill=ORANGE)
    d.text((80 + 26, py + 45), tag, font=ft, fill=WHITE, anchor='lm')
    out = os.path.join(EP, name); im.resize((1280, 720), Image.LANCZOS).save(out); print(out)


# A: 빈 지갑(손만) — 답을 바로 보여 주는 판
thumb('thumb_n1a.png', 'empty_wallet_4_12001949_2x.jpg',
      [('같은 퇴직금 3억, 시작한 해만 달랐다', 90, WHITE, '700', 50),
       ('1998년 시작', 210, ORANGE, 'black', 140),
       ('2011년 돈 바닥', 210, ORANGE, 'black', 370)],
      ('2003년 시작은 2025년 말 2억 7천 남음', 650), y_anchor=0.6, x_anchor=0.0, zoom=1.5, dark=1.0, shade_h=760)

# B: 바닷가 벤치 은퇴자 뒷모습 — thumb_A처럼 물음 + 알약이 답
thumb('thumb_n1b.png', 'old_man_bench_back_6_19089255_2x.jpg',
      [('S&P500에 퇴직금 3억, 매달 200만원', 90, WHITE, '700', 40),
       ('몇 년 버틸까?', 215, ORANGE, 'black', 110)],
      ('1998년 시작하면 2011년 돈 바닥', 400), y_anchor=1.0, dark=0.95, shade_h=640)

json.dump({
    'empty_wallet_4_12001949_2x.jpg': {'site': 'Pexels', 'id': 12001949, 'by': 'Towfiqu barbhuiya', 'url': 'https://www.pexels.com/photo/a-person-holding-an-empty-wallet-12001949/', 'license': 'Pexels License(무료·상업 이용 가능·출처 표기 의무 없음)', 'face': '없음(손만)'},
    'old_man_bench_back_6_19089255_2x.jpg': {'site': 'Pexels', 'id': 19089255, 'by': 'Osman Karagöz', 'url': 'https://www.pexels.com/photo/elderly-man-resting-on-bench-by-ocean-19089255/', 'license': 'Pexels License(무료·상업 이용 가능·출처 표기 의무 없음)', 'face': '없음(뒷모습)'},
}, open(os.path.join(PH, 'sources.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
