# npsday1007 표지 v4 (firemap-shorts 10/6) — 경계 한정 문구·라벨 키움·출처 줄 삭제·잘림 방지(폭 검사)
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
from PIL import Image, ImageDraw
import cardshort as C
W, H = 1080, 1920; M = 64
BGC = (40, 34, 58); GR = (168, 164, 184); INK = (20, 18, 28)
im = Image.new('RGB', (W, H), BGC); d = ImageDraw.Draw(im)
def T(xy, s, sz, fill):
    f = C.BHS(sz); w = d.textlength(s, font=f); assert xy[0] + w <= W - M + 4, (s, w)
    d.text(xy, s, font=f, fill=fill)
T((M, 110), '국민연금 수령나이', 112, C.WHITE)
T((M, 290), '경계 하루,', 150, C.YELLOW)
T((M, 480), '시작은 1년 차이', 118, C.YELLOW)
for k, (lab, num, col) in enumerate([('1968년 12월 31일생', '64세', GR), ('1969년 1월 1일생', '65세', C.YELLOW)]):
    y = 720 + k * 460
    d.rectangle((M, y, W - M, y + 420), fill=col)
    T((M + 30, y + 24), lab, 100, INK)
    T((M + 30, y + 150), num + '부터', 230, INK)
T((M, 1690), '가입 10년 이상 기준', 70, (210, 206, 222))
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cover_v4.png')); print('ok')
