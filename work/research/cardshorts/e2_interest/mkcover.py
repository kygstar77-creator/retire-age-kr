# v7(01:3x): 제미나이 v6 5 '글자 많다' → 출처·파이어맵 줄 빼고(출처는 카드·설명란) 요소 6개→5개. 총액 줄 84px 유지(레드팀 오해 위험 막음).
# v6(01:2x): 제미나이 v5 5점 '168px에서 작은 글씨 안 읽힘' → 총액 줄 64→84px, 출처 줄 '테슬라 10-Q' 60px(SEC XBRL은 카드·설명란). 나머지 v5 그대로.
# v5(01:0x): v4 6.67(제미나이 6·A 7·레드팀 7) — 레드팀 '번 돈'은 사실표 말 아님 → '이자수익이', 총액 줄 64px·'총액' 노랑. 제목·카드도 단정형으로 맞춤(A).
# v4(01:0x firemap-shorts): v3 6.67(제미나이 7·A 6·레드팀 7) 공통 지적 — ① 화면에 답(422>398)이 다 보이는데 '더 컸다?'로 물어 충돌 → 아래 문구를 단정형+'(이자비용 빼기 전 총액)'으로
# ② 아래 20% 빈칸 → 출처 줄(테슬라 10-Q·SEC XBRL)과 파이어맵 표시 ③ 본 카드와 색 맞춤(이자 노랑·영업 회색 막대) ④ '영업이익보다'(경쟁3 틀) 문구 뺌.
# v2·v3: 두 숫자 같은 크기·0 기준선 막대 두 개·회청색 바탕·'<' 뺌. 숫자는 E-2 facts [3]·[13] 그대로, 막대 = 값/422.
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
BGC = (38, 44, 56); GR = (150, 158, 175); LG = (200, 205, 215)
im = Image.new('RGB', (W, H), BGC); d = ImageDraw.Draw(im)
d.text((M, 110), '테슬라 2분기 실적', font=C.BHS(124), fill=C.WHITE)
d.text((M, 262), '단위 백만 달러', font=C.BHS(76), fill=LG)
BW = W - 2 * M
for k, (lab, v, col, tcol) in enumerate([('이자수익', 422, C.YELLOW, C.YELLOW), ('영업이익', 398, GR, C.WHITE)]):
    y = 400 + k * 400
    d.text((M, y), f'{lab} {v}', font=C.BHS(150), fill=tcol)
    d.rectangle((M, y + 185, M + int(BW * v / 422), y + 315), fill=col)
d.line((M, 580, M, 1120), fill=LG, width=6)   # 0 기준선
d.text((M, 1210), '이자수익이', font=C.BHS(130), fill=C.WHITE)
d.text((M, 1360), '더 컸어요', font=C.BHS(130), fill=C.YELLOW)
f64 = C.BHS(84); a = '이자비용 빼기 전 '; d.text((M, 1515), a, font=f64, fill=LG); d.text((M + d.textlength(a, font=f64), 1515), '총액', font=f64, fill=C.YELLOW)
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cover_v7.png'))
print('ok')
