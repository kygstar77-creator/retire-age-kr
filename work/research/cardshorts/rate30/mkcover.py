# rate30 표지 v1 (firemap-shorts 10/6) — 숫자 bokrate1006/pkg/facts.txt 그대로(5.25·3·0.5), 막대 길이 = 값/5.25
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
BGC = (24, 40, 64); GR = (168, 176, 196); LG = (206, 214, 230); INK = (16, 22, 36)
V = os.environ.get('V', 'v1')
im = Image.new('RGB', (W, H), BGC); d = ImageDraw.Draw(im)
d.text((M, 100), '기준금리 3%', font=C.BHS(172), fill=C.YELLOW)
d.text((M, 380), '1999년 이후', font=C.BHS(120), fill=C.WHITE)
d.text((M, 540), '어디쯤일까?', font=C.BHS(120), fill=C.WHITE)
BW = W - 2 * M
rows = [('역대 최고', '5.25%', 5.25, GR), ('지금', '3%', 3.0, C.YELLOW), ('역대 최저', '0.5%', 0.5, GR)]
for k, (lab, num, v, col) in enumerate(rows):
    y = 760 + k * 320
    d.rectangle((M, y, M + max(int(BW * v / 5.25), 14), y + 280), fill=col)
    x = M + 30
    if v < 1: x = M + int(BW * v / 5.25) + 30
    cc = INK if v >= 1 else LG
    d.text((x, y + 20), lab, font=C.BHS(84), fill=cc)
    d.text((x, y + 100), num, font=C.BHS(170), fill=cc)
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cover_%s.png' % V)); print('ok')
