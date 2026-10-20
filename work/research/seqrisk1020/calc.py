# -*- coding: utf-8 -*-
"""seqrisk1020 — C-2 쇼츠(c2s_jungwoo) 짝 글: '왜 14년 만에 바닥났나'(수익률 순서).
원자료는 2026-10-20 새로 받은 raw/(야후 ^SP500TR 일별·ECOS 731Y004 연말·731Y001 일별).
매도 규칙·세금은 C-2와 같다(C-1 calc.sell_for: 해마다 1월 초 1년 치 한 번에, 양도세 22%·공제 250만원)."""
import sys, io, json, contextlib, pathlib, datetime as dt, math
HERE = pathlib.Path(__file__).resolve().parent
RAW = HERE / 'raw'
sys.path.insert(0, str(HERE.parent / 'longform' / 'ep' / 'C-1'))
with contextlib.redirect_stdout(io.StringIO()):
    import calc as C
r = json.load(open(RAW / 'yahoo_SP500TR_1d_1020.json'))['chart']['result'][0]
ye, last = {}, None
for t, v in zip(r['timestamp'], r['indicators']['quote'][0]['close']):
    if v is None: continue
    d = dt.datetime.fromtimestamp(t, dt.UTC).date(); ye[d.year] = v; last = (d, v)
fx = {int(x['TIME']): float(x['DATA_VALUE']) for x in json.load(open(RAW / 'ecos_731Y004_A_1988_2025_1020.json', encoding='utf-8'))['StatisticSearch']['row'] if x['ITEM_NAME2'] == '말일자료'}
fxd = {x['TIME']: float(x['DATA_VALUE']) for x in json.load(open(RAW / 'ecos_731Y001_D_1020.json', encoding='utf-8'))['StatisticSearch']['row']}
YEARS = list(range(1989, 2026))
R = {y: (ye[y] / ye[y - 1]) * fx[y] / fx[y - 1] - 1 for y in YEARS}
assert all(abs(R[y] - C.R_KRW[y]) < 1e-9 for y in YEARS), 'C-2 자료와 다름'
P0, NET = 300_000_000, 24_000_000
def run(rets, p0=P0, net=NET):
    v, basis, taken = p0, p0, 0
    for i, g in enumerate(rets):
        s, tax, used = C.sell_for(net, v, basis)
        if s > v: return ('바닥', i + 1, v, taken)
        basis -= used; v = (v - s) * (1 + g); taken += 1
    return ('남음', len(rets), v, taken)
out = []; w = out.append
w('# seqrisk1020 calc_out — 3억원 · 매달 200만원(해마다 1월 1년 치 2,400만원) · S&P500 총수익 원화 · 물가 반영 안 함')
seq = [R[y] for y in range(1998, 2026)]
a = run(seq); w(f'A 1998 시작 그대로: {a[0]} {1998 + a[1] - 1}년 1월({a[1]}년차) · 다 꺼낸 해 {a[3]}번 · 남은 돈 {a[2]/1e4:,.0f}만원')
b = run(seq[::-1]); w(f'B 같은 28개 수익률 순서만 거꾸로(첫해 2025 수익률 … 마지막 1998): {b[0]} · {b[1]}해 · 끝 {b[2]/1e8:.2f}억원 · 다 꺼낸 해 {b[3]}번')
g28 = math.prod(1 + x for x in seq); w(f'C 안 꺼냈다면 3억 → 2025년 말 {P0*g28/1e8:.2f}억원 ({g28:.2f}배) · 연평균 {(g28**(1/28)-1)*100:.2f}%')
w(f'C2 거꾸로 해도 곱은 같음 {math.prod(1+x for x in seq[::-1]):.4f}')
def gm(ys): return (math.prod(1 + R[y] for y in ys)) ** (1 / len(ys)) - 1
w(f'D 첫 5년 연평균: 1998~2002 {gm(range(1998,2003))*100:+.2f}% · 2003~2007 {gm(range(2003,2008))*100:+.2f}% · 1997~2001 {gm(range(1997,2002))*100:+.2f}%')
w(f'D2 첫 3년 누적: 1998~2000 ' + f'{(math.prod(1+R[y] for y in range(1998,2001))-1)*100:+.1f}%' + f' · 2000~2002 {(math.prod(1+R[y] for y in range(2000,2003))-1)*100:+.1f}%')
w('D3 해마다 원화 수익률 1998~2012: ' + ' · '.join(f'{y} {R[y]*100:+.1f}%' for y in range(1998, 2013)))
# 37명: 시작 해별 결과 + 첫 5년 연평균
w('\nE 시작 해(1989~2025)별 · 첫 5년 연평균(5년 안 되면 있는 만큼) · 결과')
rows = []
for s in YEARS:
    res = run([R[y] for y in range(s, 2026)])
    f5 = [y for y in range(s, min(s + 5, 2026))]
    rows.append((s, gm(f5), res))
    w(f'  {s}: 첫5년 {gm(f5)*100:+.1f}% · {res[0]} ' + (f'{s+res[1]-1}년' if res[0]=='바닥' else f'{res[2]/1e8:.2f}억'))
bad = [x for x in rows if x[2][0] == '바닥']; known = [x for x in rows if x[0] <= 2012]
w(f'E2 바닥 {len(bad)}명: ' + ', '.join(f'{x[0]}(첫5년 {x[1]*100:+.1f}%)' for x in bad))
ok = [x for x in known if x[2][0] != '바닥']
w(f'E3 1989~2012 시작 24명 중 안 바닥 {len(ok)}명 첫5년 연평균의 가장 낮은 값 {min(x[1] for x in ok)*100:+.1f}% ({min(ok,key=lambda x:x[1])[0]})')
w(f'E4 바닥 6명 첫5년 연평균 가장 높은 값 {max(x[1] for x in bad)*100:+.1f}% ({max(bad,key=lambda x:x[1])[0]})')
neg = [x for x in known if x[1] < 0]; w(f'E5 첫5년 연평균이 마이너스인 시작 해: ' + ', '.join(f'{x[0]}({x[2][0]})' for x in neg))
# 2026년 올해
d0 = dt.date(2025, 12, 31); fx_last = fxd.get(last[0].strftime('%Y%m%d'))
ytd_usd = last[1] / ye[2025] - 1
w(f'\nF 2026년 올해: ^SP500TR {ye[2025]:.2f}(2025 말) → {last[1]:.2f}({last[0]}) 달러 {ytd_usd*100:+.1f}% · 환율 {fx[2025]} → {fx_last}({last[0]}) · 원화 {((1+ytd_usd)*fx_last/fx[2025]-1)*100:+.1f}%')
(HERE / 'calc_out.txt').write_text('\n'.join(out) + '\n', encoding='utf-8')
print('\n'.join(out))
