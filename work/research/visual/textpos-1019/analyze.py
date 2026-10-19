# ann.py(눈으로 본 기록) + data.json(조회·구독) → table.csv, stats.json
import os, sys, json, csv, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from ann import A
D = json.load(open(os.path.join(HERE, 'data.json'), encoding='utf-8')); rows = D['rows']
assert len(A) == len(rows) == 90, (len(A), len(rows))
chmed = collections.defaultdict(list)
for r in rows: chmed[r['channel']].append(r['views'])
chmed = {k: st.median(v) for k, v in chmed.items()}
for i, r in enumerate(rows):
    r.update(A[i]); r['n'] = i; r['row'] = r['pos'].split('-')[0]
    r['rel'] = round(r['views'] / chmed[r['channel']], 2)  # 그 채널 최근 5편 중앙값 대비
with open(os.path.join(HERE, 'table.csv'), 'w', encoding='utf-8-sig', newline='') as fp:
    w = csv.writer(fp); w.writerow(['n', 'channel', 'id', 'published', 'views', 'subs', 'views_per_sub', 'vs_channel_median', 'pos', 'lines', 'under', 'subject', 'title'])
    for r in rows: w.writerow([r['n'], r['channel'], r['id'], r['published'], r['views'], r['subs'], r['ratio'], r['rel'], r['pos'], r['lines'], r['under'], r['subj'], r['title']])
def summ(key):
    g = collections.defaultdict(list)
    for r in rows: g[r[key]].append(r)
    out = {}
    for k, v in sorted(g.items(), key=lambda x: -len(x[1])):
        out[k] = dict(n=len(v), ch=len({x['channel'] for x in v}), ratio_med=round(st.median([x['ratio'] for x in v]), 2),
                      rel_med=round(st.median([x['rel'] for x in v]), 2))
    return out
S = dict(by_row=summ('row'), by_pos=summ('pos'), by_under=summ('under'), by_lines=summ('lines'))
# 채널별: 위치가 고정인가
per = {}
for c in chmed:
    v = [r for r in rows if r['channel'] == c]
    per[c] = dict(subs=v[0]['subs'], pos=collections.Counter(r['pos'] for r in v).most_common(), under=collections.Counter(r['under'] for r in v).most_common(),
                  ratio_med=round(st.median([r['ratio'] for r in v]), 3), views_med=int(chmed[c]), dates=f"{min(r['published'] for r in v)}~{max(r['published'] for r in v)}")
S['per_channel'] = per
S['odd'] = [dict(n=r['n'], ch=r['channel'], id=r['id'], pos=r['pos'], rel=r['rel'], views=r['views']) for r in rows if r['row'] != '아래']
json.dump(S, open(os.path.join(HERE, 'stats.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(S, ensure_ascii=False, indent=1))
