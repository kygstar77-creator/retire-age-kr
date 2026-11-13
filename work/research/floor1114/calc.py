# floor1114 계산 — 같은 단지(aptSeq)·같은 전용면적(소수 첫째 자리 반올림) 안에서 층별 값 비교. 해제(cdealType) 뺌, 지하·0층 뺌.
import sys, os, json, glob, statistics as st
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sgg = json.load(open('../seoul_sgg.json', encoding='utf-8'))
rows = []; cancel = 0; total = 0
for p in glob.glob('raw/*.json'):
    code = os.path.basename(p)[:5]
    for r in json.load(open(p, encoding='utf-8')):
        total += 1
        if (r.get('cdealType') or '').strip(): cancel += 1; continue
        try: fl = int(r['floor']); amt = int(r['dealAmount'].replace(',', '')); ar = float(r['excluUseAr'])
        except: continue
        if fl < 1: continue
        rows.append(dict(g=(r['aptSeq'], round(ar, 1)), fl=fl, amt=amt, ar=ar, gu=sgg[code], dong=r['umdNm'], nm=r['aptNm'], by=r['buildYear'], direct=('직거래' in r.get('dealingGbn', ''))))
print('받은 행', total, '해제', cancel, '해제 뺀 매매', len(rows))
G = defaultdict(list)
for r in rows: G[r['g']].append(r)
def band(f):
    return '1층' if f == 1 else '2층' if f == 2 else '3~5층' if f <= 5 else '6~10층' if f <= 10 else '11~15층' if f <= 15 else '16~20층' if f <= 20 else '21층 이상'
B = ['1층', '2층', '3~5층', '6~10층', '11~15층', '16~20층', '21층 이상']
# (가) 같은 단지·같은 면적 거래가 5건 이상인 묶음: 각 거래 값 / 그 묶음 중간값
rel = defaultdict(list); ng = 0; nt = 0
for g, L in G.items():
    if len(L) < 5: continue
    ng += 1; nt += len(L); m = st.median(x['amt'] for x in L)
    for x in L: rel[band(x['fl'])].append(x['amt'] / m)
print(f'\n(가) 5건 이상 묶음 {ng}개·거래 {nt}건 — 층 띠별 (묶음 중간값 대비) 가운데 비율')
for b in B:
    v = rel[b]
    if v: print(f'  {b}: {len(v)}건  가운데 {st.median(v)*100:.1f}%')
# (나) 1층 거래 하나 ↔ 같은 묶음 6층 이상 거래 중간값 (6층 이상 2건 이상)
pairs = []
for g, L in G.items():
    hi = [x['amt'] for x in L if x['fl'] >= 6]
    if len(hi) < 2: continue
    mh = st.median(hi)
    for x in L:
        if x['fl'] == 1: pairs.append((x, mh, x['amt'] / mh))
print(f'\n(나) 1층 vs 같은 단지·같은 면적 6층 이상(2건 이상) 짝 {len(pairs)}건 (단지 {len(set(p[0]["g"][0] for p in pairs))}곳)')
rs = [p[2] for p in pairs]; diff = [p[1] - p[0]['amt'] for p in pairs]
print(f'  비율 가운데 {st.median(rs)*100:.1f}%  · 싸게 거래된 몫 {sum(1 for r in rs if r < 1)}/{len(rs)}  · 차이 가운데 {st.median(diff):,.0f}만원')
q = sorted(rs); print(f'  비율 1/4 {q[len(q)//4]*100:.1f}% · 3/4 {q[3*len(q)//4]*100:.1f}%')
print(f'  1층이 6층 이상 중간값보다 비싸거나 같은 거래 {sum(1 for r in rs if r >= 1)}건')
# 값 띠별
for lo, hi_, nm in ((0, 100000, '10억 이하'), (100000, 200000, '10억~20억'), (200000, 10**9, '20억 넘게')):
    s = [p for p in pairs if lo < p[1] <= hi_]
    if s: print(f'  6층 이상 중간값 {nm}: {len(s)}건 비율 {st.median(p[2] for p in s)*100:.1f}% · 차이 {st.median(p[1]-p[0]["amt"] for p in s):,.0f}만원')
# 84㎡ 안팎
s = [p for p in pairs if 80 <= p[0]['ar'] <= 86]
print(f'  84㎡ 안팎(80~86) {len(s)}건 비율 {st.median(p[2] for p in s)*100:.1f}% · 차이 {st.median(p[1]-p[0]["amt"] for p in s):,.0f}만원 · 6층 이상 중간값의 가운데 {st.median(p[1] for p in s):,.0f}')
# 59㎡ 안팎
s = [p for p in pairs if 57 <= p[0]['ar'] <= 61]
print(f'  59㎡ 안팎(57~61) {len(s)}건 비율 {st.median(p[2] for p in s)*100:.1f}% · 차이 {st.median(p[1]-p[0]["amt"] for p in s):,.0f}만원')
# 2층도 같은 방식
p2 = []
for g, L in G.items():
    hi = [x['amt'] for x in L if x['fl'] >= 6]
    if len(hi) < 2: continue
    mh = st.median(hi)
    for x in L:
        if x['fl'] == 2: p2.append(x['amt'] / mh)
print(f'\n(다) 2층 짝 {len(p2)}건 비율 가운데 {st.median(p2)*100:.1f}%')
p3 = []
for g, L in G.items():
    hi = [x['amt'] for x in L if x['fl'] >= 6]
    if len(hi) < 2: continue
    mh = st.median(hi)
    for x in L:
        if 3 <= x['fl'] <= 5: p3.append(x['amt'] / mh)
print(f'    3~5층 짝 {len(p3)}건 비율 가운데 {st.median(p3)*100:.1f}%')
# 연식별 1층
for lo, hi_, nm in ((0, 10, '10년 이내'), (11, 25, '11~25년'), (26, 99, '26년 이상')):
    s = [p for p in pairs if lo <= 2026 - int(p[0]['by']) <= hi_]
    if s: print(f'  1층 연식 {nm}: {len(s)}건 비율 {st.median(p[2] for p in s)*100:.1f}%')
# 직거래 빼고
s = [p for p in pairs if not p[0]['direct']]
print(f'  1층 중개거래만 {len(s)}건 비율 {st.median(p[2] for p in s)*100:.1f}%')
# 1층 비중
n1 = sum(1 for r in rows if r['fl'] == 1); print(f'\n1층 거래 {n1}/{len(rows)} = {n1/len(rows)*100:.1f}%')
# 구별 1층 짝 많은 곳
gc = defaultdict(list)
for p in pairs: gc[p[0]['gu']].append(p[2])
print('구별(짝 15건 이상):', ', '.join(f'{k} {len(v)}건 {st.median(v)*100:.1f}%' for k, v in sorted(gc.items(), key=lambda kv: st.median(kv[1])) if len(v) >= 15))
# 짝 많은 단지
dc = defaultdict(list)
for p in pairs: dc[(p[0]['gu'], p[0]['nm'], p[0]['g'][1])].append(p)
top = sorted(dc.items(), key=lambda kv: -len(kv[1]))[:8]
for k, v in top: print('  ', k, len(v), '1층', [x[0]['amt'] for x in v], '6층+중간', v[0][1])
