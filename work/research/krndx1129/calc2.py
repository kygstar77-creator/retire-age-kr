# 수정종가(분배 재투자) 기준 올해·고점 대비 · 환율은 ECOS 매매기준율(fx_ecos.json)
import json, datetime
def load(n):
    r = json.load(open(f'raw/{n}_1d.json', encoding='utf-8'))['chart']['result'][0]; tz = r['meta'].get('gmtoffset', 0)
    ts = [datetime.datetime.utcfromtimestamp(x + tz).date().isoformat() for x in r['timestamp']]
    adj = r['indicators'].get('adjclose', [{}])[0].get('adjclose') or r['indicators']['quote'][0]['close']
    return {d: a for d, a in zip(ts, adj) if a}
q, t, k = load('QQQ'), load('133690.KS'), load('379810.KS')
def at(s, d): return s[[x for x in sorted(s) if x <= d][-1]], [x for x in sorted(s) if x <= d][-1]
last = '2026-11-27'
for n, s in (('QQQ', q), ('TIGER 미국나스닥100 133690', t), ('KODEX 미국나스닥100 379810', k)):
    a, ad = at(s, '2025-12-31'); b, bd = at(s, last)
    pk = max((x for x in s if x >= '2026-01-01'), key=lambda d: s[d])
    print(f'{n}: 올해 {ad}→{bd} {(b/a-1)*100:+.1f}% · 올해 고점 {pk} 대비 {(b/s[pk]-1)*100:.1f}%')
# 1억 넣었다면 (12/31 기준가, 세금·수수료 전)
for n, s in (('QQQ(달러로 바꿔 직접)', None), ('TIGER', t)):
    pass
fx0, fx1 = 1434.9, 1342.7   # ECOS 2025-12-31, 2026-11-27
a, _ = at(q, '2025-12-31'); b, _ = at(q, last)
print('QQQ 원화 환산 올해', f'{(b*fx1/(a*fx0)-1)*100:+.1f}%', '환율', f'{(fx1/fx0-1)*100:+.1f}%')
print('1억 → QQQ 원화', round(1e8*b*fx1/(a*fx0)/1e4), '만원 · TIGER', round(1e8*at(t,last)[0]/at(t,'2025-12-31')[0]/1e4), '만원')
# 날짜 맞춤: 한국 d의 국내 ETF ↔ d 전 마지막 미국 거래일 QQQ × 한국 d 매매기준율
fx = json.load(open('raw/fx_ecos.json'))
def us_before(d): return [x for x in sorted(q) if x < d][-1]
for d0, d1 in (('2025-12-30', '2026-11-27'), ('2026-07-01', '2026-11-27')):
    u0, u1 = us_before(d0), us_before(d1)
    qk = (q[u1]*fx[d1])/(q[u0]*fx[d0]) - 1
    print(f'맞춤 {d0}→{d1}: QQQ({u0}→{u1})×환율({fx[d0]}→{fx[d1]}) {qk*100:+.1f}% · TIGER {(t[d1]/t[d0]-1)*100:+.1f}% · 환율 {(fx[d1]/fx[d0]-1)*100:+.1f}% · QQQ 달러 {(q[u1]/q[u0]-1)*100:+.1f}%')
