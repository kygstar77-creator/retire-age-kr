# npsday1007 표지 v1 (firemap-shorts 10/6) — nongji_age mkcover4 틀 복사, 숫자 npsday1007/pkg/facts.txt 그대로(64세·65세)
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
BGC = (40, 34, 58); GR = (168, 164, 184); LG = (210, 206, 222); INK = (20, 18, 28)
im = Image.new('RGB', (W, H), BGC); d = ImageDraw.Draw(im)
d.text((M, 120), '국민연금 수령나이', font=C.BHS(110), fill=C.WHITE)
d.text((M, 300), '1968년생 vs 1969년생', font=C.BHS(112), fill=C.YELLOW)
d.text((M, 480), '수령나이 1년 차이', font=C.BHS(126), fill=C.YELLOW)
for k, (lab, num, col) in enumerate([('1968년 12월 31일생', '64세', GR), ('1969년 1월 1일생', '65세', C.YELLOW)]):
    y = 740 + k * 380
    d.rectangle((M, y, W - M, y + 330), fill=col)
    d.text((M + 30, y + 24), lab, font=C.BHS(88), fill=INK)
    d.text((M + 30, y + 120), num + '부터', font=C.BHS(170), fill=INK)
d.text((M, 1560), '가입 10년 이상 기준', font=C.BHS(62), fill=LG)
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cover_v3.png')); print('ok')
