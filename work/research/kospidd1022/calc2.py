import json,datetime,re
d=json.load(open('raw/ks11_1d.json'))['chart']['result'][0]
rows=[(datetime.datetime.utcfromtimestamp(t+9*3600).date(),x) for t,x in zip(d['timestamp'],d['indicators']['quote'][0]['close']) if x]
# append fchart (1차) for 2014-07 onward, replacing
fc=[(datetime.datetime.strptime(m[0],'%Y%m%d').date(),float(m[1])) for m in re.findall(r'item data="(\d{8})\|[^|]*\|[^|]*\|[^|]*\|([^|]*)\|',open('raw/kospi_fchart.xml',encoding='utf-8',errors='ignore').read())]
cut=fc[0][0]
# compare overlap
ov={a:b for a,b in rows if a>=cut}
diffs=[abs(ov[a]-b) for a,b in fc if a in ov]
print('overlap',len(diffs),'maxdiff',max(diffs))
rows=[r for r in rows if r[0]<cut]+fc
print('last',rows[-1])
eps=[(datetime.date(1997,6,17),),(datetime.date(2000,1,4),),(datetime.date(2007,10,31),),(datetime.date(2018,1,29),),(datetime.date(2021,7,6),),(datetime.date(2026,6,22),)]
idx={r[0]:i for i,r in enumerate(rows)}
for (pk,) in eps:
    i=idx[pk]; p=rows[i][1]
    # monthly DCA: first trading day of each month from peak month (start at peak day)
    inv=0;units=0;lastm=None;rec=None;trough=min(rows[i:],key=lambda r:r[1]) 
    for dt,x in rows[i:]:
        m=(dt.year,dt.month)
        if m!=lastm:
            inv+=1;units+=1/x;lastm=m
        if inv>=3 and units*x>=inv and rec is None: rec=(dt,inv,round(units*x,3))
    # index recovery
    ir=next(((dt,x) for dt,x in rows[i+1:] if x>=p),None)
    print(pk,round(p,2),'index_rec',ir[0] if ir else None,'dca_rec',rec)
# today vs july low
jl=min((r for r in rows if datetime.date(2026,7,1)<=r[0]<=datetime.date(2026,8,31)),key=lambda r:r[1])
print('july low',jl,'today',rows[-1],'prev',rows[-2], 'chg',round((rows[-1][1]/rows[-2][1]-1)*100,2),'from peak',round((rows[-1][1]/9114.55-1)*100,2))
# 2026 DCA from June 22 current state
print('--- DCA recovery after trough (monthly 1 unit from peak month)')
for (pk,) in eps[:-1]:
    i=idx[pk]; p=rows[i][1]
    ir=next(((dt,x) for dt,x in rows[i+1:] if x>=p))
    seg=rows[i:idx[ir[0]]+1]
    tr=min(seg,key=lambda r:r[1])
    inv=0;units=0;lastm=None;rec=None
    for dt,x in rows[i:]:
        m=(dt.year,dt.month)
        if m!=lastm: inv+=1;units+=1/x;lastm=m
        if dt>tr[0] and units*x>=inv and rec is None: rec=(dt,inv)
    yrs=lambda a,b: round((b-a).days/365.25,1)
    print(f"{pk} peak {p:.2f} trough {tr[0]} {tr[1]:.2f} dd {(tr[1]/p-1)*100:.1f}% | index rec {ir[0]} ({yrs(pk,ir[0])}y from peak, {yrs(tr[0],ir[0])}y from trough) | dca rec {rec[0]} ({yrs(pk,rec[0])}y from peak, months {rec[1]})")
print('--- 2026: 100만원씩 매달 첫 거래일 (6/22 고점에 첫 번째)')
inv=0;units=0;lastm=None;buys=[]
for dt,x in rows[idx[datetime.date(2026,6,22)]:]:
    m=(dt.year,dt.month)
    if m!=lastm: inv+=100;units+=100/x;lastm=m;buys.append((str(dt),x))
val=units*rows[-1][1]
print(buys,'invested',inv,'value',round(val,1),'pct',round((val/inv-1)*100,1),'avgcost',round(inv/units,2))
print('lump 1000 at peak ->',round(1000*rows[-1][1]/9114.55,1))
# 본전까지 필요한 상승률
print('need from today to peak',round((9114.55/rows[-1][1]-1)*100,1),'need to dca avg',round(((inv/units)/rows[-1][1]-1)*100,1))
print('--- 매달 넣기: 저점 뒤 처음 본전 / 그 뒤 다시 안 깨진 날(지수 회복일까지 넣기 계속)')
for (pk,) in eps[:-1]:
    i=idx[pk]; p=rows[i][1]
    ir=next(((dt,x) for dt,x in rows[i+1:] if x>=p))
    seg=rows[i:idx[ir[0]]+1]; tr=min(seg,key=lambda r:r[1])
    inv=0;units=0;lastm=None;first=None;last_below=None;hist=[]
    for dt,x in rows[i:idx[ir[0]]+1]:
        m=(dt.year,dt.month)
        if m!=lastm: inv+=1;units+=1/x;lastm=m
        ok=units*x>=inv
        if dt>tr[0] and ok and first is None: first=dt
        if not ok: last_below=dt
    stay=next(dt for dt,x in rows[idx[last_below]+1:])
    yrs=lambda a,b: round((b-a).days/365.25,1)
    print(pk,'first',first,yrs(pk,first),'stay',stay,yrs(pk,stay))
after=[r for r in rows if r[0]>datetime.date(2026,6,22)]
print('post-peak lowest before today', min(after[:-1],key=lambda r:r[1]))
