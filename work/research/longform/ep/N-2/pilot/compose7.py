# N-2 시범작 v7 대표 장면 4장 — 무료 사진(Pexels, visual/N-2-pilot/photo/sources.json) 위에 큰 숫자 하나·자막 1줄·출처 줄을 얹는다.
#   py -3.12 compose7.py   → pilot/preview/scene_1~4.png (1920×1080) + 큰 숫자 실제 높이 출력(관문: 화면 높이 25% = 270px 이상)
# 숫자는 n2nums_out.txt [I][J][K]만. 색 4개: 흰·먹 #1B1D22·주황 #FF5A00·원문 노랑 #FFD43B.
import os, sys, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.abspath(os.path.join(H, '..', '..', '..', '..', '..'))
PH = os.path.join(WORK, 'research', 'visual', 'N-2-pilot', 'photo')
FONT = os.path.join(WORK, 'fonts')
OUT = os.path.join(H, 'preview'); os.makedirs(OUT, exist_ok=True)
W, HH = 1920, 1080
INK, ORANGE, YELLOW, WHITE = (27, 29, 34), (255, 90, 0), (255, 212, 59), (255, 255, 255)
SRC = '출처: 국가데이터처 「2024년 임금근로일자리 소득(보수) 결과」(2026-02-23) · 2024년 12월 세전 월 보수 · 일자리 기준'
NET = '통장(실수령): 파이어맵 월급 계산기(2026년 간이세액표·4대보험) · 본인 1명·식대 비과세 20만원 가정 · 10만원 단위 반올림'
REPORT = {}
KEEP = ('thumb_A.png', 'thumb_G.png')   # 미리보기 2안(judge_pilot p12: A 7.5·G 8.5 — E2는 7차 이해 시험에서 '290=평균·연금'으로 읽혀 뺌). 나머지 시안은 visual/N-2-thumb/pilot_alt/
ALT = os.path.join(WORK, 'research', 'visual', 'N-2-thumb', 'pilot_alt'); os.makedirs(ALT, exist_ok=True)
MID = (945, 620)


def f(size, w='700'):
    if w == 'black':
        ft = ImageFont.truetype(os.path.join(FONT, 'NotoSansKR-Black.ttf'), size); ft.set_variation_by_name('Black'); return ft
    return ImageFont.truetype(os.path.join(FONT, f'pd{w}.ttf'), size)


def photo(name, y_anchor=0.5, x_anchor=0.5, dark=1.0):
    im = Image.open(os.path.join(PH, name)).convert('RGB')
    r = max(W / im.width, HH / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = int((im.width - W) * x_anchor); y = int((im.height - HH) * y_anchor)
    im = im.crop((x, y, x + W, y + HH))
    return ImageEnhance.Brightness(im).enhance(dark) if dark != 1.0 else im


def shade(im, box, alpha=170, blur=60):
    """글자 뒤 어둡게: box 영역을 부드럽게 어둡힌다."""
    m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rectangle(box, fill=alpha)
    m = m.filter(ImageFilter.GaussianBlur(blur))
    return Image.composite(Image.new('RGB', im.size, (10, 11, 14)), im, m)


def big(im, x, y, num, unit='', color=ORANGE, size=420, key=''):
    """큰 숫자 하나. 실제 글자 높이(px)를 잰다."""
    d = ImageDraw.Draw(im); fb = f(size, 'black'); fu = f(int(size * 0.34), '700')
    bb = d.textbbox((x, y), num, font=fb)
    d.text((x, y), num, font=fb, fill=color)
    if unit:
        d.text((bb[2] + 16, bb[3]), unit, font=fu, fill=color, anchor='ls')
    REPORT[key] = {'big': num + unit, 'glyph_h': bb[3] - bb[1], 'ratio': round((bb[3] - bb[1]) / HH, 3)}
    return bb


def text(im, xy, s, size=56, color=WHITE, w='700', anchor='la', stroke=0):
    ImageDraw.Draw(im).text(xy, s, font=f(size, w), fill=color, anchor=anchor, stroke_width=stroke, stroke_fill=(0, 0, 0))


def caption(im, s):
    d = ImageDraw.Draw(im, 'RGBA'); ft = f(54); tw = d.textlength(s, font=ft)
    d.rounded_rectangle(((W - tw) / 2 - 36, HH - 168, (W + tw) / 2 + 36, HH - 82), 14, fill=(20, 22, 26, 215))
    d.text((W / 2, HH - 125), s, font=ft, fill=WHITE, anchor='mm')


def src(im, lines):
    d = ImageDraw.Draw(im, 'RGBA'); ft = f(22, '500')
    for i, s in enumerate(lines):
        d.text((48, HH - 58 + i * 28), s, font=ft, fill=(255, 255, 255, 215), stroke_width=2, stroke_fill=(0, 0, 0, 170))


def credit(im, who):
    d = ImageDraw.Draw(im, 'RGBA'); ft = f(20, '500')
    d.text((W - 40, HH - 30), f'사진 {who} / Pexels', font=ft, fill=(255, 255, 255, 200), anchor='rs', stroke_width=2, stroke_fill=(0, 0, 0, 160))


def s1():
    im = photo('pexels_19271539.jpg', y_anchor=0.0)
    im = shade(im, (0, 0, W, 470), alpha=210, blur=70)
    text(im, (110, 50), '직장인을 월급 순서로 한 줄에', 64)
    big(im, 96, 80, '100', '명', key='scene_1')
    caption(im, '내 월급이면 몇 등쯤일까요?')
    src(im, [SRC]); credit(im, 'Huy Phan')
    im.save(os.path.join(OUT, 'scene_1_100명.png'))


def s2():
    im = photo('pexels_761295.jpg', y_anchor=0.0)
    d = ImageDraw.Draw(im, 'RGBA')
    text(im, (W / 2, 52), '100명 줄 한가운데, 50등의 월급(세전)', 58, anchor='mt')
    fb, fu = f(400, 'black'), f(136, '700')
    gw = d.textlength('290', font=fb) + 16 + d.textlength('만원', font=fu)
    y0 = 410 - d.textbbox((0, 0), '290', font=fb)[3]          # 글자 아래 끝을 410px에 — 하늘·사람과 겹치지 않게
    big(im, int((W - gw) / 2) - 140, y0, '290', '만원', size=400, key='scene_2')
    text(im, (W - 70, 400), '통장 약 260만원', 50, anchor='rs')
    d = ImageDraw.Draw(im)
    cx, top = MID   # 줄 한가운데 사람 머리 위 주황 표시
    d.polygon([(cx - 40, top - 80), (cx + 40, top - 80), (cx, top - 16)], fill=ORANGE, outline=WHITE)
    caption(im, '줄 딱 한가운데, 50등은 290만원쯤')
    src(im, [SRC + ' · 가운데(중위) 288만원 · 실수령 2,568,400원', NET]); credit(im, 'Krizjohn Rosales')
    im.save(os.path.join(OUT, 'scene_2_한가운데.png'))


def s3():
    im = photo('pexels_4792290.jpg', y_anchor=0.35)
    im = shade(im, (1160, 0, W, HH), alpha=160, blur=90)
    text(im, (1200, 90), '세전 월 350만원이면', 60)
    text(im, (1200, 166), '100명 중', 60)
    big(im, 1180, 200, '38', '등', key='scene_3')
    text(im, (1200, 790), '통장 약 310만원', 56)
    caption(im, '350만원이면 이제 줄 앞쪽 절반')
    src(im, [SRC + ' · 350만원 이상 38.4% · 실수령 3,066,300원', NET]); credit(im, 'Anete Lusina')
    im.save(os.path.join(OUT, 'scene_3_350만원.png'))


def s4():
    im = photo('pexels_3142002.jpg', y_anchor=0.6)
    im = shade(im, (0, 0, W, 470), alpha=150, blur=70)
    text(im, (110, 70), '월 1,000만원 이상 받는 사람, 100명 중', 60)
    big(im, 96, 110, '4', '명', key='scene_4')
    caption(im, '평균 375만원이 한가운데보다 높은 까닭')
    src(im, [SRC + ' · 1,000만원 이상 4.3% · 평균 375 · 가운데 288']); credit(im, 'Ethan Brooke')
    im.save(os.path.join(OUT, 'scene_4_4명.png'))



def thumb(name, photo_name, y_anchor, lines, marker=None, dark=0.85, shade_box=(0, 0, W, HH)):
    """썸네일 1920×1080으로 그린 뒤 1280×720으로 줄인다. lines = [(글, 크기, 색, 굵기, y)]"""
    im = photo(photo_name, y_anchor=y_anchor, dark=dark)
    im = shade(im, shade_box, alpha=190, blur=80)
    d = ImageDraw.Draw(im)
    for t, size, col, w, y in lines:
        ft = f(size, w) if w != 'black' else f(size, 'black')
        d.text((80, y), t, font=ft, fill=col, stroke_width=6 if size > 150 else 0, stroke_fill=(0, 0, 0))
    if marker:
        cx, top, tag = marker
        d.polygon([(cx - 46, top - 92), (cx + 46, top - 92), (cx, top - 18)], fill=ORANGE, outline=WHITE)
        ft = f(64, '700'); tw = d.textlength(tag, font=ft)
        d.rounded_rectangle((cx - tw / 2 - 26, top - 196, cx + tw / 2 + 26, top - 106), 18, fill=ORANGE)
        d.text((cx, top - 151), tag, font=ft, fill=WHITE, anchor='mm')
    im.resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT if name in KEEP else ALT, name))


def thumb_paper(name):
    """B안 후보: 명세서 든 손(밝은 사진) 오른쪽에 큰 숫자."""
    im = photo('pexels_4792290.jpg', y_anchor=0.35)
    im = shade(im, (1060, 0, W, HH), alpha=185, blur=80)
    d = ImageDraw.Draw(im)
    d.text((1110, 90), '세전 월급', font=f(100, '700'), fill=WHITE)
    d.text((1110, 210), '350만원이면', font=f(100, '700'), fill=WHITE)
    d.text((1090, 330), '38등', font=f(330, 'black'), fill=ORANGE, stroke_width=6, stroke_fill=(0, 0, 0))
    d.text((1110, 760), '100명 중', font=f(90, '700'), fill=WHITE)
    d.rounded_rectangle((60, 880, 1010, 1010), 22, fill=(20, 22, 26, 230))
    d.text((535, 945), '평균보다 적은데 앞쪽?', font=f(76, '700'), fill=YELLOW, anchor='mm')
    im.resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT if name in KEEP else ALT, name))


def thumbs():
    thumb('thumb_A.png', 'pexels_761295.jpg', 0.0,
          [('직장인 100명 줄 세우면', 96, WHITE, '700', 50), ('내 월급 몇 등?', 230, ORANGE, 'black', 135)],
          marker=(945, 640, '100명 중 50등 = 세전 290만원'), dark=1.0, shade_box=(0, 0, 0, 0))
    thumb('thumb_B.png', 'pexels_19271539.jpg', 0.0,
          [('세전 월급 350만원이면', 104, WHITE, '700', 70), ('100명 중', 104, WHITE, '700', 195), ('38등', 300, ORANGE, 'black', 275), ('평균보다 적어도 앞쪽', 84, WHITE, '700', 690)],
          dark=0.9, shade_box=(0, 0, 1150, HH))
    thumb_paper('thumb_C.png')
    # E: 평균과 보통(한가운데)이 다르다
    thumb('thumb_E.png', 'pexels_19271539.jpg', 0.0,
          [('평균 월급 375만원?', 110, WHITE, '700', 70), ('보통 사람은', 110, WHITE, '700', 210), ('290만원', 270, ORANGE, 'black', 320),
           ('세전 · 직장인 100명 줄 세워 보니', 76, YELLOW, '700', 680)],
          dark=0.85, shade_box=(0, 0, 1250, HH))
    # E2: E에서 375를 작게(내 월급으로 오독 위험 — p10 심사), '딱 한가운데' 말로
    thumb('thumb_E2.png', 'pexels_19271539.jpg', 0.0,
          [('뉴스 속 평균(375만원) 말고', 76, (200, 200, 200), '700', 80), ('직장인 100명 중 딱 한가운데', 100, WHITE, '700', 180),
           ('290만원', 290, ORANGE, 'black', 300), ('세전 월급 · 2024년 12월', 70, YELLOW, '700', 690)],
          dark=0.85, shade_box=(0, 0, 1350, HH))
    # G: 계단 셋(세전 월급 → 등수) — 7차 이해 시험에서 E2가 '290=평균·연금'으로 읽혀 교체
    im = photo('pexels_19271539.jpg', y_anchor=0.0, dark=0.85)
    im = shade(im, (0, 0, 1300, HH), alpha=200, blur=80); d = ImageDraw.Draw(im)
    d.text((80, 60), '내 월급, 100명 중 몇 등?', font=f(120, 'black'), fill=WHITE, stroke_width=4, stroke_fill=(0, 0, 0))
    for i, (m, r) in enumerate([('세전 450만원', '27등'), ('세전 290만원', '50등'), ('세전 150만원', '79등')]):
        y = 300 + i * 230
        d.text((90, y + 40), m, font=f(96, '700'), fill=WHITE)
        d.text((720, y), r, font=f(190, 'black'), fill=ORANGE, stroke_width=5, stroke_fill=(0, 0, 0))
    im.resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT if 'thumb_G.png' in KEEP else ALT, 'thumb_G.png'))
    # F: 맨 앞 네 명
    thumb('thumb_F.png', 'pexels_3142002.jpg', 0.6,
          [('월급 1,000만원 이상 받는 사람', 96, WHITE, '700', 70), ('100명 중', 104, WHITE, '700', 200), ('4명', 330, ORANGE, 'black', 280),
           ('내 월급은 몇 등?', 84, YELLOW, '700', 730)],
          dark=0.9, shade_box=(0, 0, 1100, HH))


for fn in (s1, s2, s3, s4, thumbs): fn()
for k, v in REPORT.items(): print(k, v, '통과' if v['glyph_h'] >= 270 else '미달')
json.dump(REPORT, open(os.path.join(OUT, 'scene_bignum.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def compare():
    """N-1 같은 내용 장면(가운데 vs 평균, 1:10 캡처 src/n1_0070.jpg) ↔ 시범작 scene_2. 분석 캡처는 우리 N-1만."""
    bd = Image.new('RGB', (W, HH), (244, 241, 234)); d = ImageDraw.Draw(bd)
    d.text((W / 2, 50), '같은 내용 — "줄 한가운데 사람의 월급"', font=f(56), fill=INK, anchor='mt')
    d.text((W / 2, 116), '자료: N-1 국세청 연봉 천분위 · 시범작 국가데이터처 월급 분포', font=f(26, '500'), fill=(110, 112, 118), anchor='mt')
    left = Image.open(os.path.join(H, 'src', 'n1_0070.jpg')).convert('RGB').resize((900, 506), Image.LANCZOS)
    right = Image.open(os.path.join(OUT, 'scene_2_한가운데.png')).convert('RGB').resize((900, 506), Image.LANCZOS)
    bd.paste(left, (40, 190)); bd.paste(right, (980, 190))
    d.rectangle((40, 190, 940, 696), outline=(150, 150, 150), width=3); d.rectangle((980, 190, 1880, 696), outline=ORANGE, width=6)
    d.text((40, 140), '전: N-1 (1:10)', font=f(44), fill=(110, 112, 118))
    d.text((980, 140), '후: N-2 시범작', font=f(44), fill=ORANGE)
    rows = [('한 화면 숫자', '9개', '큰 숫자 1개 + 통장 1줄'),
            ('큰 숫자 높이', '화면의 약 4%', '화면의 약 29%'),
            ('사람·장소', '없음(흰 바탕 막대)', '줄 선 사람들 사진(Pexels)'),
            ('설명 말', "'가운데 칸 3,417만원'", "'100명 중 딱 한가운데, 50등'"),
            ('아래 자막', '3줄', '1줄')]
    y = 730
    for k, a, b in rows:
        d.text((40, y), k, font=f(34, '500'), fill=(110, 112, 118))
        d.text((300, y), a, font=f(36), fill=INK)
        d.text((980, y), b, font=f(36), fill=ORANGE)
        y += 62
    bd.save(os.path.join(OUT, 'compare_N1_vs_N2.png'))


compare()


SUMMARY = [
    ('0', '직장인 전체를 100명으로 줄여 월급 순서로 세운다. 1등이 가장 많이 받고, 맨 뒤에서 앞으로 걸어간다'),
    ('1', '국가데이터처(옛 통계청) 2024년 12월 세전 월급. 세전을 모르면 통장 금액에 1할쯤 더한다(통장 200 → 세전 약 220)'),
    ('2', '세전 150만원이면 79등, 줄 뒤쪽 (통장 약 140은 화면에만)'),
    ('3', '세전 250만원이면 59등. 그 사이 월급이면 등수도 그 사이'),
    ('4', '딱 한가운데 50등은 세전 290만원'),
    ('5', '세전 350만원이면 38등, 줄 앞쪽 절반'),
    ('6', '세전 450만원이면 27등, 꽤 앞쪽'),
    ('6-2', '세전 650만원이면 14등'),
    ('7', '1,000만원 넘게 받는 사람은 100명 중 4명. 큰 돈이 더해져 평균(375만원)이 한가운데보다 높다'),
    ('8', '내 자리는 평균 말고 한가운데(세전 290·통장 260)와 견준다. 나이별 줄은 댓글 맨 위에'),
]


def summary():
    """대본 요약(장마다 한 줄) — 미리보기 폴더용 그림 + 같은 글 txt."""
    bd = Image.new('RGB', (W, HH), (244, 241, 234)); d = ImageDraw.Draw(bd)
    d.text((80, 60), 'N-2 시범작 대본 요약 — "내 월급, 직장인 100명 줄 세우면 몇 등?"', font=f(52), fill=INK)
    d.text((80, 135), '낮은 월급 → 높은 월급, 한 방향 · 약 2분 45초(어림) · 말로는 세전과 등수만, 통장 금액은 화면 · 숫자: 국가데이터처 / 통장 = 파이어맵 계산기', font=f(28, '500'), fill=(110, 112, 118))
    y = 210
    for k, t in SUMMARY:
        d.rounded_rectangle((80, y, 180, y + 64), 14, fill=ORANGE)
        d.text((130, y + 32), k, font=f(34), fill=WHITE, anchor='mm')
        d.text((210, y + 10), t, font=f(38, '500'), fill=INK)
        y += 84
    bd.save(os.path.join(OUT, 'script_summary.png'))
    open(os.path.join(OUT, 'script_summary.txt'), 'w', encoding='utf-8').write(
        'N-2 시범작 대본 요약(장마다 한 줄) — 전문은 ../script.md\n' + '\n'.join(f'{k}장: {t}' for k, t in SUMMARY) + '\n')


summary()
