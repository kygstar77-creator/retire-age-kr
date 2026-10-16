# X-1 자료 다시 받기 (2026-10-16 밤, 자료조사 담당) — 공개일(10/22)에 가까운 최신 값으로 다시 확인.
#   py -3.12 work/research/longform/ep/X-1/collect_1016.py
# 받는 것: 한국은행 ECOS 731Y001 원/달러(0000001)·원/100엔(0000002) 일별 2024-01-01~오늘,
#          야후 SPY·QQQ 종가, 네이버 증권 하나은행 USD 고시(현찰 살 때·팔 때·송금), 국내 상장 S&P500 ETF 환노출·환헤지 종가.
import sys, os, json, datetime, urllib.request, urllib.parse
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'); sys.stdout.reconfigure(encoding='utf-8')
import apis
D = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(D, 'raw')
today = datetime.date.today(); T = today.strftime('%Y%m%d')
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30).read().decode('utf-8', 'ignore')
out = {'fetched': datetime.datetime.now().isoformat(timespec='minutes')}
ek = apis.key('ecos')
for name, item in (('USD', '0000001'), ('JPY100', '0000002')):
    d = apis._j(f'https://ecos.bok.or.kr/api/StatisticSearch/{ek}/json/kr/1/2000/731Y001/D/20240101/{T}/{item}')
    out[name] = [(r['TIME'], float(r['DATA_VALUE'])) for r in d['StatisticSearch']['row']]
p1 = int(datetime.datetime(2024, 1, 1).timestamp()); p2 = int(datetime.datetime.now().timestamp())
for s in ('SPY', 'QQQ'):
    j = json.loads(get(f'https://query1.finance.yahoo.com/v8/finance/chart/{s}?period1={p1}&period2={p2}&interval=1d'))['chart']['result'][0]
    ts = j['timestamp']; c = j['indicators']['quote'][0]['close']
    # 미국 장 날짜(뉴욕 시간) — 타임스탬프는 개장 시각(UTC 13:30~14:30)이라 UTC 날짜 = 뉴욕 날짜
    out[s] = [(datetime.datetime.utcfromtimestamp(t).strftime('%Y-%m-%d'), v) for t, v in zip(ts, c) if v is not None]
# 하나은행 고시(네이버 증권 marketIndex) — 최근 회차들
h = json.loads(get('https://m.stock.naver.com/front-api/marketIndex/prices?category=exchange&reutersCode=FX_USDKRW&page=1&pageSize=10'))
out['HANA_USD'] = h.get('result', h)
# 국내 상장 S&P500 ETF(네이버 차트 siseJson) — 코드는 argv로 덧붙일 수 있음
codes = sys.argv[1:] or []
for code in codes:
    t = get(f'https://api.finance.naver.com/siseJson.naver?symbol={code}&requestType=1&startTime=20240101&endTime={T}&timeframe=day')
    rows = [x for x in eval(t.strip().replace('\n', '')) [1:]]
    out['KR_' + code] = [(str(r[0]), r[4]) for r in rows]
fn = os.path.join(R, f'collect_{today.strftime("%Y%m%d")}.json')
json.dump(out, open(fn, 'w', encoding='utf-8'), ensure_ascii=False)
for k, v in out.items():
    if isinstance(v, list) and v and isinstance(v[0], (list, tuple)): print(k, len(v), v[0], v[-3:])
    else: print(k, str(v)[:600])
print('저장', fn)
