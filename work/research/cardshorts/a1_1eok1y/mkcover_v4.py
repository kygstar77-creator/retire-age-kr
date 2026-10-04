# v4(10/5 00:2x firemap-shorts): v3(제미나이 6.5 '작다') → 숫자를 막대 위 큰 글씨로, 막대는 그 아래 넓은 띠(1,005:330 실제 비율), 빈 위아래 줄임.
# v3 기준: review.md '고칠 것' ①~⑥ — 글자 덩어리 3개(누구·얼마 / 분배금 막대 그림 / 질문), SCHD 숫자 JEPQ와 같은 크기·파랑, '미국 세금 15% 뗀 분배금', '어느 쪽이', '1년 뒤 합계'. 승자는 영상 안(spyi v8 틀).
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
im = Image.new('RGB', (W, H), C.BG); d = ImageDraw.Draw(im)
T = C.BHS(142); V = C.BHS(92)
d.text((M, 130), 'SCHD', font=T, fill=C.BLUE)
x = M + d.textlength('SCHD ', font=T); d.text((x, 160), 'vs', font=V, fill=C.GREY)
x += d.textlength('vs ', font=V); d.text((x, 130), 'JEPQ', font=T, fill=C.YELLOW)
d.text((M, 320), '1억씩 넣고 1년', font=C.BHS(132), fill=C.WHITE)
d.text((M, 540), '미국 세금 15% 뗀 분배금', font=C.PD7(66), fill=C.WHITE)
BW = W - 2 * M - 40
for k, (lab, v, s, col) in enumerate([('JEPQ', 1005, '1,005만', C.YELLOW), ('SCHD', 330, '330만', C.BLUE)]):
    y = 640 + k * 290
    d.text((M, y), lab + ' ' + s, font=C.BHS(150), fill=col)
    d.rectangle((M, y + 190, M + int(BW * v / 1005), y + 250), fill=col)
d.text((M, 1260), '1년 뒤 합계는', font=C.BHS(150), fill=C.WHITE)
d.text((M, 1450), '어느 쪽이 클까?', font=C.BHS(150), fill=C.YELLOW)
d.text((M, 1700), '2025.9.26 → 2026.9.28 종가', font=C.PD7(48), fill=(150, 150, 160))
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cover.png'))
print('ok', M + d.textlength('JEPQ 1,005만', font=C.BHS(150)))
