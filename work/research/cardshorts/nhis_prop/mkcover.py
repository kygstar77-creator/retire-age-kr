# nhis_prop 표지 v1(firemap-shorts 10/5 03:5x) — nongji_age mkcover4 틀(막대 안 결론 숫자 둘·단색 바탕).
# 숫자 nhisprop1005/pkg/facts.txt 그대로(117,240·162,950원), 막대 길이 = 값/162,950.
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
BGC = (22, 44, 52); GR = (160, 176, 182); LG = (206, 218, 222); INK = (16, 22, 26)
im = Image.new('RGB', (W, H), BGC); d = ImageDraw.Draw(im)
d.text((M, 120), '퇴직 후 집 한 채', font=C.BHS(110), fill=C.WHITE)
d.text((M, 300), '건보료 월 얼마?', font=C.BHS(140), fill=C.YELLOW)
BW = W - 2 * M
for k, (lab, num, v, col) in enumerate([('공시가 5억', '117,240원', 117240, GR), ('공시가 9억', '162,950원', 162950, C.YELLOW)]):
    y = 620 + k * 400
    d.rectangle((M, y, M + int(BW * v / 162950), y + 340), fill=col)
    d.text((M + 30, y + 24), lab, font=C.BHS(84), fill=INK)
    d.text((M + 30, y + 150), num, font=C.BHS(140), fill=INK)
d.text((M, 1480), '지역가입자, 소득·차 없이 재산만', font=C.BHS(70), fill=LG)
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cover_v1.png'))
print('ok')
