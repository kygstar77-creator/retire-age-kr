# qqqi1123 직접 계산 — 야후 chart API(11/21 받은 yahoo_*_1121.json) 원래 종가·adjclose·분배금
import json,datetime,statistics as st
def load(t):
    r=json.load(open(f"yahoo_{t}_1121.json"))["chart"]["result"][0]
    ds=[datetime.date.fromtimestamp(x) for x in r["timestamp"]]
    c=r["indicators"]["quote"][0]["close"]; a=r["indicators"]["adjclose"][0]["adjclose"]
    dv={datetime.date.fromtimestamp(int(k)):v["amount"] for k,v in r.get("events",{}).get("dividends",{}).items()}
    return ds,c,a,dict(sorted(dv.items()))
qd,qc,qa,qdv=load("QQQI"); Qd,Qc,Qa,Qdv=load("QQQ"); jd,jc,ja,jdv=load("JEPQ")
print("== QQQI 분배금 전체", len(qdv), "번")
prev=None
for d,v in qdv.items():
    i=qd.index(d) if d in qd else None
    px=qc[i-1] if i else None
    chg=f"{(v/prev-1)*100:+.1f}%" if prev else ""
    print(d, v, chg, f"직전 종가 {px:.2f} 월분배율 {v/px*100:.2f}%" if px else "")
    prev=v
vals=list(qdv.values())
print("최근12번 합", round(sum(vals[-12:]),3), "그전12번 합", round(sum(vals[-24:-12]),3))
print("가장 적은 달", min(qdv.items(),key=lambda x:x[1]))
def at(ds,arr,d):
    for i,x in enumerate(ds):
        if x>=d: return x,arr[i]
def ret(ds,arr,d0,d1):
    a0=at(ds,arr,d0); a1=at(ds,arr,d1) if d1 else (ds[-1],arr[-1])
    return a0,a1,(a1[1]/a0[1]-1)*100
start=datetime.date(2024,1,30); last=qd[-1]
print("== 마지막 날", last)
for name,(ds,c,a) in {"QQQI":(qd,qc,qa),"QQQ":(Qd,Qc,Qa),"JEPQ":(jd,jc,ja)}.items():
    p=ret(ds,c,start,None); t=ret(ds,a,start,None)
    print(name,"상장 뒤(2024-01-30~) 값만", f"{p[2]:+.1f}%", "분배 다시 넣으면", f"{t[2]:+.1f}%", p[0],round(p[0][1],2),"->",round(p[1][1],2))
pk=datetime.date(2026,10,6)
for name,(ds,c,a) in {"QQQI":(qd,qc,qa),"QQQ":(Qd,Qc,Qa),"JEPQ":(jd,jc,ja)}.items():
    p=ret(ds,c,pk,None); t=ret(ds,a,pk,None)
    print(name,"10/6 뒤 값", f"{p[2]:+.1f}%","분배 포함", f"{t[2]:+.1f}%")
# 2025 하락: 2025-02-19 ~ 2025-04-08
for name,(ds,c,a) in {"QQQI":(qd,qc,qa),"QQQ":(Qd,Qc,Qa),"JEPQ":(jd,jc,ja)}.items():
    seg=[(d,x) for d,x in zip(ds,a) if datetime.date(2025,2,1)<=d<=datetime.date(2025,5,1)]
    hi=max(seg,key=lambda x:x[1]); lo=min([s for s in seg if s[0]>hi[0]],key=lambda x:x[1])
    # 회복: lo 뒤 처음으로 hi 이상
    rec=next(((d,x) for d,x in zip(ds,a) if d>lo[0] and x>=hi[1]),None)
    print(name,"2025 하락(분배 포함)",hi[0],lo[0],f"{(lo[1]/hi[1]-1)*100:.1f}%","되찾은 날",rec[0] if rec else None)
# 1만 달러 상장 첫날 넣고 분배는 현금으로 받기
for name,(ds,c,dv) in {"QQQI":(qd,qc,qdv),"QQQ":(Qd,Qc,Qdv),"JEPQ":(jd,jc,jdv)}.items():
    a0=at(ds,c,start); sh=10000/a0[1]
    cash=sum(v*sh for d,v in dv.items() if d>a0[0])
    print(name,"1만달러, 분배 현금으로", "남은 값",round(sh*c[-1]),"받은 분배",round(cash),"합",round(sh*c[-1]+cash))
