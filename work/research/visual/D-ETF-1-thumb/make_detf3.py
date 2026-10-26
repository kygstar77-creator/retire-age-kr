# D-ETF-1 썸네일 3차(10/27 visual) — copywriter 2차 1위 문구(copy/titles.md '썸네일 문구 2차' 10/21 18:54) 그대로, 새 말 없음.
#   흰 줄 'SCHD 한 주당 받는 배당금 · 10년 평균 vs 최근 1년'(SCHD만 크게 — 2차 168px SCHD 0/3→3/3 고친 꼴 유지) / 큰 흰 '11%씩 늘던 배당금' / 큰 주황 '최근엔 2%만 늘었다'(9+9=18자, 알약 없음 C-10).
#   숫자: facts [Y3] SCHD 한 주당 배당 10년 연 10.8%(→11%)·최근 1년 2.0% · 꼴 N-2 thumb_A(C-01), 큰 글 아래 40~45%(C-02), 짙은 그라데이션(상자 없음 C-04).
#   사진(재탕 금지 — a~d와 다른 사진): e = Pexels 9648153 높이 다른 동전 탑 여러 줄(사람·얼굴 없음) · f = Pexels 12920771 미국 25센트 동전(동전에 워싱턴 옆얼굴 새김 — 얼굴 금지라 예비) · 8369695는 암호화폐 무늬라 버림.
#   py -3.12 make_detf3.py → ep/D-ETF-1/thumb_detf_e.png, thumb_detf_f.png
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location('m2', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'make_detf2.py'))
src = open(spec.origin, encoding='utf-8').read().split("\nmake2('thumb_detf_c.png'")[0]
g = {'__file__': spec.origin}; exec(compile(src, spec.origin, 'exec'), g)
g['TOP'] = 'SCHD 한 주당 받는 배당금 · 10년 평균 vs 최근 1년'
g['BIG'] = ['11%씩 늘던 배당금', '최근엔 2%만 늘었다']
from PIL import ImageDraw
def make3(name, pic, y_anchor, zoom=1.0, dark=0.85, schd=190, rest=60):
    f, fit, shade, photo = g['f'], g['fit'], g['shade'], g['photo']; W, HH, X0, LS = g['W'], g['HH'], g['X0'], g['LS']
    im = photo(pic, y_anchor=y_anchor, zoom=zoom, dark=dark); d0 = ImageDraw.Draw(im)
    bs = min(fit(d0, t, 230, 'black') for t in g['BIG'])
    hb = len(g['BIG']) * int(bs * LS); y = HH - 40 - hb
    im = shade(im, max(0, y - 160), HH, 225); im = shade(im, 0, 330, 210, top=True)
    d = ImageDraw.Draw(im); INK = g['INK']
    a, b = 'SCHD', g['TOP'].replace('SCHD ', '')
    fa, fb = f(schd, 'black'), f(rest, '700'); b_ = fit(d, b, rest, '700', maxw=1760 - d.textlength(a, font=fa) - 28); fb = f(b_, '700')
    asc_a = fa.getbbox('SCHD')[3]; asc_b = fb.getbbox('한')[3]
    d.text((X0, 30), a, font=fa, fill=g['WHITE'], stroke_width=5, stroke_fill=INK)
    xa = X0 + d.textlength(a, font=fa) + 28
    d.text((xa, 30 + asc_a - asc_b), b, font=fb, fill=g['WHITE'], stroke_width=3, stroke_fill=INK)
    for k, t in enumerate(g['BIG']):
        d.text((X0, y - int(bs * 0.12)), t, font=f(bs, 'black'), fill=g['WHITE'] if k == 0 else g['ORANGE'], stroke_width=7, stroke_fill=INK)
        y += int(bs * LS)
    out = os.path.join(g['EP'], name); im.resize((1280, 720), g['Image'].LANCZOS).save(out)
    print(out, f'SCHD {schd}px · 윗줄 {b_}px · 큰 글 {bs}px · 덩어리 {hb / HH:.0%}')
make3('thumb_detf_e.png', 'detf_e_9648153.jpg', y_anchor=0.2)
make3('thumb_detf_f.png', 'detf_e_12920771.jpg', y_anchor=0.25)
P = os.path.join(g['PH'], 'sources.json'); s = json.load(open(P, encoding='utf-8'))
s['detf_e_12920771.jpg'] = {'site': 'Pexels', 'id': 12920771, 'by': 'crazy motions', 'url': 'https://www.pexels.com/photo/close-up-photo-of-dollar-coins-12920771/', 'alt': 'Detailed image of stacked silver US quarter coins', 'license': 'Pexels License(무료·상업 이용 가능·출처 표기 의무 없음)', 'face': '없음(사람 없음)'}
s['detf_e_9648153.jpg'] = {'site': 'Pexels', 'id': 9648153, 'by': 'Panos and Marenia Stavrinos', 'url': 'https://www.pexels.com/photo/close-up-shot-of-stacks-of-coins-9648153/', 'alt': 'Close-up of stacked euro coins', 'license': 'Pexels License(무료·상업 이용 가능·출처 표기 의무 없음)', 'face': '없음(사람 없음)'}
json.dump(s, open(P, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
