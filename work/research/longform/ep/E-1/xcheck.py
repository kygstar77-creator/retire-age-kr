"""주가 교차 확인 (2026-09-30): 야후(raw/*_5y.json) vs 네이버 금융 일별 시세(한국 2종목) · 나스닥 공식 과거 시세(MU).
공식 금융위 시세(data.go.kr)는 우리 키 활용신청이 없어 403 — 확인 안 함. 결과 → xcheck.json"""
import json, os, sys, urllib.request, datetime, re
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(H, 'raw')
UA = {'User-Agent': 'Mozilla/5.0'}
def yahoo(sym):
    j = json.load(open(os.path.join(R, f'{sym}_5y.json'), encoding='utf-8'))['chart']['result'][0]
    ts = j['timestamp']; c = j['indicators']['quote'][0]['close']
    off = j['meta'].get('gmtoffset', 0)
    return {datetime.datetime.utcfromtimestamp(t + off).strftime('%Y%m%d'): v for t, v in zip(ts, c) if v}
def naver(code):
    p = os.path.join(R, f'naver_{code}.txt')
    if not os.path.exists(p):
        u = f'https://api.finance.naver.com/siseJson.naver?symbol={code}&requestType=1&startTime=20250901&endTime=20260930&timeframe=day'
        open(p, 'wb').write(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read())
    t = open(p, encoding='utf-8', errors='replace').read()
    return {m[0]: float(m[1]) for m in re.findall(r'\["(\d{8})",\s*[\d.]+,\s*[\d.]+,\s*[\d.]+,\s*([\d.]+)', t)}
def nasdaq(sym):
    p = os.path.join(R, f'nasdaq_{sym}.json')
    if not os.path.exists(p):
        u = f'https://api.nasdaq.com/api/quote/{sym}/historical?assetclass=stocks&fromdate=2025-09-01&todate=2026-09-30&limit=400'
        open(p, 'wb').write(urllib.request.urlopen(urllib.request.Request(u, headers={**UA, 'Accept': 'application/json'}), timeout=30).read())
    rows = json.load(open(p, encoding='utf-8'))['data']['tradesTable']['rows']
    return {datetime.datetime.strptime(r['date'], '%m/%d/%Y').strftime('%Y%m%d'): float(r['close'].replace('$', '').replace(',', '')) for r in rows}
def stats(s):
    ks = sorted(s); last = ks[-1]
    d0 = (datetime.date(int(last[:4]) - 1, int(last[4:6]), int(last[6:]))).strftime('%Y%m%d')
    base = [k for k in ks if k <= d0][-1]
    win = [k for k in ks if k >= base]
    peak, mdd, pk, tr = 0, 0, None, None
    for k in win:
        if s[k] > peak: peak, pkk = s[k], k
        dd = s[k] / peak - 1
        if dd < mdd: mdd, pk, tr = dd, pkk, k
    return {'last': last, 'close': s[last], 'base': base, 'base_close': s[base], 'ret1y': s[last] / s[base] - 1, 'mdd': mdd, 'peak': pk, 'trough': tr}
out = {}
for name, y, other in (('SK하이닉스', '000660.KS', ('naver', '000660')), ('삼성전자', '005930.KS', ('naver', '005930')), ('마이크론', 'MU', ('nasdaq', 'MU'))):
    a = yahoo(y); b = naver(other[1]) if other[0] == 'naver' else nasdaq(other[1])
    common = sorted(set(a) & set(b)); diff = [k for k in common if abs(a[k] / b[k] - 1) > 0.005]
    out[name] = {'yahoo': stats(a), other[0]: stats(b), 'common_days': len(common), 'mismatch_days_over_0.5pct': diff[:10], 'n_mismatch': len(diff)}
    print(name, 'Y', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in out[name]['yahoo'].items()})
    print(name, other[0][0].upper(), {k: (round(v, 4) if isinstance(v, float) else v) for k, v in out[name][other[0]].items()}, '공통', len(common), '불일치', len(diff), diff[:5])
json.dump(out, open(os.path.join(H, 'xcheck.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
