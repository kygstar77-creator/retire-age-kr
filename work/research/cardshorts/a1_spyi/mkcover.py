import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
im = Image.new('RGB', (W, H), C.BG); d = ImageDraw.Draw(im)
RED = (255, 84, 84); LG = (205, 210, 222)
d.rounded_rectangle((M, 150, 255, 208), 12, fill=(255, 106, 0)); d.text((84, 158), '파이어맵', font=C.PD7(36), fill=C.WHITE)
d.text((M, 250), 'SPYI vs SPY', font=C.BHS(120), fill=C.WHITE)
d.text((M, 400), '커버드콜 1년 성적', font=C.BHS(100), fill=C.WHITE)
S = 880 / 20.0; x0 = M
y = 570
for name, p, dv, tot, big, col in [('SPYI', 2.38, 12.17, '14.55%', 100, LG), ('SPY', 15.68, 1.15, '16.83%', 130, C.YELLOW)]:
    d.text((x0, y), name + (' 커버드콜' if name=='SPYI' else ' 지수'), font=C.PD7(56), fill=C.WHITE)
    by = y + 80; bh = 150
    w1 = int(p * S); w2 = int(dv * S)
    d.rectangle((x0, by, x0 + w1, by + bh), fill=LG)
    d.rectangle((x0 + w1, by, x0 + w1 + w2, by + bh), fill=C.YELLOW)
    if name == 'SPYI': d.text((x0 + w1 + 24, by + 40), '분배금 12.17%', font=C.PD7(60), fill=C.BG)
    d.text((x0, by + bh + 8), '합계 ' + tot, font=C.BHS(big), fill=col)
    y += 390
d.text((M, 1420), '분배금 많아도', font=C.PD7(70), fill=C.WHITE)
d.text((M, 1510), '총수익은 SPY가 앞섬', font=C.BHS(100), fill=RED)
d.text((M, 1700), '분배금 SPYI 12.17% vs SPY 1.15%', font=C.PD7(48), fill=C.WHITE)
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cover.png'))
