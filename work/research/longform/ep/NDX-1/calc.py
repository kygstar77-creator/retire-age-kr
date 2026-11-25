# 12/2 예비 후보(지수): 나스닥100 고점에서 샀다면 원금 회복까지 — FRED NASDAQ100(가격지수, 배당 빠짐) 일별 종가
import csv,sys,datetime as dt; sys.stdout.reconfigure(encoding='utf-8')
p=sys.argv[1] if len(sys.argv)>1 else 'research/longform/loop/slot1202b/fred_NASDAQ100_1124.csv'
r=[(dt.date.fromisoformat(a),float(b)) for a,b in csv.reader(open(p)) if a[0].isdigit() and b not in('','.')]
print('기간',r[0][0],'~',r[-1][0],len(r),'일')
# 낙폭 구간: 고점 → 바닥 → 고점 회복
eps=[];peak=r[0];trough=r[0];inDD=False
for d,v in r:
    if v>=peak[1]:
        if inDD and (peak[1]-trough[1])/peak[1]>=0.10: eps.append((peak,trough,(d,v)))
        peak=(d,v);trough=(d,v);inDD=False
    else:
        inDD=True
        if v<trough[1]: trough=(d,v)
if inDD: eps.append((peak,trough,None))
print('\n고점 대비 -10% 넘게 빠진 구간',len(eps))
for pk,tr,rc in eps:
    dd=(tr[1]/pk[1]-1)*100
    days=(rc[0]-pk[0]).days if rc else None
    print(f"{pk[0]} {pk[1]:,.0f} → 바닥 {tr[0]} {tr[1]:,.0f} ({dd:.1f}%) → 회복 {rc[0] if rc else '아직'} · 고점에서 {days if days is not None else (r[-1][0]-pk[0]).days}일{'' if rc else '(진행 중)'}")
for th in (20,30,50):
    s=[e for e in eps if (e[1][1]/e[0][1]-1)*100<=-th]
    print(f"-{th}% 넘은 구간 {len(s)}")
last=r[-1]; pk=max(r,key=lambda x:x[1])
print('\n최근',last,'역대 최고',pk,f"{(last[1]/pk[1]-1)*100:.1f}%")
