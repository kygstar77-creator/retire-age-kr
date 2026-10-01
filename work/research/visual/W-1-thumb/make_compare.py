# W-1 주간 리포트 썸네일 경쟁 비교판 — 경쟁 상위 5(채널 중복 없이, 조회순) + 우리 상위 3
import json, io, urllib.request, pathlib
from PIL import Image, ImageDraw, ImageFont
HERE = pathlib.Path(__file__).parent
EP = HERE.parents[1] / 'longform' / 'ep' / 'W-1'
d = json.load(open(EP / 'yt_top.json', encoding='utf-8'))
rows = sorted(d['rows'], key=lambda r: -int(r['views']))
comp, seen = [], set()
for r in rows:
    if r['chid'] in seen: continue
    seen.add(r['chid']); comp.append(r)
    if len(comp) == 5: break
ours = [  # baseline-2026-10-01.md 조회 상위 3
    dict(id='zhTjJwy1mwQ', ch='우리', views=1971, subs=39, title='QQQM과 SCHD 파이어 시뮬레이션'),
    dict(id='wwfFszPl06g', ch='우리', views=1131, subs=39, title='QQQM 딱 하나로 파이어'),
    dict(id='scV67BQvC4Q', ch='우리', views=272, subs=39, title='5억이면 충분합니다'),
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
cols = 4; nrows = (len(items) + cols - 1) // cols
img = Image.new('RGB', (cols * (W + PAD) + PAD, 60 + nrows * (TH + CAP + PAD)), '#f2f4f6')
dr = ImageDraw.Draw(img)
dr.text((PAD, 14), 'W-1 비교: 미국증시 정리·다음주 일정 상위 5(채널당 1) + 우리 조회 상위 3 · yt_top.json 2026-09-30', font=f1, fill='#191f28')
for i, (who, r) in enumerate(items):
    x, y = PAD + (i % cols) * (W + PAD), 60 + (i // cols) * (TH + CAP + PAD)
    t = grab(r['id']); t = t.resize((W, int(t.height * W / t.width)))
    t = t.crop((0, (t.height - TH) // 2, W, (t.height - TH) // 2 + TH)) if t.height > TH else t
    img.paste(t, (x, y))
    col = '#ff5a00' if who == '우리' else '#191f28'
    dr.text((x, y + TH + 4), f"[{who}] {r['ch'][:14]}", font=f1, fill=col)
    dr.text((x, y + TH + 34), f"조회 {int(r['views']):,} · 구독 {int(r['subs']):,} · 배수 {int(r['views'])/max(int(r['subs']),1):.2f}", font=f2, fill=col)
    dr.text((x, y + TH + 60), r['title'][:28], font=f2, fill='#4e5968')
img.save(HERE / 'compare.png', optimize=True)
json.dump([dict(who=w, **{k: r[k] for k in ('id', 'ch', 'views', 'subs', 'title')}) for w, r in items],
          open(HERE / 'compare.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', img.size)
