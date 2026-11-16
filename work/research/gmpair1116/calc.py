# 광명 vs 구로·금천 84㎡대(전용 80~85㎡) 매매 가운데 값, 반기별 2023~2026 — 국토부 실거래 S1(raw/*_trade.json, 11/16 받음). 해제(cdealType) 거래 뺌.
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
NM = {'41210': '광명', '11530': '구로', '11545': '금천'}
num = lambda s: float(str(s or '0').replace(',', '') or 0)
rows = []; cancel = 0
for p in sorted(glob.glob(os.path.join(H, 'raw', '*_trade.json'))):
    code = os.path.basename(p)[:5]
    for r in json.load(open(p, encoding='utf-8')):
        if r.get('cdealType'): cancel += 1; continue
        a = num(r['excluUseAr'])
        if not (80 <= a <= 85): continue
        r['_g'] = code; r['_ym'] = int(r['dealYear']) * 100 + int(r['dealMonth']); r['_p'] = num(r['dealAmount']); r['_by'] = int(r.get('buildYear') or 0)
        rows.append(r)
print(f'# 84㎡대 매매 {len(rows):,}건(해제 {cancel:,}건 뺌, 전체 면적 기준), 계약 2023-01~2026-11')
def half(ym):
    y, m = divmod(ym, 100); return f'{y}{"상" if m <= 6 else "하"}'
def qtr(ym):
    y, m = divmod(ym, 100); return f'{y}Q{(m-1)//3+1}'
for lab, fn in (('반기', half), ('분기', qtr)):
    print(f'\n## {lab}별 가운데 값(만원)·건수')
    g = C.defaultdict(list)
    for r in rows: g[(fn(r['_ym']), r['_g'])].append(r['_p'])
    for per in sorted({k[0] for k in g}):
        vals = {c: g.get((per, c), []) for c in NM}
        s = ' · '.join(f"{NM[c]} {st.median(v):,.0f}({len(v)})" if v else f"{NM[c]} -" for c, v in vals.items())
        gm = vals['41210']; gr = vals['11530']; gc = vals['11545']
        d = f" | 광명-구로 {st.median(gm)-st.median(gr):+,.0f} · 광명-금천 {st.median(gm)-st.median(gc):+,.0f}" if gm and gr and gc else ''
        print(f'{per}: {s}{d}')
# 2019년 이후 지은 단지 몫(광명)
print('\n## 광명 84㎡대 거래 중 2019년 이후 준공 몫, 반기별 / 그 빼고 가운데 값')
g = C.defaultdict(list)
for r in rows:
    if r['_g'] == '41210': g[half(r['_ym'])].append(r)
for per in sorted(g):
    v = g[per]; new = [r for r in v if r['_by'] >= 2019]; old = [r['_p'] for r in v if r['_by'] < 2019]
    print(f"{per}: {len(v)}건 중 새 단지 {len(new)}건({len(new)/len(v)*100:.0f}%) · 새 단지 빼면 {st.median(old):,.0f} · 새 단지 {st.median([r['_p'] for r in new]) if new else 0:,.0f}")
# 구로·금천도 같은 방식
for c in ('11530', '11545'):
    print(f'\n## {NM[c]} 2019년 이후 준공 몫, 반기별')
    g = C.defaultdict(list)
    for r in rows:
        if r['_g'] == c: g[half(r['_ym'])].append(r)
    for per in sorted(g):
        v = g[per]; new = [r for r in v if r['_by'] >= 2019]; old = [r['_p'] for r in v if r['_by'] < 2019]
        print(f"{per}: {len(v)}건 중 새 단지 {len(new)}건({len(new)/len(v)*100:.0f}%) · 새 단지 빼면 {st.median(old) if old else 0:,.0f}")
