# qqqi1123 계산 2 — NEOS 공식 분배 표(neos_qqqi_1121.txt, 소수 넷째 자리) × 야후 직전 종가
import re,json,datetime,statistics as st
s=open("neos_qqqi_1121.txt",encoding="utf-8").read()
rows=re.findall(r"(\d\d/\d\d/\d{4}) (\d\d/\d\d/\d{4}) (\d\d/\d\d/\d{4}) (\d\d/\d\d/\d{4}) \$(\d\.\d{4})",s)
neos={datetime.datetime.strptime(r[1],"%m/%d/%Y").date():float(r[4]) for r in rows}
neos=dict(sorted(neos.items()))
r=json.load(open("yahoo_QQQI_1121.json"))["chart"]["result"][0]
ds=[datetime.date.fromtimestamp(x) for x in r["timestamp"]]; c=r["indicators"]["quote"][0]["close"]
print("NEOS 표",len(neos),"번", min(neos), "~", max(neos))
rat=[];prevv=None;prevp=None;same=0;n=0;rows2=[]
for d,v in neos.items():
    i=ds.index(d); p=c[i-1]; q=v/p*100; rat.append(q)
    if prevv is not None:
        n+=1; dv=v-prevv; dp=p-prevp
        if (dv>0)==(dp>0): same+=1
        rows2.append((d,v,round(p,2),round(q,2),f"{dv/prevv*100:+.1f}",f"{dp/prevp*100:+.1f}"))
    prevv=v;prevp=p
for x in rows2: print(*x)
print("직전 종가 대비 비율: 최소 %.2f 최대 %.2f 중앙 %.2f"%(min(rat),max(rat),st.median(rat)))
print("1.16~1.19%% 안: %d / %d"%(sum(1.155<=x<1.195 for x in rat),len(rat)))
print("분배금이 오르내린 방향 = 직전 종가 방향: %d / %d"%(same,n))
# 2026 1~11월 합, 12개월 합
y26=sum(v for d,v in neos.items() if d.year==2026); l12=sum(list(neos.values())[-12:])
print("2026 1~11월 합 %.4f, 최근 12번 합 %.4f, 11/20 종가 %.2f -> 12개월 분배율 %.2f%%"%(y26,l12,c[-1],l12/c[-1]*100))
print("11월 0.5838*12/직전 종가 49.55 = %.2f%%"%(0.5838*12/49.55*100))
