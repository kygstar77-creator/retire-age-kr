import json, sys, statistics, os, collections
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
ch = json.load(open(os.path.join(H, 'channels.json'), encoding='utf-8')); vd = json.load(open(os.path.join(H, 'videos.json'), encoding='utf-8'))
out = []
for cid, vs in vd.items():
    c = ch[cid]; subs = max(c['subs'], 1)
    if not vs: continue
    hits = [v for v in vs if v['views']/subs >= 10 and v['views'] >= 3000]
    if len(hits) < 2: continue
    lr = statistics.median([v['likes']/max(v['views'],1)*100 for v in hits])
    sh = sum(v['sec'] <= 180 for v in vs)
    out.append(dict(cid=cid, title=c['title'], subs=c['subs'], opened=c['opened'], n90=len(vs), short90=sh, nhit=len(hits),
                    hit_rate=round(len(hits)/len(vs),2), med_views90=round(statistics.median([v['views'] for v in vs])),
                    med_x=round(statistics.median([v['views']/subs for v in hits]),1), like_pct=round(lr,2),
                    top=[(v['views'], v['sec'], v['title']) for v in sorted(hits, key=lambda v:-v['views'])[:6]]))
out.sort(key=lambda r: -r['nhit'])
json.dump(out, open(os.path.join(H, 'by_channel.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for r in out:
    print(f"\n## {r['title']} | 구독 {r['subs']:,} | 개설 {r['opened']} | 90일 {r['n90']}편(쇼츠 {r['short90']}) | 적중 {r['nhit']} ({r['hit_rate']}) | 중앙조회 {r['med_views90']:,} | 적중 배수중앙 {r['med_x']} | 좋아요% {r['like_pct']}")
    for t in r['top']: print(f"   {t[0]:>9,} {t[1]}s {t[2][:70]}")
