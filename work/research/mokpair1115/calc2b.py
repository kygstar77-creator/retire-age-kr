# (calc2 변형) 95~108㎡ 단지별 — 면적 띠별 단지 커버리지 — 최근 1년(2025.11~2026.11), 그 전 1년. 재료·제외 기준 calc.py와 같음
import json, os, glob, re, statistics as st, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); PY = 3.305785
def num(s): return float(str(s or '0').replace(',', '') or 0)
rows = []
for p in sorted(glob.glob(os.path.join(H, 'raw', '11470_*_trade.json'))): rows += json.load(open(p, encoding='utf-8'))
ok = lambda r: not r.get('cdealType') and r.get('buyerGbn') != '공공기관'
pp = lambda r: num(r['dealAmount']) / num(r['excluUseAr']) * PY
ar = lambda r: num(r['excluUseAr']); ymi = lambda r: int(r['dealYear']) * 100 + int(r['dealMonth'])
med = lambda v: st.median(v) if v else 0
MS = [r for r in rows if ok(r) and '목동신시가지' in r['aptNm']]
dan = lambda r: int(re.search(r'\d+', r['aptNm'].replace('목동신시가지', '')).group())
NOW = [r for r in MS if 202511 <= ymi(r) <= 202611]; OLD = [r for r in MS if 202411 <= ymi(r) <= 202510]
for lo, hi in [(95, 109)]:
    print(f'\n## 전용 {lo}~{hi}㎡ 최근 1년 — 평당 중앙 높은 순 (한 채 중앙 · 건수 · 1년 전 대비)')
    out = []
    for k in range(1, 15):
        b = [r for r in NOW if dan(r) == k and lo <= ar(r) < hi]; bo = [r for r in OLD if dan(r) == k and lo <= ar(r) < hi]
        if b: out.append((med([pp(r) for r in b]), k, len(b), med([num(r['dealAmount']) for r in b]), med([ar(r) for r in b]), med([pp(r) for r in bo]), len(bo)))
    for p, k, n, a, area, po, no in sorted(out, reverse=True):
        ch = f'{p/po*100-100:+.1f}%(전년 {no}건)' if no >= 3 else f'전년 {no}건'
        print(f'- {k}단지 · {n}건 · 평당 {p:,.0f} · 한 채 {a/10000:.2f}억 · 전용 {area:.1f}㎡ · {ch}')
    print(f'  없는 단지: {[k for k in range(1,15) if k not in {o[1] for o in out}]}')
