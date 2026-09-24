# 고배당·월배당 ETF 12종 — 주기를 먼저 판별하고(월/분기) 최근 12회·4회 분배금 합계로 배당률을 낸다.
# 12개월 창으로만 자르면 분기배당이 3회만 잡혀 배당률이 과소 계산된다(2026-09-24 확인).
import json, sys, datetime, urllib.request, time
sys.stdout.reconfigure(encoding='utf-8')
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
SYMS = ['SCHD', 'VYM', 'HDV', 'DVY', 'SPYD', 'DGRO', 'VIG', 'NOBL', 'SDY', 'JEPI', 'JEPQ', 'QYLD']

def get(u, t=30, tries=3):
    for i in range(tries):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t))
        except Exception:
            if i == tries - 1: raise
            time.sleep(1.5 * (i + 1))

def day(ts): return datetime.datetime.fromtimestamp(int(ts), datetime.UTC).strftime('%Y-%m-%d')

out = {}
for s in SYMS:
    r = get(f'https://query1.finance.yahoo.com/v8/finance/chart/{s}?range=3y&interval=1d&events=div')['chart']['result'][0]
    m = r['meta']; price = m.get('regularMarketPrice')
    ts = r['timestamp']; close = r['indicators']['quote'][0]['close']
    adj = r['indicators'].get('adjclose', [{}])[0].get('adjclose')
    divs = [(day(k), round(v['amount'], 6)) for k, v in sorted(r.get('events', {}).get('dividends', {}).items(), key=lambda kv: int(kv[0]))]
    today = datetime.date.today(); y1 = today - datetime.timedelta(days=365)
    in12 = [d for d in divs if datetime.date.fromisoformat(d[0]) > y1]
    n = 12 if len(in12) >= 10 else 4          # 월배당이면 12회, 분기면 4회
    freq = '월' if n == 12 else '분기'
    recent = divs[-n:]
    tot = round(sum(a for _, a in recent), 6)
    i0 = next((i for i, t in enumerate(ts) if datetime.date.fromtimestamp(t) >= y1), None)
    px0 = close[i0]; adj0 = adj[i0]; adjN = adj[-1]
    out[s] = {
        'price': round(price, 4), 'price_date': day(ts[-1]), 'exchange': m.get('fullExchangeName'),
        'freq': freq, 'n_used': n, 'recent_divs': recent, 'sum_recent': tot,
        'yield_calc_pct': round(tot / price * 100, 2),
        'in12_count': len(in12), 'sum_in12': round(sum(a for _, a in in12), 6),
        'last_ex': divs[-1][0], 'last_amt': divs[-1][1],
        'px_1y_ago': round(px0, 4), 'px_1y_ago_date': day(ts[i0]),
        'price_ret_1y_pct': round((price / px0 - 1) * 100, 2),
        'total_ret_1y_pct': round((adjN / adj0 - 1) * 100, 2),
    }
    o = out[s]
    print(f"{s:5s} {freq:2s} {price:8.2f} 최근{n}회합 {tot:7.4f} → 배당률 {o['yield_calc_pct']:5.2f}% | 12개월창 {o['in12_count']}회 {o['sum_in12']:.4f} | 주가1년 {o['price_ret_1y_pct']:+6.2f}% 총수익 {o['total_ret_1y_pct']:+6.2f}% | 최근배당락 {o['last_ex']} {o['last_amt']}")
json.dump(out, open('work/research/hidiv12/raw.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('저장 raw.json  · 오늘', datetime.date.today())
