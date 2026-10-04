# v8(firemap-shorts 10/5 01:1x): 제미나이 v5~v7 '글자 많다·핵심 비교를 크게' 반복 → 덩어리 4개로: 제목 / 결론 2줄(맨 위로) / 막대 안에 이름·숫자 / 단위·총액 한 줄.
# 숫자는 E-2 facts [3] 그대로(422·398, 백만 달러), 막대 길이 = 값/422. '<' 기호·'본업'·'번 돈' 안 씀(1~5차 지적).
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
BGC = (38, 44, 56); GR = (150, 158, 175); LG = (200, 205, 215); INK = (20, 22, 28)
im = Image.new('RGB', (W, H), BGC); d = ImageDraw.Draw(im)
d.text((M, 120), '테슬라 2분기 실적', font=C.BHS(124), fill=C.WHITE)
d.text((M, 330), '이자수익이', font=C.BHS(170), fill=C.YELLOW)
d.text((M, 530), '더 컸다', font=C.BHS(170), fill=C.YELLOW)
BW = W - 2 * M
for k, (lab, v, col) in enumerate([('이자수익 422', 422, C.YELLOW), ('영업이익 398', 398, GR)]):
    y = 830 + k * 300
    d.rectangle((M, y, M + int(BW * v / 422), y + 240), fill=col)
    d.text((M + 36, y + 42), lab, font=C.BHS(130), fill=INK)
d.line((M, 810, M, 1390), fill=LG, width=6)   # 0 기준선
f = C.BHS(72); d.text((M, 1440), '단위 백만 달러', font=f, fill=LG)
a = '이자비용 빼기 전 '; d.text((M, 1540), a, font=f, fill=LG); d.text((M + d.textlength(a, font=f), 1540), '총액', font=f, fill=C.YELLOW)
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cover_v8.png'))
print('ok')
