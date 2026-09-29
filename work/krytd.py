# -*- coding: utf-8 -*-
"""코스피 시총 상위 N곳의 기간 등락률(정규장 종가).

사용: py -3.12 work/krytd.py [N=60] [기준일=작년 마지막 거래일 YYYY-MM-DD] [--market KOSDAQ]
출처: 시총 순위 m.stock.naver.com/api/stocks/marketValue/<시장> · 종가 Yahoo chart <코드>.KS/.KQ

2026-09-29 23시 회차에서 만들었다. 네이버 API의 closePrice는 밤 20시 넥스트레이드 가격이다
(삼성전자 9/29 KRX 종가 272,500원인데 API는 275,000원 +1.85%). 그래서 순위만 네이버에서 받고
종가는 Yahoo(정규장)에서 받는다. ETF(KODEX·TIGER 등)와 이름이 '우'로 끝나는 우선주는 뺀다.
"""
import sys, json, time, datetime, urllib.request, statistics
sys.stdout.reconfigure(encoding='utf-8')
H = {'User-Agent': 'Mozilla/5.0'}
KST = datetime.timezone(datetime.timedelta(hours=9))
ETF = ('KODEX', 'TIGER', 'ACE', 'RISE', 'SOL', 'KIWOOM', 'PLUS', 'HANARO')

def get(u):
    return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=20).read())

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    mkt = sys.argv[sys.argv.index('--market') + 1] if '--market' in sys.argv else 'KOSPI'
    args = [a for a in args if a != mkt]
    n = int(args[0]) if args else 60
    today = datetime.datetime.now(KST).date()
    base_day = datetime.date.fromisoformat(args[1]) if len(args) > 1 else datetime.date(today.year - 1, 12, 31)
    sfx = '.KS' if mkt == 'KOSPI' else '.KQ'
    stocks = get(f'https://m.stock.naver.com/api/stocks/marketValue/{mkt}?page=1&pageSize={n}')['stocks']
    p1 = int(datetime.datetime.combine(base_day - datetime.timedelta(days=14), datetime.time()).timestamp())
    out = []
    for s in stocks:
        code, name = s['itemCode'], s['stockName']
        if name.startswith(ETF) or name.endswith('우'): continue
        try:
            r = get(f'https://query1.finance.yahoo.com/v8/finance/chart/{code}{sfx}?period1={p1}&period2={int(time.time())}&interval=1d')['chart']['result'][0]
            pts = [(datetime.datetime.fromtimestamp(t, KST).date(), v)
                   for t, v in zip(r['timestamp'], r['indicators']['quote'][0]['close']) if v]
            b = [p for p in pts if p[0] <= base_day][-1]; last = pts[-1]
            out.append(dict(name=name, code=code, cap_eok=s['marketValue'], base_date=str(b[0]), base=b[1],
                            last_date=str(last[0]), last=last[1], chg=round((last[1] / b[1] - 1) * 100, 1)))
        except Exception as e:
            print('# 실패', name, type(e).__name__, file=sys.stderr)
        time.sleep(0.25)
    out.sort(key=lambda o: o['chg'])
    print(f'# {mkt} 시총 상위 {n} → 종목 {len(out)}곳 · 하락 {sum(o["chg"] < 0 for o in out)}곳 · 중앙값 {statistics.median(o["chg"] for o in out)}%')
    for o in out: print(json.dumps(o, ensure_ascii=False))

if __name__ == '__main__':
    main()
