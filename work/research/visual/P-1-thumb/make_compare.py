# P-1 썸네일 경쟁 비교판 재료 — ep/P-1/compete.md 상위 5(조회는 compete.md 10/9 값) + 우리 롱폼 조회 상위 3(G-1 compare.json과 같은 3편, 10/7 값)
import json, urllib.request, pathlib
HERE = pathlib.Path(__file__).parent
comp = [
    dict(who='경쟁', id='RxGymln5vQo', ch='돈의 심리학', views=15580, title='~받지 마세요(명령형)'),
    dict(who='경쟁', id='OJUjwfzJsXI', ch='리클래스', views=93243, title='고민 끝, 숫자로 정해드립니다'),
    dict(who='경쟁', id='jG3DlA1TpVU', ch='경제포커스', views=9216, title='5년 미루면 2억?'),
    dict(who='경쟁', id='_Wj-RnAxOa0', ch='정치가치관', views=18464, title='68세로 더 늦추자고?'),
    dict(who='경쟁', id='mCwA1tJSU6I', ch='머니인더트랩', views=390782, title='늦게 받을수록 더 준다는데'),
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
