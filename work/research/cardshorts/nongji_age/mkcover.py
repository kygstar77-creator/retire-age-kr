# v3: 머리 줄 줄이고 숫자 150px(제미나이 v2 '숫자 작다·위 글 길다'), 조건은 아래 한 줄로
# nongji_age 첫 1초 표지(firemap-shorts 10/5 01:4x) — e2_interest mkcover8.py 틀(덩어리 4개: 머리 줄/질문/막대 두 개 안에 숫자/조건 한 줄).
# 숫자는 nongji1005/pkg/facts.txt 그대로(1,051,330·845,100원), 막대 길이 = 값/1,051,330. 경쟁 1위(나이별 표·논 사진)와 다르게 표·사진 없이 막대 두 개.
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
V = os.environ.get('V', '1')
W, H = 1080, 1920; M = 64
BGC = (34, 52, 44); GR = (150, 165, 158); LG = (205, 215, 210); INK = (18, 22, 20)
im = Image.new('RGB', (W, H), BGC); d = ImageDraw.Draw(im)
d.text((M, 120), '농지연금', font=C.BHS(130), fill=C.WHITE)
d.text((M, 300), '배우자 승계하면', font=C.BHS(140), fill=C.YELLOW)
d.text((M, 480), '월 얼마 줄까?', font=C.BHS(140), fill=C.YELLOW)
BW = W - 2 * M
for k, (lab, num, v, col) in enumerate([('승계 없음', '1,051,330원', 1051330, GR), ('배우자 55세 승계', '845,100원', 845100, C.YELLOW)]):
    y = 720 + k * 420
    d.text((M, y), lab, font=C.BHS(76), fill=LG if k == 0 else C.YELLOW)
    d.rectangle((M, y + 100, M + int(BW * v / 1051330), y + 340), fill=col)
    d.text((M + 24, y + 128), num, font=C.BHS(150), fill=INK)
d.line((M, 810, M, 1490), fill=LG, width=6)
d.text((M, 1560), '3억 농지, 본인 65세 기준', font=C.BHS(76), fill=LG)
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'cover_v{V}.png'))
print('ok')
