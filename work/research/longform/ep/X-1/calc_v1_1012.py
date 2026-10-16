# X-1 환율 편 계산 — 원문: raw/ecos_731Y001_20261013.json(한국은행 ECOS 731Y001 매매기준율, 일), raw/yahoo_spy_qqq_20261013.json(야후 종가)
# 날짜 규칙: 같은 달력 날짜에 미국 종가와 한국 고시가 둘 다 있는 날만 쓴다. 시작일이 빠지면 그 앞의 가장 가까운 날.
# 끝날 = 둘 다 있는 마지막 날. 환전 수수료·스프레드·세금·배당은 넣지 않는다(매매기준율 그대로 — 실제 환전보다 유리한 값).
import json, os
D = os.path.dirname(os.path.abspath(__file__))
fx = json.load(open(os.path.join(D, 'raw/ecos_731Y001_20261013.json'), encoding='utf-8'))
y = json.load(open(os.path.join(D, 'raw/yahoo_spy_qqq_20261013.json')))
usd = {k[:4]+'-'+k[4:6]+'-'+k[6:]: v for k, v in fx['USD']}
jpy = {k[:4]+'-'+k[4:6]+'-'+k[6:]: v for k, v in fx['JPY100']}
spy = dict(y['SPY']); qqq = dict(y['QQQ'])
both = sorted(set(usd) & set(spy))
def on(d):
    c = [x for x in both if x <= d]; return c[-1]
END = both[-1]
STARTS = [('1년 전', '2025-10-13'), ('올해 첫날', '2026-01-02'), ('환율 최고점', '2026-07-02'), ('석 달 전', '2026-07-13')]
out = [f'끝날 {END}: 원/달러 {usd[END]:,} · 원/100엔 {jpy[END]} · SPY {spy[END]:.2f} · QQQ {qqq[END]:.2f}', '']
out.append('## 1. 1억원을 그날 달러로 바꿔 두었다면(매매기준율, 수수료 없음) → 끝날 원화')
for name, s in STARTS:
    d = on(s); dollars = 1e8 / usd[d]; now = dollars * usd[END]
    out.append(f'{name} {d}: 환율 {usd[d]:,} → 달러 {dollars:,.0f} → {now:,.0f}원 ({now-1e8:+,.0f}원, {(now/1e8-1)*100:+.2f}%)')
out.append('')
out.append('## 2. 1억원으로 그날 SPY·QQQ를 샀다면 — 달러 수익률 / 원화 수익률 / 환율 몫')
for name, s in STARTS:
    d = on(s)
    fxr = usd[END] / usd[d] - 1
    for sym, px in (('SPY', spy), ('QQQ', qqq)):
        r = px[END] / px[d] - 1; rk = (1 + r) * (1 + fxr) - 1
        out.append(f'{name} {d} {sym}: 달러 {r*100:+.2f}% · 환율 {fxr*100:+.2f}% · 원화 {rk*100:+.2f}% → 1억 → {1e8*(1+rk):,.0f}원 ({1e8*rk:+,.0f}원)')
out.append('')
out.append('## 3. 해외 결제 1,000달러·10만엔이 원화로 얼마(매매기준율, 카드 수수료 없음)')
for name, s in STARTS:
    d = on(s)
    out.append(f'{name} {d}: 1,000달러 {usd[d]*1000:,.0f}원 · 10만엔 {jpy[d]*1000:,.0f}원')
out.append(f'끝날 {END}: 1,000달러 {usd[END]*1000:,.0f}원 · 10만엔 {jpy[END]*1000:,.0f}원')
out.append('')
hi = max(usd.items(), key=lambda x: x[1]); lo26 = min((k, v) for k, v in usd.items() if k >= '2026-01-01')
out.append(f'## 4. 범위: 2024~ 원/달러 최고 {hi[0]} {hi[1]:,} · 2026년 최저 {min(((v,k) for k,v in usd.items() if k>="2026-01-01"))} · 원/100엔 2024~ 최저 {min(((v,k) for k,v in jpy.items()))}')
open(os.path.join(D, 'calc_out.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
