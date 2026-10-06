# schdacct1007 계산 — firemap-write 10/6
div=[0.2782,0.2569,0.2525,0.2665]  # 슈왑 공식 Distributions(12/15/2025·3/30·6/29·9/28/2026 지급)
px=32.72; fx=1341.54                # Yahoo SCHD 10/5 종가 · USD/KRW 10/6
yr=sum(div); print('최근 4회 합',round(yr,4),'배당률',round(yr/px*100,2),'%')
pre=2_000_000
sh=pre/(yr*fx); amt=sh*px*fx
print('세전 연 200만원 받으려면',round(sh),'주 ·',round(amt/1e4),'만원어치')
us=pre*0.15; net=pre-us; print('미국 15%',us,'남는 돈',net,'월',round(net/12))
for r,a in ((0.055,'70세 미만'),(0.044,'70~79'),(0.033,'80+')): print('연금소득세',a,r,round(net*r))
# ISA 일반형 한도 200만: 분배 170만 < 200만 → 국내 0
# 금융소득 2천만: SCHD 직접만으로 넘으려면 세전 배당 2천만 → 원금
print('세전 배당 2천만원 원금',round(20_000_000/(yr/px)/1e8,2),'억원')
