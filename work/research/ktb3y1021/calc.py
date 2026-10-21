# ktb3y1021 계산 — 원자료 raw/ecos_1021.json (한국은행 ECOS 817Y002 국고채3년·10년 일별, 722Y001 기준금리 일별, 2026-10-21 조회)
import json,statistics
e=json.load(open('raw/ecos_1021.json',encoding='utf-8'))
k3={a:float(b) for a,b,c in e['ktb3']}; base={a:float(b) for a,b,c in e['base']}; k10={a:float(b) for a,b,c in e['ktb10']}
ds=sorted(d for d in k3 if d in base and d>='20080307')
sp={d:round(k3[d]-base[d],3) for d in ds}
last=ds[-1]; print('최근',last,'국고3',k3[last],'기준',base[last],'차',sp[last], '10년',k10.get(last))
print('기준금리 도입 뒤 영업일',len(ds), ds[0])
ge=[d for d in ds if sp[d]>=sp[last]]
print('차 >= 지금 일수',len(ge), round(len(ge)/len(ds)*100,2),'%')
# 연도별 그런 날
from collections import Counter
print('연도별', sorted(Counter(d[:4] for d in ge).items()))
mx=max(ds,key=lambda d:sp[d]); mn=min(ds,key=lambda d:sp[d]); print('최대',mx,sp[mx],k3[mx],base[mx],'최소',mn,sp[mn],k3[mn],base[mn])
# 연도별 평균 차
for y in range(2008,2027):
    v=[sp[d] for d in ds if d[:4]==str(y)]
    if v: print(y,'평균차',round(statistics.mean(v),3),'최대',max(v),'기준금리 연말',base[[d for d in ds if d[:4]==str(y)][-1]])
# 최근 1년 흐름
for d in ['20251020','20260102','20260401','20260701','20260715','20260716','20260826','20260827','20260901','20261001','20261015','20261016','20261017','20261019','20261020','20261021']:
    dd=max(x for x in ds if x<=d); print(d,dd,'국고3',k3[dd],'기준',base[dd],'차',sp[dd])
# 0.8 넘은 구간(연속)
runs=[];cur=None
for d in ds:
    if sp[d]>=0.8:
        if cur is None: cur=[d,d]
        else: cur[1]=d
    else:
        if cur: runs.append(cur); cur=None
if cur: runs.append(cur)
print('0.8%p 넘은 구간',[(a,b) for a,b in runs][:40], len(runs))
# 1년 전 같은 때
y1=max(x for x in ds if x<='20251021'); print('1년 전',y1,k3[y1],base[y1],sp[y1])
# 이번 인상 사이클 중 국고3 최저·지금
lo=min((d for d in ds if d>='20250101'),key=lambda d:k3[d]); print('2025년 이후 국고3 최저',lo,k3[lo],base[lo])

print('--- 10/21 기준(기준금리는 8/27 3.0% 뒤 바뀐 적 없음 — 10/20·10/21은 ECOS 일별 아직 없어 3.0으로 채움) ---')
base2=dict(base); base2['20261020']=3.0; base2['20261021']=3.0
ds2=sorted(d for d in k3 if d in base2 and d>='20080307')
sp2={d:round(k3[d]-base2[d],3) for d in ds2}
t=sp2['20261021']; print('10/21 국고3',k3['20261021'],'차',t,'영업일',len(ds2))
ge2=[d for d in ds2 if sp2[d]>=t]; print('차>=0.822 일수',len(ge2),round(len(ge2)/len(ds2)*100,1),'%', sorted(Counter(d[:4] for d in ge2).items()))
mx26=max((d for d in ds2 if d>='20260101'),key=lambda d:sp2[d]); print('올해 최대',mx26,sp2[mx26],k3[mx26])
# 구간별: 0.8 넘은 덩어리 시기와 그 시기 앞뒤 기준금리 변화
for a,b,nm in [('20080307','20081231','2008'),('20090101','20110630','2009~2011'),('20171001','20180630','2017~2018'),('20210601','20221130','2021~2022'),('20260301','20261021','2026')]:
    dd=[d for d in ds2 if a<=d<=b and sp2[d]>=0.8]
    print(nm,'0.8넘은날',len(dd), dd[:1], dd[-1:], '구간 기준금리', base2[min(x for x in ds2 if x>=a)],'→',base2[max(x for x in ds2 if x<=b)])
# 10년
print('10년 10/21',k10['20261021'],'1년전',k10.get(max(x for x in k10 if x<='20251021')))
