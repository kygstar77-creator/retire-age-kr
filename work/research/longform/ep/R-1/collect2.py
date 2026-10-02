# R-1 영수증 막대: SPY·SCHD·GLD 1년(2025-10-02 → 2026-10-02) 종가·분배금 + 원/달러 매매기준율(ECOS 731Y001)
import sys, json, os, urllib.request
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'); sys.stdout.reconfigure(encoding='utf-8')
import apis
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'raw')
k = apis.key('fmp'); out = {}
for s in ['SPY', 'SCHD', 'GLD']:
    for name, u in [('px', f'https://financialmodelingprep.com/stable/historical-price-eod/light?symbol={s}&from=2025-09-25&to=2026-10-03&apikey={k}'),
                    ('div', f'https://financialmodelingprep.com/stable/dividends?symbol={s}&apikey={k}')]:
        try: out[f'{s}_{name}'] = json.load(urllib.request.urlopen(u, timeout=30))
        except Exception as e: out[f'{s}_{name}'] = str(e)
ek = apis.key('ecos')
d = apis._j(f'https://ecos.bok.or.kr/api/StatisticSearch/{ek}/json/kr/1/400/731Y001/D/20250925/20261003/0000001')
out['USDKRW_D'] = [(r['TIME'], r['DATA_VALUE']) for r in d.get('StatisticSearch', {}).get('row', [])]
json.dump(out, open(os.path.join(D, 'collect2_20261003.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for kk, v in out.items():
    if isinstance(v, list): print(kk, len(v), v[:2] if kk.startswith('USD') else [ (x.get('date'), x.get('price') or x.get('dividend')) for x in v[:3]], v[-1] if kk.startswith('USD') else '')
    else: print(kk, v[:200])
