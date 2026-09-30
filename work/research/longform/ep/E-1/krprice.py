"""한국 두 종목 1년 종가 — 금융위원회 주식시세정보(data.go.kr GetStockSecuritiesInfoService) → raw/krx_<코드>.json, 야후(raw/*.KS_5y.json)와 대조 (2026-09-30)."""
import json, os, sys, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
key = [l.split('=', 1)[1].strip() for l in open(os.path.expanduser('~/Documents/datago_key.txt'), encoding='utf-8-sig') if l.startswith('KEY=')][0]
out = {}
for code in ('000660', '005930'):
    p = os.path.join(H, 'raw', f'krx_{code}.json')
    if not os.path.exists(p):
        q = urllib.parse.urlencode({'resultType': 'json', 'likeSrtnCd': code, 'beginBasDt': '20250901', 'numOfRows': 400, 'pageNo': 1})
        u = f'https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey={urllib.parse.quote(key, safe="")}&{q}'
        j = json.load(urllib.request.urlopen(u, timeout=60)); json.dump(j, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
    j = json.load(open(p, encoding='utf-8'))
    it = [x for x in j['response']['body']['items']['item'] if x['srtnCd'] == code]
    s = sorted((x['basDt'], int(x['clpr'])) for x in it)
    out[code] = s
    print(code, it[0]['itmsNm'], len(s), s[0], s[-1])
json.dump(out, open(os.path.join(H, 'krx_close.json'), 'w'), ensure_ascii=False)
