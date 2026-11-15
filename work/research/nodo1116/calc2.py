# 노도강 세부 — 84㎡ 띠 한 채 중간값, 법정동별 같은 집 변화, 월별 거래, 서울 안 거래 비중. 재료·기준 calc.py와 같음
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(H, '..', '..'))
SG = json.load(open(os.path.join(W, 'research', 'seoul_sgg.json'), encoding='utf-8'))
num = lambda s: float(str(s or '0').replace(',', '') or 0); ymi = lambda r: int(r['dealYear']) * 100 + int(r['dealMonth'])
rows = []
for p in sorted(glob.glob(os.path.join(H, 'raw', '*_trade.json'))):
    code = os.path.basename(p)[:5]
    for r in json.load(open(p, encoding='utf-8')):
        if r.get('cdealType'): continue
        r['_g'] = code; rows.append(r)
win = lambda r: 'now' if 202511 <= ymi(r) <= 202611 else ('pre' if 202411 <= ymi(r) <= 202510 else None)
NODO = ['11350', '11320', '11305']; nd = [r for r in rows if r['_g'] in NODO]
ar = lambda r: num(r['excluUseAr'])
print('## §2 전용 80~90㎡(84㎡ 안팎) 한 채 중간값')
for tag, codes in [('노도강', NODO), ('노원', ['11350']), ('도봉', ['11320']), ('강북', ['11305']), ('노도강 뺀 22개 구', [c for c in SG if c not in NODO])]:
    s = {w: [num(r['dealAmount']) for r in rows if r['_g'] in codes and win(r) == w and 80 <= ar(r) < 90] for w in ('pre', 'now')}
    print(f'- {tag}: 1년 전 {st.median(s["pre"])/1e4:.2f}억({len(s["pre"])}건) → 최근 {st.median(s["now"])/1e4:.2f}억({len(s["now"])}건) · {(st.median(s["now"])-st.median(s["pre"]))/1e4:+.2f}억')
print('\n## §3 같은 집 묶음(두 해 각 3건+) — 노도강 안 법정동별(묶음 8개 이상)')
key = lambda r: (r['_g'], r.get('aptSeq') or (r['aptNm'] + '|' + r.get('umdNm', '')), round(ar(r)))
g = C.defaultdict(lambda: {'now': [], 'pre': [], 'dong': '', 'nm': ''})
for r in nd:
    w = win(r)
    if w: k = key(r); g[k][w].append(num(r['dealAmount'])); g[k]['dong'] = SG[r['_g']][:2] + ' ' + r['umdNm']; g[k]['nm'] = r['aptNm']
pairs = [(v['dong'], st.median(v['now']) / st.median(v['pre']) - 1, v, k) for k, v in g.items() if len(v['now']) >= 3 and len(v['pre']) >= 3]
byd = C.defaultdict(list)
for d, x, v, k in pairs: byd[d].append(x)
for d, xs in sorted(byd.items(), key=lambda t: -st.median(t[1])):
    if len(xs) >= 8: print(f'- {d}: {st.median(xs)*100:+.1f}% ({len(xs)}묶음)')
xs = [x for _, x, _, _ in pairs]
print(f'- 노도강 묶음 {len(xs)}개: 15.5% 넘게 오른 곳 {sum(1 for x in xs if x > .155)}개({sum(1 for x in xs if x > .155)/len(xs)*100:.0f}%) · 내린 곳 {sum(1 for x in xs if x < 0)}개({sum(1 for x in xs if x < 0)/len(xs)*100:.0f}%)')
print('\n## §4 월별 거래(노도강 / 서울 전체)')
for y in (2024, 2025, 2026):
    for m in range(1, 13):
        ym = y * 100 + m
        if 202411 <= ym <= 202611:
            a = sum(1 for r in nd if ymi(r) == ym); b = sum(1 for r in rows if ymi(r) == ym)
            print(f'{ym}: 노도강 {a:,} / 서울 {b:,} ({a/b*100:.1f}%)')
print('\n## §5 두 해 거래 합')
for w in ('pre', 'now'):
    a = sum(1 for r in nd if win(r) == w); b = sum(1 for r in rows if win(r) == w)
    print(f'- {w}: 노도강 {a:,} / 서울 {b:,} → 노도강 비중 {a/b*100:.1f}%')
