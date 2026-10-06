# gold1y 표지 v8(firemap-shorts 10/6 11:1x): v7 반전 두 칸(제미나이 고정 5·5, '표처럼 느껴짐·내 돈 결과 없음') → 내 돈 결과 한 숫자 + 반전 한 줄. 숫자 = goldway1005/pkg/facts.txt 그대로(9,758,142원·+3.38%)
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
BG = (255, 214, 0); INK = (20, 20, 28); RED = (200, 20, 20)
im = Image.new('RGB', (W, H), BG); d = ImageDraw.Draw(im)
d.text((M, 150), '금 1천만원', font=C.BHS(180), fill=INK)
d.text((M, 390), '1년 전 KRX에서 샀다면', font=C.BHS(86), fill=INK)
d.text((M, 560), '지금', font=C.BHS(120), fill=INK)
d.text((M, 720), '975만', font=C.BHS(300), fill=RED)
d.text((M, 1050), '8천원', font=C.BHS(150), fill=RED)
d.rounded_rectangle((M, 1290, W - M, 1450), 30, fill=INK)
d.text((M + 40, 1318), '국제 금값(원화) +3.38%인데', font=C.BHS(74), fill=BG)
d.text((M, 1520), '왜 손해?', font=C.BHS(150), fill=INK)
d.text((M, 1760), '2025.10.2 ~ 2026.10.2 · 수수료 별도', font=C.BHS(46), fill=INK)
for t, s in [('975만', 300), ('1년 전 KRX에서 샀다면', 86), ('금 1천만원', 180)]:
    assert d.textlength(t, font=C.BHS(s)) < W - 2 * M, t
assert d.textlength('국제 금값(원화) +3.38%인데', font=C.BHS(74)) < W - 2 * M - 80
p = os.path.dirname(os.path.abspath(__file__))
im.save(os.path.join(p, 'cover_v8.png')); print('ok')
