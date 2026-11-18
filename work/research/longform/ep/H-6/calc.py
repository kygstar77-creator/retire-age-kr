# H-6 은마 1년 실거래 재현 — 재료: work/research/rt/11680_<월>_{trade,rent}.json(국토교통부 실거래, rtmolit.py 2026-11-19 받음)
# 실행: py -3.12 work/research/longform/ep/H-6/calc.py > calc_out.txt · 해제·공공기관 매수 제외, 단위 만원
import json, os, sys, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
RT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'rt')
MS = ['202510','202511','202512','202601','202602','202603','202604','202605','202606','202607','202608','202609','202610','202611']
def num(s): return float(str(s or '0').replace(',', '') or 0)
def load(kind):
    out=[]
    for m in MS:
        p=os.path.join(RT,f'11680_{m}_{kind}.json')
        if os.path.exists(p):
            d=json.load(open(p,encoding='utf-8')); out+=[r for r in d if isinstance(r,dict) and 'aptNm' in r]
    return out
T=[r for r in load('trade') if r['aptNm'].replace(' ','')=='은마' and r['umdNm']=='대치동']
canc=[r for r in T if r.get('cdealType')]
T=[r for r in T if not r.get('cdealType') and r.get('buyerGbn')!='공공기관']
print(f'# 은마 매매 {len(T)}건(해제 {len(canc)}건 뺌) · 계약월 {MS[0]}~{MS[-1]}')
g=collections.defaultdict(list)
for r in T: g[round(num(r['excluUseAr']))].append(r)
for a,rows in sorted(g.items()):
    print(f'\n## 전용 {a}㎡ {len(rows)}건')
    for r in sorted(rows,key=lambda r:(int(r['dealYear']),int(r['dealMonth']),int(r['dealDay']))):
        print(f"{r['dealYear']}.{str(r['dealMonth']).zfill(2)}.{str(r['dealDay']).zfill(2)} {num(r['dealAmount'])/10000:.2f}억 {r['floor']}층 {r.get('dealingGbn','')}")
    am=[num(r['dealAmount']) for r in rows]
    print(f'최고 {max(am)/10000:.2f}억 · 최저 {min(am)/10000:.2f}억 · 중앙 {st.median(am)/10000:.2f}억')
print('\n## 월별 건수(모든 면적)')
c=collections.Counter(f"{r['dealYear']}.{str(r['dealMonth']).zfill(2)}" for r in T)
for k in sorted(c): print(k,c[k])
R=[r for r in load('rent') if r['aptNm'].replace(' ','')=='은마' and r['umdNm']=='대치동']
print(f'\n## 전월세 {len(R)}건 · 월별')
c=collections.Counter(f"{r['dealYear']}.{str(r['dealMonth']).zfill(2)}" for r in R)
for k in sorted(c): print(k,c[k])
