# H-1 썸네일 경쟁 비교판 재료 — ep/H-1/compete.md 상위 5(조회 10/11 값) + 우리 롱폼 조회 상위 3(P-1 compare.json과 같은 3편)
import json, urllib.request, pathlib
HERE = pathlib.Path(__file__).parent
comp = [
    dict(who='경쟁', id='VLj3irGy-ic', ch='쇼킹부동산', views=18609, title='헬리오시티 VS 올림픽파크포레온 완벽 분석'),
    dict(who='경쟁', id='1IKLm6u2-H8', ch='돈불리GO', views=3104, title='30억으로 어디 살까? 정면 비교'),
    dict(who='경쟁', id='F9i-pHSY9cI', ch='경제/부동산 뉴스룸', views=9089, title='33억이 26억으로 주저앉았습니다'),
    dict(who='경쟁', id='zJVjmpTH7ys', ch='서울꿈', views=4005, title='헬리오시티 8억 하락 거래 현장'),
    dict(who='경쟁', id='w-lRWKUPPWw', ch='쇼킹부동산', views=25849, title='고덕·명일·상일 사기 전에 꼭'),
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
