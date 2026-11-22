# 다우지수: DIA 보유 파일(SSGA 11/19)·야후 종가로 주가가중 효과 직접 계산
import json, urllib.request, datetime as dt, openpyxl, os
H={"User-Agent":"Mozilla/5.0"}
def rows(f):
    ws=openpyxl.load_workbook(f,read_only=True).active
    return [r for r in ws.iter_rows(values_only=True) if r and r[1] and r[4] is not None and r[1]!='-' and r[0]!='Name']
dia=rows("raw/dia_holdings.xlsx"); spy={r[1]:r[4] for r in rows("raw/spy_holdings.xlsx")}
print("DIA 종목 수",len(dia),"주식 수 같은지",len({r[6] for r in dia})==1, dia[0][6])
D=dt.date(2026,11,19)
def close(t,day=D):
    fn=f"raw/q_{t}.json"
    if not os.path.exists(fn):
        u=f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=1mo&interval=1d"
        open(fn,"wb").write(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=30).read())
    r=json.load(open(fn))["chart"]["result"][0]
    for a,c in zip(r["timestamp"],r["indicators"]["quote"][0]["close"]):
        d=(dt.datetime.fromtimestamp(a,dt.UTC)-dt.timedelta(hours=5)).date()
        if d==day: return c
px={r[1]:close(r[1]) for r in dia}
dji=close("^DJI"); s=sum(px.values()); div=s/dji
print("11/19 다우",round(dji,2),"30종목 주가 합",round(s,2),"나눗수(계산)",round(div,6),"1달러 = 지수",round(1/div,2),"포인트")
tot=sum(px.values())
print("종목 | DIA비중 | 주가비중(계산) | SPY비중 | 주가 | 5%오르면 다우 포인트")
for r in sorted(dia,key=lambda r:-r[4]):
    t=r[1]; p=px[t]
    print(t,round(r[4],2),round(p/tot*100,2),round(spy.get(t,0),2),round(p,2),round(p*0.05/div,0))
top5=sorted(dia,key=lambda r:-r[4])[:5]; print("다우 상위 5개 합",round(sum(r[4] for r in top5),1))
print("SPY 안 30종목 비중 합",round(sum(spy.get(r[1],0) for r in dia),1))
# 다우 vs S&P 1년·올해 (가격 지수)
def ser(t):
    r=json.load(open(f"raw/{t}.json"))["chart"]["result"][0]
    return {(dt.datetime.fromtimestamp(a,dt.UTC)-dt.timedelta(hours=5)).date():c for a,c in zip(r["timestamp"],r["indicators"]["quote"][0]["close"]) if c}
J=ser("DJI"); G=ser("GSPC"); ds=sorted(set(J)&set(G)); L=ds[-1]
def ob(d): return [x for x in ds if x<=d][-1]
for nm,a in [("1년",ob(L.replace(year=L.year-1))),("올해",ob(dt.date(L.year-1,12,31)))]:
    print(nm,a,"~",L,"다우",f"{(J[L]/J[a]-1)*100:+.1f}%","S&P500",f"{(G[L]/G[a]-1)*100:+.1f}%")
print("최근",L,"다우",round(J[L],2),"S&P",round(G[L],2))
