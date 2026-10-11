# C-1 썸네일 c1r (10/11 PD, 순돌이 지시 — thumb-gap-1011.md 7장 C-1 안 A)
# 큰 글 두 줄: 'S&P500 같은 3억' / '1년 늦게 시작하면 11년째 바닥'(대본 0:3 '1년 늦게 시작한 사람은 11년째에 통장이 비었고요', calc_out 39행 3억·월200·A 1997:29+ 1998:11)
# 그림: 1997·1998 통장 두 권(1997 잔액 막대 초록 남음, 1998 잔액 막대 빨강 바닥). 사람 얼굴 없음 · 작은 글 0조각 · 출처 줄 없음(설명란) · 오른쪽 아래 길이 표시 자리 비움
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(HERE, '..', '..', '..', '..', 'fonts')
BH = lambda n: ImageFont.truetype(os.path.join(FD, 'BlackHanSans.ttf'), n)
CREAM, INK, NAVY, GREEN, RED, PAPER = (232, 216, 181), (24, 24, 28), (30, 42, 68), (16, 124, 96), (228, 52, 44), (250, 246, 236)
W, H = 1280, 720
im = Image.new('RGB', (W, H), CREAM); d = ImageDraw.Draw(im)

def text(x, y, parts, font):
    for s, c in parts:
        d.text((x, y), s, font=font, fill=c); x += d.textlength(s, font=font)
    return x

# 큰 글 두 줄
text(48, 22, [('S&P500 같은 3억', INK)], BH(118))
text(48, 160, [('1년 늦게 시작하면 ', INK), ('11년째', RED), (' 바닥', INK)], BH(96))

def book(x, y, w, h, year, fill, color):
    # 펼친 통장: 남색 표지 테두리 + 종이 + 연도 띠 + 잔액 칸 줄 + 잔액 막대
    d.rounded_rectangle((x, y, x + w, y + h), 26, fill=NAVY)
    d.rounded_rectangle((x + 26, y + 26, x + w - 26, y + h - 26), 14, fill=PAPER)
    d.rounded_rectangle((x + 26, y + 26, x + w - 26, y + 118), 14, fill=NAVY)
    d.rectangle((x + 26, y + 90, x + w - 26, y + 118), fill=NAVY)
    f = BH(84); tw = d.textlength(year, font=f); d.text((x + (w - tw) / 2, y + 12), year, font=f, fill=PAPER)
    for k in range(4):   # 통장 줄
        yy = y + 150 + k * 40; d.line((x + 40, yy, x + w - 40, yy), fill=(205, 196, 176), width=4)
    bx0, bx1, by = x + 40, x + w - 40, y + h - 92
    d.rounded_rectangle((bx0, by, bx1, by + 52), 14, outline=color, width=8)
    if fill > 0: d.rounded_rectangle((bx0, by, bx0 + (bx1 - bx0) * fill, by + 52), 14, fill=color)
    else:
        d.rounded_rectangle((bx0, by, bx0 + 26, by + 52), 10, fill=color)   # 바닥: 막대가 0에 붙음

bw, bh, top = 430, 400, 296
book(70, top, bw, bh, '1997', 0.9, GREEN)
book(560, top, bw, bh, '1998', 0, RED)
out = os.path.join(HERE, 'thumb_c1r.png'); im.save(out); print(out)
