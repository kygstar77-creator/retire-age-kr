# v9(10/5 00:2x firemap-shorts): v8 6.33(제미나이 5·A 7·레드팀 7) 공통 지적 — '1년 뒤 합계'를 회색 칸 안 '?' 위로(덩어리 6→5), '?' 칸 키움, 질문 줄 150px 올려 쇼츠 아래 제목 가림 구역 피함.
# 맨 위 'SCHD vs JEPQ' 빼고 '1억씩 넣고 1년'을 머리 줄로(종목명 반복 3→2), '세후 분배금'(사실표·설명란과 같은 말),
# 합계는 종목별 막대 대신 중립 회색 칸 하나에 큰 흰 '?'(길이=금액 규칙 안 깨짐), 바탕 짙은 회청색(경쟁 검정·남색과 다르게).
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
BGC = (38, 44, 56); OR = (255, 120, 30); BL = C.BLUE; NEU = (78, 86, 104)
im = Image.new('RGB', (W, H), BGC); d = ImageDraw.Draw(im)
d.text((M, 100), '1억씩 넣고 1년', font=C.BHS(124), fill=C.WHITE)
d.text((M, 320), '세후 분배금', font=C.BHS(92), fill=C.GREY)
BW = W - 2 * M
for k, (lab, v, s, col) in enumerate([('JEPQ', 1005, '1,005만', OR), ('SCHD', 330, '330만', BL)]):
    y = 450 + k * 300
    d.text((M, y), lab + ' ' + s, font=C.BHS(140), fill=col)
    d.rectangle((M, y + 180, M + int(BW * v / 1005), y + 250), fill=col)
pass
d.rounded_rectangle((M, 1070, W - M, 1440), 24, fill=NEU); hd = C.BHS(84); d.text((W / 2 - d.textlength('1년 뒤 합계', font=hd) / 2, 1095), '1년 뒤 합계', font=hd, fill=C.WHITE)
q = C.BHS(250); d.text((W / 2 - d.textlength('?', font=q) / 2, 1170), '?', font=q, fill=C.WHITE)
d.text((M, 1480), '어느 쪽이 클까?', font=C.BHS(140), fill=C.YELLOW)
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cover.png'))
print('ok', M + d.textlength('1억씩 넣고 1년', font=C.BHS(124)))
