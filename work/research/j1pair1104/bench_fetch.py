# 2026-11-03 firemap-write: 가까운 카페 주간 인기글에서 종부세·보유세 글 찾기 (SKILL '잘되는 카페 글 꼴' 경쟁 글 고르기)
import json, os, sys, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
IDS = {'배투모': 31050378, '은오': 23676262, '월재연': 22290117, '짠돌이': 14028420, '정가거부': 30786704,
       '평생ETF': 31097286, '티끌': 30852806, '미주미': 28497937, '노후연구소': 20898041}
KW = ('종부세', '종합부동산', '보유세', '공시가격', '재산세')
out = []
for name, cid in IDS.items():
    u = f'https://apis.naver.com/cafe-web/cafe2/WeeklyPopularArticleList.json?cafeId={cid}'
    r = urllib.request.Request(u, headers={'Referer': 'https://m.cafe.naver.com/'})
    try:
        d = json.loads(urllib.request.urlopen(r, timeout=20).read().decode('utf-8'))
    except Exception as e:
        print(name, 'ERR', e); continue
    json.dump(d, open(os.path.join(HERE, 'bench_raw', f'weekly_{cid}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    arts = d.get('message', {}).get('result', {}).get('popularArticleList', [])
    print(name, len(arts))
    for a in arts:
        t = a.get('subject', '')
        if any(k in t for k in KW):
            out.append((name, cid, a.get('articleId'), t, a.get('readCount'), a.get('commentCount'), a.get('likeItCount')))
for o in out: print(o)
