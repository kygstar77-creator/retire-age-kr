# 전세대출 금리 — 금감원 금융상품통합비교공시(finlife) 2026-09 공시, raw_finlife_full.json에서 직접 계산
import json, collections
d = json.load(open('raw_finlife_full.json', encoding='utf-8'))
base = {(b['fin_co_no'], b['fin_prdt_cd']): b for b in d['baseList']}
rows = []
for o in d['optionList']:
    b = base[(o['fin_co_no'], o['fin_prdt_cd'])]
    rows.append(dict(bank=b['kor_co_nm'].replace('주식회사 ', '').replace(' 주식회사', '').replace('농협은행주식회사', '농협은행'),
                     prod=b['fin_prdt_nm'].replace('\n', ''), typ=o['lend_rate_type_nm'], rp=o['rpay_type_nm'],
                     mn=o['lend_rate_min'], mx=o['lend_rate_max'], avg=o.get('lend_rate_avg'),
                     fee=b.get('erly_rpay_fee'), lmt=b.get('loan_lmt')))
LOAN = 200_000_000
mon = lambda r: round(LOAN * r / 100 / 12)
print('§1 전체 줄', len(rows), '은행', len({r['bank'] for r in rows}), '평균 칸 있는 줄', sum(r['avg'] is not None for r in rows))
# §2 은행별 변동·만기일시 줄 중 평균금리 가장 낮은 상품
print('§2 은행별 변동금리(만기일시) 실제 평균 최저 상품, 2억 한 달 이자')
best = {}
for r in rows:
    if r['typ'] == '변동금리' and r['rp'] == '만기일시상환방식' and r['avg']:
        if r['bank'] not in best or r['avg'] < best[r['bank']]['avg']: best[r['bank']] = r
for r in sorted(best.values(), key=lambda r: r['avg']):
    print(f"  {r['bank']:10} {r['prod'][:22]:24} 평균 {r['avg']:.2f} (공시 {r['mn']}~{r['mx']}) 월 {mon(r['avg']):,}원")
# §3 고정 vs 변동 같은 상품
print('§3 같은 상품 고정-변동 평균 차이(만기일시)')
g = collections.defaultdict(dict)
for r in rows:
    if r['rp'] == '만기일시상환방식' and r['avg']: g[(r['bank'], r['prod'])][r['typ']] = r['avg']
for k, v in g.items():
    if len(v) == 2: print(f"  {k[0]} {k[1][:22]} 변동 {v['변동금리']:.2f} 고정 {v['고정금리']:.2f} 차 {v['고정금리']-v['변동금리']:+.2f} 월차 {mon(v['고정금리'])-mon(v['변동금리']):,}원")
# §4 공시 최저 vs 실제 평균 (변동·만기일시)
print('§4 공시 최저 vs 실제 평균')
for r in sorted(best.values(), key=lambda r: r['avg'] - r['mn']):
    print(f"  {r['bank']:10} 최저 {r['mn']:.2f} 평균 {r['avg']:.2f} 차 {r['avg']-r['mn']:+.2f}")
# §5 중도상환수수료 · 한도 (§2 상품)
print('§5 중도상환수수료·한도')
for r in sorted(best.values(), key=lambda r: r['avg']):
    print(f"  {r['bank']}: {(r['fee'] or '').replace(chr(10),' / ')[:140]} | 한도 {(r['lmt'] or '').replace(chr(10),' ')[:60]}")
lo, hi = min(best.values(), key=lambda r: r['avg']), max(best.values(), key=lambda r: r['avg'])
print('§6 최저', lo['bank'], lo['avg'], mon(lo['avg']), '최고', hi['bank'], hi['avg'], mon(hi['avg']), '월차', mon(hi['avg']) - mon(lo['avg']), '연차', 12*(mon(hi['avg']) - mon(lo['avg'])))
avgs = sorted(r['avg'] for r in best.values()); print('§7 은행 수', len(avgs), '중앙', avgs[len(avgs)//2] if len(avgs)%2 else (avgs[len(avgs)//2-1]+avgs[len(avgs)//2])/2)
