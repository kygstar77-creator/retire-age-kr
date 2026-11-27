# forenon1128 계산 — raw/11740_*_trade.json(국토부 아파트 매매 실거래, 강동구) · 취소(cdealType) 뺌
import json, glob, collections, statistics as S, sys
sys.stdout.reconfigure(encoding='utf-8')
rows = [r for f in sorted(glob.glob('raw/11740_*_trade.json')) for r in json.load(open(f, encoding='utf-8'))]
ok = [r for r in rows if not r['cdealType']]
def amt(r): return int(r['dealAmount'].replace(',', ''))
def ym(r): return f"{r['dealYear']}-{int(r['dealMonth']):02d}"
out = []
def p(s): out.append(s); print(s)
fo = [r for r in ok if r['aptNm'] == '올림픽파크포레온']
p(f"포레온 매매 신고(취소 뺌) 2024-11~2026-11-27 받은 날까지: {len(fo)}건 · 취소 {sum(1 for r in rows if r['aptNm']=='올림픽파크포레온' and r['cdealType'])}건")
by = collections.Counter(r['dealYear'] for r in fo); p('  해별: ' + ', '.join(f'{k} {v}' for k, v in sorted(by.items())))
p('  달별: ' + ', '.join(f'{k} {v}' for k, v in sorted(collections.Counter(ym(r) for r in fo).items())))
def band(r, lo, hi): a = float(r['excluUseAr']); return lo <= a < hi
for nm, lo, hi in [('84㎡대', 84, 85), ('59㎡대', 59, 60.5), ('39㎡대', 39, 40.5)]:
    xs = [r for r in fo if band(r, lo, hi)]
    g = collections.defaultdict(list)
    for r in xs: g[ym(r)].append(amt(r))
    p(f"포레온 {nm} {len(xs)}건: " + ' · '.join(f"{k} {len(v)}건 가운데 {S.median(v)/1e4:.2f}억(최저 {min(v)/1e4:.2f}·최고 {max(v)/1e4:.2f})" for k, v in sorted(g.items())))
    y26 = [amt(r) for r in xs if r['dealYear'] == '2026']
    if y26: p(f"  {nm} 2026년 {len(y26)}건 가운데 {S.median(y26)/1e4:.2f}억 · 최저 {min(y26)/1e4:.2f} · 최고 {max(y26)/1e4:.2f}")
    h2 = [amt(r) for r in xs if ym(r) >= '2026-08']
    if h2: p(f"  {nm} 2026-08~11 {len(h2)}건 가운데 {S.median(h2)/1e4:.2f}억")
    h1 = [amt(r) for r in xs if '2026-04' <= ym(r) <= '2026-06']
    if h1: p(f"  {nm} 2026-04~06 {len(h1)}건 가운데 {S.median(h1)/1e4:.2f}억")
# 직거래 비율
p(f"포레온 직거래 {sum(1 for r in fo if r['dealingGbn']=='직거래')}건 / {len(fo)}")
# 견줄 단지: 강동 신축 고덕그라시움(2019)·고덕아르테온(2020) 84㎡대
for apt in ['고덕그라시움', '고덕아르테온', '래미안힐스테이트고덕']:
    xs = [r for r in ok if r['aptNm'] == apt and band(r, 84, 85)]
    if not xs: continue
    by = xs[0]['buildYear']
    a = [amt(r) for r in xs if '2025-04' <= ym(r) <= '2025-06']
    b = [amt(r) for r in xs if '2026-04' <= ym(r) <= '2026-06']
    c = [amt(r) for r in xs if ym(r) >= '2026-08']
    p(f"{apt}({by}) 84㎡대: 2025-04~06 {len(a)}건 {S.median(a)/1e4:.2f}억 · 2026-04~06 {len(b)}건 {S.median(b)/1e4:.2f}억 · 2026-08~11 {len(c)}건 {S.median(c)/1e4:.2f}억")
open('calc_out.txt', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
