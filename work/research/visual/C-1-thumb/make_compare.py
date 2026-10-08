# C-1 썸네일 경쟁 비교판 재료 — ep/C-1/compete.md 상위 5(조회는 compete.md 10/8 값) + 우리 롱폼 조회 상위 3(G-1 비교판과 같은 3편)
import json, urllib.request, pathlib
HERE = pathlib.Path(__file__).parent
comp = [  # compete.md 1~5
    dict(who='경쟁', id='XbXfph9KUXY', ch='수페TV', views=187870, title='3억원으로 월 300만원 평생 받는 법 (커버드콜 vs 나스닥100)'),
    dict(who='경쟁', id='3-cTeZHQq68', ch='쩐문가', views=114238, title='"일 안해도 월450 들어와요" 3억으로 은퇴한 40대'),
    dict(who='경쟁', id='Ct5WUuD7uqM', ch='어쩌다마흔', views=37272, title='3억 배당 파이어족? 제발 정신 차리세요'),
    dict(who='경쟁', id='Dda5MOs3DPA', ch='마인드TV', views=16638, title='은퇴 후 주식 팔지 말고 배당만 받아야 할까? 4% 인출 vs 배당생활'),
    dict(who='경쟁', id='z9eQl6OSd84', ch='박대리와 황과장', views=12844, title='은퇴 후 매년 4% 인출, 14년 — VOO 50억, SCHD 34억'),
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
