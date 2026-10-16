# 저축은행 vs 은행 정기예금 — 금감원 금융상품통합비교공시(finlife) 공시월 202609, raw/finlife_deposit_1017.json(2026-10-17 06:3x 수신)
import json, statistics as st, sys
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open('raw/finlife_deposit_1017.json', encoding='utf-8'))
TAX = 0.154; P = 100_000_000
def nm(s): return s.replace('주식회사 ','').replace(' 주식회사','').replace('농협은행주식회사','농협은행').replace('\n','')
def U(g): return {(nm(r['은행']), r['상품'].replace('\n',''), r['기간'], r['금리'], r['최고금리'], r['금리유형']) for r in d[g]}
BIG5 = {'국민은행','신한은행','하나은행','우리은행','농협은행'}
NET = {'케이뱅크','카카오뱅크','토스뱅크'}
def best(rows, term='12', col=3):
    b = {}
    for x in rows:
        if x[2] != term or x[col] is None: continue
        if x[0] not in b or x[col] > b[x[0]][col]: b[x[0]] = x
    return b
bank, sb = U('020000'), U('030300')
print('§0 은행 회사', len({x[0] for x in bank}), '상품줄', len(bank), '| 저축은행 회사', len({x[0] for x in sb}), '상품줄', len(sb))
for term in ('6','12','24'):
    bb, ss = best(bank, term), best(sb, term)
    print(f'§1 {term}개월 회사별 가장 높은 기본금리 중앙: 은행 {st.median([x[3] for x in bb.values()])} ({len(bb)}곳) / 저축은행 {st.median([x[3] for x in ss.values()])} ({len(ss)}곳)')
bb, ss = best(bank), best(sb)
print('§2 12개월 은행별 기본(우대 포함 최고):')
for x in sorted(bb.values(), key=lambda x: -x[3]):
    tag = '5대' if x[0] in BIG5 else ('인터넷' if x[0] in NET else '')
    print(f'   {x[0]:14} {tag:4} 기본 {x[3]:.2f} 최고 {x[4]:.2f} {x[5]} | {x[1][:24]}')
bm = best(bank, col=4)
print('§3 5대 은행 12개월 우대 포함 최고금리(회사별 가장 높은 상품):', {k: (v[3], v[4], v[1][:18]) for k, v in bm.items() if k in BIG5})
smed = st.median([x[3] for x in ss.values()])
print('§4 저축은행 중앙', smed, '이상인 은행 기본금리 회사:', [k for k, v in bb.items() if v[3] >= smed])
print('   저축은행 79곳 중 은행 1위(기본)', max(x[3] for x in bb.values()), '이상인 곳', sum(1 for x in ss.values() if x[3] >= max(y[3] for y in bb.values())))
print('   저축은행 기본=최고 비율(12개월 상품줄)', round(sum(1 for x in sb if x[2]=='12' and x[3]==x[4]) / sum(1 for x in sb if x[2]=='12'), 3),
      '/ 은행', round(sum(1 for x in bank if x[2]=='12' and x[3]==x[4]) / sum(1 for x in bank if x[2]=='12'), 3))
def simple(r): return round(P * r / 100)
def mcomp(r): return round(P * ((1 + r / 100 / 12) ** 12 - 1))
def net(i): return i - int(i * 0.14 / 10) * 10 - int(i * 0.014 / 10) * 10
print('§5 1억 1년 이자(세전→세후 15.4%, 소득세 14%·지방세 1.4% 10원 미만 절사)')
for lab, r in [('저축은행 중앙 기본', smed), ('저축은행 1위 기본', max(x[3] for x in ss.values())), ('은행 중앙 기본', st.median([x[3] for x in bb.values()])),
               ('은행 1위 기본(전북)', max(x[3] for x in bb.values())), ('국민 기본', bb['국민은행'][3]), ('하나 기본', bb['하나은행'][3])]:
    print(f'   {lab:16} {r:.2f}% 단리 세전 {simple(r):,} 세후 {net(simple(r)):,} | 월복리 세전 {mcomp(r):,} 세후 {net(mcomp(r)):,}')
print('   차이 저축은행 중앙 vs 은행 중앙 세후', net(simple(smed)) - net(simple(st.median([x[3] for x in bb.values()]))), '/ vs 국민 기본', net(simple(smed)) - net(simple(bb['국민은행'][3])))
# 레드팀 1차(10/17) 반영: 3년 비교·5대 은행 기간별 기본금리
b36, s36 = best(bank, '36'), best(sb, '36')
print(f'§6 36개월 중간값: 은행 {st.median([x[3] for x in b36.values()])} ({len(b36)}곳) / 저축은행 {st.median([x[3] for x in s36.values()])} ({len(s36)}곳)')
for term in ('6', '24'):
    bt = best(bank, term); print(f'§7 {term}개월 5대 은행 기본:', {k: bt[k][3] for k in bt if k in BIG5})
