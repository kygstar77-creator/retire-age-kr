# 채널 색깔 안 1·2·3 견본(쇼츠 1장 + 롱폼 썸네일 1장씩) — 2026-10-17 채널 전략가
#   py -3.12 work/research/strategy/identity-1017/make_samples.py
# 숫자는 전부 이미 공개된 편의 사실표·설명란에서 그대로 가져왔다(새로 계산한 숫자 0).
#   안1: W-1 0yWQeW38UJE · 쇼츠 DRtKbSuCUiQ 설명란(코스피 1천만원 −539,440원, 삼성전자 100주 2,760만→2,620만)
#   안2: R-1 G1oI47miUuo 썸네일 r4a(예금 1억 218만 · SCHD 1억 1,599만) · 쇼츠 r1s_fx 설명란(1억 → −3,300,142원)
#   안3: P-1 vsL7mojDW7w calc_out.txt(5년 당김 76.67세 · 1년 당김 80.67세, 1969년생·제때 월 100만원 가정)
# 색은 디자인 정체성 4색(배경 #f6f7f9·카드 #fff·잉크 #18191d·주황 #ff5a00) + 다크 #101114, 주황은 핵심 숫자 하나에만.
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, '..', '..', '..', 'fonts')
BG, CARD, INK, OR, DARK, GRAY, LINE = '#f6f7f9', '#ffffff', '#18191d', '#ff5a00', '#101114', '#6b7280', '#d9dce1'


def bh(size):
    return ImageFont.truetype(os.path.join(FONTS, 'BlackHanSans.ttf'), size)


def pd(size, w=700):
    f = ImageFont.truetype(os.path.join(FONTS, 'pd700.ttf'), size)
    try:
        f.set_variation_by_axes([w])
    except Exception:
        pass
    return f


def text(d, xy, s, font, fill, anchor='la'):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


def runs(d, x, y, parts, anchor_baseline=True):
    """[(글자, 글꼴, 색)…]을 한 줄로 이어 쓴다. y는 글자 밑선."""
    for s, f, c in parts:
        d.text((x, y), s, font=f, fill=c, anchor='ls')
        x += d.textlength(s, font=f)
    return x


def width(d, parts):
    return sum(d.textlength(s, font=f) for s, f, _ in parts)


def sample_tag(d, W, H, dark=False):
    s = '견본 · 숫자는 공개된 편 그대로'
    f = pd(22, 500)
    text(d, (W - 18, H - 14), s, f, '#9aa0a8' if not dark else '#6b7280', 'rs')


# ───────────────── 안 1: 파이어맵 영수증 (요일 편성 매체형) ─────────────────
def masthead(d, W, h, corner, date):
    d.rectangle([0, 0, W, h], fill=INK)
    text(d, (40, h // 2), '파이어맵 영수증', bh(int(h * 0.46)), '#ffffff', 'lm')
    x = 40 + d.textlength('파이어맵 영수증', font=bh(int(h * 0.46))) + 22
    d.rounded_rectangle([x, h // 2 - int(h * 0.24), x + d.textlength(corner, font=pd(int(h * 0.3))) + 36, h // 2 + int(h * 0.24)], radius=12, fill=OR)
    text(d, (x + 18, h // 2), corner, pd(int(h * 0.3)), '#ffffff', 'lm')
    text(d, (W - 40, h // 2), date, pd(int(h * 0.28), 500), '#b8bcc4', 'rm')


def perforation(d, x0, x1, y):
    for x in range(x0, x1, 22):
        d.line([x, y, x + 11, y], fill=LINE, width=3)


def a1_thumb():
    W, H = 1280, 720
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    masthead(d, W, 104, '토요일 주간', '10월 5~9일 주')
    d.rounded_rectangle([40, 140, W - 40, H - 46], radius=20, fill=CARD)
    text(d, (84, 236), '107조 실적 낸 주,', bh(84), INK, 'ls')
    runs(d, 84, 380, [('내 100주 ', bh(96), INK), ('-140만원', bh(132), OR)])
    perforation(d, 84, W - 84, 440)
    text(d, (84, 512), '삼성전자 100주 평가액', pd(34, 500), GRAY, 'ls')
    runs(d, 84, 580, [('2,760만원', pd(46), INK), ('  →  ', pd(40, 500), GRAY), ('2,620만원', pd(46), INK)])
    text(d, (W - 84, 580), '종가 10/2 → 10/8', pd(30, 500), GRAY, 'rs')
    sample_tag(d, W, H)
    im.save(os.path.join(HERE, 'a1_thumb.png'))


def a1_short():
    W, H = 1080, 1920
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    masthead(d, W, 150, '토요일 주간', '10/5~10/9')
    text(d, (W // 2, 330), '코스피 1천만원,', bh(104), INK, 'ms')
    runs(d, (W - width(d, [('지난주 ', bh(104), INK), ('사흘', bh(104), OR), (' 장에 얼마?', bh(104), INK)])) // 2, 470,
         [('지난주 ', bh(104), INK), ('사흘', bh(104), OR), (' 장에 얼마?', bh(104), INK)])
    d.rounded_rectangle([60, 560, W - 60, 1180], radius=28, fill=CARD)
    text(d, (110, 660), '영수증', pd(40), GRAY, 'ls')
    text(d, (W - 110, 660), '종가 10/2 → 10/8', pd(36, 500), GRAY, 'rs')
    perforation(d, 110, W - 110, 700)
    text(d, (110, 790), '코스피를 그대로 따라간 1천만원', pd(42, 600), INK, 'ls')
    text(d, (110, 980), '-54만원', bh(190), OR, 'ls')
    text(d, (110, 1060), '−539,440원 · −5.39%', pd(44, 600), GRAY, 'ls')
    perforation(d, 110, W - 110, 1110)
    text(d, (110, 1160), '같은 주 삼성전자 100주 −140만원(−5.07%)', pd(36, 500), GRAY, 'ls')
    # 다음 편 예고 줄 = 매체형 '맺는 말'을 화면에도
    d.rounded_rectangle([60, 1300, W - 60, 1480], radius=24, fill=DARK)
    text(d, (W // 2, 1370), '이번 주 영수증 다음 회', pd(40, 500), '#b8bcc4', 'ms')
    text(d, (W // 2, 1440), '다음 주 토요일 11:30', pd(52), '#ffffff', 'ms')
    text(d, (W // 2, 1600), '한국은행 ECOS 코스피 종가 · 지나간 값', pd(32, 500), GRAY, 'ms')
    sample_tag(d, W, H)
    im.save(os.path.join(HERE, 'a1_short.png'))


# ───────────────── 안 2: 1억 실험 (한 가지 꼴 반복) ─────────────────
def badge(d, x, y, s, size):
    f = pd(size)
    w = d.textlength(s, font=f)
    d.rounded_rectangle([x, y, x + w + size * 1.2, y + size * 1.7], radius=size * 0.85, fill=OR)
    text(d, (x + size * 0.6, y + size * 0.85), s, f, '#ffffff', 'lm')
    return x + w + size * 1.2


def a2_thumb():
    W, H = 1280, 720
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    badge(d, 40, 34, '1억 실험 #12', 34)
    text(d, (W - 40, 70), '세금·환율 떼고 1년 뒤', pd(34, 600), GRAY, 'rm')
    text(d, (40, 210), '작년에 1억 넣었다면?', bh(104), INK, 'ls')
    for i, (lab, big, col, dark) in enumerate([('예금', '1억 218만', INK, False), ('SCHD', '1억 1,599만', OR, True)]):
        x0 = 40 + i * 610
        d.rounded_rectangle([x0, 262, x0 + 590, 650], radius=20, fill=DARK if dark else CARD)
        text(d, (x0 + 295, 350), lab, bh(64), '#ffffff' if dark else '#4b5563', 'ms')
        text(d, (x0 + 295, 540), big, bh(92), col if dark else INK, 'ms')
    sample_tag(d, W, H)
    im.save(os.path.join(HERE, 'a2_thumb.png'))


def a2_short():
    W, H = 1080, 1920
    im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
    badge(d, 60, 70, '1억 실험 #12', 44)
    text(d, (W - 60, 112), '1년 뒤 통장', pd(40, 600), GRAY, 'rm')
    text(d, (W // 2, 340), '달러로 산 미국 ETF,', bh(100), INK, 'ms')
    text(d, (W // 2, 470), '환율만 따로 떼면?', bh(100), INK, 'ms')
    d.rounded_rectangle([60, 560, W - 60, 1140], radius=28, fill=CARD)
    text(d, (110, 660), '1억어치 · 1년 들고 있었다면', pd(42, 600), INK, 'ls')
    text(d, (110, 880), '-330만원', bh(200), OR, 'ls')
    text(d, (110, 960), '환율만으로 3,300,142원', pd(44, 600), GRAY, 'ls')
    perforation(d, 110, W - 110, 1010)
    text(d, (110, 1080), '원/달러 1,406.0 → 1,359.6원 (−3.30%)', pd(38, 500), GRAY, 'ls')
    d.rounded_rectangle([60, 1240, W - 60, 1420], radius=24, fill=DARK)
    text(d, (W // 2, 1310), '본편', pd(40, 500), '#b8bcc4', 'ms')
    text(d, (W // 2, 1380), '예금·S&P500·SCHD·금 1억씩', pd(50), '#ffffff', 'ms')
    text(d, (W // 2, 1560), '한국은행 ECOS 매매기준율 2025.10.2 → 2026.10.2', pd(30, 500), GRAY, 'ms')
    sample_tag(d, W, H)
    im.save(os.path.join(HERE, 'a2_short.png'))


# ───────────────── 안 3: 몇 살 계산 (나이 눈금자가 고정 출연) ─────────────────
def ruler(d, x0, x1, y, a0, a1, marks, dark=True, big=56, small=30):
    col = '#3a3d46' if dark else LINE
    d.line([x0, y, x1, y], fill=col, width=8)
    pos = lambda a: x0 + (x1 - x0) * (a - a0) / (a1 - a0)
    for a in range(a0, a1 + 1, 5):
        d.line([pos(a), y - 14, pos(a), y + 14], fill=col, width=4)
        text(d, (pos(a), y + 54), f'{a}', pd(small, 500), '#7c818c', 'ms')
    for k, (a, lab, c) in enumerate(marks):
        x = pos(a)
        anc = 'ms' if len(marks) == 1 else ('rs' if k == 0 else 'ls')
        dx = 0 if anc == 'ms' else (-10 if anc == 'rs' else 10)
        d.ellipse([x - 18, y - 18, x + 18, y + 18], fill=c)
        if big:
            text(d, (x + dx, y - 40), f'{a}세', bh(big), c, anc)
            text(d, (x + dx, y - 40 - big - 6), lab, pd(int(big * 0.5)), '#c7cad1' if dark else GRAY, anc)


def a3_thumb():
    W, H = 1280, 720
    im = Image.new('RGB', (W, H), DARK); d = ImageDraw.Draw(im)
    text(d, (40, 70), '몇 살 계산', pd(36), OR, 'lm')
    text(d, (40, 200), '국민연금 당겨 받으면', bh(92), '#ffffff', 'ls')
    text(d, (40, 310), '몇 살부터 뒤집히나', bh(92), '#ffffff', 'ls')
    ruler(d, 80, W - 80, 560, 60, 90, [(76.7, '5년 당김', '#ffffff'), (80.7, '1년 당김', OR)], big=72)
    text(d, (40, H - 24), '1969년생 · 제때 65세 월 100만원 가정 · 받은 합계가 같아지는 나이', pd(24, 500), '#7c818c', 'ls')
    sample_tag(d, W, H, dark=True)
    im.save(os.path.join(HERE, 'a3_thumb.png'))


def a3_short():
    W, H = 1080, 1920
    im = Image.new('RGB', (W, H), DARK); d = ImageDraw.Draw(im)
    text(d, (60, 110), '몇 살 계산', pd(48), OR, 'lm')
    text(d, (W // 2, 330), '국민연금, 1년만', bh(104), '#ffffff', 'ms')
    text(d, (W // 2, 470), '당겨 받아도 손해?', bh(104), '#ffffff', 'ms')
    d.rounded_rectangle([60, 580, W - 60, 1180], radius=28, fill='#1b1c21')
    text(d, (110, 680), '제때 받은 사람과 합계가 같아지는 나이', pd(40, 600), '#c7cad1', 'ls')
    text(d, (110, 900), '80.7세', bh(220), OR, 'ls')
    text(d, (110, 990), '1년 당김 월 94만원 · 제때 월 100만원', pd(40, 600), '#9aa0a8', 'ls')
    ruler(d, 120, W - 120, 1110, 60, 90, [(80.7, '', OR)], big=0, small=28)
    text(d, (W // 2, 1330), '5년 당기면 76.7세', pd(56), '#ffffff', 'ms')
    d.rounded_rectangle([60, 1440, W - 60, 1600], radius=24, fill=CARD)
    text(d, (W // 2, 1540), '내 나이로 계산 · firemap.kr', pd(50), INK, 'ms')
    text(d, (W // 2, 1700), '국민연금법 제63조 · 1969년생 가정', pd(30, 500), '#7c818c', 'ms')
    sample_tag(d, W, H, dark=True)
    im.save(os.path.join(HERE, 'a3_short.png'))


if __name__ == '__main__':
    for f in (a1_thumb, a1_short, a2_thumb, a2_short, a3_thumb, a3_short):
        f()
    print('저장:', sorted(x for x in os.listdir(HERE) if x.endswith('.png')))
