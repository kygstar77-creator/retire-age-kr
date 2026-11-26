# B-58 시범 설계안 목업(visual 2026-11-26) — 적용 아님(12/3 판정 뒤). de1s_divo(S-bh4F6JB-k) oar2 위에 위 제목만 다시 그림.
#   지금: 줄 높이 약 3%·끝 19.8% · 시범: 줄 높이 약 5%(글자 92px 안팎)·끝 22~24%·0초~끝 고정 · 띠는 색 상자가 아니라 위→아래 짙은 그라데이션(클로드 티 금지 목록 '상자·판' 피함)
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
O = os.path.dirname(os.path.abspath(__file__)); FONT = os.path.abspath(os.path.join(O, '..', '..', '..', 'fonts'))
W, H = 1080, 1920; YEL = (255, 196, 0); INK = (10, 11, 14)
src = Image.open(os.path.join(O, 'oar2_S-bh4F6JB-k.jpg')).convert('RGB')
im = src.copy(); top = int(H * 0.27)
im.paste(src.crop((0, 0, W, top)).filter(ImageFilter.GaussianBlur(28)), (0, 0))   # 옛 작은 제목 지움(목업용)
m = Image.new('L', (W, H), 0); d = ImageDraw.Draw(m)
for y in range(0, int(H * 0.30)): d.line([(0, y), (W, y)], fill=int(200 * max(0, 1 - max(0, y - H * 0.18) / (H * 0.12))))
im = Image.composite(Image.new('RGB', (W, H), INK), im, m); d = ImageDraw.Draw(im)
L = [[('분배율 6%대 배당 ETF', (255, 255, 255))], [('정말 ', (255, 255, 255)), ('6%일까', YEL)]]
size = 100
f = lambda s: ImageFont.truetype(os.path.join(FONT, 'pd700.ttf'), s)
while max(sum(d.textlength(t, font=f(size)) for t, _ in ln) for ln in L) > W * 0.88: size -= 2
y = int(H * 0.125)
for ln in L:
    tw = sum(d.textlength(t, font=f(size)) for t, _ in ln); x = (W - tw) / 2
    for t, c in ln: d.text((x, y), t, font=f(size), fill=c, stroke_width=6, stroke_fill=INK); x += d.textlength(t, font=f(size))
    y += int(size * 1.12)
print('글자', size, 'px · 줄 간격', round(size * 1.12 / H * 100, 1), '% · 제목 끝', round(y / H * 100, 1), '%')
bb = Image.new('RGB', (W * 2 + 40, H), 'white'); bb.paste(src, (0, 0)); bb.paste(im, (W + 40, 0))
dd = ImageDraw.Draw(bb)
for p in (10, 15, 20, 25):
    for x0 in (0, W + 40): dd.line([(x0, H * p // 100), (x0 + W, H * p // 100)], fill=(255, 0, 255), width=3)
bb.resize((bb.width // 3, H // 3), Image.LANCZOS).save(os.path.join(O, 'mock_b58.png'))
