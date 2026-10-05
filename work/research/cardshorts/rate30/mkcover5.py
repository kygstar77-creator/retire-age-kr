# rate30 표지 v5 — v4 심사 6(작은 글자 가독성) 고침: 줄당 한 덩어리 '라벨 숫자' 한 줄 크게, 아래 출처줄 없음. 숫자 bokrate1006/pkg/facts.txt 그대로, 막대 길이 = 값/5.25
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
BGC = (24, 40, 64); GR = (168, 176, 196); LG = (206, 214, 230); INK = (16, 22, 36)
im = Image.new('RGB', (W, H), BGC); d = ImageDraw.Draw(im)
d.text((M, 110), '기준금리 3%', font=C.BHS(172), fill=C.YELLOW)
d.text((M, 400), '1999년 이후', font=C.BHS(150), fill=C.WHITE)
d.text((M, 590), '어디쯤일까?', font=C.BHS(150), fill=C.WHITE)
BW = W - 2 * M
for k, (lab, num, v, col) in enumerate([('최고', '5.25%', 5.25, GR), ('지금', '3%', 3.0, C.YELLOW), ('최저', '0.5%', 0.5, GR)]):
    y = 880 + k * 300
    d.rectangle((M, y, M + max(int(BW * v / 5.25), 14), y + 260), fill=col)
    t = lab + ' ' + num; f = C.BHS(150)
    if v >= 1: d.text((M + 30, y + 40), t, font=f, fill=INK)
    else: d.text((M + 14 + int(BW * v / 5.25) + 30, y + 40), t, font=f, fill=LG)
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cover_v5.png')); print('ok')
