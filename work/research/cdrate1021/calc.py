# cdrate1021 계산 — 원자료 raw/ecos_1021.json (한국은행 ECOS 817Y002·722Y001, 2026-10-21 조회)
import json
e=json.load(open('raw/ecos_1021.json',encoding='utf-8'))
cd={a:float(b) for a,b,c in e['cd91']}; kf={a:float(b) for a,b,c in e['kofr']}; base={a:float(b) for a,b,c in e['base']}
both=sorted(d for d in cd if d in kf)
print('최근', both[-1], 'CD', cd[both[-1]], 'KOFR', kf[both[-1]], '차', round(cd[both[-1]]-kf[both[-1]],3), '기준금리', base.get(both[-1]))
def avg(dd,lo,hi): v=[dd[d] for d in both if lo<=d<=hi]; return sum(v)/len(v), len(v)
for lo,hi,nm in [('20251020','20261019','최근 1년'),('20260101','20261019','올해'),('20260716','20261019','7/16 인상 뒤'),('20260827','20261019','8/27 인상 뒤')]:
    a,n=avg(cd,lo,hi); b,_=avg(kf,lo,hi); print(nm, n,'일', 'CD 평균',round(a,3),'KOFR 평균',round(b,3),'차',round(a-b,3))
a,_=avg(cd,'20251020','20261019'); b,_=avg(kf,'20251020','20261019')
print('1억 1년 단리 세전 CD', round(1e8*a/100), 'KOFR', round(1e8*b/100), '차', round(1e8*(a-b)/100))
print('세후(15.4%) 차', round(1e8*(a-b)/100*0.846))
sp=[(d,round(cd[d]-kf[d],3)) for d in both]
print('차 최소', min(sp,key=lambda x:x[1]), '최대', max(sp,key=lambda x:x[1]))
print('KOFR-기준금리 최근', round(kf[both[-1]]-base[both[-1]],3), 'CD-기준금리', round(cd[both[-1]]-base[both[-1]],3))
for d in ['20260715','20260716','20260717','20260826','20260827','20260828']: print(d,'CD',cd.get(d),'KOFR',kf.get(d),'기준',base.get(d))
# 하루 변동 크기
import statistics
dc=[abs(cd[both[i]]-cd[both[i-1]]) for i in range(1,len(both)) if both[i]>='20251020']
dk=[abs(kf[both[i]]-kf[both[i-1]]) for i in range(1,len(both)) if both[i]>='20251020']
print('하루 변동 평균 CD',round(statistics.mean(dc),4),'KOFR',round(statistics.mean(dk),4), '0 변동 일수 CD', sum(1 for x in dc if x==0),'/',len(dc))
