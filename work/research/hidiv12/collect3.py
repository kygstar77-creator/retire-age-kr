# 고배당·월배당 ETF 12종. 배당률 = 최근 1년치 분배금 합계 ÷ 현재가.
# 1년치를 세는 법이 종목마다 다르다:
#   월배당 → 최근 12회 / 분기배당 → 최근 4회 / 그 해에 주기가 바뀐 종목 → 최근 365일 안의 전부
# 12개월 창으로만 자르면 분기배당이 3회만 잡혀 과소 계산된다(SCHD·NOBL, 2026-09-24 확인).
import json, sys, datetime, urllib.request, time
sys.stdout.reconfigure(encoding='utf-8')
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
# 유형: 성장=배당성장형, 고배당=고배당주, 커버드콜=옵션매도형
SYMS = [('SCHD','성장'),('VYM','고배당'),('DVY','고배당'),('SPYD','고배당'),('SPHD','고배당'),
        ('DGRO','성장'),('VIG','성장'),('NOBL','성장'),('SDY','성장'),
        ('JEPI','커버드콜'),('JEPQ','커버드콜'),('QYLD','커버드콜')]

def get(u, t=30, tries=3):
    for i in range(tries):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t))
        except Exception:
            if i == tries - 1: raise
            time.sleep(1.5 * (i + 1))

def day(ts): return datetime.datetime.fromtimestamp(int(ts), datetime.UTC).strftime('%Y-%m-%d')

out = {}
for s, kind in SYMS:
    r = get(f'https://query1.finance.yahoo.com/v8/finance/chart/{s}?range=3y&interval=1d&events=div')['chart']['result'][0]
    m = r['meta']; price = m.get('regularMarketPrice')
    ts = r['timestamp']; close = r['indicators']['quote'][0]['close']
    adj = r['indicators'].get('adjclose', [{}])[0].get('adjclose')
    divs = [(day(k), round(v['amount'], 6)) for k, v in sorted(r.get('events', {}).get('dividends', {}).items(), key=lambda kv: int(kv[0]))]
    today = datetime.date.today(); y1 = today - datetime.timedelta(days=365)
    in12 = [d for d in divs if datetime.date.fromisoformat(d[0]) > y1]
    if len(in12) >= 11:   freq, used, note = '월', divs[-12:], ''
    elif len(in12) <= 4:  freq, used, note = '분기', divs[-4:], ''
    else:                 freq, used, note = '주기변경', in12, '최근 1년 안에 분배 주기가 바뀌어 365일 안의 분배금을 전부 더했다'
    tot = round(sum(a for _, a in used), 6)
    i0 = next(i for i, t in enumerate(ts) if datetime.date.fromtimestamp(t) >= y1)
    px0, adj0, adjN = close[i0], adj[i0], adj[-1]
    out[s] = {'kind': kind, 'price': round(price, 4), 'price_date': day(ts[-1]), 'exchange': m.get('fullExchangeName'),
              'freq': freq, 'note': note, 'divs_used': used, 'sum_used': tot,
              'yield_calc_pct': round(tot / price * 100, 2),
              'last_ex': divs[-1][0], 'last_amt': divs[-1][1], 'prev_ex': divs[-2][0], 'prev_amt': divs[-2][1],
              'px_1y_ago': round(px0, 4), 'px_1y_ago_date': day(ts[i0]),
              'price_ret_1y_pct': round((price / px0 - 1) * 100, 2),
              'total_ret_1y_pct': round((adjN / adj0 - 1) * 100, 2)}
    o = out[s]
    print(f"{s:5s} {kind:5s} {freq:4s} {price:8.2f} 합{tot:7.4f}({len(used)}회) 배당률{o['yield_calc_pct']:6.2f}%  주가1년{o['price_ret_1y_pct']:+7.2f}%  총수익1년{o['total_ret_1y_pct']:+7.2f}%  최근배당락 {o['last_ex']}")
json.dump(out, open('work/research/hidiv12/raw.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('오늘', datetime.date.today())
