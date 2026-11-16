# 동탄구(41597) 아파트 매매 — 달별 건수·84㎡대(80~85㎡) 가운데 값, 동(umdNm)별 몫 — 국토부 실거래 S1(raw/*_trade.json, 11/16 받음). 해제(cdealType) 거래 뺌.
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
num = lambda s: float(str(s or '0').replace(',', '') or 0)
rows = []; cancel = 0
for p in sorted(glob.glob(os.path.join(H, 'raw', '*_trade.json'))):
    for r in json.load(open(p, encoding='utf-8')):
        if r.get('cdealType'): cancel += 1; continue
        r['_ym'] = int(r['dealYear']) * 100 + int(r['dealMonth']); r['_p'] = num(r['dealAmount']); r['_a'] = num(r['excluUseAr'])
        rows.append(r)
print(f'# 전체 {len(rows):,}건(해제 {cancel:,}건 뺌), 계약 2023-01~2026-11(11월은 16일까지 신고분)')
g = C.defaultdict(list)
for r in rows: g[r['_ym']].append(r)
print('\n## 달별: 건수 · 84㎡대 건수·가운데 값(만원) · 직거래 몫 · 1위 동')
for ym in sorted(g):
    v = g[ym]; m84 = [r['_p'] for r in v if 80 <= r['_a'] <= 85]
    dg = C.Counter(r['umdNm'] for r in v).most_common(2)
    dd = sum(1 for r in v if (r.get('dealingGbn') or '').strip() == '직거래')
    print(f"{ym}: {len(v):,}건 · 84㎡ {len(m84)}건 {st.median(m84):,.0f} · 직거래 {dd/len(v)*100:.0f}% · {dg}")
# 동별 전체 건수
print('\n## 동별 전체 건수')
print(C.Counter(r['umdNm'] for r in rows).most_common(30))
