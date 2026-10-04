# nongji_age 표지 v4(firemap-shorts 10/5 02:0x) — v3 심사 제미나이 7·A 6·레드팀 7=6.67 미통과 고침:
# ① 초록 바탕+노랑이 경쟁 1·2위(논 사진)와 비슷(A) → 짙은 남보라 바탕 ② '줄까' 두 뜻(A·레드팀) → '줄어들까?'
# ③ 덩어리 7→5: 이름표를 막대 안으로, 조건은 머리 줄+맨 아래 한 줄(레드팀: 공시지가·종신정액형 표지에 없음)
# 숫자 nongji1005/pkg/facts.txt 그대로(1,051,330·845,100원), 막대 길이 = 값/1,051,330.
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
BGC = (40, 34, 58); GR = (168, 164, 184); LG = (210, 206, 222); INK = (20, 18, 28)
im = Image.new('RGB', (W, H), BGC); d = ImageDraw.Draw(im)
d.text((M, 120), '농지연금 3억, 65세', font=C.BHS(110), fill=C.WHITE)
d.text((M, 300), '배우자 승계하면', font=C.BHS(140), fill=C.YELLOW)
d.text((M, 480), '월 얼마 줄어들까?', font=C.BHS(126), fill=C.YELLOW)
BW = W - 2 * M
for k, (lab, num, v, col) in enumerate([('승계 없음', '1,051,330원', 1051330, GR), ('배우자 55세 승계', '845,100원', 845100, C.YELLOW)]):
    y = 740 + k * 380
    d.rectangle((M, y, M + int(BW * v / 1051330), y + 330), fill=col)
    d.text((M + 30, y + 24), lab, font=C.BHS(76), fill=INK)
    d.text((M + 30, y + 140), num, font=C.BHS(140), fill=INK)
d.text((M, 1560), '공시지가, 종신정액형 기준', font=C.BHS(70), fill=LG)
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cover_v4.png'))
print('ok')
