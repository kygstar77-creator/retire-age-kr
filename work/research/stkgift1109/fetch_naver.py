# 네이버 금융 일별 시세(siseJson, 거래소 종가)를 raw/px_<코드>.json 으로 — 야후는 11/6·11/9 종가가 달라(188,700·189,900 vs 193,500·187,400) 바꿈
import json, sys, urllib.request, datetime as dt, ast
for code, name in (('005930', '005930.KS'), ('069500', '069500.KS'), ('KOSPI', '^KS11')):
    u = f'https://api.finance.naver.com/siseJson.naver?symbol={code}&requestType=1&startTime=20250101&endTime=20261109&timeframe=day'
    t = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=60).read().decode('utf-8', 'ignore')
    rows = ast.literal_eval(t.strip().replace('\n', ''))[1:]
    out = [[f'{r[0][:4]}-{r[0][4:6]}-{r[0][6:]}', float(r[4])] for r in rows]
    json.dump({'ticker': code, 'got': dt.datetime.now().strftime('%Y-%m-%d %H:%M'), 'src': u, 'rows': out}, open(f'raw/px_{name}.json', 'w'), ensure_ascii=False)
    print(code, len(out), out[0], out[-1])
