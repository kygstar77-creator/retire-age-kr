# NDG-1 1장 근거: 2026년 서울 25개 구 아파트 매매 ㎡당 가운데 값·준공 연도 가운데 (youtube-loop 2026-11-27)
# 입력 work/research/rt/11*_2026*_trade.json (해제 거래 뺌) · 출력 calc_age_price_out_1127.txt
import json, glob, statistics as st, collections as C, os
NM = {'11320':'도봉','11305':'강북','11350':'노원'}
root = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'rt')
by = C.defaultdict(lambda: ([], []))
for f in glob.glob(os.path.join(root, '11*_2026*_trade.json')):
    if 'offi' in f: continue
    g = os.path.basename(f).split('_')[0]
    for r in json.load(open(f, encoding='utf-8')):
        if r.get('cdealType') or not r.get('buildYear'): continue
        by[g][0].append(int(r['buildYear'])); by[g][1].append(int(r['dealAmount'].replace(',', '')) / float(r['excluUseAr']))
out = []
allb = [x for v in by.values() for x in v[0]]; allp = [x for v in by.values() for x in v[1]]
out.append(f'구 {len(by)} · 건 {len(allb)} · 서울 ㎡당 가운데 {round(st.median(allp))}만원 · 준공 가운데 {st.median(allb)}')
for i, g in enumerate(sorted(by, key=lambda g: st.median(by[g][1])), 1):
    out.append(f'㎡당 낮은 순 {i} {NM.get(g,g)} {round(st.median(by[g][1]))}만원')
for i, g in enumerate(sorted(by, key=lambda g: st.median(by[g][0])), 1):
    out.append(f'준공 오래된 순 {i} {NM.get(g,g)} {st.median(by[g][0])}')
open(os.path.join(os.path.dirname(__file__), 'calc_age_price_out_1127.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out[:8]))
