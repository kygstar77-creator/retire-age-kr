"""W-1 10/11편 원문 받기 — DART 공시 원문(삼성전자 잠정실적·배당결정)·금융위 주식시세(data.go.kr) → raw/ (2026-10-09)"""
import json, os, sys, io, zipfile, re, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(H, 'raw'); os.makedirs(RAW, exist_ok=True)
sys.path.insert(0, os.path.join(H, *['..'] * 5)); import apis
dk = apis.key('dart')
def doc(rcp):
    p = os.path.join(RAW, f'dart_{rcp}.txt')
    if not os.path.exists(p):
        b = urllib.request.urlopen(f'https://opendart.fss.or.kr/api/document.xml?crtfc_key={dk}&rcept_no={rcp}', timeout=60).read()
        z = zipfile.ZipFile(io.BytesIO(b)); x = ''.join(z.read(n).decode('utf-8', 'ignore') for n in z.namelist())
        t = re.sub(r'<[^>]+>', ' ', x); t = re.sub(r'[ \t\r]+', ' ', t); t = re.sub(r'\n\s*\n+', '\n', t)
        open(p, 'w', encoding='utf-8').write(t)
    return open(p, encoding='utf-8').read()
dkey = [l.split('=', 1)[1].strip() for l in open(os.path.expanduser('~/Documents/datago_key.txt'), encoding='utf-8-sig') if l.startswith('KEY=')][0]
def price(code, bgn='20260901'):
    p = os.path.join(RAW, f'krx_{code}.json')
    if not os.path.exists(p):
        q = urllib.parse.urlencode({'resultType': 'json', 'likeSrtnCd': code, 'beginBasDt': bgn, 'numOfRows': 100, 'pageNo': 1})
        u = f'https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey={urllib.parse.quote(dkey, safe="")}&{q}'
        json.dump(json.load(urllib.request.urlopen(u, timeout=60)), open(p, 'w', encoding='utf-8'), ensure_ascii=False)
    j = json.load(open(p, encoding='utf-8'))
    return sorted((x['basDt'], int(x['clpr']), x['itmsNm']) for x in j['response']['body']['items']['item'] if x['srtnCd'] == code)
if __name__ == '__main__':
    for a in sys.argv[1:]:
        if a.startswith('doc:'): print(doc(a[4:])[:6000])
        elif a.startswith('px:'): print(price(a[3:])[-12:])
        elif a.startswith('list:'):
            _, cc, b, e = a.split(':')
            for x in apis.dart_list(b, e, 100, corp_code=cc): print(x)
