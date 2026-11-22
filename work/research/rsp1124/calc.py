# RSP(동일가중) vs SPY(시가총액 가중) — 야후 수정 종가(분배 재투자, 세전·달러 기준)
import json, datetime as dt
def load(t):
    r=json.load(open(f"raw/{t}.json"))["chart"]["result"][0]
    ts=r["timestamp"]; adj=r["indicators"]["adjclose"][0]["adjclose"]; cl=r["indicators"]["quote"][0]["close"]
    out={}
    for a,b,c in zip(ts,adj,cl):
        if b is None: continue
        d=(dt.datetime.fromtimestamp(a,dt.UTC).replace(tzinfo=None)-dt.timedelta(hours=5)).date()
        out[d]=(b,c)
    return out
R=load("RSP"); S=load("SPY")
days=sorted(set(R)&set(S)); last=days[-1]
print("기준일",last,"RSP",round(R[last][1],2),"SPY",round(S[last][1],2))
def on_or_before(d):
    c=[x for x in days if x<=d]; return c[-1]
def ret(X,a,b): return X[b][0]/X[a][0]-1
for y in [1,3,5,10,20]:
    a=on_or_before(last.replace(year=last.year-y))
    rr,ss=ret(R,a,last),ret(S,a,last)
    print(f"{y}년({a}~): RSP {rr*100:+.1f}% SPY {ss*100:+.1f}%  1억→ RSP {1e4*(1+rr):,.0f}만 SPY {1e4*(1+ss):,.0f}만  연평균 RSP {((1+rr)**(1/y)-1)*100:.1f}% SPY {((1+ss)**(1/y)-1)*100:.1f}%")
a=days[0]; rr,ss=ret(R,a,last),ret(S,a,last); n=(last-a).days/365.25
print(f"상장 뒤({a}~, {n:.1f}년): RSP {rr*100:+.0f}% SPY {ss*100:+.0f}% 연평균 RSP {((1+rr)**(1/n)-1)*100:.1f}% SPY {((1+ss)**(1/n)-1)*100:.1f}%")
# 해마다
wins=[];rows=[]
for y in range(a.year+1,last.year+1):
    s=on_or_before(dt.date(y-1,12,31)); e=on_or_before(dt.date(y,12,31)) if y<last.year else last
    rr,ss=ret(R,s,e),ret(S,s,e); rows.append((y,rr,ss)); wins.append(rr>ss)
for y,rr,ss in rows: print(y,f"RSP {rr*100:+.1f} SPY {ss*100:+.1f} {'RSP' if rr>ss else 'SPY'} 차이 {abs(rr-ss)*100:.1f}%p")
full=[w for (y,_,_),w in zip(rows,wins) if y<last.year]
print("완전한 해",len(full),"RSP 이긴 해",sum(full), "SPY",len(full)-sum(full))
# 연속 구간: 최근 몇 년 연속 SPY
# 낙폭
def mdd(X,s,e):
    pk=None;m=0;pd=None;bd=None
    for d in days:
        if d<s or d>e: continue
        v=X[d][0]
        if pk is None or v>pk: pk=v;pkd=d
        dd=v/pk-1
        if dd<m: m=dd;bd=d;pd=pkd
    return m,pd,bd
for nm,s,e in [("2008 금융위기",dt.date(2007,1,1),dt.date(2009,12,31)),("2020 코로나",dt.date(2020,1,1),dt.date(2020,12,31)),("2022 금리",dt.date(2022,1,1),dt.date(2022,12,31))]:
    mr=mdd(R,s,e); ms=mdd(S,s,e)
    print(nm,f"RSP {mr[0]*100:.1f}% ({mr[1]}→{mr[2]}) SPY {ms[0]*100:.1f}% ({ms[1]}→{ms[2]})")
# 분배 1년
def divs(t):
    r=json.load(open(f"raw/{t}.json"))["chart"]["result"][0]; ev=r.get("events",{}).get("dividends",{})
    out=[]
    for k,v in ev.items():
        d=(dt.datetime.fromtimestamp(int(k),dt.UTC).replace(tzinfo=None)-dt.timedelta(hours=5)).date(); out.append((d,v["amount"]))
    return sorted(out)
for t,X in [("RSP",R),("SPY",S)]:
    dv=[x for x in divs(t) if x[0]>last.replace(year=last.year-1)]
    tot=sum(v for _,v in dv); print(t,"최근 1년 분배",len(dv),"번",round(tot,4),"달러 분배율",round(tot/X[last][1]*100,2),"%",[(str(d),round(v,4)) for d,v in dv])
# 국내 상장: TIGER 미국S&P500동일가중(488500) vs TIGER 미국S&P500(360750) — 원화, 야후 수정 종가(분배 반영)
def loadk(t):
    r=json.load(open(f"raw/{t}.json"))["chart"]["result"][0]
    ts=r["timestamp"]; adj=r["indicators"]["adjclose"][0]["adjclose"]; cl=r["indicators"]["quote"][0]["close"]
    return {(dt.datetime.fromtimestamp(a,dt.UTC)+dt.timedelta(hours=9)).date():(b,c) for a,b,c in zip(ts,adj,cl) if b}
E=loadk("488500.KS"); T=loadk("360750.KS"); kd=sorted(set(E)&set(T)); kl=kd[-1]
def kb(d): return [x for x in kd if x<=d][-1]
print("국내 기준일",kl,"488500",E[kl][1],"360750",T[kl][1])
for nm,a in [("상장 뒤",kd[0]),("1년",kb(kl.replace(year=kl.year-1))),("올해",kb(dt.date(kl.year-1,12,31)))]:
    e=E[kl][0]/E[a][0]-1; s=T[kl][0]/T[a][0]-1
    print(f"국내 {nm}({a}~): 동일가중 {e*100:+.1f}% S&P500 {s*100:+.1f}%  1억→ {1e4*(1+e):,.0f}만 vs {1e4*(1+s):,.0f}만")
# 아무 날 사서 N년 들고 있었다면 — 매 거래일 시작, 동일가중이 앞선 비율(세전·분배 재투자·달러)
import bisect
for y in [1,3,5,10]:
    w=n=0; gaps=[]
    for i,a in enumerate(days):
        try: b=a.replace(year=a.year+y)
        except ValueError: b=a.replace(year=a.year+y,day=28)
        if b>last: break
        j=bisect.bisect_right(days,b)-1; e=days[j]
        rr,ss=ret(R,a,e),ret(S,a,e); n+=1; w+= rr>ss; gaps.append(rr-ss)
    gaps.sort()
    print(f"보유 {y}년 시작일 {n}개: 동일가중 앞섬 {w/n*100:.0f}% ({w}) · 차이 중앙 {gaps[len(gaps)//2]*100:+.1f}%p")
# 고점 회복 기간
def recover(X,s,e):
    pk=max((X[d][0],d) for d in days if s<=d<=e and d<=e)
    return pk
for nm,pkR,pkS in [("2008",dt.date(2007,7,19),dt.date(2007,10,9)),("2020",dt.date(2020,2,12),dt.date(2020,2,19)),("2022",dt.date(2022,1,4),dt.date(2022,1,3))]:
    out=[]
    for X,p in [(R,pkR),(S,pkS)]:
        v=X[p][0]; rec=next((d for d in days if d>p and X[d][0]>=v and d>p+dt.timedelta(days=30)),None)
        out.append(f"{p}→{rec} {((rec-p).days/30.44) if rec else 0:.0f}달")
    print("회복",nm,"RSP",out[0],"SPY",out[1])
