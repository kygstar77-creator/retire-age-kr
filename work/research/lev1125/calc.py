# lev1125 직접 계산 — 야후 수정 종가(분배 재투자·분할 반영) QQQ·QLD·TQQQ
# ① 1년(252거래일) 굴려 보기: QQQ가 -5%~+5%(제자리)였던 시작일에서 QLD·TQQQ 1년 수익
# ② 2021년 11월 고점 → QQQ가 그 값을 되찾은 날, 그날 QLD·TQQQ는 자기 고점 대비 몇 %, 언제 되찾았나
# ③ 낙폭(2022), 처음부터 지금까지 연평균
import json, datetime, statistics as st
def load(t):
    d=json.load(open(f"raw/{t}.json"))["chart"]["result"][0]
    ts=d["timestamp"]; adj=d["indicators"]["adjclose"][0]["adjclose"]
    out={}
    for a,b in zip(ts,adj):
        if b is None: continue
        out[datetime.datetime.fromtimestamp(a,datetime.UTC).date()]=b
    return out
Q,L,T=load("QQQ"),load("QLD"),load("TQQQ")
def common(*ds):
    s=set(ds[0]);[s:=s&set(x) for x in ds[1:]];return sorted(s)
def pct(a,b): return (b/a-1)*100
print("마지막 날", max(Q), "QQQ",round(Q[max(Q)],2),"QLD",round(L[max(L)],2),"TQQQ",round(T[max(T)],2))
for name,X,lab in [("QLD",L,"2006-06 상장부터"),("TQQQ",T,"2010-02 상장부터")]:
    days=common(Q,X); N=252
    rows=[(days[i],pct(Q[days[i]],Q[days[i+N]]),pct(X[days[i]],X[days[i+N]])) for i in range(len(days)-N)]
    flat=[r for r in rows if -5<=r[1]<=5]
    neg=[r for r in flat if r[2]<0]
    xs=[r[2] for r in flat]
    print(f"\n[{name} {lab}] 1년 시작일 {len(rows)}개 · QQQ 제자리(-5~+5%) {len(flat)}개({len(flat)/len(rows)*100:.1f}%)")
    print(f"  그때 {name} 1년: 가운데 {st.median(xs):.1f}% · 가장 나쁨 {min(xs):.1f}% · 가장 좋음 {max(xs):.1f}% · 손실 {len(neg)}개({len(neg)/len(flat)*100:.0f}%)")
    print(f"  그때 QQQ 1년 가운데 {st.median([r[1] for r in flat]):.1f}%")
    # 해별로 어디서 나왔나
    yrs={}
    for r in flat: yrs[r[0].year]=yrs.get(r[0].year,0)+1
    print("  시작 해별 개수", yrs)
    # QQQ 정확히 0% 근처(±1%)
    f1=[r[2] for r in rows if -1<=r[1]<=1]
    print(f"  QQQ ±1% {len(f1)}개: {name} 가운데 {st.median(f1):.1f}% · 손실 {sum(1 for x in f1 if x<0)}개")
    # 반대로 QQQ +20% 넘은 해: 몇 배?
    up=[r for r in rows if r[1]>=20]
    print(f"  QQQ +20%↑ {len(up)}개: QQQ 가운데 {st.median([r[1] for r in up]):.1f}% · {name} 가운데 {st.median([r[2] for r in up]):.1f}%")
    # 3년
    N3=756; rows3=[(days[i],pct(Q[days[i]],Q[days[i+N3]]),pct(X[days[i]],X[days[i+N3]])) for i in range(len(days)-N3)]
    fl3=[r for r in rows3 if -10<=r[1]<=10]
    if fl3:
        x3=[r[2] for r in fl3]
        print(f"  3년 QQQ -10~+10% {len(fl3)}개: {name} 가운데 {st.median(x3):.1f}% · 가장 나쁨 {min(x3):.1f}% · 손실 {sum(1 for x in x3 if x<0)}개")
# ② 2021 고점
d=common(Q,L,T)
pk=max((x for x in d if x.year==2021),key=lambda x:Q[x])
print("\n[2021 고점] QQQ 고점", pk, round(Q[pk],2))
for name,X in [("QLD",L),("TQQQ",T)]:
    xp=max((x for x in d if x.year==2021),key=lambda x:X[x]); print(f"  {name} 고점 {xp} {X[xp]:.2f}")
after=[x for x in d if x>pk]
rq=next(x for x in after if Q[x]>=Q[pk]); print("  QQQ 되찾은 날", rq, f"{(rq-pk).days}일")
for name,X in [("QLD",L),("TQQQ",T)]:
    xp=max((x for x in d if x.year==2021),key=lambda x:X[x])
    print(f"  그날 {name} 자기 고점 대비 {pct(X[xp],X[rq]):.1f}%")
    r=next((x for x in d if x>xp and X[x]>=X[xp]),None)
    print(f"  {name} 되찾은 날 {r} {(r-xp).days if r else '-'}일")
    lo=min((x for x in d if xp<x<=(r or max(d))),key=lambda x:X[x]); print(f"  {name} 바닥 {lo} {pct(X[xp],X[lo]):.1f}%")
lo=min((x for x in d if pk<x<=rq),key=lambda x:Q[x]); print(f"  QQQ 바닥 {lo} {pct(Q[pk],Q[lo]):.1f}%")
# ③ 처음부터 연평균 (TQQQ 상장일 기준 같은 날)
d0=common(Q,L,T); a,b=d0[0],d0[-1]; yrs=(b-a).days/365.25
for name,X in [("QQQ",Q),("QLD",L),("TQQQ",T)]:
    print(f"[{a}~{b}] {name} 누적 {pct(X[a],X[b]):.0f}% 연평균 {((X[b]/X[a])**(1/yrs)-1)*100:.1f}%  1억→{X[b]/X[a]:.1f}억")
# 올해
y0=max(x for x in d0 if x.year==2025)
for name,X in [("QQQ",Q),("QLD",L),("TQQQ",T)]: print(f"올해({y0}종가→{b}) {name} {pct(X[y0],X[b]):.1f}%")
# ④ 올해 고점 → 마지막 날 (이번 하락)
for name,X in [("QQQ",Q),("QLD",L),("TQQQ",T)]:
    hp=max((x for x in X if x.year==2026),key=lambda x:X[x]); last=max(X)
    print(f"[올해 고점] {name} {hp} {X[hp]:.2f} → {last} {pct(X[hp],X[last]):.1f}%")
# 11/20 하루
dd=sorted(d0); a,b=dd[-2],dd[-1]
for name,X in [("QQQ",Q),("QLD",L),("TQQQ",T)]: print(f"[하루 {b}] {name} {pct(X[a],X[b]):.2f}%")
# ⑤ 6/2 → 10/6: QQQ는 더 올랐는데 TQQQ는?
a,b=datetime.date(2026,6,2),datetime.date(2026,10,6)
for name,X in [("QQQ",Q),("QLD",L),("TQQQ",T)]: print(f"[6/2→10/6] {name} {X[a]:.2f}→{X[b]:.2f} {pct(X[a],X[b]):.1f}%")
seg=[x for x in d0 if a<=x<=b]; import math
r=[Q[seg[i+1]]/Q[seg[i]]-1 for i in range(len(seg)-1)]
print(f"  그 사이 거래일 {len(seg)-1}일 · QQQ 하루 2% 넘게 움직인 날 {sum(1 for x in r if abs(x)>0.02)}일")
