# N-2 시범작 대표 장면 합성 — 생성 그림(visual/N-2-pilot/*.png) 위에 큰 숫자·자막 1줄·'가상 인물' 표시를 얹어 1920×1080 PNG로.
#   py -3.12 compose.py            → pilot/scene_*.png, pilot/thumb_*.png (그림이 없는 칸은 건너뜀)
# 디자인 규칙(scenes.md): 숫자 최대 2개·큰 숫자 높이 ≥216px·자막 1줄 54px·색 4개(흰·먹 #1B1D22·주황 #FF5A00·원문 노랑 #FFD43B)
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(H, '..', '..', '..', '..', '..'))
ART = os.path.join(ROOT, 'research', 'visual', 'N-2-pilot')
FONT = os.path.join(ROOT, 'fonts')
W, HH = 1920, 1080
INK, ORANGE, YELLOW, WHITE = (27, 29, 34), (255, 90, 0), (255, 212, 59), (255, 255, 255)

def f(size, w='700'):
    if w == 'black':
        ft = ImageFont.truetype(os.path.join(FONT, 'NotoSansKR-Black.ttf'), size)
        ft.set_variation_by_name('Black')   # 가변 글꼴 — 지정 안 하면 Thin으로 그려진다(10/15 확인)
        return ft
    return ImageFont.truetype(os.path.join(FONT, f'pd{w}.ttf'), size)

def base(name):
    p = os.path.join(ART, name + '.png')
    if not os.path.exists(p): return None
    im = Image.open(p).convert('RGB')
    r = max(W / im.width, HH / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - HH) // 2
    return im.crop((x, y, x + W, y + HH))

def caption(im, text):
    d = ImageDraw.Draw(im, 'RGBA'); ft = f(54)
    tw = d.textlength(text, font=ft)
    d.rounded_rectangle(((W - tw) / 2 - 36, HH - 150, (W + tw) / 2 + 36, HH - 62), 14, fill=(20, 22, 26, 215))
    d.text((W / 2, HH - 106), text, font=ft, fill=WHITE, anchor='mm')

def card(im, x, y, small, big, unit='', sub='', accent=ORANGE, w=None):
    """흰 카드: 작은 머리말 1줄 + 큰 숫자(높이 ≥216px 글자) + 작은 정확값 줄."""
    d = ImageDraw.Draw(im, 'RGBA')
    fb, fs, fu, fsub = f(230, 'black'), f(46), f(80, '700'), f(36, '500')
    bw = d.textlength(big, font=fb) + (d.textlength(unit, font=fu) + 10 if unit else 0)
    w = w or max(bw, d.textlength(small, font=fs)) + 100
    h = 420 if sub else 370
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle((x + 8, y + 14, x + w + 8, y + h + 14), 28, fill=(0, 0, 0, 70))
    im.paste(Image.alpha_composite(im.convert('RGBA'), sh.filter(ImageFilter.GaussianBlur(14))).convert('RGB'))
    d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle((x, y, x + w, y + h), 28, fill=(255, 255, 255, 245))
    d.text((x + 50, y + 40), small, font=fs, fill=INK)
    d.text((x + 44, y + 92), big, font=fb, fill=accent)
    if unit: d.text((x + 50 + d.textlength(big, font=fb), y + 225), unit, font=fu, fill=accent)
    if sub: d.text((x + 50, y + 350), sub, font=fsub, fill=(110, 112, 118))
    return w

def stamp(im, text='가상 인물', big=True):
    d = ImageDraw.Draw(im, 'RGBA'); ft = f(44 if big else 30)
    tw = d.textlength(text, font=ft); x, y = (60, 56) if big else (W - tw - 80, HH - 56)
    d.rounded_rectangle((x - 22, y - 14, x + tw + 22, y + (62 if big else 44)), 12, outline=ORANGE, width=5 if big else 3, fill=(255, 255, 255, 230))
    d.text((x, y - 4), text, font=ft, fill=ORANGE)

def src(im, text):
    d = ImageDraw.Draw(im, 'RGBA'); ft = f(28, '500')
    d.text((60, HH - 44), text, font=ft, fill=(255, 255, 255, 230), stroke_width=3, stroke_fill=(0, 0, 0, 160))

def bubble(im, x, y, text):
    d = ImageDraw.Draw(im, 'RGBA'); ft = f(50)
    lines = text.split('\n'); tw = max(d.textlength(l, font=ft) for l in lines); th = 74 * len(lines)
    d.rounded_rectangle((x, y, x + tw + 80, y + th + 50), 36, fill=(255, 255, 255, 245))
    d.polygon([(x + tw + 20, y + th + 48), (x + tw + 90, y + th + 110), (x + tw - 30, y + th + 48)], fill=(255, 255, 255, 245))
    for i, l in enumerate(lines): d.text((x + 40, y + 25 + 74 * i), l, font=ft, fill=INK)

SRC = '국가데이터처 「2024년 임금근로일자리 소득(보수) 결과」 표7 · 2024년 12월 세전 월 보수'

def s1():
    im = base('s1')
    if im is None: return
    card(im, 70, 150, '상호 씨 월급(세전)', '350', '만원')
    card(im, 70, 560, '또래 평균 월급', '약 420', '만원', accent=INK)
    stamp(im, '가상 인물', big=False); caption(im, '평균보다 70만원 넘게 적습니다'); src(im, SRC + ' · 55~59세 평균 424만원')
    im.save(os.path.join(H, 'scene_1_lunch.png'))

def s2():
    im = base('s2')
    if im is None: return
    stamp(im); caption(im, '쉰일곱 상호 씨, 작은 부품 공장 22년째')
    im.save(os.path.join(H, 'scene_2_desk.png'))

def s3():
    im = base('s3')
    if im is None: return
    d = ImageDraw.Draw(im, 'RGBA')
    d.rounded_rectangle((560, 40, 1360, 330), 30, fill=(255, 255, 255, 240))
    d.text((960, 100), '같은 나이 100명 중', font=f(60), fill=INK, anchor='mm')
    d.text((960, 225), '40등', font=f(190, 'black'), fill=ORANGE, anchor='mm')
    stamp(im, '가상 인물', big=False); caption(im, '평균보다 적어도, 줄에서는 앞쪽 절반'); src(im, SRC + ' · 55~59세 월 350만원 이상 39.9%')
    im.save(os.path.join(H, 'scene_3_line.png'))

def s4():
    im = base('s4')
    if im is None: return
    bubble(im, 90, 140, '"평균보다 적다길래 철렁했는데,\n같은 나이 줄에선 앞에서 40등쯤이더라."')
    stamp(im, '가상 인물', big=False); caption(im, '내 자리는 평균 말고, 내 나이 한가운데와 견준다')
    im.save(os.path.join(H, 'scene_4_dinner.png'))

def s_src():
    """원문 화면: 표7 2024년 블록을 그대로 보여 주고 55~59세 열 350만원 위 6칸을 칠한다(PDF 23쪽 렌더 pilot/src/wagejob_p29.png)."""
    pg = Image.open(os.path.join(H, 'src', 'wagejob_p29.png')).convert('RGB')
    k = 1.05  # 표시 좌표 → 원본 좌표
    crop = pg.crop((int(135 * k), int(215 * k), int(1280 * k), int(1105 * k)))
    d = ImageDraw.Draw(crop, 'RGBA')
    cx0, cx1 = int((993 - 135) * k), int((1063 - 135) * k)          # 55~59세 열
    for top in [673, 727, 781, 835, 889, 943]:                        # 350~450 … 1,000 이상 행
        d.rectangle((cx0, int((top - 215) * k), cx1, int((top + 52 - 215) * k)), fill=(255, 90, 0, 90), outline=ORANGE, width=3)
    d.rectangle((cx0 - 4, int((215 - 215) * k), cx1 + 4, int((1100 - 215) * k)), outline=ORANGE, width=6)
    im = Image.new('RGB', (W, HH), (244, 241, 234))
    r = 960 / crop.height; crop = crop.resize((int(crop.width * r), 960), Image.LANCZOS)
    im.paste(crop, (50, 60))
    d = ImageDraw.Draw(im)
    x = 50 + crop.width + 60
    d.text((x, 150), '55~59세 100명 중', font=f(54), fill=INK)
    d.text((x, 225), '350만원 이상은', font=f(54), fill=INK)
    d.text((x - 6, 290), '40명', font=f(220, 'black'), fill=ORANGE)
    d.text((x, 700), '8.8+6.4+4.5+6.9+6.1+7.2', font=f(34, '500'), fill=(90, 92, 98))
    d.text((x, 748), '= 39.9%', font=f(34, '500'), fill=(90, 92, 98))
    d.text((x, 900), '원문 23쪽 표7', font=f(34, '500'), fill=(90, 92, 98))
    d.text((x, 945), '국가데이터처 2026-02-23', font=f(30, '500'), fill=(90, 92, 98))
    im.save(os.path.join(H, 'scene_5_source.png'))

def thumb(name, imgname, lines, out):
    im = base(imgname)
    if im is None: return
    d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle((0, 0, 1010, HH), fill=(255, 255, 255, 232))
    y = 110
    for txt, size, col in lines:
        ft = f(size, 'black'); d.text((70, y), txt, font=ft, fill=col); y += int(size * 1.22)
    stamp(im, '가상 인물', big=False)
    im.save(os.path.join(H, out))

def compare():
    """N-1(실제 공개본 10초 칸 4장) vs 시범작 대표 장면 4장을 나란히 한 장으로 → pilot_vs_n1.png"""
    L = [os.path.join(H, 'src', f'n1_{t}.jpg') for t in ('0010', '0070', '0130', '0250')]
    R = [os.path.join(H, n) for n in ('scene_1_lunch.png', 'scene_5_source.png', 'scene_3_line.png', 'scene_4_dinner.png')]
    if not all(os.path.exists(x) for x in R): print('compare: 장면 없음'); return
    cw, ch = 900, 506
    im = Image.new('RGB', (cw * 2 + 90, 150 + (ch + 30) * 4), (244, 241, 234)); d = ImageDraw.Draw(im)
    d.text((30, 40), 'N-1 실제 공개본 (2,742회) — 10초 칸 38개 중 사람·장소 0', font=f(36), fill=INK)
    d.text((cw + 60, 40), 'N-2 시범작 — 상호 씨 한 사람 · 원문 표 · 숫자 하나 크게', font=f(36), fill=ORANGE)
    for i, (a, b) in enumerate(zip(L, R)):
        y = 120 + i * (ch + 30)
        im.paste(Image.open(a).convert('RGB').resize((cw, ch), Image.LANCZOS), (30, y))
        im.paste(Image.open(b).convert('RGB').resize((cw, ch), Image.LANCZOS), (cw + 60, y))
    im.save(os.path.join(H, 'pilot_vs_n1.png'))

if __name__ == '__main__':
    s_src(); s1(); s2(); s3(); s4()
    thumb('A', 'th', [('쉰일곱, 월급 350', 120, INK), ('평균보다 적은데', 120, INK), ('같은 나이', 150, INK), ('100명 중 40등', 150, ORANGE)], 'thumb_A.png')
    thumb('B', 's3', [('평균 월급 420', 130, INK), ('가운데 사람은', 130, INK), ('290', 300, ORANGE)], 'thumb_B.png')
    compare()
    print('done', [p for p in os.listdir(H) if p.endswith('.png')])
