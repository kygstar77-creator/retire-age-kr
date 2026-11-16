# KOSPI-1 계산 3 — '누구라면' 두 갈래: 무리 첫날 1천만원 한 번에 vs 첫날부터 12번(21거래일마다) 나눠 넣기, 둘 다 첫날+252거래일 종가로 평가.
# 지수 값만(배당·세금·수수료·보수 뺌). 나눠 넣는 동안 아직 안 넣은 돈은 이자 없이 둔 것으로 셈(예금 이자 뺌 — 한 갈래를 유리하게 만들지 않으려고 둘 다 뺌). 지난 값만, 예측 없음.
import json, statistics as st
rows = json.load(open('kospi_daily_ecos.json'))
ch = [(rows[i][0], rows[i][1], (rows[i][1]/rows[i-1][1]-1)*100, i) for i in range(1,len(rows))]
eps=[]; last=-999
for d,v,c,i in ch:
    if c<=-5:
        if i-last>60: eps.append((d,v,c,i))
        last=i
T=10_000_000; out=[]
for d,v,c,i in eps:
    if i+252>=len(rows): continue
    end=rows[i+252][1]
    lump=T*end/v
    units=sum((T/12)/rows[i+21*k][1] for k in range(12))
    dca=units*end
    out.append((d,round(lump),round(dca)))
    print(f"{d} 한 번에 {lump/1e4:,.0f}만 · 나눠 넣기 {dca/1e4:,.0f}만 · {'나눠 넣기가 많음' if dca>lump else '한 번에가 많음'}")
L=[x[1] for x in out]; D=[x[2] for x in out]
print('편수',len(out),'| 한 번에: 최저',min(L),'중앙',st.median(L),'최고',max(L),'원금 넘은 편',sum(x>T for x in L))
print('나눠 넣기: 최저',min(D),'중앙',st.median(D),'최고',max(D),'원금 넘은 편',sum(x>T for x in D))
print('나눠 넣기가 더 많은 편',sum(b>a for _,a,b in out),'/',len(out))
