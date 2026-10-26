# fxdepfee1026 자료 받기 (firemap-write 2026-10-26) — ECOS 원/달러, 하나은행 USD 고시(네이버 증권), KB 외화예금 금리 페이지
import sys, os, json, datetime, urllib.request
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'); sys.stdout.reconfigure(encoding='utf-8')
import apis
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(D, 'raw')
T = datetime.date.today().strftime('%Y%m%d')
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read().decode('utf-8', 'ignore')
out = {'fetched': datetime.datetime.now().isoformat(timespec='minutes')}
ek = apis.key('ecos')
d = apis._j(f'https://ecos.bok.or.kr/api/StatisticSearch/{ek}/json/kr/1/2000/731Y001/D/20240101/{T}/0000001')
out['USD'] = [(r['TIME'], float(r['DATA_VALUE'])) for r in d['StatisticSearch']['row']]
h = json.loads(get('https://m.stock.naver.com/front-api/marketIndex/prices?category=exchange&reutersCode=FX_USDKRW&page=1&pageSize=10'))
out['hana'] = h
open(os.path.join(R, f'collect_{T}.json'), 'w', encoding='utf-8').write(json.dumps(out, ensure_ascii=False, indent=1))
print(out['USD'][-5:])
print(json.dumps(h, ensure_ascii=False)[:1500])
