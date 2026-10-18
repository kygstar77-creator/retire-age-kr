import json, statistics as st, sys
sys.stdout.reconfigure(encoding='utf-8')
exec(open('calc.py',encoding='utf-8').read().split("by = collections")[0])
def ym(r): return r['dealYear']+r['dealMonth'].zfill(2)
res=[]
for a in ['목동신시가지1','목동신시가지2','목동신시가지3','목동신시가지4','목동신시가지5','목동신시가지6','목동신시가지7','목동청구한신아파트','롯데캐슬위너','목동롯데캐슬마에스트로','금호어울림','우성','대원칸타빌2']:
    rs=[r for r in T if r['aptNm']==a]
    import collections as C
    b=C.Counter(int(num(r['excluUseAr'])//5*5) for r in rs).most_common(1)[0][0]
    sel=[r for r in rs if int(num(r['excluUseAr'])//5*5)==b]
    e=[num(r['dealAmount']) for r in sel if ym(r)<='202602']; l=[num(r['dealAmount']) for r in sel if ym(r)>='202606']
    ar=st.median(num(r['excluUseAr']) for r in sel)
    o=dict(apt=a,area=round(ar,2),pyeong=round(ar/3.305785,1),n=len(sel),early_n=len(e),early=st.median(e) if e else None,late_n=len(l),late=st.median(l) if l else None,all=st.median(num(r['dealAmount']) for r in sel))
    if e and l: o['chg']=round((o['late']/o['early']-1)*100,1)
    res.append(o); print(o)
json.dump(res,open('cmp.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
# 신시가지 전체 vs 나머지 거래 비중
s=sum(1 for r in T if '신시가지' in r['aptNm']); print('신시가지 거래',s,'/',len(T))
mon=C.Counter((ym(r),'신' if '신시가지' in r['aptNm'] else '기타') for r in T); print(sorted(mon.items()))
