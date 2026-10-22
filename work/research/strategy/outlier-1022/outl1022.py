# 10/22 넓은 표본 아웃라이어 목록 → outliers_1022.csv (기준 10/21과 같음: 조회÷구독 ≥10, 조회 3,000+, 구독 1만 미만, 90일)
import json, csv, sys, os, statistics
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
ch = json.load(open(os.path.join(H, 'channels.json'), encoding='utf-8')); vd = json.load(open(os.path.join(H, 'videos.json'), encoding='utf-8'))
rows = []; allv = 0
for cid, vs in vd.items():
    c = ch[cid]; subs = max(c['subs'], 1); allv += len(vs)
    for v in vs:
        x = v['views'] / subs
        if x >= 10 and v['views'] >= 3000:
            rows.append(dict(x_subs=round(x, 1), views=v['views'], subs=c['subs'], sec=v['sec'], pub=v['pub'], opened=c['opened'], nvid90=len(vs),
                             likes=v.get('likes', 0), comments=v.get('comments', 0), channel=c['title'], cid=cid, src=c['src'], id=v['id'], title=v['title']))
rows.sort(key=lambda r: -r['x_subs'])
with open(os.path.join(H, 'outliers_1022.csv'), 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print('작은 채널', len(vd), '90일 영상', allv, '아웃라이어', len(rows), '채널', len({r['cid'] for r in rows}))
