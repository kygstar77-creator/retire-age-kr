# 두 번째 출처 — Alpha Vantage DIVIDENDS(키는 work/apis.py). raw/av_div_<티커>.json, 11/4 기준 12개월 합을 야후와 대조
import sys, json, time, urllib.request, datetime, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2])); import apis
k = apis.key('alphavantage'); END = datetime.date(2026, 11, 4)
def ttm(rows, end):
    st = end.replace(year=end.year - 1)
    return sum(float(r['amount']) for r in rows if st < datetime.date.fromisoformat(r['ex_dividend_date']) <= end)
for t in sys.argv[1:]:
    b = urllib.request.urlopen(f'https://www.alphavantage.co/query?function=DIVIDENDS&symbol={t}&apikey={k}', timeout=40).read()
    open(f'raw/av_div_{t}.json', 'wb').write(b); d = json.loads(b); rows = d.get('data') or []
    if not rows: print(t, 'ERR', str(d)[:150]); continue
    a, p = ttm(rows, END), ttm(rows, END.replace(year=2025))
    print(f'{t} AV 12개월 {a:.4f} · 1년 전 {p:.4f} · {(a/p-1)*100:+.1f}% · 마지막 {rows[0]["ex_dividend_date"]} {rows[0]["amount"]}')
    time.sleep(13)
