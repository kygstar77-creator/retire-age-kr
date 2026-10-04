# a1_spyi 표지 v8(firemap-shorts 10/4 19:3x): v7 지적 반영 — 결론 숫자(14.55·16.83) 표지에서 빼 궁금증 남김(제미나이), 후킹 질문 크게(레드팀), 줄 수 줄임, 기간 표시
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
im = Image.new('RGB', (W, H), C.BG); d = ImageDraw.Draw(im)
d.text((M, 260), 'SPYI vs SPY', font=C.BHS(150), fill=C.WHITE)
d.text((M, 470), '1년 받은 분배금', font=C.PD7(88), fill=C.WHITE)
d.text((M, 630), 'SPYI', font=C.PD7(76), fill=C.YELLOW); d.text((M + 250, 580), '12.17%', font=C.BHS(200), fill=C.YELLOW)
d.text((M, 860), 'SPY', font=C.PD7(76), fill=C.WHITE); d.text((M + 250, 810), '1.15%', font=C.BHS(200), fill=C.WHITE)
d.text((M, 1150), '총수익은', font=C.BHS(150), fill=C.WHITE)
d.text((M, 1330), '누가 이겼을까?', font=C.BHS(150), fill=C.WHITE)
d.text((M, 1640), '2025.9.26 → 2026.9.28 종가 기준', font=C.PD7(56), fill=C.WHITE)
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cover3.png'))
