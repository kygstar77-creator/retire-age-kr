# sdi1015b 10/15 종가로 다시 계산(10/15 write 15시 회차) — 주가는 야후(KRX 정규장 종가). 네이버 fchart는 넥스트레이드 애프터마켓 포함이라
# 10/13 565,000·10/14 596,000처럼 KRX 종가(560,000·591,000, 연합 +5.54%)와 갈린다. 코스피 지수는 네이버(지수엔 NXT 없음).
import json, sys, datetime, urllib.request
sys.stdout.reconfigure(encoding='utf-8')
UA = {'User-Agent': 'Mozilla/5.0'}
def yh(sym, rng='10y'):
    r = json.load(urllib.request.urlopen(urllib.request.Request(f'https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range={rng}&interval=1d', headers=UA), timeout=30))['chart']['result'][0]
    d = {datetime.datetime.fromtimestamp(t).strftime('%Y%m%d'): c for t, c in zip(r['timestamp'], r['indicators']['quote'][0]['close']) if c}
    return d, r['meta']
now = sys.argv[1] if len(sys.argv) > 1 else '20261015'
sdi, m = yh('006400.KS')
print('야후 meta', m['regularMarketPrice'], datetime.datetime.fromtimestamp(m['regularMarketTime']))
kos = {x['localDate']: x['closePrice'] for x in json.load(urllib.request.urlopen(urllib.request.Request(
    'https://api.stock.naver.com/chart/domestic/index/KOSPI/day?startDateTime=202510010000&endDateTime=202610170000', headers=UA)))}
lg, _ = yh('373220.KS', '1y')
c = sdi[now]
prev = sorted(k for k in sdi if k < now)[-1]
y1 = str(int(now[:4]) - 1) + now[4:]
print('SDI', now, '종가', c, '| 전날', prev, sdi[prev], '%.2f%%' % ((c / sdi[prev] - 1) * 100))
print('SDI 1년 전', y1, sdi.get(y1), '배수 %.3f' % (c / sdi[y1]))
for lab, start in (('1년', y1), ('5년(수정)', str(int(now[:4]) - 5) + now[4:])):
    w = {k: v for k, v in sdi.items() if start <= k <= now}
    hk = max(w, key=w.get); lk = min(w, key=w.get)
    print(lab, '최고', hk, w[hk], '최저', lk, w[lk], '| 고점 대비 %.1f%%' % ((c / w[hk] - 1) * 100), '| 최저 대비 %.2f배' % (c / w[lk]), '| 위치 %.1f%%' % ((c - w[lk]) / (w[hk] - w[lk]) * 100))
print('SDI 10/2→', now, sdi['20261002'], c, '%.2f%%' % ((c / sdi['20261002'] - 1) * 100), '| 10/14→ %.2f%%' % ((c / sdi['20261014'] - 1) * 100))
ks = sorted(k for k in kos if '20261002' <= k <= now)
print('KOSPI 10/2→', now, kos['20261002'], kos[now], '%.2f%%' % ((kos[now] / kos['20261002'] - 1) * 100), '연속 하락 거래일', len(ks) - 1,
      '하루', '%.2f%%' % ((kos[now] / kos[ks[-2]] - 1) * 100))
w = {k: v for k, v in kos.items() if y1 <= k <= now}; hk = max(w, key=w.get)
print('KOSPI 1년 전', kos.get(y1), '→', kos[now], '%.1f%%' % ((kos[now] / kos[y1] - 1) * 100), '| 1년 최고', hk, w[hk], '고점 대비 %.1f%%' % ((kos[now] / w[hk] - 1) * 100))
print('LG엔솔 10/2→', now, lg.get('20261002'), lg.get(now), '%.2f%%' % ((lg[now] / lg['20261002'] - 1) * 100))
print('배당 1,000원 / 종가 = %.3f%%' % (1000 / c * 100))
