# gold1y 표지 v7(firemap-shorts 10/6 11:2x): 틀 교체 — 표·한 숫자 대신 '같은 금, 반대 방향' 위아래 반전 두 칸. 숫자 = goldway1005/pkg/facts.txt 적힌 그대로(+3.38%·-2.42%)
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
INK = (20, 20, 28); YEL = (255, 214, 0); WHITE = (255, 255, 255)
GRN = (240, 60, 60)  # 오름=빨강(한국 시세 관례)
RED = (20, 70, 200)  # 내림=파랑
im = Image.new('RGB', (W, H), INK); d = ImageDraw.Draw(im)
d.text((M, 120), '같은 금, 1년', font=C.BHS(150), fill=WHITE)
# 위 칸: 국제 금값(원화) 오름
d.rounded_rectangle((M, 360, W - M, 900), 40, fill=(38, 40, 52))
d.text((M + 40, 400), '국제 금값(원화)', font=C.BHS(90), fill=WHITE)
d.polygon([(M+40,760),(M+190,760),(M+115,600)], fill=GRN)
d.text((M + 230, 560), '+3.38%', font=C.BHS(190), fill=GRN)
# 아래 칸: KRX 금 내림
d.rounded_rectangle((M, 940, W - M, 1480), 40, fill=YEL)
d.text((M + 40, 980), '한국 KRX 금', font=C.BHS(96), fill=INK)
d.polygon([(M+40,1180),(M+190,1180),(M+115,1340)], fill=RED)
d.text((M + 230, 1140), '-2.42%', font=C.BHS(190), fill=RED)
d.text((M, 1560), '왜 갈렸을까?', font=C.BHS(130), fill=YEL)
d.text((M, 1760), '2025.10.2 ~ 2026.10.2', font=C.BHS(46), fill=(190, 190, 200))
p = os.path.dirname(os.path.abspath(__file__))
assert d.textlength('+3.38%', font=C.BHS(190)) < W-M-(M+230), d.textlength('+3.38%', font=C.BHS(190))
im.save(os.path.join(p, 'cover_v7.png')); print('ok')
