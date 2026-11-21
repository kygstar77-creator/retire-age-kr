# H-6 대조군: 같은 강남구(11680) 국토부 실거래로, 1년 전(2025.10~12 계약)과 요즘(2026.10~11 계약) 둘 다 거래가 있는 단지·면적(전용 80~86㎡)별 가운데 값 변화
# 제미나이 반론(11/20 '강남구 지수와 대조') 대응 — 한국부동산원 지수 API는 키 필요라 같은 원자료로 셈. 해제·공공기관·직거래 뺌
# 실행: py -3.12 work/research/longform/ep/H-6/calc3.py > calc3_out.txt
import json, os, sys, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
RT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'rt')
A=['202510','202511','202512']; B=['202610','202611']
def num(s): return float(str(s or '0').replace(',', '') or 0)
def load(ms):
    out=[]
    for m in ms:
        p=os.path.join(RT,f'11680_{m}_trade.json')
        d=json.load(open(p,encoding='utf-8')); out+=[r for r in d if isinstance(r,dict) and 'aptNm' in r]
    return [r for r in out if not r.get('cdealType') and r.get('buyerGbn')!='공공기관' and r.get('dealingGbn')!='직거래' and 80<=num(r['excluUseAr'])<=86]
def grp(rows):
    g=collections.defaultdict(list)
    for r in rows: g[(r['umdNm'],r['aptNm'].replace(' ',''))].append(num(r['dealAmount']))
    return g
ga,gb=grp(load(A)),grp(load(B))
allA=load(A); print(f'# 강남구 80~86㎡ 1년 전 묶음 {len(allA)}건(해제·공공기관·직거래 뺌) · 은마 직거래 0/75건(calc_out)')
rows=[]
for k in ga:
    if k in gb:
        a,b=st.median(ga[k]),st.median(gb[k]); rows.append((b/a-1,k,len(ga[k]),len(gb[k]),a,b))
rows.sort()
for p,k,na,nb,a,b in rows: print(f"{k[0]} {k[1]} · {na}건 {a/1e4:.2f}억 → {nb}건 {b/1e4:.2f}억 · {p*100:+.1f}%")
ps=[r[0] for r in rows]
print(f'\n단지 {len(rows)}곳 · 변화 가운데 값 {st.median(ps)*100:+.1f}% · 내린 곳 {sum(1 for p in ps if p<0)} · 오른 곳 {sum(1 for p in ps if p>0)}')
big=[r for r in rows if r[2]>=2 and r[3]>=2]
if big: print(f'양쪽 2건 이상 {len(big)}곳 · 가운데 값 {st.median([r[0] for r in big])*100:+.1f}%')
