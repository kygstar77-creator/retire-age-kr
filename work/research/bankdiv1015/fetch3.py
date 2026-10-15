# 다음 금융 KRX 정규장 종가 대조(네이버 basic은 넥스트레이드 애프터마켓 값)
import json, urllib.request
T = {'KB금융': '105560', '신한지주': '055550', '하나금융지주': '086790', '우리금융지주': '316140', 'BNK금융지주': '138930'}
H = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.daum.net/'}
o = {}
for n, c in T.items():
    j = json.loads(urllib.request.urlopen(urllib.request.Request(f'https://finance.daum.net/api/quotes/A{c}?summary=false', headers=H), timeout=25).read())
    o[n] = {k: j.get(k) for k in ('tradePrice', 'prevClosingPrice', 'changeRate', 'tradeTime', 'tradeDate', 'high52wPrice', 'low52wPrice')}
    print(n, o[n])
json.dump(o, open('src/daum.json', 'w', encoding='utf-8'), ensure_ascii=False)
