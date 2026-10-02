# a1_need100 첫 1초 표지 3차 — firemap-shorts 10/3 04:1x (순돌이 03:5x 지시: e1_micron_q4 m6처럼 큰 숫자·주제 3~6단어)
# 마이너스는 BlackHanSans에 U+2212 글자가 없어 '-'로 씀.
# 숫자는 longform/ep/A-1/facts.txt [6]의 따옴표 표기 그대로: SCHD "4억 4천만원", KODEX 200타겟위클리커버드콜 "7,900만원", [13] yieldMon3 -19.95%.
# 틀: visual/micron-cover/make_covers.py m6(7.00 통과) — 같은 크기 두 숫자, 아래 상자 하나. 1080x1920, SAFE_R 930·SAFE_B 1540.
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); FD = os.path.join(H, '..', '..', '..', '..', 'fonts')
W, HH = 1080, 1920; M = 64; SAFE_R = 930
BG = (16, 18, 24); WHITE = (246, 246, 250); YELLOW = (255, 208, 0); GREY = (120, 126, 140); ORANGE = (255, 107, 0); LG = (190, 196, 208)
f = lambda n, s: ImageFont.truetype(os.path.join(FD, n), s)
BHS = lambda s: f('BlackHanSans.ttf', s); PD7 = lambda s: f('pd700.ttf', s)
def fit(d, t, s, maxw=SAFE_R - M):
    while d.textlength(t, font=BHS(s)) > maxw: s -= 4
    return s
def make(box, foot):
    im = Image.new('RGB', (W, HH), BG); d = ImageDraw.Draw(im)
    d.rounded_rectangle((M, 150, M + 190, 208), 12, fill=ORANGE); d.text((M + 22, 158), '파이어맵', font=PD7(36), fill=WHITE)
    d.text((M, 250), '세후 월 100만원 배당', font=BHS(fit(d, '세후 월 100만원 배당', 124)), fill=WHITE)
    d.text((M, 400), '필요한 원금', font=BHS(96), fill=WHITE)
    ns = fit(d, '4억 4천만원', 230)
    for y, lab, num, col in ((560, 'SCHD', '4억 4천만원', LG), (900, 'KODEX 200타겟위클리커버드콜', '7,900만원', YELLOW)):
        d.text((M, y), lab, font=BHS(fit(d, lab, 84)), fill=col)
        d.text((M, y + 100), num, font=BHS(ns), fill=col)
    bw = d.textlength(box, font=BHS(110)) + 72
    d.rounded_rectangle((M, 1250, M + bw, 1400), 24, fill=YELLOW); d.text((M + 36, 1266), box, font=BHS(110), fill=BG)
    d.text((M, 1430), foot, font=PD7(46), fill=GREY)
    return im
for n, box, foot in (('n1', '3개월 -19.95%', '7,900만원 쪽 · 2026.9.28 공시'), ('n2', '왜 이렇게 차이?', '최근 12개월 분배금 기준 · 2026.9.28')):
    im = make(box, foot); im.save(os.path.join(H, f'cover_{n}.png')); im.resize((168, 299), Image.LANCZOS).save(os.path.join(H, f'cover_{n}_168.png'))
print('ok')

# ---- 2차(04:2x): 제미나이 n1 6·n2 5 '글이 많다, 핵심 대비만 크게, VS' → 제목 한 줄, 숫자 둘을 더 크게, 상품 전체 이름은 숫자 아래 작게(레드팀 10/2 '커버드콜 한 단어 뭉뚱그림' 방지), 잔글씨 뺌.
def make2(box):
    im = Image.new('RGB', (W, HH), BG); d = ImageDraw.Draw(im)
    d.rounded_rectangle((M, 150, M + 190, 208), 12, fill=ORANGE); d.text((M + 22, 158), '파이어맵', font=PD7(36), fill=WHITE)
    d.text((M, 250), '세후 월 100만원 배당 원금', font=BHS(fit(d, '세후 월 100만원 배당 원금', 130)), fill=WHITE)
    ns = fit(d, '4억 4천만', 270)
    d.text((M, 440), '4억 4천만', font=BHS(ns), fill=LG); d.text((M, 730), 'SCHD', font=BHS(76), fill=LG)
    d.text((M, 850), 'vs', font=BHS(90), fill=GREY)
    d.text((M, 960), '7,900만', font=BHS(ns), fill=YELLOW); d.text((M, 1250), 'KODEX 200타겟위클리커버드콜', font=BHS(fit(d, 'KODEX 200타겟위클리커버드콜', 60)), fill=YELLOW)
    bw = d.textlength(box, font=BHS(100)) + 72
    d.rounded_rectangle((M, 1350, M + bw, 1490), 24, fill=YELLOW); d.text((M + 36, 1364), box, font=BHS(100), fill=BG)
    return im
for n, box in (('n3', '왜 이렇게 차이?'), ('n4', '3개월 -19.95%')):
    im = make2(box); im.save(os.path.join(H, f'cover_{n}.png'))
print('ok2')

# ---- 3차(04:3x): n3 5·n4 5 '정보 문장형 머리는 스크롤을 못 멈춤, 168px에서 머리글 작음' → 머리 두 줄 크게(질문), 숫자 둘만, 상자·잔글씨 없음.
def make3():
    im = Image.new('RGB', (W, HH), BG); d = ImageDraw.Draw(im)
    d.rounded_rectangle((M, 150, M + 190, 208), 12, fill=ORANGE); d.text((M + 22, 158), '파이어맵', font=PD7(36), fill=WHITE)
    hs = fit(d, '세후 월 100만원', 170)
    d.text((M, 240), '세후 월 100만원', font=BHS(hs), fill=WHITE); d.text((M, 420), '배당 원금은?', font=BHS(hs), fill=WHITE)
    ns = fit(d, '4억 4천만', 250)
    d.text((M, 660), '4억 4천만', font=BHS(ns), fill=LG); d.text((M, 930), 'SCHD', font=BHS(80), fill=LG)
    d.text((M, 1080), '7,900만', font=BHS(ns), fill=YELLOW); d.text((M, 1350), 'KODEX 200타겟위클리커버드콜', font=BHS(fit(d, 'KODEX 200타겟위클리커버드콜', 60)), fill=YELLOW)
    return im
make3().save(os.path.join(H, 'cover_n5.png')); print('ok3')

# ---- 4차(04:2x): n3 = Claude 7·레드팀 7.5·제미나이 lite 5. 공통 지적 → 이름표를 숫자 위로('SCHD vs 7,900만' 이어 읽힘 방지), 기준 줄(최근 12개월 분배금 유지 가정) 추가.
def make4():
    im = Image.new('RGB', (W, HH), BG); d = ImageDraw.Draw(im)
    d.rounded_rectangle((M, 150, M + 190, 208), 12, fill=ORANGE); d.text((M + 22, 158), '파이어맵', font=PD7(36), fill=WHITE)
    d.text((M, 240), '세후 월 100만원 배당 원금', font=BHS(fit(d, '세후 월 100만원 배당 원금', 130)), fill=WHITE)
    ns = fit(d, '4억 4천만', 250)
    d.text((M, 420), 'SCHD', font=BHS(84), fill=LG); d.text((M, 520), '4억 4천만', font=BHS(ns), fill=LG)
    d.text((M, 800), 'vs', font=BHS(80), fill=GREY)
    d.text((M, 910), 'KODEX 200타겟위클리커버드콜', font=BHS(fit(d, 'KODEX 200타겟위클리커버드콜', 64)), fill=YELLOW)
    d.text((M, 990), '7,900만', font=BHS(ns), fill=YELLOW)
    box = '왜 이렇게 차이?'; bw = d.textlength(box, font=BHS(100)) + 72
    d.rounded_rectangle((M, 1290, M + bw, 1430), 24, fill=YELLOW); d.text((M + 36, 1304), box, font=BHS(100), fill=BG)
    d.text((M, 1460), '최근 12개월 분배금 유지 가정 · 2026.9.28', font=PD7(44), fill=GREY)
    return im
make4().save(os.path.join(H, 'cover_n6.png')); print('ok4')

# ---- 5차(04:2x): n6 = Claude 7.5·레드팀 7.5·제미나이 lite 5(두 번) = 6.67. 제미나이·Claude 공통 '맨 윗줄이 168px에서 작다', 제미나이 '왜 이렇게 차이? 모호' → 머리 두 줄로 키우고 상자 뺌(후킹=vs 비교), 기준 줄은 남김(레드팀 조건).
def make5():
    im = Image.new('RGB', (W, HH), BG); d = ImageDraw.Draw(im)
    d.rounded_rectangle((M, 150, M + 190, 208), 12, fill=ORANGE); d.text((M + 22, 158), '파이어맵', font=PD7(36), fill=WHITE)
    hs = fit(d, '세후 월 100만원', 160)
    d.text((M, 235), '세후 월 100만원', font=BHS(hs), fill=WHITE); d.text((M, 400), '배당 원금', font=BHS(hs), fill=WHITE)
    ns = fit(d, '4억 4천만', 250)
    d.text((M, 600), 'SCHD', font=BHS(84), fill=LG); d.text((M, 690), '4억 4천만', font=BHS(ns), fill=LG)
    d.text((M, 890), 'vs', font=BHS(80), fill=GREY)
    d.text((M, 1000), 'KODEX 200타겟위클리커버드콜', font=BHS(fit(d, 'KODEX 200타겟위클리커버드콜', 60)), fill=YELLOW)
    d.text((M, 1080), '7,900만', font=BHS(ns), fill=YELLOW)
    d.text((M, 1440), '최근 12개월 분배금 유지 가정 · 2026.9.28', font=PD7(44), fill=GREY)
    return im
make5().save(os.path.join(H, 'cover_n7.png')); print('ok5')
