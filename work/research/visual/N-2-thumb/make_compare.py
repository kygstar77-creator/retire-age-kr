# N-2 썸네일 경쟁 비교판 재료 — ep/N-2/compete.md 상위 5(조회는 compete.md 10/11 값) + 우리 최근 확정 썸네일 5(바탕 겹침 확인용, 10/12 교훈)
import json, urllib.request, pathlib, shutil
HERE = pathlib.Path(__file__).parent; EP = HERE.parent.parent / 'longform' / 'ep'
comp = [
    dict(who='경쟁', id='vr5qMqpwPZM', ch='가인지TV', views=566082),
    dict(who='경쟁', id='zwbPgDs11OM', ch='송현영', views=412821),
    dict(who='경쟁', id='6FuD_U-HVWw', ch='슈카월드', views=1070187),
    dict(who='경쟁', id='BigDizC2mwg', ch='가인지TV', views=683830),
    dict(who='경쟁', id='PAqQEOEPWC0', ch='머니노트', views=4),
]
ours = {'N-1': 'thumb_n1l.png', 'P-1': 'thumb_p2z.png', 'W-1': 'thumb_w1p.png', 'R-1': 'thumb_r2i.png', 'H-1': 'thumb_h1k.png'}
(HERE / 'src').mkdir(exist_ok=True)
for r in comp:
    cache = HERE / 'src' / f"{r['id']}.jpg"
    if not cache.exists():
        for q in ('maxresdefault', 'hqdefault'):
            try: cache.write_bytes(urllib.request.urlopen(f"https://i.ytimg.com/vi/{r['id']}/{q}.jpg", timeout=20).read()); break
            except Exception: pass
    print(r['id'], cache.exists())
for e, f in ours.items():
    shutil.copy(EP / e / f, HERE / 'src' / f'our_{e}.png'); comp.append(dict(who='우리', id=f'our_{e}', ch=e, views=None))
json.dump(comp, open(HERE / 'compare.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
