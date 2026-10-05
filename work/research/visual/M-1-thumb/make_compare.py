# M-1 썸네일 경쟁 비교판 — ep/M-1/compete.md 30일 상위 5(조회는 compete.md 값, yt_top30.json)
import json, urllib.request, pathlib
HERE = pathlib.Path(__file__).parent
comp = [  # compete.md 1~5
    dict(id='wWzZWzS3cKM', ch='잼투리', views=179230, title='커버드콜 경고(JEPQ)'),
    dict(id='avtqvUjq6dc', ch='부티플', views=110879, title='매달 100만원이면 됩니다 5060 ETF'),
    dict(id='-Lw12k4u8m8', ch='김범곤의 연금수업', views=90473, title='월 100만 원 배당받으려면 얼마가 필요할까?'),
    dict(id='BmIpyeXKc20', ch='연금 받는 형', views=35242, title='수익률에 속지 마세요'),
    dict(id='bmplJE7gCpA', ch='경제기상도', views=21872, title='매달 100만원, 3억 만드는 데 걸린 시간'),
]
for r in comp:
    cache = HERE / 'src' / f"{r['id']}.jpg"
    if not cache.exists():
        cache.parent.mkdir(exist_ok=True)
        for q in ('maxresdefault', 'hqdefault'):
            try:
                cache.write_bytes(urllib.request.urlopen(f"https://i.ytimg.com/vi/{r['id']}/{q}.jpg", timeout=20).read()); break
            except Exception: pass
    print(r['id'], cache.exists())
json.dump([dict(who='경쟁', **r) for r in comp], open(HERE / 'compare.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
