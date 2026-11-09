# 캡처 여러 장을 내용만 잘라 위아래로 붙인다. 실행: py -3.12 compose.py out.png a.png b.png ... (첫 장만 머리 남김)
import sys
from PIL import Image, ImageChops, ImageDraw, ImageFont
out, ins = sys.argv[1], sys.argv[2:]
parts = []
for i, f in enumerate(ins):
    im = Image.open(f).convert('RGB')
    g = im.convert('L').crop((12, 0, im.width - 12, im.height)).point(lambda v: 255 if v < 200 else 0)
    rows = [y for y in range(im.height) if g.crop((0, y, g.width, y + 1)).getbbox()]
    top = 0 if i == 0 else min(y for y in rows if y > 330) - 20   # 둘째 장부터는 머리·법 이름 빼고 조문만
    im = im.crop((0, top, im.width, max(rows) + 30))
    parts.append(im)
W = max(p.width for p in parts); H = sum(p.height for p in parts) + 60
c = Image.new('RGB', (W, H), 'white'); y = 0
for p in parts: c.paste(p, (0, y)); y += p.height
d = ImageDraw.Draw(c); d.line((0, 0, W - 1, 0), fill='#D0D5DD'); d.rectangle((0, 0, W - 1, H - 1), outline='#D0D5DD', width=2)
f = ImageFont.truetype('C:/Users/강영준/Documents/GitHub/retire-age-kr/work/fonts/pd700.ttf', 24)
d.text((24, H - 46), '국가법령정보센터 원문 캡처 · 2026.11.9 · 노란 표시는 서울 기준', font=f, fill='#4B5563')
c = c.resize((900, int(H * 900 / W)), Image.LANCZOS); c.save(out); print(out, c.size)
