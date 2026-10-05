# gold1y 표지 v3(firemap-shorts 10/6): v2 5점(제미나이 5·레드팀 5) 지적 반영 — 숫자 1개 크게(677만 4천원), 연도·기간(8개월) 표기, 975만 8천원은 보조.
# 숫자 = calc.txt (goldway1005/pkg/facts.txt KRX 종가 g당 2025-10-02 187,300 · 2026-01-29 269,810 · 2026-10-02 182,770)
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
BGC = (40, 34, 58); LG = (210, 206, 222)
V = os.environ.get('V', 'v3')
im = Image.new('RGB', (W, H), BGC); d = ImageDraw.Draw(im)
d.text((M, 150), '금 1천만원어치,', font=C.BHS(130), fill=C.WHITE)
d.text((M, 330), '1월 고점에 샀다면', font=C.BHS(130), fill=C.WHITE)
d.text((M, 620), '677만', font=C.BHS(330), fill=C.YELLOW)
d.text((M, 960), '4천원', font=C.BHS(230), fill=C.YELLOW)
d.text((M, 1330), '2026.1.29 고점 → 10.2 종가(8개월)', font=C.BHS(62), fill=LG)
d.text((M, 1440), '2025.10.2에 샀다면 975만 8천원', font=C.BHS(70), fill=C.WHITE)
d.text((M, 1560), 'KRX 금시장 종가 · 수수료 별도', font=C.BHS(58), fill=LG)
p = os.path.dirname(os.path.abspath(__file__))
im.save(os.path.join(p, 'cover.png')); im.save(os.path.join(p, f'cover_{V}.png')); print('ok')
