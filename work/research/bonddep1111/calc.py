import json,statistics as st
d=json.load(open('raw/ecos_1111.json',encoding='utf-8'))
k={t:float(v) for t,v,_ in d['ktb3_m']}; p={t:float(v) for t,v,_ in d['dep_BEABAA211']}; b={t:float(v) for t,v,_ in d['base_m']}
ms=sorted(set(k)&set(p))
print('최근 15개월 월·국고3년·정기예금신규·기준금리')
for m in ms[-15:]: print(m,k[m],p[m],b.get(m))
dk=[k[ms[i]]-k[ms[i-1]] for i in range(1,len(ms))]; dp=[p[ms[i]]-p[ms[i-1]] for i in range(1,len(ms))]
def corr(a,b_):
    ma,mb=st.mean(a),st.mean(b_); 
    return sum((x-ma)*(y-mb) for x,y in zip(a,b_))/ (sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b_))**.5
print('월 변화 상관(국고채 변화 → L달 뒤 예금 변화)')
for L in range(0,7): print(L, round(corr(dk[:len(dk)-L], dp[L:]),3))
# 수준 차이
sp=[p[m]-k[m] for m in ms]
print('예금-국고채 차이 중앙(전체)',round(st.median(sp),2),'최근',round(sp[-1],2))
# 국고채 3달 새 0.3%p 넘게 오른 때, 그다음 3달 예금 변화
print('국고채가 3달 새 0.3%p 넘게 오른 시점 → 같은 3달 예금 변화, 이후 3달 예금 변화')
cnt=0;same=[];after=[]
for i in range(3,len(ms)-3):
    up=k[ms[i]]-k[ms[i-3]]
    if up>=0.3:
        same.append(p[ms[i]]-p[ms[i-3]]); after.append(p[ms[i+3]]-p[ms[i]]); cnt+=1
print('개월 수',cnt,'같은3달 예금 중앙',round(st.median(same),2),'뒤3달 예금 중앙',round(st.median(after),2), '뒤3달 오른 비율', sum(1 for x in after if x>0),'/',len(after))
# 2022 사이클
for m in ms:
    if m.startswith('2021') or m.startswith('2022') or m.startswith('2023'): pass
pk_k=max((m for m in ms if '202101'<=m<='202312'),key=lambda m:k[m]); pk_p=max((m for m in ms if '202101'<=m<='202312'),key=lambda m:p[m])
print('2021~2023 국고채 최고',pk_k,k[pk_k],'예금 최고',pk_p,p[pk_p])
for m in ms:
    if '202201'<=m<='202302': print(m,k[m],p[m],b.get(m))
print('--- 차이(예금-국고채)가 -0.6%p 이하였던 달 → 3달 뒤 예금 변화')
xs=[]
for i in range(len(ms)-3):
    if p[ms[i]]-k[ms[i]]<=-0.6: xs.append((ms[i],round(p[ms[i+3]]-p[ms[i]],2)))
print(len(xs),'달', '오른 달',sum(1 for _,x in xs if x>0),'중앙',st.median([x for _,x in xs]) if xs else None)
print([m for m,_ in xs])
print('2025.08→2026.09 국고채',round(k['202609']-k['202508'],2),'예금',round(p['202609']-p['202508'],2))
print('1억 0.6%p 세전 연',int(1e8*0.006))
print('--- 54달 나머지 내역')
up=sum(1 for _,x in xs if x>0); same=sum(1 for _,x in xs if x==0); dn=sum(1 for _,x in xs if x<0)
print('오름',up,'그대로',same,'내림',dn)
dd=[(t,float(v)) for t,v,_ in d['ktb3_d'] if t.startswith('202609')]
print('9월 일별 최고',max(dd,key=lambda a:a[1]), '4% 넘은 날',sum(1 for _,v in dd if v>=4))
print('--- 54달 석 달 뒤 틈 좁혀진 원인')
a=b_=c=0
for m,_ in xs:
    i=ms.index(m); j=i+3
    g0=p[m]-k[m]; g1=p[ms[j]]-k[ms[j]]
    if g1>g0:
        dpp=p[ms[j]]-p[m]; dkk=k[ms[j]]-k[m]
        if dpp>0 and dkk>=0: a+=1
        elif dkk<0 and dpp<=0: b_+=1
        else: c+=1
print('좁혀짐: 예금 올라서',a,'국고채 내려서',b_,'둘 다(예금↑·국고채↓)',c,'안 좁혀짐',len(xs)-a-b_-c)
