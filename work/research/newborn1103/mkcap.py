# 본문 01: 공식 원문 캡처(주택도시기금포털 FP05030808, 11/3 Playwright 캡처 raw/FP05030808_cap_1103.png)
# 지시 today.md 11/3 '법·고시 근거 글은 차트 1장을 원문 캡처로' — 옛 선 차트는 pkg/img/01_chart.png.bak
import math, os
from PIL import Image, ImageDraw, ImageFont
H = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(H, '..', '..', 'fonts')
src = Image.open(os.path.join(H, 'raw', 'FP05030808_cap_1103.png')).convert('RGB')
W = 900; PAD = 24
s = (W - PAD * 2) / src.width
cap = src.resize((W - PAD * 2, round(src.height * s)), Image.LANCZOS)
d = ImageDraw.Draw(cap)
# 1억원 이하·30년 칸(본문 예시 '소득 1억원 집')에 손으로 그린 듯한 주황 동그라미
cx, cy, rx, ry = 1565 * s, 1185 * s, 95 * s, 46 * s
pts = [(cx + rx * (1 + .04 * math.sin(3 * t)) * math.cos(t), cy + ry * (1 + .05 * math.cos(2 * t)) * math.sin(t))
       for t in [i / 60 * 2.15 * math.pi - .4 for i in range(61)]]
d.line(pts, fill=(255, 90, 0), width=4, joint='curve')
foot = 40
out = Image.new('RGB', (W, cap.height + PAD + foot), 'white')
out.paste(cap, (PAD, PAD))
od = ImageDraw.Draw(out)
od.rectangle([PAD - 1, PAD - 1, PAD + cap.width, PAD + cap.height], outline=(210, 214, 220))
f = ImageFont.truetype(os.path.join(FONT, 'pd700.ttf'), 15)
od.text((PAD, PAD + cap.height + 12), "주택도시기금포털 '특례금리 적용 종료 후 적용 금리' 화면 (2026년 11월 3일 캡처)", font=f, fill=(110, 116, 126))
out.save(os.path.join(H, 'pkg', 'img', '01.png'))
print(out.size)
