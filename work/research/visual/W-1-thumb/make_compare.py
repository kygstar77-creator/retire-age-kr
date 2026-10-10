# W-1 썸네일 경쟁 비교판 재료 (2026-10-10 visual-designer) — ep/W-1/compete.md 상위 5(같은 주제 '삼성전자 실적 코스피 하락', 최근 30일 조회순) + 우리 롱폼 조회 상위 3
# 10/1 틀 잡기 때 쓴 '미국증시 정리' 5장은 old1001/에 둠(주제가 W-1 1화와 달라 이번 판정에 안 씀).
import json, urllib.request, pathlib
HERE = pathlib.Path(__file__).parent
comp = [
    dict(who='경쟁', id='IqwNtfVL8Vg', ch='1분썰배달', views=34439, title="숫자 찍은 날, 주가는 오히려 하락?!"),
    dict(who='경쟁', id='ukM-9TlxLv4', ch='SBS Biz 뉴스', views=244237, title='[주간증시전망] 5% 급락'),
    dict(who='경쟁', id='O7buSsw-IDE', ch='에디', views=134595, title='동반 하락, 지금 무슨 일이'),
    dict(who='경쟁', id='MNF1cNdD6ko', ch='에디', views=100586, title='잘 오르던 ~, 갑자기 하락한 이유'),
    dict(who='경쟁', id='xLwih1CCpoY', ch='에디', views=83701, title='사상 최고가! ~ 하락, 걱정할 필요 없는 이유'),
    dict(who='우리', id='SCOI0DP-l-s', ch='파이어맵 A-1', views=2382, title='A-1'),
    dict(who='우리', id='zhTjJwy1mwQ', ch='파이어맵', views=1971, title='QQQM과 SCHD 파이어 시뮬레이션'),
    dict(who='우리', id='wwfFszPl06g', ch='파이어맵', views=1131, title='QQQM 딱 하나로 파이어'),
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
