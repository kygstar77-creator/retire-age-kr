# bundil1117 — '2023년 상반기가 바닥인가' 확인: 일산 두 구 반기별, 같은 평형 짝(기준 2021년 7~12월) 가운데 변화 + 84㎡ 안팎 가운데 값. S1 raw 그대로, 해제 뺌.
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
num = lambda s: float(str(s or '0').replace(',', '') or 0)
rows = []
for p in sorted(glob.glob(os.path.join(H, 'raw', '*_trade.json'))):
    code = os.path.basename(p)[:5]
    for r in json.load(open(p, encoding='utf-8')):
        if r.get('cdealType'): continue
        ym = int(r['dealYear']) * 100 + int(r['dealMonth'])
        rows.append((code, f"{r['dealYear']}H{1 if int(r['dealMonth'])<=6 else 2}", ym, (r.get('aptSeq'), round(num(r['excluUseAr']))), num(r['dealAmount'])))
for grp, codes in (('일산 두 구', ('41285', '41287')), ('분당구', ('41135',))):
    base = C.defaultdict(list)
    for c, h, ym, k, p in rows:
        if c in codes and h == '2021H2': base[k].append(p)
    base = {k: st.median(v) for k, v in base.items()}
    print('#', grp, '— 기준 2021년 하반기 같은 평형 대비 반기별 가운데 변화')
    for h in sorted({x[1] for x in rows}):
        d = C.defaultdict(list)
        for c, hh, ym, k, p in rows:
            if c in codes and hh == h and k in base and ym <= 202610: d[k].append(p)
        rs = [st.median(v) / base[k] - 1 for k, v in d.items()]
        if rs: print(f'  {h}: {len(rs)}곳 · {st.median(rs)*100:+.1f}%')
