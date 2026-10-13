# rateloan1014 계산 — finlife_mortgage.json(금감원 금융상품통합비교공시 2026.09 공시)·ecos.json만
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
r = json.load(open('finlife_mortgage.json', encoding='utf-8'))
rows = [x for x in r if x['담보'] == '아파트' and x['상환방식'] == '분할상환방식' and x['대출최저']]
def bank(n): return n.replace('주식회사 ', '').replace('주식회사', '')
best = {}
for x in rows:
    b = bank(x['은행']); k = (b, x['금리유형'])
    if k not in best or x['대출최저'] < best[k]['대출최저']: best[k] = x
def pay(P, rate, n=360):
    i = rate / 100 / 12
    return P * i / (1 - (1 + i) ** -n)
P = 300_000_000
out = []
for b in sorted({k[0] for k in best}):
    v, f = best.get((b, '변동금리')), best.get((b, '고정금리'))
    if not (v and f): continue
    pv, pf = pay(P, v['대출최저']), pay(P, f['대출최저'])
    out.append((b, v['상품'].replace('\n', ''), v['대출최저'], f['상품'].replace('\n', ''), f['대출최저'], round(f['대출최저'] - v['대출최저'], 2), round(pv), round(pf), round(pf - pv)))
out.sort(key=lambda t: -t[5])
print('은행 | 변동 상품 | 변동 최저 | 고정 상품 | 고정 최저 | 차(%p) | 3억 30년 원리금균등 월 상환(변동) | (고정) | 차')
for t in out: print(' | '.join(map(str, t)))
e = json.load(open('ecos.json', encoding='utf-8'))
print('ECOS 신규 주담대(예금은행 가중평균, 신규취급액):', e['mortgage_new'][-4:])
print('ECOS 기준금리:', e['base'][-4:])
# 0.25%p 오를 때 3억 월 상환 증가(변동 최저 중앙 근처 예: 우리 4.41)
for base in (4.41,):
    print('0.25%p 오를 때', base, '→', round(pay(P, base + 0.25) - pay(P, base)), '원/월')
    print('0.30%p(6월→8월 신규 주담대 상승폭)', round(pay(P, base + 0.30) - pay(P, base)))
json.dump(out, open('calc_out.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
