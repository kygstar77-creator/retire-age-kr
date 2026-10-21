# X-1 짝 글 — 영상(끝날 10/15) 숫자를 10/21 값으로 다시 계산. 시작일 값은 X-1 raw/collect_20261021.json, 끝날 값은 오늘 새로 받음(raw/now_1022.json)
import json, sys, urllib.request, datetime
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import apis
X = r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work\research\longform\ep\X-1\raw\collect_20261021.json'
c = json.load(open(X, encoding='utf-8'))
usd = dict(c['USD']); spy = dict(c['SPY']); qqq = dict(c['QQQ'])
now = {'fetched': datetime.datetime.now().isoformat(timespec='minutes')}
now['ecos'] = apis.ecos('731Y001', 'D', start='20261015', end='20261022', item='0000001', n=10)
def yh(t):
    u = f'https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=1mo&interval=1d'
    d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})))['chart']['result'][0]
    return [(datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d'), round(cl, 2)) for ts, cl in zip(d['timestamp'], d['indicators']['quote'][0]['close']) if cl]
now['SPY'] = yh('SPY'); now['QQQ'] = yh('QQQ')
def krx(code):
    u = f'https://api.finance.naver.com/siseJson.naver?symbol={code}&requestType=1&startTime=20261015&endTime=20261022&timeframe=day'
    t = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})).read().decode('utf-8', 'ignore')
    return [l.strip() for l in t.splitlines() if l.strip().startswith('["2026')]
now['379800'] = krx('379800'); now['449180'] = krx('449180')
json.dump(now, open('raw/now_1022.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
E = '20261021'; e_usd = float(dict(now['ecos'] and [(a, b) for a, b, _ in now['ecos']])[E])
e_spy = dict(now['SPY'])['2026-10-21']; e_qqq = dict(now['QQQ'])['2026-10-21']
print(f'끝날 2026-10-21: 원/달러 {e_usd} · SPY {e_spy} · QQQ {e_qqq}')
days = [('1년 전', '20251013'), ('올해 첫날', '20260102'), ('가장 비싸던 날', '20260702'), ('석 달 전', '20260713'), ('2024년 첫날', '20240102')]
for nm, d in days:
    r0 = usd[d]; dd = f'{d[:4]}-{d[4:6]}-{d[6:]}'
    s0 = spy[dd]; q0 = qqq[dd]
    cash = 1e8 / r0 * e_usd
    sd = e_spy / s0; qd = e_qqq / q0
    sw = 1e8 / r0 / s0 * e_spy * e_usd; qw = 1e8 / r0 / q0 * e_qqq * e_usd
    be = r0 / sd
    print(f'{nm} {d}: 환율 {r0} → 달러만 {cash:,.0f}원 ({cash/1e8-1:+.2%}) · SPY 달러 {sd-1:+.2%} 원화 {sw/1e8-1:+.2%} → {sw:,.0f}원 · QQQ 달러 {qd-1:+.2%} 원화 {qw/1e8-1:+.2%} · 본전 환율 {be:,.1f}원 (지금보다 {be-e_usd:+.1f})')
print('KRX', now['379800'][-2:], now['449180'][-2:])
# 국내 상장 두 상품 10/21 KRX 종가로 다시(분배금은 X-1 calc_out §7 그대로 — 8/1~10/21 새 분배 없음, 다음 기준일 10/31)
for nm, a0, ad, h0, hd in [('1년 전', 21173, 479, 14992, 160), ('올해 첫날', 22262, 369, 15483, 122), ('가장 비싸던 날', 26179, 132, 16714, 40), ('석 달 전', 25542, 132, 16859, 40), ('2024년 첫날', 13638, 639, 11048, 406)]:
    a = (23110 + ad) / a0 * 1e8; h = (17270 + hd) / h0 * 1e8
    print(f'KRX 10/21 {nm}: 환노출 {a:,.0f}원 · H {h:,.0f}원 · 차(H−노출) {h-a:+,.0f}원')
