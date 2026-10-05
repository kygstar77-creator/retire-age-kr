# gold1y 표지 v5(firemap-shorts 10/6 03:2x): 밝은 바탕 + 손실폭 한 숫자(-32.3%) + 반전 한 줄. 숫자 = calc.txt 그대로
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
BG = (255, 214, 0); INK = (20, 20, 28); RED = (200, 20, 20)
im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
d.text((M, 170), '금 1천만원', font=C.BHS(170), fill=INK)
d.text((M, 380), '1월 고점에 샀더니', font=C.BHS(120), fill=INK)
d.text((M, 700), '677만원', font=C.BHS(262), fill=RED)
d.text((M, 1050), '-32.3%', font=C.BHS(250), fill=INK)
d.rounded_rectangle((M, 1400, W - M, 1580), 30, fill=INK)
d.text((M + 40, 1430), '1.29 고점 → 10.2 · 8개월', font=C.BHS(68), fill=BG)
d.text((M, 1700), 'KRX 금시장 종가 · 수수료 별도', font=C.BHS(54), fill=INK)
p = os.path.dirname(os.path.abspath(__file__))
im.save(os.path.join(p, 'cover_v5.png')); print('ok')
