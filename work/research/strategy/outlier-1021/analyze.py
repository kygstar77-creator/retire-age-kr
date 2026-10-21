# 조회÷구독 배수 표 만들기 → outliers.csv
import json, csv, sys, statistics, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
ch = json.load(open(os.path.join(H, 'channels.json'), encoding='utf-8')); vd = json.load(open(os.path.join(H, 'videos.json'), encoding='utf-8'))
MINX = float(sys.argv[1]) if len(sys.argv) > 1 else 10
rows = []
for cid, vs in vd.items():
    c = ch[cid]; subs = max(c['subs'], 1)
    if not vs: continue
    med = statistics.median([v['views'] for v in vs])
    for v in vs:
        x = v['views'] / subs
        if x >= MINX and v['views'] >= 3000:
            rows.append(dict(x_subs=round(x, 1), views=v['views'], subs=c['subs'], ch_med90=round(med), x_med=round(v['views']/max(med,1), 1),
                             fmt='쇼츠' if v['sec'] <= 180 else '롱폼', sec=v['sec'], pub=v['pub'], opened=c['opened'], nvid90=len(vs),
                             channel=c['title'], cid=cid, src=c['src'], id=v['id'], title=v['title']))
rows.sort(key=lambda r: -r['x_subs'])

with open(os.path.join(H, 'outliers.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
chs = {r['cid'] for r in rows}
print('아웃라이어', len(rows), '채널', len(chs), '| 50배+', sum(r['x_subs'] >= 50 for r in rows))
for r in rows: print(f"{r['x_subs']:>7} | {r['views']:>9,} | 구독{r['subs']:>6,} | {r['fmt']}{r['sec']}s | {r['pub']} | 개설{r['opened'][:7]} | {r['channel'][:14]} | {r['title'][:60]}")
