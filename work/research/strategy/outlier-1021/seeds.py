# 시드별 수확: 그 검색 결과 50편 중 '구독 1만 미만 + 조회÷구독 10배 이상' 영상 수
import json, sys, os, statistics
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
c = json.load(open(os.path.join(H,'cache_search.json'),encoding='utf-8')); ch = json.load(open(os.path.join(H,'channels.json'),encoding='utf-8'))
vd = json.load(open(os.path.join(H,'videos.json'),encoding='utf-8'))
views = {v['id']: v['views'] for vs in vd.values() for v in vs}
res = []
for q, vs in c.items():
    hit = []
    for v in vs:
        s = (ch.get(v['cid']) or {}).get('subs')
        if s is None or s >= 1e4 or v['id'] not in views: continue
        if views[v['id']] / max(s,1) >= 10 and views[v['id']] >= 3000: hit.append((views[v['id']], s, v['title']))
    res.append(dict(seed=q, n=len(vs), small_hits=len(hit), best=sorted(hit, reverse=True)[:2]))
res.sort(key=lambda r: -r['small_hits'])
json.dump(res, open(os.path.join(H,'seeds.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=1)
for r in res: print(f"{r['small_hits']:>3}/{r['n']} {r['seed']} | " + ' / '.join(f"{b[0]:,}({b[1]:,}) {b[2][:35]}" for b in r['best']))
