# nhis_prop 표지 v2(firemap-shorts 10/5 03:5x) — v1 심사(제미나이 7·A 6) 고침: ① '·' 글자 깨짐(폰트) → 쉼표
# ② 표지가 답을 다 말함 → 9억은 '?' 칸으로 감춤(a1_1eok1y v9 통과 틀) ③ '퇴직 후' 경쟁 1~3과 같은 첫머리 뺌
# ④ 우리만의 차이 '2026 1주택 특례율'을 아래 줄로 크게. 숫자 nhisprop1005/pkg/facts.txt 그대로(117,240원).
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
BGC = (22, 44, 52); LG = (226, 234, 236); MID = (70, 96, 104); INK = (16, 22, 26)
im = Image.new('RGB', (W, H), BGC); d = ImageDraw.Draw(im)
d.text((M, 130), '집 한 채, 소득 없어도', font=C.BHS(100), fill=C.WHITE)
d.text((M, 300), '건보료 월 얼마?', font=C.BHS(146), fill=C.YELLOW)
BW = W - 2 * M
y = 620; d.rectangle((M, y, M + int(BW * 117240 / 162950), y + 340), fill=LG)
d.text((M + 30, y + 24), '공시가 5억', font=C.BHS(84), fill=INK)
d.text((M + 30, y + 150), '117,240원', font=C.BHS(140), fill=INK)
y = 1020; d.rectangle((M, y, M + BW, y + 340), fill=MID, outline=C.YELLOW, width=10)
d.text((M + 30, y + 24), '공시가 9억', font=C.BHS(84), fill=C.WHITE)
d.text((M + 30, y + 140), '?', font=C.BHS(170), fill=C.YELLOW)
d.text((M, 1460), '1세대 1주택 특례율 적용', font=C.BHS(88), fill=C.YELLOW)
d.text((M, 1580), '2026년, 지역가입자 재산 보험료만', font=C.BHS(70), fill=LG)
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cover_v2.png'))
print('ok')
