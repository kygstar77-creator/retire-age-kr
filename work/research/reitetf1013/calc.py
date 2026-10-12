# 리츠 ETF 두 개 1년 보유 계산 — 가격은 야후 일별 종가, 분배금은 야후 분배 이력(KODEX 9월 60원은 삼성자산운용 분배금 현황과 대조)
P={'TIGER':{'p0':4370,'p1':4020,'d':[33]*12},'KODEX':{'p0':4790,'p1':4205,'d':[33,31,29,29,29,29,30,30,29,29,29,60]}}
TAX=0.154
for k,v in P.items():
    n=int(1e8//v['p0']); cost=n*v['p0']; D=sum(v['d']); dist=n*D; px=n*(v['p1']-v['p0'])
    pre=px+dist; post=px+dist*(1-TAX)
    print(k,'주수',n,'원금',cost,'분배합/주',D,'분배금 세전',dist,'세후',round(dist*(1-TAX)),'가격차',px,
          '세전합',pre,round(pre/cost*100,2),'%','세후합',round(post),round(post/cost*100,2),'%','가격%',round((v['p1']/v['p0']-1)*100,2),'분배%',round(D/v['p0']*100,2),
          '세후1억의',round(1e8+post))
    print(' 월평균 세전',round(dist/12),'세후',round(dist*(1-TAX)/12))
