# e1_micron_q4 쇼츠 첫 1초 표지 시안 3개 — firemap-visual-designer 10/3 02:0x
# 숫자는 ep/E-1/facts.txt [11]·[12]만: 6월 전망 490~510억$, 실제 542억 2,900만$, 1년 전 113억 1,500만$, 4.79배, 전망 상단보다 32억 3천만$.
# 막대는 0에서 시작(축 자르기 금지). 1080x1920, 쇼츠 가림 자리(위 140·아래 380·오른쪽 150) 밖에만 글자.
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(H, '..', '..', '..', 'fonts')
W, HH = 1080, 1920; M = 64; SAFE_R, SAFE_B = 930, 1540
BG = (16, 18, 24); WHITE = (246, 246, 250); YELLOW = (255, 208, 0); GREY = (120, 126, 140); ORANGE = (255, 107, 0); DIM = (60, 64, 76)
f = lambda n, s: ImageFont.truetype(os.path.join(FD, n), s)
BHS = lambda s: f('BlackHanSans.ttf', s); PD7 = lambda s: f('pd700.ttf', s); PD5 = lambda s: f('pd500.ttf', s)

def base():
    im = Image.new('RGB', (W, HH), BG); d = ImageDraw.Draw(im)
    d.rounded_rectangle((M, 150, M + 190, 208), 12, fill=ORANGE); d.text((M + 22, 158), '파이어맵', font=PD7(36), fill=WHITE)
    return im, d

def fit(d, txt, s, maxw=SAFE_R - M):
    while d.textlength(txt, font=BHS(s)) > maxw: s -= 4
    return s

def m1():
    """전망 띠 위로 뚫고 나간 막대 — 반전(회사 전망을 회사가 넘음)."""
    im, d = base()
    d.text((M, 260), '마이크론 매출', font=BHS(fit(d, '마이크론 매출', 150)), fill=WHITE)
    d.text((M, 440), '회사 전망 뚫었다', font=BHS(fit(d, '회사 전망 뚫었다', 150)), fill=YELLOW)
    # 세로 막대 두 개(0부터): 1년 전 113, 이번 542 · 전망 490~510 띠
    x0, base_y, top_y = M + 40, 1330, 700; scale = (base_y - top_y) / 560
    yv = lambda v: base_y - v * scale
    d.rectangle((M, yv(510), SAFE_R, yv(490)), fill=(70, 60, 20))
    d.line((M, yv(510), SAFE_R, yv(510)), fill=YELLOW, width=6)
    d.text((M + 10, yv(510) - 70), '6월 전망 최대 510', font=PD7(50), fill=YELLOW)
    bw = 250
    d.rectangle((x0, yv(113), x0 + bw, base_y), fill=GREY)
    bx = x0 + 380; d.rectangle((bx, yv(542), bx + bw, base_y), fill=WHITE)
    d.rectangle((bx, yv(542), bx + bw, yv(510)), fill=YELLOW)
    d.line((M, base_y, SAFE_R, base_y), fill=DIM, width=4)
    d.text((x0, yv(113) - 70), '113', font=PD7(60), fill=WHITE)
    d.text((bx + 10, yv(542) - 100), '542', font=BHS(110), fill=YELLOW)
    d.text((x0, base_y + 16), '1년 전', font=PD7(52), fill=GREY); d.text((bx, base_y + 16), '이번 분기', font=PD7(52), fill=WHITE)
    d.text((M, base_y + 110), '단위 억 달러 · SEC 8-K 원문', font=PD5(44), fill=GREY)
    return im

def m2():
    """큰 숫자 하나 4.79배 + 두 막대."""
    im, d = base()
    d.text((M, 270), '마이크론 매출 1년 새', font=BHS(fit(d, '마이크론 매출 1년 새', 120)), fill=WHITE)
    d.text((M, 400), '4.79배', font=BHS(300), fill=YELLOW)
    base_y, top_y = 1360, 800; scale = (base_y - top_y) / 560; yv = lambda v: base_y - v * scale
    x0 = M + 40; bw = 280
    d.rectangle((x0, yv(113), x0 + bw, base_y), fill=GREY); d.text((x0, yv(113) - 72), '113', font=PD7(62), fill=WHITE)
    bx = x0 + 420; d.rectangle((bx, yv(542), bx + bw, base_y), fill=YELLOW); d.text((bx, yv(542) - 76), '542', font=PD7(66), fill=YELLOW)
    d.line((M, base_y, SAFE_R, base_y), fill=DIM, width=4)
    d.text((x0, base_y + 16), '1년 전 분기', font=PD7(48), fill=GREY); d.text((bx, base_y + 16), '이번 분기', font=PD7(48), fill=WHITE)
    d.text((M, base_y + 100), '억 달러 · 6월 회사 전망(최대 510)도 넘김', font=PD5(42), fill=GREY)
    return im

def m3():
    """예상 vs 실제 두 숫자 맞대기 — 비교."""
    im, d = base()
    d.text((M, 270), '마이크론 4분기 매출', font=BHS(fit(d, '마이크론 4분기 매출', 120)), fill=WHITE)
    d.text((M, 470), '회사 예상 최대', font=PD7(66), fill=GREY)
    d.text((M, 550), '510', font=BHS(260), fill=GREY)
    d.line((M, 850, SAFE_R, 850), fill=DIM, width=4)
    d.text((M, 900), '실제', font=PD7(66), fill=YELLOW)
    d.text((M, 980), '542', font=BHS(330), fill=YELLOW)
    d.text((M + d.textlength('542', font=BHS(330)) + 24, 1180), '억 달러', font=PD7(70), fill=YELLOW)
    d.text((M, 1380), '6월 전망 → 9월 30일 발표', font=PD7(54), fill=WHITE)
    d.text((M, 1450), 'SEC 8-K 원문', font=PD5(44), fill=GREY)
    return im

for n, fn in (('m1', m1), ('m2', m2), ('m3', m3)):
    im = fn(); im.save(os.path.join(H, f'cover_{n}.png'))
    im.resize((168, 299), Image.LANCZOS).save(os.path.join(H, f'cover_{n}_168.png'))
print('ok')

# ---- 2차(02:2x): 심사 1차 평균 m1 6.83·m3 6.67·m2 6.5 → 지적 반영. m2(4.79배)는 14주 vs 13주로 부풀어 보인다(레드팀) → 뺌.
LG = (190, 196, 208)
def m4():
    """m3 고침: 라벨 90px+, 510에도 억 달러, 차이 +32억 달러를 상자로."""
    im, d = base()
    d.text((M, 250), '마이크론 4분기 매출', font=BHS(fit(d, '마이크론 4분기 매출', 120)), fill=WHITE)
    d.text((M, 430), '회사 6월 예상 최대', font=BHS(92), fill=LG)
    d.text((M, 530), '510', font=BHS(230), fill=LG); d.text((M + d.textlength('510', font=BHS(230)) + 20, 680), '억 달러', font=BHS(80), fill=LG)
    d.text((M, 810), '실제 발표', font=BHS(100), fill=YELLOW)
    d.text((M, 910), '542', font=BHS(330), fill=YELLOW); d.text((M + d.textlength('542', font=BHS(330)) + 20, 1130), '억 달러', font=BHS(90), fill=YELLOW)
    d.rounded_rectangle((M, 1290, M + 640, 1420), 20, fill=YELLOW); d.text((M + 30, 1302), '+32억 달러 더', font=BHS(96), fill=BG)
    d.text((M, 1450), 'SEC 8-K 원문 · 회사 전망 대비', font=PD7(48), fill=GREY)
    return im

def m5():
    """m1 고침: 넘었다, 막대 회색, 넘친 부분 노랑+'+32억$', 542억$ 크게."""
    im, d = base()
    d.text((M, 250), '마이크론 매출', font=BHS(fit(d, '마이크론 매출', 140)), fill=WHITE)
    d.text((M, 420), '회사 전망 넘었다', font=BHS(fit(d, '회사 전망 넘었다', 140)), fill=YELLOW)
    base_y = 1480; scale = 1.33; yv = lambda v: base_y - v * scale
    bx, bw = M + 20, 330
    d.rectangle((bx, yv(510), bx + bw, base_y), fill=(88, 94, 108))
    d.rectangle((bx, yv(542), bx + bw, yv(510)), fill=YELLOW)
    d.line((M, yv(510), SAFE_R, yv(510)), fill=WHITE, width=6)
    tx = bx + bw + 30
    d.text((tx, yv(542) - 120), '542억$', font=BHS(150), fill=YELLOW)
    d.text((tx, yv(510) + 20), '회사 6월 전망', font=BHS(78), fill=WHITE)
    d.text((tx, yv(510) + 110), '최대 510억$', font=BHS(78), fill=WHITE)
    d.rounded_rectangle((tx, yv(510) + 230, tx + 430, yv(510) + 340), 18, fill=YELLOW); d.text((tx + 22, yv(510) + 238), '+32억$', font=BHS(92), fill=BG)
    d.text((M, base_y + 20), 'SEC 8-K 원문 · 막대 0부터', font=PD7(44), fill=GREY)
    return im

for n, fn in (('m4', m4), ('m5', m5)):
    im = fn(); im.save(os.path.join(H, f'cover_{n}.png'))

# ---- 3차(02:4x): m4 6.5(제미나이 5 '글이 많다'·Claude 7.5 '더 크게'·레드팀 7 '510·542 크기 차가 6%를 과장') → m6
def m6():
    im, d = base()
    d.text((M, 250), '마이크론 4분기 매출', font=BHS(fit(d, '마이크론 4분기 매출', 124)), fill=WHITE)
    for y, lab, num, col in ((460, '회사 예상 최대', '510억$', LG), (820, '실제', '542억$', YELLOW)):
        d.text((M, y), lab, font=BHS(96), fill=col)
        d.text((M, y + 100), num, font=BHS(fit(d, '510억$', 250)), fill=col)
    d.rounded_rectangle((M, 1230, M + 720, 1390), 24, fill=YELLOW); d.text((M + 36, 1246), '+32억$ 더', font=BHS(124), fill=BG)
    d.text((M, 1430), 'SEC 8-K 원문', font=PD7(50), fill=GREY)
    return im
im = m6(); im.save(os.path.join(H, 'cover_m6.png'))

# ---- 4차(10/3 visual): 레드팀 사실 정확도 지적 반영(review.md 17행) — '회사 예상'→'회사 6월 전망', '4분기'→'회계 4분기', 'SEC 8-K 원문' 줄 뺌. 배치·크기는 m6 그대로
def m7():
    im, d = base()
    d.text((M, 250), '마이크론 회계 4분기 매출', font=BHS(fit(d, '마이크론 회계 4분기 매출', 124)), fill=WHITE)
    for y, lab, num, col in ((460, '회사 6월 전망 최대', '510억$', LG), (820, '실제', '542억$', YELLOW)):
        d.text((M, y), lab, font=BHS(fit(d, '회사 6월 전망 최대', 96)), fill=col)
        d.text((M, y + 100), num, font=BHS(fit(d, '510억$', 250)), fill=col)
    d.rounded_rectangle((M, 1230, M + 720, 1390), 24, fill=YELLOW); d.text((M + 36, 1246), '+32억$ 더', font=BHS(124), fill=BG)
    return im
if __name__ == '__main__' and 'm7' in sys.argv:
    im = m7(); im.save(os.path.join(H, 'cover_m7.png')); im.resize((168, round(168 * im.height / im.width))).save(os.path.join(H, 'cover_m7_168.png'))
