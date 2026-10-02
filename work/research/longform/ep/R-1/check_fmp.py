# SCHD·GLD 종가·분배금 교차 확인(FMP) — 야후 값과 대조, 2026-10-03
import sys, json, urllib.request
sys.path.insert(0, '../../../../'); import apis
k = apis.key('fmp'); out = {}
for s in ['SCHD', 'GLD', 'SPY']:
    for name, u in [('px', f'https://financialmodelingprep.com/stable/historical-price-eod/light?symbol={s}&from=2025-09-30&to=2026-10-03&apikey={k}'),
                    ('div', f'https://financialmodelingprep.com/stable/dividends?symbol={s}&apikey={k}')]:
        try: out.setdefault(s, {})[name] = json.load(urllib.request.urlopen(u, timeout=30))
        except Exception as e: out.setdefault(s, {})[name] = str(e)[:80]
y = json.load(open('raw/yahoo_20261003.json', encoding='utf-8'))
for s in out:
    px = out[s]['px']
    if isinstance(px, list):
        d = {x['date']: x['price'] for x in px}
        for D in ['2025-10-02', '2026-10-02']: print(s, D, 'FMP', d.get(D), '야후', round(y[s]['px'][D], 2))
    else: print(s, 'px', px)
    dv = out[s]['div']
    if isinstance(dv, list): print(s, 'div', [(x.get('date'), x.get('dividend') or x.get('adjDividend')) for x in dv if '2025-10-02' < x.get('date', '') <= '2026-10-02'])
    else: print(s, 'div', dv)
json.dump(out, open('raw/fmp_check_20261003.json', 'w', encoding='utf-8'), ensure_ascii=False)
