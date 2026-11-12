# 저축은행 vs 은행 정기예금 11월 — finlife 공시월 202610(raw/finlife_deposit_1112.json, 11/12 18:25 받음) vs 202609(../sbdep1017/raw/finlife_deposit_1017.json, 10/17 받음)
import json, statistics as st, sys
sys.stdout.reconfigure(encoding='utf-8')
P = 100_000_000
def nm(s): return (s or '').replace('주식회사 ','').replace(' 주식회사','').replace('농협은행주식회사','농협은행').replace('\n','').strip()
def U(d, g): return {(nm(r['은행']), (r['상품'] or '').replace('\n',''), str(r['기간']), r['금리'], r['최고금리'], r['금리유형']) for r in d[g]}
def best(rows, term='12', col=3):
    b = {}
    for x in rows:
        if x[2] != term or x[col] is None: continue
        if x[0] not in b or x[col] > b[x[0]][col]: b[x[0]] = x
    return b
def net(i): return i - int(i * 0.14 / 10) * 10 - int(i * 0.014 / 10) * 10
def simple(r): return round(P * r / 100)
new = json.load(open('raw/finlife_deposit_1112.json', encoding='utf-8'))
old = json.load(open('../sbdep1017/raw/finlife_deposit_1017.json', encoding='utf-8'))
for lab, d in (('10월 공시(9월분, 10/17 받음)', old), ('11월 공시(10월분, 11/12 받음)', new)):
    b, s = U(d, '020000'), U(d, '030300')
    print('==', lab, '| 은행 회사', len({x[0] for x in b}), '줄', len(b), '| 저축은행 회사', len({x[0] for x in s}), '줄', len(s), '| 12개월 줄', sum(1 for x in s if x[2]=='12'))
    for term in ('6','12','24','36'):
        bb, ss = best(b, term), best(s, term)
        if bb and ss: print(f'  {term}개월 회사별 최고 기본금리 중앙: 은행 {st.median([x[3] for x in bb.values()])}({len(bb)}곳) / 저축은행 {st.median([x[3] for x in ss.values()])}({len(ss)}곳) / 저축은행 최고 {max(x[3] for x in ss.values())}')
sb_o, sb_n = best(U(old,'030300')), best(U(new,'030300'))
bk_o, bk_n = best(U(old,'020000')), best(U(new,'020000'))
for lab, o, n in (('저축은행', sb_o, sb_n), ('은행', bk_o, bk_n)):
    both = sorted(set(o) & set(n))
    diff = {k: round(n[k][3] - o[k][3], 2) for k in both}
    up = {k: v for k, v in diff.items() if v > 0}; dn = {k: v for k, v in diff.items() if v < 0}
    print(f'§변화 {lab}: 두 달 다 있는 {len(both)}곳 · 올림 {len(up)} · 내림 {len(dn)} · 같음 {len(both)-len(up)-len(dn)} · 변화 중앙 {st.median(diff.values())}')
    print('   올림 상위', sorted(up.items(), key=lambda x: -x[1])[:8]); print('   내림 상위', sorted(dn.items(), key=lambda x: x[1])[:8])
    print('   새로 생김', sorted(set(n)-set(o))[:10], '빠짐', sorted(set(o)-set(n))[:10])
ss = sb_n; smed = st.median([x[3] for x in ss.values()]); bmed = st.median([x[3] for x in bk_n.values()])
print('§1년 저축은행 상위 10(기본):'); [print('  ', x[0], x[3], x[4], x[5], x[1][:20]) for x in sorted(ss.values(), key=lambda x: -x[3])[:10]]
print('§1년 은행 상위 8(기본):'); [print('  ', x[0], x[3], x[4], x[5], x[1][:20]) for x in sorted(bk_n.values(), key=lambda x: -x[3])[:8]]
print('§저축은행 기본 4% 이상 곳 수', sum(1 for x in ss.values() if x[3] >= 4.0), '/', len(ss), '| 10월 공시', sum(1 for x in sb_o.values() if x[3] >= 4.0), '/', len(sb_o))
print('§은행 1위 기본', max(x[3] for x in bk_n.values()), '이상인 저축은행', sum(1 for x in ss.values() if x[3] >= max(y[3] for y in bk_n.values())))
for lab, r in (('저축은행 중앙', smed), ('은행 중앙', bmed), ('저축은행 1위', max(x[3] for x in ss.values()))):
    print(f'§1억 1년 단리 {lab} {r}% 세전 {simple(r):,} 세후 {net(simple(r)):,}')
print('§세후 차이 저축은행 중앙-은행 중앙', net(simple(smed)) - net(simple(bmed)))
o_s = st.median([x[3] for x in sb_o.values()]); o_b = st.median([x[3] for x in bk_o.values()])
print(f'§격차 10월공시 {round(o_s-o_b,3)}%p → 11월공시 {round(smed-bmed,3)}%p')
s12 = [x for x in U(new,'030300') if x[2]=='12']; print('§저축은행 12개월 줄 기본=최고 비율', round(sum(1 for x in s12 if x[3]==x[4])/len(s12),3), '복리 비율', round(sum(1 for x in s12 if x[5] and '복리' in x[5])/len(s12),3))
