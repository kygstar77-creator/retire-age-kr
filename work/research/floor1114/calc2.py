# floor1114 계산 2 — 매매·전세를 같은 방식으로: 같은 단지(aptSeq)·같은 전용면적(㎡ 정수 반올림) 안에서 1층 거래 하나 ↔ 6층 이상 거래(2건 이상) 중간값.
# 매매는 해제(cdealType) 뺌, 전세는 월세 0원만. 지하·0층 뺌.
import sys, os, json, glob, statistics as st
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sgg = json.load(open('../seoul_sgg.json', encoding='utf-8'))
def load(d, kind):
    out = []; n = 0; drop = 0
    for p in glob.glob(d + '/*.json'):
        code = os.path.basename(p)[:5]
        for r in json.load(open(p, encoding='utf-8')):
            n += 1
            try: fl = int(r['floor']); ar = float(r['excluUseAr'])
            except: continue
            if kind == 'trade':
                if (r.get('cdealType') or '').strip(): drop += 1; continue
                v = int(r['dealAmount'].replace(',', ''))
            else:
                if int((r.get('monthlyRent') or '0').replace(',', '') or 0) != 0: drop += 1; continue
                v = int(r['deposit'].replace(',', '')); 
            if fl < 1 or v <= 0: continue
            out.append(dict(g=(r['aptSeq'], round(ar)), fl=fl, v=v, ar=ar, gu=sgg[code], nm=r['aptNm'], ct=r.get('contractType', ''), by=r.get('buildYear', '')))
    return out, n, drop
def pairs(rows, flo, fhi, minhi=2):
    G = defaultdict(list)
    for r in rows: G[r['g']].append(r)
    P = []
    for g, L in G.items():
        hi = [x['v'] for x in L if x['fl'] >= 6]
        if len(hi) < minhi: continue
        mh = st.median(hi)
        for x in L:
            if flo <= x['fl'] <= fhi: P.append((x, mh, x['v'] / mh))
    return P
def show(nm, P):
    r = [p[2] for p in P]; d = [p[1] - p[0]['v'] for p in P]; q = sorted(r)
    print(f'  {nm}: {len(P)}건(단지 {len(set(p[0]["g"][0] for p in P))}곳) 비율 가운데 {st.median(r)*100:.1f}% (1/4 {q[len(q)//4]*100:.1f}·3/4 {q[3*len(q)//4]*100:.1f}) · 더 싼 몫 {sum(1 for x in r if x<1)}/{len(r)} · 차이 가운데 {st.median(d):,.0f}만원 · 6층+ 중간값의 가운데 {st.median(p[1] for p in P):,.0f}')
T, nt, dt = load('raw', 'trade'); J, nj, dj = load('raw_rent', 'rent')
print(f'매매: 받은 {nt} · 해제 {dt} · 남은 {len(T)} | 전월세: 받은 {nj} · 월세 낀 것 {dj} · 전세 {len(J)}')
for nm, rows in (('매매', T), ('전세', J)):
    print(nm)
    show('1층', pairs(rows, 1, 1)); show('2층', pairs(rows, 2, 2)); show('3~5층', pairs(rows, 3, 5))
    P = pairs(rows, 1, 1)
    s = [p for p in P if 80 <= p[0]['ar'] <= 86]; show('1층 84㎡ 안팎', s)
    s = [p for p in P if 57 <= p[0]['ar'] <= 61]; show('1층 59㎡ 안팎', s)
    n1 = sum(1 for r in rows if r['fl'] == 1); print(f'  1층 비중 {n1}/{len(rows)} = {n1/len(rows)*100:.1f}%')
JP = pairs(J, 1, 1)
show('전세 1층 신규만', [p for p in JP if p[0]['ct'] == '신규']); show('전세 1층 갱신만', [p for p in JP if p[0]['ct'] == '갱신'])
# 같은 묶음 안 전세가율: 1층 전세 중간/1층 매매 중간 vs 6층+ 전세 중간/6층+ 매매 중간 (각 칸 1건 이상, 6층+는 2건 이상)
GT = defaultdict(list); GJ = defaultdict(list)
for r in T: GT[r['g']].append(r)
for r in J: GJ[r['g']].append(r)
R1 = []; RH = []; ex = []
for g in GT:
    if g not in GJ: continue
    t1 = [x['v'] for x in GT[g] if x['fl'] == 1]; j1 = [x['v'] for x in GJ[g] if x['fl'] == 1]
    th = [x['v'] for x in GT[g] if x['fl'] >= 6]; jh = [x['v'] for x in GJ[g] if x['fl'] >= 6]
    if t1 and j1 and len(th) >= 2 and len(jh) >= 2:
        a = st.median(j1) / st.median(t1); b = st.median(jh) / st.median(th); R1.append(a); RH.append(b); ex.append((GT[g][0]['gu'], GT[g][0]['nm'], g[1], st.median(t1), st.median(j1), st.median(th), st.median(jh)))
print(f'\n같은 단지·면적 안 전세가율(4칸 다 있는 묶음 {len(R1)}개): 1층 가운데 {st.median(R1)*100:.1f}% · 6층 이상 가운데 {st.median(RH)*100:.1f}% · 1층이 높은 묶음 {sum(1 for a,b in zip(R1,RH) if a>b)}/{len(R1)}')
for e in ex: print('   ', e)
# 계약 구분을 맞춰서: 신규끼리·갱신끼리(6층 이상도 같은 구분만 2건 이상)
print()
for ct in ('신규', '갱신'):
    rows = [r for r in J if r['ct'] == ct]
    print(f'전세 {ct}끼리 ({len(rows)}건)'); show('1층', pairs(rows, 1, 1)); show('2층', pairs(rows, 2, 2))
    s = [p for p in pairs(rows, 1, 1) if 80 <= p[0]['ar'] <= 86]; show('1층 84㎡ 안팎', s)
print('구분 칸 비어 있는 전세', sum(1 for r in J if r['ct'] not in ('신규', '갱신')))
