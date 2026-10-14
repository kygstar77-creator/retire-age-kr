import json, datetime, sys
sys.stdout.reconfigure(encoding='utf-8')
def load(fn):
    d=json.load(open(fn))['chart']['result'][0]
    ts=d['timestamp']; q=d['indicators']['quote'][0]
    rows=[]
    for t,c,h,l in zip(ts,q['close'],q['high'],q['low']):
        if c is None: continue
        dt=(datetime.datetime.utcfromtimestamp(t)+datetime.timedelta(hours=9)).date()
        rows.append((dt,c,h,l))
    return d['meta'],rows
for fn in ['y_SDI.json','y_KOSPI.json']:
    m,r=load(fn); print(fn,m.get('currency'),m.get('regularMarketPrice'),m.get('fiftyTwoWeekHigh'),m.get('fiftyTwoWeekLow'))
    for x in r[-10:]: print(x)
    print('first',r[0])
