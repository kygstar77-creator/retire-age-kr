# S-1 썸네일(visual 10/29 18시) — N-3 make_n3n.py 복사, 사진·문구만 바꿈(C-35 줄별 폭 85~95%).
#   문구 ep/S-1/copy/titles.md '10/29 고친 판' 1위 그대로: 흰 줄 '2017년부터 삼성전자 실적 발표 날 주가' / 큰 흰 '최대 이익 발표한 날' / 큰 주황 '주가 9번 중 1번만 올랐다' · 알약 없음
#   사실 facts R6(첫 사상 최대 2017-07-07)·9번 중 1번. 사진 Pexels original 27742643(휴대폰 주가 그래프 든 두 손)·35118208(내려가는 봉 차트 화면)·39135247(차트 화면을 짚는 손) — 얼굴 없음, photo/sources.json
import os, sys
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding='utf-8')
O = os.path.dirname(os.path.abspath(__file__)); H = os.path.join(O, 'photo'); WORK = os.path.abspath(os.path.join(O, '..', '..', '..'))
FONT = os.path.join(WORK, 'fonts'); W, HH = 1920, 1080; X0 = 80; MAXW = 1760
ORANGE, WHITE, INK = (255, 90, 0), (255, 255, 255), (10, 11, 14)
BIG = ['최대 이익 발표한 날', '주가 9번 중 1번만 올랐다']
def f(size, w='700'):
    if w == 'black':
        ft = ImageFont.truetype(os.path.join(FONT, 'NotoSansKR-Black.ttf'), size); ft.set_variation_by_name('Black'); return ft
    return ImageFont.truetype(os.path.join(FONT, f'pd{w}.ttf'), size)
def photo(name, y_anchor=0.0, x_anchor=0.5, zoom=1.0):
    im = Image.open(os.path.join(H, name)).convert('RGB'); r = max(W / im.width, HH / im.height) * zoom
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x = int((im.width - W) * x_anchor); y = int((im.height - HH) * y_anchor); return im.crop((x, y, x + W, y + HH))
def shade(im, y0, y1, alpha, top=False):
    m = Image.new('L', im.size, 0); d = ImageDraw.Draw(m)
    for y in range(y0, y1):
        t = (y - y0) / max(1, (y1 - y0) * 0.45) if not top else (y1 - y) / max(1, (y1 - y0) * 0.45)
        d.line([(0, y), (W, y)], fill=int(alpha * min(1, t)))
    return Image.composite(Image.new('RGB', im.size, INK), im, m)
def fit(d, t, size, w, maxw=MAXW, floor=40):
    while size > floor and d.textlength(t, font=f(size, w)) > maxw: size -= 2
    return size
def make(out, pic, ya, top, top_size=96, band=235, ls=1.10, target=0.90, xa=0.5, zoom=1.0, blur=None, top_sizes=None):
    im = photo(pic, y_anchor=ya, x_anchor=xa, zoom=zoom)
    if blur:  # 사진 속 남의 상표 글자(휴대폰 화면 'Apple Inc' 등) 흐리게
        from PIL import ImageFilter; im.paste(im.crop(blur).filter(ImageFilter.GaussianBlur(14)), blur[:2])
    d0 = ImageDraw.Draw(im)
    # C-35: 줄마다 크기 따로 — 폭 target(85~95%)에 맞춤. 둘째 줄 끝은 x 1808(1280판 1205)라 길이 칸(약 1215~)에 안 걸림(C-15)
    sizes = [fit(d0, t, 320, 'black', maxw=int(W * target)) for t in BIG]
    hb = sum(int(s * ls) for s in sizes); y = HH - 30 - hb
    top_size = min(fit(d0, tl, top_size, '700') for tl in top.split('|'))
    tsz = top_sizes or [top_size] * len(top.split('|'))
    im = shade(im, max(0, y - 160), HH, band); im = shade(im, 0, 300, 200, top=True); d = ImageDraw.Draw(im)
    ty = 36
    for tl, ts in zip(top.split('|'), tsz):
        d.text((X0, ty), tl, font=f(ts, '700'), fill=WHITE, stroke_width=4 if ts < 120 else 6, stroke_fill=INK); ty += int(ts * 1.18)
    widths = []
    for k, (t, s) in enumerate(zip(BIG, sizes)):
        bb = d.textbbox((X0, y - int(s * 0.12)), t, font=f(s, 'black'), stroke_width=6); widths.append((bb[2] - bb[0]) / W)
        d.text((X0, y - int(s * 0.12)), t, font=f(s, 'black'), fill=WHITE if k == 0 else ORANGE, stroke_width=6, stroke_fill=INK); y += int(s * ls)
    sm = im.resize((1280, 720), Image.LANCZOS); sm.save(os.path.join(O, out))
    for px in (412, 168): sm.resize((px, px * 9 // 16), Image.LANCZOS).save(os.path.join(O, out.replace('.png', f'_{px}.png')))
    print(out, f'흰 줄 {top_size}px · 큰 글 {sizes}px · 줄별 폭 ' + '·'.join(f'{w:.0%}' for w in widths) + f' · 높이 {hb / HH:.0%}')


T = '2017년부터 삼성전자 실적 발표 날 주가'
make('s1n_a.png', 'phone_chart_hands_27742643.jpg', 0.25, T, blur=(700, 120, 1200, 640))  # 휴대폰 화면 위쪽 종목 이름·숫자
make('s1n_b.png', 'candle_down_35118208.jpg', 0.3, T)
make('s1n_c.png', 'hand_point_chart_39135247.jpg', 0.2, T)
# c2·d(10/29 18:3x 레드팀 c 미통과: 168px에서 '삼성전자' 안 읽힘·초록=상승 외국 차트) — krcolor.py로 한국식 색(빨강 오름·파랑 내림) 바꾼 사진
make('s1n_c2.png', 'hand_point_chart_39135247_kr.jpg', 0.2, T)
# d: 흰 줄 같은 낱말을 두 줄로 — '삼성전자 주가'를 크게(168px에서 회사 이름), 나머지 '2017년부터 실적 발표 날'은 작게. 문구 낱말은 그대로(순서만)
make('s1n_d.png', 'hand_point_chart_39135247_kr.jpg', 0.2, '삼성전자 주가|2017년부터 실적 발표 날', top_sizes=[150, 84])
# d2(10/29 18:2x 새 심사관·레드팀 d: '배경 차트는 오른쪽 위로 오르고 손가락도 꼭대기 — 1번만 올랐다와 반대') — 같은 사진 좌우 뒤집어 오른쪽으로 내려가게
make('s1n_d2.png', 'hand_point_chart_39135247_kr_flip.jpg', 0.2, '삼성전자 주가|2017년부터 실적 발표 날', top_sizes=[150, 84])
