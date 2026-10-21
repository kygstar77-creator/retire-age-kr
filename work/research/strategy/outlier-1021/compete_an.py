import json, sys, re, statistics, collections, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(H,'compete_web.json'),encoding='utf-8'))
KEY = {'실제로 남은 돈': r'남은 돈|남는 돈|실제로 남', '몰락의 진짜 이유': r'몰락', '50대 돈 실수': r'실수', '노후 함정': r'함정',
       '기준표': r'기준표|표\b|한눈에', '모르면 손해 보는': r'모르면|손해', '싹 다 비교해봤습니다': r'비교', '반응 정리': r'반응',
       '입지 분석': r'입지', 'TOP10 총정리': r'TOP|총정리'}
res = {}
for q, rows in d.items():
    k = KEY.get(q, re.escape(q)); m = [r for r in rows if re.search(k, r['title'], re.I) and r['pub'] >= '2025-10-21']
    chs = {}
    for r in m: chs.setdefault(r['cid'], r)
    sz = collections.Counter('?' if r['subs'] is None else '<1만' if r['subs'] < 1e4 else '1만~10만' if r['subs'] < 1e5 else '10만+' for r in chs.values())
    small_win = [r for r in m if r['subs'] is not None and r['subs'] < 1e4 and r['views'] >= 10*max(r['subs'],1) and r['views'] >= 3000]
    res[q] = dict(match_videos=len(m), channels=len(chs), size=dict(sz), med_views=round(statistics.median([r['views'] for r in m])) if m else None,
                  long_share=round(sum(r['sec']>180 for r in m)/len(m),2) if m else None, small_wins=len(small_win), small_win_ch=len({r['cid'] for r in small_win}),
                  new_ch_12m=len({r['cid'] for r in m if (r['opened'] or '') >= '2025-10-21'}),
                  examples=[f"{r['views']:,}({r['subs'] if r['subs'] is not None else '?'}) {r['title'][:50]}" for r in sorted(m, key=lambda r:-r['views'])[:4]])
    print('##', q, {k: v for k, v in res[q].items() if k != 'examples'})
    for e in res[q]['examples']: print('   ', e)
json.dump(res, open(os.path.join(H,'compete_summary.json'),'w',encoding='utf-8'), ensure_ascii=False, indent=1)
