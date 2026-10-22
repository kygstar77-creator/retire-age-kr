import json,datetime
d=json.load(open('raw/ks11_1d.json'))['chart']['result'][0]
rows=[(datetime.datetime.utcfromtimestamp(t+9*3600).date(),x) for t,x in zip(d['timestamp'],d['indicators']['quote'][0]['close']) if x]
print('first',rows[0],'last',rows[-1],'n',len(rows))
# drawdown episodes: from ATH peak, trough, recovery date
eps=[];peak=rows[0];trough=rows[0];indd=False
for dt,x in rows:
    if x>=peak[1]:
        if indd and (trough[1]/peak[1]-1)<=-0.30:
            eps.append((peak,trough,(dt,x)))
        peak=(dt,x);trough=(dt,x);indd=False
    else:
        indd=True
        if x<trough[1]: trough=(dt,x)
if indd: eps.append((peak,trough,None))
for p,t,r in eps:
    dd=(t[1]/p[1]-1)*100
    print(f"peak {p[0]} {p[1]:.2f} trough {t[0]} {t[1]:.2f} dd {dd:.1f}% days_to_trough {(t[0]-p[0]).days} recover {r[0] if r else '-'} total_days {(r[0]-p[0]).days if r else '-'} trough_to_recover {(r[0]-t[0]).days if r else '-'}")
