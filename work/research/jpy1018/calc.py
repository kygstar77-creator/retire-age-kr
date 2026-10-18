# 원/100엔 한국은행 매매기준율로 '100만원 → 몇 엔' 계산 (2026-10-18 firemap-write-b)
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
fx = {a: float(b) for a, b, _ in json.load(open('raw/ecos_731Y001_jpy_1018.json', encoding='utf-8'))}
ks = sorted(fx); last = ks[-1]
def at(d):
    k = max(x for x in ks if x <= d); return k, fx[k]
print('최근', last, fx[last])
oc = {k: v for k, v in fx.items() if k.startswith('202610')}
lo = min(oc.items(), key=lambda x: x[1]); print('10월 최저', lo)
prev = [k for k in ks if k < lo[0] and fx[k] <= lo[1]]; print('그 이하였던 마지막 날', prev[-1] if prev else None, fx[prev[-1]] if prev else None)
for y in ('2024', '2025'):
    yy = {k: v for k, v in fx.items() if k.startswith(y)}
    print(y, '최고', max(yy.items(), key=lambda x: x[1]), '최저', min(yy.items(), key=lambda x: x[1]), '평균', round(sum(yy.values())/len(yy), 2))
yy = {k: v for k, v in fx.items() if k.startswith('2026')}
print('2026', '최고', max(yy.items(), key=lambda x: x[1]), '최저', min(yy.items(), key=lambda x: x[1]))
W = 1_000_000
for d in ('20231016', '20241016', '20251016', '20260416', last):
    k, r = at(d); print(f'{k} 100엔={r:,.2f}원 · 100만원 → {W/r*100:,.0f}엔 · 10만엔 = {r*1000:,.0f}원')
# 10만엔 사려면
for d in ('20251016', last):
    k, r = at(d); print(f'10만엔 필요 원화 {k}: {r*1000:,.0f}원')
k0, r0 = at('20251016'); k1, r1 = at(last)
print(f'1년 전 대비 환율 {(r1/r0-1)*100:+.2f}% · 같은 100만원 엔 {(W/r1*100)-(W/r0*100):+,.0f}엔 ({(r0/r1-1)*100:+.2f}%) · 10만엔 원화 차 {(r1-r0)*1000:+,.0f}원')
# 엔 사 둔 사람: 1년 전 100만원어치 엔을 지금 원화로
yen = W / r0 * 100; print(f'1년 전 100만원으로 산 {yen:,.0f}엔 → 지금 {yen*r1/100:,.0f}원 ({yen*r1/100-W:+,.0f}원)')
k2, r2 = at('20231016'); yen2 = W / r2 * 100; print(f'3년 전 100만원 엔 {yen2:,.0f} → 지금 {yen2*r1/100:,.0f}원 ({yen2*r1/100-W:+,.0f})')
# 하나은행 10/16 마지막 고시(네이버 증권 api.stock.naver.com, raw/hana_jpy_1018.json)
h = json.load(open('raw/hana_jpy_1018.json', encoding='utf-8'))[0]
b, cb, cs = float(h['closePrice']), float(h['cashBuyValue']), float(h['cashSellValue'])
print('하나', h['localTradedAt'], '기준', b, '현찰 살 때', cb, '팔 때', cs, f'살때 가산 {(cb/b-1)*100:.2f}%')
print(f'100만원 기준 {W/b*100:,.0f}엔 · 현찰 {W/cb*100:,.0f}엔 · 차 {W/b*100-W/cb*100:,.0f}엔')
print(f'10만엔 살 때 {cb*1000:,.0f}원 팔 때 {cs*1000:,.0f}원 차 {(cb-cs)*1000:,.0f}원 ({(cb-cs)/cb*100:.2f}%)')
# 두 환율 분해: ECOS 원/달러, FRED 엔/달러(DEXJPUS)
u = {a: float(b) for a, b, _ in json.load(open('raw/ecos_usd_1018.json', encoding='cp949'))}
print('원/달러', u['20251016'], '→', u['20261016'], f'{(u["20261016"]/u["20251016"]-1)*100:+.2f}%')
print('엔/달러 2025-10-16 150.75 → 2026-10-09 158.34', f'{(158.34/150.75-1)*100:+.2f}%')
