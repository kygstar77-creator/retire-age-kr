# 장르별 숫자 → genre_stats.json, seed_hits.json
import json, csv, sys, os, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
from classify import GENRES
lab = json.load(open(os.path.join(H, 'labels.json'), encoding='utf-8'))
NEW = '2025-10-22'
def stats(rows):
    out = {}
    by = collections.defaultdict(list)
    for r in rows: by[lab.get(r['id'], 26)].append(r)
    for g, m in sorted(by.items(), key=lambda a: -len(a[1])):
        chs = {r['cid']: r['opened'] for r in m}
        lg = [r for r in m if int(r['sec']) > 180]
        top_ch = collections.Counter(r['channel'] for r in m).most_common(1)[0]
        out[GENRES[g]] = dict(n=len(m), channels=len(chs), new_ch_share=round(sum(o >= NEW for o in chs.values()) / len(chs), 2),
            med_x=round(st.median(float(r['x_subs']) for r in m), 1), med_views=round(st.median(int(r['views']) for r in m)),
            long_n=len(lg), long_med_views=round(st.median(int(r['views']) for r in lg)) if lg else None,
            short_share=round(1 - len(lg) / len(m), 2), top_channel_share=round(top_ch[1] / len(m), 2), top_channel=top_ch[0],
            like_pct=round(st.median(int(r['likes']) / max(int(r['views']), 1) * 100 for r in m), 2) if 'likes' in m[0] else None)
    return out
A = list(csv.DictReader(open(os.path.join(H, 'nonmoney_1021.csv'), encoding='utf-8-sig')))
B = list(csv.DictReader(open(os.path.join(H, 'outliers_1022.csv'), encoding='utf-8-sig')))
res = dict(biased_1021_nonmoney=stats(A), broad_1022=stats(B))
json.dump(res, open(os.path.join(H, 'genre_stats.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k, v in res.items():
    print('\n###', k, sum(x['n'] for x in v.values()))
    for g, s in v.items(): print(f"{s['n']:>4} ch{s['channels']:>3} 새{s['new_ch_share']:.2f} x{s['med_x']:>6} 조회{s['med_views']:>8,} 롱{s['long_n']:>3}/{s['long_med_views']} 1채널{s['top_channel_share']:.2f} 좋{s['like_pct']} | {g[:28]} ({s['top_channel'][:10]})")
# 시드별: 그 검색 결과(90일 안) 중 작은 채널 아웃라이어
c = json.load(open(os.path.join(H, 'cache_web.json'), encoding='utf-8')); sv = json.load(open(os.path.join(H, 'seedvids.json'), encoding='utf-8'))
ch = json.load(open(os.path.join(H, 'channels.json'), encoding='utf-8'))
sh = []
for q, d in c.items():
    vs = [dict(sv[i], id=i) for i in d['ids'] if i in sv and sv[i]['pub'] >= '2026-07-24']
    hit = [v for v in vs if (ch.get(v['cid']) or {}).get('subs') is not None and ch[v['cid']]['subs'] < 1e4 and v['views'] / max(ch[v['cid']]['subs'], 1) >= 10 and v['views'] >= 3000]
    sh.append(dict(genre=d['genre'], seed=q, n90=len(vs), small_hits=len(hit), med_views90=round(st.median([v['views'] for v in vs])) if vs else None,
                   best=[(v['views'], ch[v['cid']]['subs'], v['sec'], v['id'], v['title'][:60]) for v in sorted(hit, key=lambda v: -v['views'])[:3]]))
json.dump(sh, open(os.path.join(H, 'seed_hits.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('\n### 시드별 (90일 결과 중 작은 채널 10배+)')
for r in sorted(sh, key=lambda r: -r['small_hits']): print(f"{r['small_hits']:>3}/{r['n90']:>3} 중앙{r['med_views90']} {r['genre'][:8]} {r['seed']} | " + ' / '.join(f"{b[0]:,}({b[1]:,},{b[2]}s) {b[4][:30]}" for b in r['best'][:2]))
