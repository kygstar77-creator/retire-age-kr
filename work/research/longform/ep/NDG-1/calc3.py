# NDG-1 calc3 — 댓글 질문 답용 (youtube-loop 2026-11-23): 노원 2026 최고 거래·20억 넘는 거래 · 신고가 묶음 중 월계동 몫 · 2026 월별 최고 달 대비 8~10월
import runpy, io, contextlib, collections, statistics as st, sys
sys.stdout.reconfigure(encoding='utf-8')
import os; _o = sys.stdout; sys.stdout = open(os.devnull, "w", encoding="utf-8"); ns = runpy.run_path("calc.py"); sys.stdout = _o
rows = ns['rows']
r26 = [r for r in rows if r['ym'][:4] == '2026']
for g in ('노원구', '도봉구', '강북구'):
    v = sorted([r for r in r26 if r['gu'] == g], key=lambda r: -r['amt'])
    print(g, '2026 최고', [(x['dong'], x['apt'], x['a'], x['ym'], x['amt']) for x in v[:3]], '· 20억↑', sum(1 for x in v if x['amt'] >= 20))
g = collections.defaultdict(list)
for r in rows: g[(r['gu'], r['dong'], r['apt'], r['a'])].append(r)
new = [k for k, v in g.items() if any(r['ym'][:4]=='2026' for r in v) and [r['amt'] for r in v if '202101'<=r['ym']<='202512'] and max(r['amt'] for r in v if r['ym'][:4]=='2026') > max(r['amt'] for r in v if '202101'<=r['ym']<='202512')]
print('신고가 묶음', len(new), '· 동별 상위', collections.Counter(k[1] for k in new).most_common(6))
wol = [k for k in g if k[1] == '월계동' and any(r['ym'][:4]=='2026' for r in g[k])]
print('월계동 2026 거래 묶음', len(wol), '· 그중 신고가', sum(1 for k in new if k[1]=='월계동'))
m = collections.Counter(r['ym'] for r in r26)
print('2026 월별', dict(sorted(m.items())), '· 8~10월 평균/4월', round((m['202608']+m['202609']+m['202610'])/3/m['202604']*100,1), '%')
