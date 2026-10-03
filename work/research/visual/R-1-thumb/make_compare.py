# R-1 썸네일 경쟁 비교판 — ep/R-1/compare.md 경쟁 5(조회·배수는 compare.md 값) + 우리 조회 상위 3(E-2 판과 같은 값)
import json, urllib.request, pathlib
from PIL import Image, ImageDraw, ImageFont
HERE = pathlib.Path(__file__).parent
comp = [  # ep/R-1/compare.md 1~5
    dict(id='QtciAE40DlU', ch='알아두면 경제TV', views=29015, mult='x69.9', title='50대에 현금 1억이 생긴다면'),
    dict(id='lSmbW1Par1M', ch='돈길연구소', views=8802, mult='x91.7', title='N월 파킹통장 추천 금액별 1등'),
    dict(id='gosYz3ho038', ch='단희TV', views=1390147, mult='x1.45', title='10억 예금하면 매달 이 금액'),
    dict(id='LjHlXKeRH5s', ch='야무진 경제학', views=114069, mult='x5.09', title='노후자금 구멍 5개'),
    dict(id='tFS9Ga_v5_U', ch='나두시니어', views=11322, mult='x4.94', title='은행·저축은행 예적금 금리 Top5'),
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
dr.text((PAD, 14), 'R-1 비교: 1억 예금·1년 경쟁 5(compare.md) + 우리 조회 상위 3', font=f1, fill='#191f28')
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
