# QQQ vs QQQM 미국 현지 2025-10-13 종가 → 2026-10-12 종가, 1억 기준. 종가=네이버 증권/야후 일치, 분배금=나스닥 API(락일 기준).
# 분배금은 다시 사지 않고 단순 합. 환율·세금·수수료·소수점 주식은 뺌.
P={'QQQ':dict(p0=602.01,p1=746.04,d=[0.79408,0.73282,0.81349,0.75143]),
   'QQQM':dict(p0=247.83,p1=307.19,d=[0.32301,0.32769,0.35215,0.31266])}
R={}
for k,v in P.items():
    S=sum(v['d']); price=v['p1']/v['p0']-1; dy=S/v['p0']; tot=price+dy
    R[k]=dict(S=S,price=price,dy=dy,tot=tot)
    print(k,'가격변화 %.3f%%'%(price*100),'분배합 %.5f달러'%S,'분배율 %.3f%%'%(dy*100),'합계 %.3f%%'%(tot*100),'1억이 ->',round(1e8*(1+tot)),'원 (이익',round(1e8*tot),')')
g_p=R['QQQM']['price']-R['QQQ']['price']; g_d=R['QQQM']['dy']-R['QQQ']['dy']; g=R['QQQM']['tot']-R['QQQ']['tot']
print('차이 가격 %.4f%%p'%(g_p*100),round(g_p*1e8),'원 / 분배 %.4f%%p'%(g_d*100),round(g_d*1e8),'원 / 합계 %.4f%%p'%(g*100),round(g*1e8),'원')
print('보수차(0.18-0.15)=0.03%p ->',round(0.0003*1e8),'원')
print('남는 차이',round(g*1e8)-30000,'원')
