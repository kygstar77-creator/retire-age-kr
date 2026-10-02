# N-1 썸네일 경쟁 비교판 — ep/N-1/compare.md 경쟁 5(조회·배수는 compare.md 값) + 우리 조회 상위 3(E-2 판과 같은 값)
import json, urllib.request, pathlib
from PIL import Image, ImageDraw, ImageFont
HERE = pathlib.Path(__file__).parent
comp = [  # compare.md 1~5
    dict(id='vr5qMqpwPZM', ch='가인지TV', views=526034, mult='x5.74', title='내 연봉은 상위 몇%일까?'),
    dict(id='zjie3J7lIRw', ch='탐구하는 변호사 송현영', views=71012, mult='x7.42', title='순자산 1억·5억·10억, 나는 몇 층일까'),
    dict(id='vJ6VxHMQsyA', ch='연금왕 배형', views=12710, mult='x17.78', title='내 순자산은 상위 10%일까'),
    dict(id='-gcRoQnRARY', ch='억빌더', views=33011, mult='x5.14', title='순자산 10억 | 주식계좌에 1억 있으면'),
    dict(id='Kj8qcEGSJfk', ch='나라투자', views=9359, mult='x4.5', title='순자산 10억이면 상위 몇 %일까'),
]
ours = [
    dict(id='zhTjJwy1mwQ', ch='우리', views=1971, mult='x50.5', title='QQQM과 SCHD 파이어 시뮬레이션'),
    dict(id='wwfFszPl06g', ch='우리', views=1131, mult='x29.0', title='QQQM 딱 하나로 파이어'),
    dict(id='scV67BQvC4Q', ch='우리', views=272, mult='x7.0', title='5억이면 충분합니다'),
]
def grab(vid):
    cache = HERE / 'src' / f'{vid}.jpg'
    if not cache.exists():
        cache.parent.mkdir(exist_ok=True)
        for q in ('maxresdefault', 'hqdefault'):
            try:
                cache.write_bytes(urllib.request.urlopen(f'https://i.ytimg.com/vi/{vid}/{q}.jpg', timeout=20).read()); break
            except Exception: pass
    return Image.open(cache).convert('RGB')
F = 'C:/Windows/Fonts/malgunbd.ttf'
f1, f2 = ImageFont.truetype(F, 22), ImageFont.truetype('C:/Windows/Fonts/malgun.ttf', 18)
W, TH, CAP, PAD = 480, 270, 100, 16
items = [('경쟁', r) for r in comp] + [('우리', r) for r in ours]
cols = 4; nrows = 2
img = Image.new('RGB', (cols * (W + PAD) + PAD, 60 + nrows * (TH + CAP + PAD)), '#f2f4f6')
dr = ImageDraw.Draw(img)
dr.text((PAD, 14), 'N-1 비교: 연봉·순자산 상위 몇% 경쟁 5(compare.md) + 우리 조회 상위 3', font=f1, fill='#191f28')
for i, (who, r) in enumerate(items):
    x, y = PAD + (i % cols) * (W + PAD), 60 + (i // cols) * (TH + CAP + PAD)
    t = grab(r['id']); t = t.resize((W, int(t.height * W / t.width)))
    t = t.crop((0, (t.height - TH) // 2, W, (t.height - TH) // 2 + TH)) if t.height > TH else t
    img.paste(t, (x, y))
    col = '#ff5a00' if who == '우리' else '#191f28'
    dr.text((x, y + TH + 4), f"[{who}] {r['ch'][:14]}", font=f1, fill=col)
    dr.text((x, y + TH + 34), f"조회 {r['views']:,} · 배수 {r['mult']}", font=f2, fill=col)
    dr.text((x, y + TH + 60), r['title'][:28], font=f2, fill='#4e5968')
img.save(HERE / 'compare.png', optimize=True)
json.dump([dict(who=w, **r) for w, r in items], open(HERE / 'compare.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', img.size)
