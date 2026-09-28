import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.load(open('data.json',encoding='utf-8'))
print(d['fetched'])
for s in d['yahoo']:
    m=d['yahoo'][s]['meta']; rows=d['yahoo'][s]['rows']
    print('\n##',s,m)
    print('last 6',rows[-6:])
    ser={r[0][:10]:r[1] for r in rows}
    keys=sorted(ser)
    hi=max(keys,key=lambda k:ser[k]); print('ALL high close',hi,ser[hi])
    y26=[k for k in keys if k>='2026-01-01']; h26=max(y26,key=lambda k:ser[k]); l26=min(y26,key=lambda k:ser[k])
    print('2026 high',h26,ser[h26],'2026 low',l26,ser[l26])
    last25=[k for k in keys if k<'2026-01-01'][-1]; print('last 2025',last25,ser[last25])
    yr=[k for k in keys if k<='2025-09-26'][-1]; print('1y ago',yr,ser[yr])
    # month-end
    me={}
    for k in keys: me[k[:7]]=(k,ser[k])
    print('month-ends',[ (v[0],round(v[1],2)) for kk,v in sorted(me.items()) if kk>='2025-01'])
