"""미국 금요일 종가가 들어온 뒤(한국 10/10 06시 이후) SPY 일별 종가를 다시 받는다 → raw/yh_SPY.json. 그다음 calc.py."""
import urllib.request, json, os
H = os.path.dirname(os.path.abspath(__file__))
u = 'https://query1.finance.yahoo.com/v8/finance/chart/SPY?range=1mo&interval=1d'
j = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=30))
json.dump(j, open(os.path.join(H, 'raw', 'yh_SPY.json'), 'w')); print('ok')
