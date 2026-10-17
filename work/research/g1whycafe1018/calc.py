import sys, os, json, time, datetime as dt
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'); sys.stdout.reconfigure(encoding='utf-8')
import apis
HERE = os.path.dirname(os.path.abspath(__file__)); OZ = 31.1034768
def krx_gold():
    out, page = {}, 1
    while page < 40:
        d = apis._j(f'https://m.stock.naver.com/front-api/marketIndex/prices?category=metals&reutersCode=M04020000&page={page}&pageSize=60')
        rows = d.get('result') or []
        if not rows: break
        for r in rows: out[r['localTradedAt'][:10]] = float(r['closePrice'].replace(',', ''))
        if min(out) < '2025-09-01': break
        page += 1; time.sleep(0.3)
    return dict(sorted(out.items()))
def yahoo(sym):
    p1 = int(dt.datetime(2025, 8, 25).timestamp()); p2 = int(time.time()) + 86400
    d = apis._j(f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}?period1={p1}&period2={p2}&interval=1d')
    r = d['chart']['result'][0]; tz = r['meta']['gmtoffset']; out = {}
    for t, c in zip(r['timestamp'], r['indicators']['quote'][0]['close']):
        if c is not None: out[dt.datetime.fromtimestamp(t + tz, dt.timezone.utc).strftime('%Y-%m-%d')] = float(c)
    return out
def ecos_fx(end):
    k = apis.key('ecos')
    d = apis._j(f'https://ecos.bok.or.kr/api/StatisticSearch/{k}/json/kr/1/600/731Y001/D/20250825/{end}/0000001')
    return {f"{r['TIME'][:4]}-{r['TIME'][4:6]}-{r['TIME'][6:]}": float(r['DATA_VALUE']) for r in d['StatisticSearch']['row']}
def on_or_before(s, day):
    ks = [k for k in s if k <= day]; return (ks[-1], s[ks[-1]])
def before(s, day):
    ks = [k for k in s if k < day]; return (ks[-1], s[ks[-1]])
krx = krx_gold(); gc = yahoo('GC=F'); fx = ecos_fx(dt.date.today().strftime('%Y%m%d'))
json.dump({'KRX':krx,'GC':gc,'FX':fx}, open(os.path.join(HERE,'raw_20261017.json'),'w',encoding='utf-8'), ensure_ascii=False)
def parts(buy, sell):
    r = {}
    for tag, d in (('b', buy), ('s', sell)):
        kd, k = on_or_before(krx, d); gd, g = before(gc, kd); fd, f = on_or_before(fx, kd)
        i = g*f/OZ
        r[tag] = dict(krx_day=kd, krx=k, gc_day=gd, gc=g, fx_day=fd, fx=f, intl=i, prem=(k/i-1))
    b, s = r['b'], r['s']
    out = dict(buy=b, sell=s, usd=s['gc']/b['gc']-1, fxchg=s['fx']/b['fx']-1, prem=(1+s['prem'])/(1+b['prem'])-1, total=s['krx']/b['krx']-1)
    out['check'] = (1+out['usd'])*(1+out['fxchg'])*(1+out['prem'])-1
    return out
last = max(krx)
print('last KRX day', last, krx[last])
for sell in ('2026-10-06', last):
    p = parts('2025-10-02', sell)
    print('==== sell', sell)
    print(json.dumps(p, ensure_ascii=False, indent=1))
    print('1천만원 ->', round(10_000_000*(1+p['total'])))
