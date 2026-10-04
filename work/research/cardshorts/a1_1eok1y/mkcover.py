# v6(10/5 00:4x firemap-shorts): v4 6.4(제미나이 6.8·A 6.4·레드팀 6) 지적 반영 — 덩어리 3개(제목 한 줄 / 분배금 막대 ↔ 합계 '?' 막대 그림 / 질문),
# 뒤집힘을 그림으로(합계 자리는 값 가린 '?' 막대), 검정+노랑 겹침 → JEPQ 주황·질문 흰색, 날짜 줄에 '환율 변동 제외'. 분배금 막대는 1,005:330 실제 비율.
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
OR = (255, 120, 30); GH = (95, 100, 115)
im = Image.new('RGB', (W, H), C.BG); d = ImageDraw.Draw(im)
T = C.BHS(100)
x = M
for s, col, f in [('1억씩 ', C.WHITE, T), ('SCHD', C.BLUE, T), (' vs ', C.GREY, C.BHS(68)), ('JEPQ', OR, T)]:
    d.text((x, 150 + (22 if f is not T else 0)), s, font=f, fill=col); x += d.textlength(s, font=f)
X0, BW = M + 268, 292
def sect(y, head, sub):
    d.text((M, y), head, font=C.BHS(84), fill=C.WHITE)
    if sub: d.text((M + d.textlength(head + ' ', font=C.BHS(84)), y + 30), sub, font=C.PD7(44), fill=C.GREY)
sect(380, '분배금', '미국 세금 15% 뗀')
for k, (lab, v, s, col) in enumerate([('JEPQ', 1005, '1,005만', OR), ('SCHD', 330, '330만', C.BLUE)]):
    y = 500 + k * 150
    d.text((M, y + 14), lab, font=C.BHS(84), fill=col)
    bw = int(BW * v / 1005); d.rectangle((X0, y, X0 + bw, y + 110), fill=col)
    d.text((X0 + bw + 24, y), s, font=C.BHS(104), fill=col)
sect(840, '1년 뒤 합계', '분배금 + 평가금액')
for k, (lab, col) in enumerate([('JEPQ', OR), ('SCHD', C.BLUE)]):
    y = 960 + k * 150
    d.text((M, y + 14), lab, font=C.BHS(84), fill=col)
    d.rounded_rectangle((X0, y, X0 + 540, y + 110), 14, outline=GH, width=8)
    q = C.BHS(96); d.text((X0 + 270 - d.textlength('?', font=q) / 2, y + 2), '?', font=q, fill=C.WHITE)
d.text((M, 1330), '어느 쪽이 클까?', font=C.BHS(150), fill=C.WHITE)
d.text((M, 1700), '2025.9.26 → 2026.9.28 종가 · 환율 변동 제외', font=C.PD7(40), fill=(150, 150, 160))
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cover.png'))
print('ok', x, X0 + 300 + 24 + d.textlength('1,005만', font=C.BHS(104)))
