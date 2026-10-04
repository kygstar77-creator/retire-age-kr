# v7(10/5 00:2x firemap-shorts): v6 6.93(제미나이 7·A 6.8·레드팀 7) 공통 지적 반영 —
# ① 빈 공간을 숫자에: 분배금 줄 '종목 숫자'를 140px(v6 104)로, 회색 보조 글씨 3개('미국 세금 15% 뗀'·'분배금+평가금액'·날짜)는 표지에서 빼고 첫 카드·설명란에만
# ② 합계 '?' 칸을 같은 길이로 채운 종목 색 막대(굵은 흰 테두리) ③ 경쟁 비슷한 점 줄이기: 검정 바탕→남색, '1억씩'은 작은 둘째 줄로.
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
NAVY = (20, 34, 72); OR = (255, 120, 30); BL = C.BLUE
im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
T = C.BHS(132); x = M
for s, col, f, dy in [('SCHD', BL, T, 0), (' vs ', C.GREY, C.BHS(84), 34), ('JEPQ', OR, T, 0)]:
    d.text((x, 80 + dy), s, font=f, fill=col); x += d.textlength(s, font=f)
d.text((M, 262), '1억씩 넣고 1년', font=C.BHS(68), fill=C.WHITE)
d.text((M, 420), '분배금', font=C.BHS(96), fill=C.WHITE)
BW = W - 2 * M
for k, (lab, v, s, col) in enumerate([('JEPQ', 1005, '1,005만', OR), ('SCHD', 330, '330만', BL)]):
    y = 560 + k * 300
    d.text((M, y), lab + ' ' + s, font=C.BHS(140), fill=col)
    d.rectangle((M, y + 180, M + int(BW * v / 1005), y + 250), fill=col)
d.text((M, 1180), '1년 뒤 합계', font=C.BHS(96), fill=C.WHITE)
q = C.BHS(104); LX = M + 300
for k, (lab, col) in enumerate([('JEPQ', OR), ('SCHD', BL)]):
    y = 1320 + k * 160
    d.text((M, y + 12), lab, font=C.BHS(96), fill=col)
    d.rounded_rectangle((LX, y, W - M, y + 130), 16, fill=col, outline=C.WHITE, width=10)
    d.text(((LX + W - M) / 2 - d.textlength('?', font=q) / 2, y + 4), '?', font=q, fill=NAVY)
d.text((M, 1660), '어느 쪽이 클까?', font=C.BHS(140), fill=C.WHITE)
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cover.png'))
print('ok title', x, 'num', M + d.textlength('JEPQ 1,005만', font=C.BHS(140)), 'q', M + d.textlength('어느 쪽이 클까?', font=C.BHS(140)))
