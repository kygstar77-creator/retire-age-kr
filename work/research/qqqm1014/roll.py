# 산 날을 바꿔 가며 1년(달력 기준 365일 뒤 첫 거래일 종가) 보유 합계 차이(QQQM - QQQ). 야후 종가·분배(락일). 분배 단순 합.
import json,datetime,bisect
def load(t):
    r=json.load(open(f'y_{t}.json'))['chart']['result'][0]
    ts=r['timestamp']; c=r['indicators']['quote'][0]['close']
    px=sorted((datetime.date.fromtimestamp(a),b) for a,b in zip(ts,c) if b)
    dv=sorted((datetime.date.fromtimestamp(v['date']),v['amount']) for v in r['events']['dividends'].values())
    return px,dv
A=load('QQQ'); B=load('QQQM')
def tot(x,d0,d1):
    px,dv=x; dates=[p[0] for p in px]
    i=bisect.bisect_left(dates,d0); j=bisect.bisect_right(dates,d1)-1
    p0=px[i][1]; p1=px[j][1]; S=sum(a for d,a in dv if d0<d<=d1)
    return (p1+S)/p0-1, dates[i], dates[j]
last=A[0][-1][0]; res=[]
for d0 in [p[0] for p in A[0]]:
    d1=d0.replace(year=d0.year+1) if not (d0.month==2 and d0.day==29) else d0.replace(year=d0.year+1,day=28)
    if d1>last: break
    a,i0,j0=tot(A,d0,d1); b,i1,j1=tot(B,d0,d1)
    res.append((d0,(b-a)*1e8))
vals=[v for _,v in res]
print('창',len(res),'개 첫날',res[0][0],'끝',res[-1][0])
print('차이(원/1억) 최소',round(min(vals)),'최대',round(max(vals)),'평균',round(sum(vals)/len(vals)),'중앙',round(sorted(vals)[len(vals)//2]))
print('QQQM이 더 큰 창',sum(1 for v in vals if v>0),'/',len(vals))
print('가장 작은 날',min(res,key=lambda x:x[1]),'가장 큰 날',max(res,key=lambda x:x[1]))
