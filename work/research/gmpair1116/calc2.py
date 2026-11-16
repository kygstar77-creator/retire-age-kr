# 광명 84㎡대 반기별 동(umdNm)별 건수·가운데 값 — 가운데 값이 움직인 게 '같은 집 값'인지 '팔린 동네 구성'인지 보려고. S1 raw 그대로, 해제 뺌.
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
num = lambda s: float(str(s or '0').replace(',', '') or 0)
def half(ym):
    y, m = divmod(ym, 100); return f'{y}{"상" if m <= 6 else "하"}'
rows = []
for code in ('41210', '11530', '11545'):
  for p in sorted(glob.glob(os.path.join(H, 'raw', code + '_*_trade.json'))):
    for r in json.load(open(p, encoding='utf-8')):
        if r.get('cdealType') or not (80 <= num(r['excluUseAr']) <= 85): continue
        r['_g']=code; r['_h'] = half(int(r['dealYear']) * 100 + int(r['dealMonth'])); r['_p'] = num(r['dealAmount']); rows.append(r)
g = C.defaultdict(lambda: C.defaultdict(list))
for r in rows:
    if r['_g']=='41210': g[r['_h']][r['umdNm']].append(r['_p'])
dongs = sorted({d for h in g for d in g[h]})
for h in sorted(g):
    tot = sum(len(v) for v in g[h].values())
    print(h, ' · '.join(f"{d} {len(g[h][d])}건({len(g[h][d])/tot*100:.0f}%) {st.median(g[h][d]):,.0f}" for d in dongs if g[h][d]))
# 같은 단지·같은 넓이(1㎡ 반올림) 짝: 앞 반기 vs 뒤 반기 가운데 값 비의 가운데 값
key = lambda r: (r['_g'], r.get('aptSeq') or r['aptNm'], round(num(r['excluUseAr'])))
k2 = C.defaultdict(lambda: C.defaultdict(list))
for r in rows: k2[key(r)][r['_h']].append(r['_p'])
hs = sorted({r['_h'] for r in rows})
print('\n## 같은 단지·같은 넓이, 바로 앞 반기 대비 변화(두 반기 다 거래 있는 묶음의 가운데 값)')
for code, nm in (('41210','광명'),('11530','구로'),('11545','금천')):
    out=[]
    for a,b in zip(hs,hs[1:]):
        rs=[st.median(v[b])/st.median(v[a])-1 for k,v in k2.items() if k[0]==code and v[a] and v[b]]
        out.append(f"{b} {st.median(rs)*100:+.1f}%({len(rs)})")
    print(nm, ' · '.join(out))
# 2024하 → 2026하(7~11월) 같은 집 누적
print('\n## 같은 단지·같은 넓이, 2023상 → 2026하 / 2024하 → 2026하')
for code, nm in (('41210','광명'),('11530','구로'),('11545','금천')):
    for a in ('2023상','2024하'):
        rs=[st.median(v['2026하'])/st.median(v[a])-1 for k,v in k2.items() if k[0]==code and v[a] and v['2026하']]
        print(nm, a,'→2026하', f"{st.median(rs)*100:+.1f}% ({len(rs)}묶음)")
