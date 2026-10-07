# G-1 썸네일 경쟁 비교판 재료 — ep/G-1/compete.md 상위 5(조회는 compete.md 값) + 우리 롱폼 조회 상위 3(ytanalytics recent 28, 10/7 09시)
import json, urllib.request, pathlib
HERE = pathlib.Path(__file__).parent
comp = [  # compete.md 1~5
    dict(who='경쟁', id='ZlGbs_sIbQg', ch='SBS 뉴스', views=4131912, title="금값 '최저' 찍었다, 왜 이래"),
    dict(who='경쟁', id='lE9yv1C-Ffk', ch='KBS News', views=604545, title='"한 돈에 110만 원 했는데" 금값 폭락'),
    dict(who='경쟁', id='Bfn9yDoe_bM', ch='SBS Biz', views=265508, title='급락하는데, 한은은 1톤 산다'),
    dict(who='경쟁', id='Xu4oVwGj_QU', ch='경제야', views=927, title='국제 금값은 올랐는데 내 금은 -11%'),
    dict(who='경쟁', id='Vb5JModMdh4', ch='경제읽는오리', views=4705, title='금값이 올라도 돈을 잃습니다'),
    dict(who='우리', id='SCOI0DP-l-s', ch='파이어맵 A-1', views=2382, title='A-1'),
    dict(who='우리', id='scV67BQvC4Q', ch='파이어맵', views=176, title=''),
    dict(who='우리', id='420buEFKB8k', ch='파이어맵', views=69, title=''),
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
json.dump(comp, open(HERE / 'compare.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
