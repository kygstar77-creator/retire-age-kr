# 동탄구(41597) 토허·규제지역(2026-07-01·07-05) 앞뒤 — 같은 단지·같은 넓이(1㎡ 반올림) 짝 비교, 동별 몫, 가격대별 몫. S1 raw 그대로, 해제 뺌.
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
num = lambda s: float(str(s or '0').replace(',', '') or 0)
rows = []
for p in sorted(glob.glob(os.path.join(H, 'raw', '*_trade.json'))):
    for r in json.load(open(p, encoding='utf-8')):
        if r.get('cdealType'): continue
        r['_ym'] = int(r['dealYear']) * 100 + int(r['dealMonth']); r['_d']=int(r['dealDay']); r['_p'] = num(r['dealAmount']); r['_a'] = round(num(r['excluUseAr']))
        r['_k'] = (r.get('aptSeq') or r['aptNm'], r['_a']); rows.append(r)
def per(r):
    ym=r['_ym']
    if 202601<=ym<=202606: return 'A'      # 2026년 1~6월(규제 전)
    if 202607<=ym<=202611: return 'B'      # 2026년 7~11월(규제 뒤)
    if 202507<=ym<=202511: return 'Y'      # 1년 전 같은 달 2025년 7~11월
    return None
g=C.defaultdict(lambda: C.defaultdict(list))
for r in rows:
    p=per(r)
    if p: g[r['_k']][p].append(r['_p'])
def pair(a,b,minn=1):
    rs=[]; n=0
    for k,v in g.items():
        if len(v[a])>=minn and len(v[b])>=minn:
            rs.append(st.median(v[b])/st.median(v[a])-1); n+=1
    return n, st.median(rs) if rs else None
for mn in (1,2,3):
    n,m=pair('A','B',mn); print(f'같은 집(각 {mn}건↑) 2026년 1~6월 → 7~11월: {n}쌍, 가운데 변화 {m*100:+.1f}%')
    n,m=pair('Y','B',mn); print(f'같은 집(각 {mn}건↑) 2025년 7~11월 → 2026년 7~11월: {n}쌍, 가운데 변화 {m*100:+.1f}%')
# 6월 한 달 vs 9~11월
g2=C.defaultdict(lambda: C.defaultdict(list))
for r in rows:
    if r['_ym']==202606: g2[r['_k']]['J'].append(r['_p'])
    if 202609<=r['_ym']<=202611: g2[r['_k']]['S'].append(r['_p'])
rs=[st.median(v['S'])/st.median(v['J'])-1 for v in g2.values() if v['J'] and v['S']]
print(f'같은 집 2026년 6월 → 9~11월: {len(rs)}쌍, 가운데 {st.median(rs)*100:+.1f}%, 오른 쌍 {sum(1 for x in rs if x>0)/len(rs)*100:.0f}%')
# 6월 말 막차: 6월 날짜별
jun=[r for r in rows if r['_ym']==202606]
print('6월 1~15일', sum(1 for r in jun if r['_d']<=15),'· 16~29일', sum(1 for r in jun if 16<=r['_d']<=29), '· 30일', sum(1 for r in jun if r['_d']==30))
jul=[r for r in rows if r['_ym']==202607]
print('7월 1~4일', sum(1 for r in jul if r['_d']<=4),'· 5~31일', sum(1 for r in jul if r['_d']>=5))
# 기간별 한 달 평균 건수
for lab,lo,hi in (('2025년 1~9월',202501,202509),('2025년 10월~2026년 5월',202510,202605),('2026년 6월',202606,202606),('2026년 7~10월',202607,202610)):
    v=[r for r in rows if lo<=r['_ym']<=hi]; months=len({r['_ym'] for r in v})
    print(f'{lab}: 월평균 {len(v)/months:,.0f}건')
# 가격대별 몫: 규제 전(1~6월) vs 뒤(7~11월)
for lab,p in (('1~6월','A'),('7~11월','B')):
    v=[r['_p'] for r in rows if per(r)==p]
    bands=[(0,60000),(60000,90000),(90000,150000),(150000,10**9)]
    print(lab, len(v),'건 · ', ' · '.join(f'{lo//10000}~{hi//10000 if hi<10**8 else ""}억 {sum(1 for x in v if lo<=x<hi)/len(v)*100:.0f}%' for lo,hi in bands))
# 동별 몫
for lab,p in (('1~6월','A'),('7~11월','B')):
    v=[r for r in rows if per(r)==p]; c=C.Counter(r['umdNm'] for r in v)
    print(lab,' · '.join(f'{d} {n/len(v)*100:.0f}%' for d,n in c.most_common(6)))
