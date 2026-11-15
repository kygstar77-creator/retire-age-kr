# 노도강 1년 새 얼마나 올랐나 — 같은 단지·같은 크기끼리(국토부 실거래 S1, raw/*_trade.json)
# 최근 1년 = 계약 2025-11~2026-11, 그 전 1년 = 2024-11~2025-10. 해제(cdealType) 거래 뺌.
# 같은 집 묶음 = 구·단지(aptSeq 없으면 aptNm+umdNm)·전용면적 1㎡ 반올림. 묶음마다 두 해 중간값 비 → 구별 중간값.
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(H, '..', '..'))
SG = json.load(open(os.path.join(W, 'research', 'seoul_sgg.json'), encoding='utf-8'))
num = lambda s: float(str(s or '0').replace(',', '') or 0)
ymi = lambda r: int(r['dealYear']) * 100 + int(r['dealMonth'])
rows = []; cancel = 0
for p in sorted(glob.glob(os.path.join(H, 'raw', '*_trade.json'))):
    code = os.path.basename(p)[:5]
    for r in json.load(open(p, encoding='utf-8')):
        if r.get('cdealType'): cancel += 1; continue
        r['_g'] = code; rows.append(r)
win = lambda r: 'now' if 202511 <= ymi(r) <= 202611 else ('pre' if 202411 <= ymi(r) <= 202510 else None)
key = lambda r: (r['_g'], r.get('aptSeq') or (r['aptNm'] + '|' + r.get('umdNm', '')), round(num(r['excluUseAr'])))
NODO = ['11350', '11320', '11305']
grp = C.defaultdict(lambda: {'now': [], 'pre': []})
for r in rows:
    w = win(r)
    if w: grp[key(r)][w].append(num(r['dealAmount']))
def gu_stat(codes, mn=1):
    ratios = []; n_now = n_pre = 0; pairs = 0; tr_now = 0
    for k, v in grp.items():
        if k[0] in codes and len(v['now']) >= mn and len(v['pre']) >= mn:
            ratios.append(st.median(v['now']) / st.median(v['pre']) - 1); pairs += 1; tr_now += len(v['now'])
    return ratios, pairs, tr_now
print(f'# 매매 {len(rows):,}건(해제 {cancel:,}건 뺌), 서울 25개 구, 계약 2024-11~2026-11')
print('\n## §1 구별 — 같은 단지·같은 크기 묶음 중간값 변화(두 해 각 1건 이상 / 각 3건 이상)')
res = []
for code, nm in SG.items():
    r1, p1, t1 = gu_stat([code], 1); r3, p3, t3 = gu_stat([code], 3)
    cnt_now = sum(1 for r in rows if r['_g'] == code and win(r) == 'now'); cnt_pre = sum(1 for r in rows if r['_g'] == code and win(r) == 'pre')
    allnow = [num(r['dealAmount']) for r in rows if r['_g'] == code and win(r) == 'now']; allpre = [num(r['dealAmount']) for r in rows if r['_g'] == code and win(r) == 'pre']
    res.append((st.median(r3) if r3 else 0, nm, code, st.median(r1), p1, st.median(r3) if r3 else 0, p3, cnt_now, cnt_pre, st.median(allnow) / st.median(allpre) - 1))
res.sort(reverse=True)
for i, x in enumerate(res, 1):
    print(f'{i:2d}. {x[1]} 같은집(≥1) {x[3]*100:+.1f}% ({x[4]}묶음) · 같은집(≥3) {x[5]*100:+.1f}% ({x[6]}묶음) · 거래 {x[8]:,}→{x[7]:,}건 · 그냥 중간값 {x[9]*100:+.1f}%')
for tag, codes in [('노도강 셋', NODO), ('서울 전체', list(SG)), ('노도강 뺀 22개 구', [c for c in SG if c not in NODO])]:
    r1, p1, _ = gu_stat(codes, 1); r3, p3, _ = gu_stat(codes, 3)
    print(f'- {tag}: 같은집(≥1) {st.median(r1)*100:+.1f}% ({p1}묶음) · (≥3) {st.median(r3)*100:+.1f}% ({p3}묶음) · 오른 묶음 비율(≥3) {sum(1 for x in r3 if x > 0)/len(r3)*100:.0f}%')
