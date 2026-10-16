# 저축은행 vs 은행 적금 — 금감원 금융상품통합비교공시(finlife) 공시월 202609, raw/finlife_saving_1017.json(2026-10-17 07:3x 수신)
import json, statistics as st, sys, collections, re
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open('raw/finlife_saving_1017.json', encoding='utf-8'))
TAX = 0.154
def nm(s): return s.replace('주식회사 ','').replace(' 주식회사','').replace('농협은행주식회사','농협은행').replace('\n','').strip()
BIG5 = {'국민은행','신한은행','하나은행','우리은행','농협은행'}
NET = {'케이뱅크','카카오뱅크','토스뱅크'}
def rows(g):
    base = {(b['fin_co_no'], b['fin_prdt_cd']): b for b in d[g]['base']}
    out = []
    for o in d[g]['opt']:
        b = base[(o['fin_co_no'], o['fin_prdt_cd'])]
        out.append(dict(co=nm(b['kor_co_nm']), prd=b['fin_prdt_nm'].replace('\n',' ').strip(), trm=o['save_trm'], r=o['intr_rate'], rmax=o['intr_rate2'],
                        rs=o['rsrv_type'], it=o['intr_rate_type'], lim=b['max_limit'], deny=b['join_deny'], etc=(b['etc_note'] or '').replace('\n',' / ')))
    return out
B, S = rows('020000'), rows('030300')
def bestco(R, term='12', filt=lambda x: True, col='r'):
    b = {}
    for x in R:
        if x['trm'] != term or x[col] is None or not filt(x): continue
        if x['co'] not in b or x[col] > b[x['co']][col]: b[x['co']] = x
    return b
print('§0 은행 회사', len({x['co'] for x in B}), '상품 줄', len(B), '| 저축은행 회사', len({x['co'] for x in S}), '상품 줄', len(S))
for term in ('6','12','24','36'):
    bb, ss = bestco(B, term), bestco(S, term)
    print(f'§1 {term}개월 회사별 가장 높은 기본금리 중앙: 은행 {st.median([x["r"] for x in bb.values()])} ({len(bb)}곳) / 저축은행 {st.median([x["r"] for x in ss.values()])} ({len(ss)}곳)')
ok50 = lambda x: (x['lim'] is None) or int(x['lim']) >= 500000
bb, ss = bestco(B, '12', ok50), bestco(S, '12', ok50)
print(f'§2 12개월·월 50만원 넣을 수 있는(한도 칸 비었거나 50만원 이상) 상품만: 은행 {st.median([x["r"] for x in bb.values()])} ({len(bb)}곳) / 저축은행 {st.median([x["r"] for x in ss.values()])} ({len(ss)}곳)')
def share(R):
    t = [x for x in R if x['trm']=='12']
    lim = [x for x in t if x['lim'] is not None and int(x['lim']) < 500000]
    nl = [x for x in t if x['lim'] is None]
    return len(t), len(lim), len(nl)
for lab, R in (('은행', B), ('저축은행', S)):
    t, l, n = share(R); print(f'§3 {lab} 12개월 상품 줄 {t} 중 월 한도 50만원 미만 {l}줄({l/t:.1%}) · 한도 칸 비어 있음 {n}줄({n/t:.1%})')
# 상품 단위(회사·상품 기준)
def prod_share(R):
    p = {}
    for x in R:
        if x['trm']=='12': p[(x['co'], x['prd'])] = x['lim']
    return len(p), sum(1 for v in p.values() if v is not None and int(v) < 500000), sum(1 for v in p.values() if v is None)
for lab, R in (('은행', B), ('저축은행', S)):
    t, l, n = prod_share(R); print(f'§3b {lab} 12개월 적금 상품 {t}개 중 월 한도 50만원 미만 {l}개({l/t:.1%}) · 한도 칸 비어 있음 {n}개')
print('§4 12개월 기본금리 상위(회사별 최고, 한도 무관):')
for lab, R in (('은행', B), ('저축은행', S)):
    bt = sorted(bestco(R).values(), key=lambda x: -x['r'])[:6]
    for x in bt: print(f'   {lab} {x["co"]:12} 기본 {x["r"]:.2f} 최고 {x["rmax"]} 한도 {x["lim"]} {x["rs"]} {x["it"]} | {x["prd"][:28]} | deny {x["deny"]}')
print('§5 5대 은행·인터넷은행 12개월 회사별 최고 기본(우대 포함 최고):')
bbb = bestco(B)
for k, v in bbb.items():
    if k in BIG5 or k in NET: print(f'   {k:10} 기본 {v["r"]:.2f} 최고 {v["rmax"]} 한도 {v["lim"]} {v["rs"]} | {v["prd"][:26]}')
# 기본=최고 비율
for lab, R in (('은행', B), ('저축은행', S)):
    t = [x for x in R if x['trm']=='12']
    print(f'§6 {lab} 12개월 줄 중 기본=최고(우대 없이 그 금리) {sum(1 for x in t if x["r"]==x["rmax"])/len(t):.1%}')
# 정액 vs 자유
for lab, R in (('은행', B), ('저축은행', S)):
    for rs in ('S','F'):
        bt = bestco(R, '12', lambda x: x['rs']==rs)
        print(f'§7 {lab} {rs} 회사별 최고 기본 중앙 {st.median([x["r"] for x in bt.values()])} ({len(bt)}곳)')
# 이자 계산: 정액 매달 50만원 12개월, 단리, 세후 15.4%
def simple(m, r, n=12): return m * (r/100) * n*(n+1)/2/12
def net(i): return i - int(i*0.14/10)*10 - int(i*0.014/10)*10
def comp(m, r, n=12):  # 월복리 정액적립, 월초 납입 가정(이자 = 각 회차 (1+r/12)^k)
    rr = r/100/12; return sum(m*((1+rr)**(n-k+1)) for k in range(1, n+1)) - m*n
bmed = st.median([x['r'] for x in bestco(B).values()]); smed = st.median([x['r'] for x in bestco(S).values()])
print('§8 월 50만원 12개월(원금 600만원) 단리 세후 이자')
for lab, r in (('저축은행 중앙', smed), ('은행 중앙', bmed), ('저축은행 1위', max(x['r'] for x in bestco(S).values())), ('은행 1위', max(x['r'] for x in bestco(B).values()))):
    i = simple(500000, r); print(f'   {lab:10} {r:.2f}% 세전 {round(i):,} 세후 {net(round(i)):,} | 월복리 세전 {round(comp(500000, r)):,}')
print('   차이 세후(저축은행 중앙 − 은행 중앙)', net(round(simple(500000, smed))) - net(round(simple(500000, bmed))))
print('   원금 600만원 대비 세후 이자율', round(net(round(simple(500000, smed)))/6000000*100, 2), '% (금리', smed, ')')
print('   같은 금리 예금 600만원 1년 세후', net(round(6000000*smed/100)))
