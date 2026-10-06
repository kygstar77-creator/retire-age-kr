# rate30 표지 v8 — A 지적 "조용하다": '최저 ?'를 노랑 큰 글자 주인공으로. 숫자는 bokrate1006/pkg/facts.txt 그대로(5.25%, 3%), 평가 말 없음.
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
BGC = (24, 40, 64); GR = (168, 176, 196); LG = (206, 214, 230); INK = (16, 22, 36)
im = Image.new('RGB', (W, H), BGC); d = ImageDraw.Draw(im)
d.text((M, 120), '기준금리', font=C.BHS(150), fill=C.WHITE)
d.text((M, 320), '1999년 이후', font=C.BHS(150), fill=C.WHITE)
d.text((M, 640), '최저는?', font=C.BHS(330), fill=C.YELLOW)
BW = W - 2 * M
for k, (lab, num, v, col) in enumerate([('최고', '5.25%', 5.25, GR), ('지금', '3%', 3.0, LG)]):
    y = 1180 + k * 280
    d.rectangle((M, y, M + int(BW * v / 5.25), y + 240), fill=col)
    d.text((M + 30, y + 35), lab + ' ' + num, font=C.BHS(140), fill=INK)
d.text((M, 1790), 'ECOS 2026년 9월 기준', font=C.BHS(62), fill=LG)
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cover_v8.png')); print('ok')
