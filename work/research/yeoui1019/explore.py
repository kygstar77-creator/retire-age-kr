import json, glob, os, statistics as st, collections, sys
sys.stdout.reconfigure(encoding='utf-8')
RT = os.path.join(os.path.dirname(__file__), '..', 'rt')
def num(s): return float(str(s or '0').replace(',', '') or 0)
months=[f'2025{m:02d}' for m in range(11,13)]+[f'2026{m:02d}' for m in range(1,11)]
out=[]
for m in months:
    d=json.load(open(os.path.join(RT,f'11560_{m}_trade.json'),encoding='utf-8')); out+=d
R=[r for r in out if not r.get('cdealType') and r.get('buyerGbn')!='공공기관' and r['umdNm']=='여의도동']
print(len(out),len(R)); print(R[0])
c=collections.Counter(r['aptNm'] for r in R); print(c.most_common(25))
ar=collections.Counter(round(num(r['excluUseAr'])) for r in R); print(sorted(ar.items()))
g=collections.defaultdict(list)
for r in R: g[(r['aptNm'],round(num(r['excluUseAr']),1))].append((int(r['floor']),num(r['dealAmount'])/1e4,r['dealYear']+r['dealMonth'].zfill(2)+r['dealDay'].zfill(2)))
for k,v in sorted(g.items(), key=lambda x:-len(x[1])):
    if len(v)>=4:
        print(k,len(v),sorted(v))
print('=== floor split')
rows=[]
for k,v in sorted(g.items(), key=lambda x:-len(x[1])):
    lo=[p for f,p,_ in v if f<=5]; hi=[p for f,p,_ in v if f>=10]; mid=[p for f,p,_ in v if 6<=f<=9]
    if len(lo)>=2 and len(hi)>=2:
        a,b=st.median(lo),st.median(hi); print(k,len(v),'저층(≤5)',len(lo),a,'고층(≥10)',len(hi),b,f'{(b/a-1)*100:+.1f}%'); rows.append((b/a-1)*100)
print(len(rows), st.median(rows), rows)
