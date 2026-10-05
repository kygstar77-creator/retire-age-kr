# gold1y 표지 v6(firemap-shorts 10/6 03:4x): '1천만원 → 677만원' 화살표로 원금 대비 명시 + 알약 세로 가운데·연도 포함. 숫자 = calc.txt 그대로
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
BG = (255, 214, 0); INK = (20, 20, 28); RED = (200, 20, 20)
im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
def ctr(y, s, f, fill):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill)
ctr(150, '금 1천만원 넣었더니', C.BHS(110), INK)
ctr(400, '1천만원', C.BHS(230), INK)
d.polygon([(450,700),(630,700),(630,800),(700,800),(540,930),(380,800),(450,800)], fill=INK)
ctr(980, '677만원', C.BHS(262), RED)
ctr(1330, '-32.3%', C.BHS(210), INK)
d.rounded_rectangle((M, 1590, W - M, 1790), 100, fill=INK)
f = C.BHS(64); s = '1.29 고점에 샀다면 · 8개월 뒤'
w = d.textlength(s, font=f); bb = d.textbbox((0, 0), s, font=f)
d.text(((W - w) / 2, 1690 - (bb[1] + bb[3]) / 2), s, font=f, fill=BG)
p = os.path.dirname(os.path.abspath(__file__))
im.save(os.path.join(p, 'cover_v6.png')); print('ok')
