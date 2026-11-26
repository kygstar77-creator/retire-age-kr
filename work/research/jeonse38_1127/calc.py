# jeonse38_1127 계산 — 송도동 84㎡대(전용 80~86㎡) 단지별 전세가율, H-5 §4와 같은 정의
#   매매: 해제·공공기관 매수 제외, 2021~2026.06은 H-5 raw(11/21 받음), 2026.07~11은 오늘 받은 raw
#   단지 = 2026.07~10 매매 3건 이상 + 2021~22 매매 있는 곳(H-5 §3), 그중 같은 기간 순수전세(월세 0) 3건 이상
#   py -3.12 work/research/jeonse38_1127/calc.py > calc_out_1126.txt
import json, os, sys, glob, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(HERE, 'raw')
H5 = os.path.join(HERE, '..', 'longform', 'ep', 'H-5', 'raw', 'rt')
num = lambda s: float(str(s or '0').replace(',', '') or 0)
ym = lambda r: int(r['dealYear']) * 100 + int(r['dealMonth'])
eok = lambda v: f'{v/10000:.2f}억'
T = []
for p in sorted(glob.glob(os.path.join(H5, '28185_*_trade.json'))):
    if p[-17:-11] < '202607': T += json.load(open(p, encoding='utf-8'))
for p in sorted(glob.glob(os.path.join(RAW, '28185_*_trade.json'))): T += json.load(open(p, encoding='utf-8'))
T = [r for r in T if not r.get('cdealType') and r.get('buyerGbn') != '공공기관' and r['umdNm'] == '송도동']
S = [r for r in T if 80 <= num(r['excluUseAr']) <= 86]
R0 = []
for p in sorted(glob.glob(os.path.join(RAW, '28185_*_rent.json'))): R0 += json.load(open(p, encoding='utf-8'))
R0 = [r for r in R0 if r['umdNm'] == '송도동' and 80 <= num(r['excluUseAr']) <= 86]
def run(lo, hi, label):
    print(f'\n## {label} — 계약 {lo}~{hi}')
    rows = []
    for name in sorted({r['aptNm'] for r in S}):
        rs = [r for r in S if r['aptNm'] == name]
        pk = [r for r in rs if 202101 <= ym(r) <= 202212]
        rc = [num(r['dealAmount']) for r in rs if lo <= ym(r) <= hi]
        if len(rc) >= 3 and pk: rows.append((name, rs[0].get('buildYear'), st.median(rc), len(rc)))
    R = [r for r in R0 if num(r.get('monthlyRent')) == 0 and lo <= ym(r) <= hi]
    allrent = [r for r in R0 if lo <= ym(r) <= hi]
    print(f'  84㎡대 전월세 {len(allrent)}건 · 그중 순수전세 {len(R)}건(신규 {sum(1 for r in R if r.get("contractType")=="신규")} · 갱신 {sum(1 for r in R if r.get("contractType")=="갱신")} · 빈칸 {sum(1 for r in R if not r.get("contractType"))}) · 전세 중앙 {eok(st.median([num(r["deposit"]) for r in R]))}')
    gap = []
    for name, by, mm, n in rows:
        d = [num(x['deposit']) for x in R if x['aptNm'] == name]
        dn = [num(x['deposit']) for x in R if x['aptNm'] == name and x.get('contractType') == '신규']
        if len(d) >= 3: gap.append((st.median(d) / mm, name, by, st.median(d), len(d), mm, n, st.median(dn) / mm if len(dn) >= 3 else None, len(dn)))
    gap.sort(reverse=True)
    for g in gap:
        nw = f' · 신규만 {g[7]*100:.0f}%({g[8]}건)' if g[7] else ''
        print(f'  {g[1]}({g[2]}) 전세 중앙 {eok(g[3])}({g[4]}건) ÷ 매매 중앙 {eok(g[5])}({g[6]}건) = {g[0]*100:.0f}% · 차이 {eok(g[5]-g[3])}{nw}')
    rr = [g[0] for g in gap]
    print(f'  단지 {len(gap)}곳 · 전세가율 중앙 {st.median(rr)*100:.0f}% · 최고 {max(rr)*100:.0f}% · 최저 {min(rr)*100:.0f}% · 60% 이상 {sum(1 for x in rr if x >= .6)}곳 · 50% 미만 {sum(1 for x in rr if x < .5)}곳')
    df = [g[5] - g[3] for g in gap]
    print(f'  매매-전세 차이 중앙 {eok(st.median(df))} · 최소 {eok(min(df))} · 최대 {eok(max(df))}')
    nn = [g[7] for g in gap if g[7]]
    if nn: print(f'  신규 3건 이상 단지 {len(nn)}곳 · 신규만 전세가율 중앙 {st.median(nn)*100:.0f}%')
    # 준공 연도별
    for a, b, lab in ((0, 2009, '2009년 이전 준공'), (2010, 2016, '2010~2016년'), (2017, 2100, '2017년 이후')):
        x = [g[0] for g in gap if a <= int(g[2] or 0) <= b]
        if x: print(f'  {lab} {len(x)}곳 · 전세가율 중앙 {st.median(x)*100:.0f}%')
    return gap
run(202607, 202610, 'A. H-5·쇼츠와 같은 창(7~10월), 오늘 다시 받은 자료')
run(202607, 202611, 'B. 11월 신고분까지(7~11월)')
# C. 7~11월 덧붙임 — 갱신 계약 중 계약갱신요구권 사용(useRRRight), 전세·매매 가운데 값의 폭, 단순 계산(집값이 몇 % 내리면 전세금과 같아지나)

R = [r for r in R0 if num(r.get('monthlyRent')) == 0 and 202607 <= ym(r) <= 202611]
gs = [r for r in R if r.get('contractType') == '갱신']
print('\n## C. 7~11월 순수전세 덧붙임')
print(f'  갱신 {len(gs)}건 중 갱신요구권 사용(useRRRight=사용) {sum(1 for r in gs if (r.get("useRRRight") or "").strip() == "사용")}건 · 빈칸 {sum(1 for r in gs if not (r.get("useRRRight") or "").strip())}건')
nw = [num(r['deposit']) for r in R if r.get('contractType') == '신규']; gg = [num(r['deposit']) for r in gs]
print(f'  전세 중앙 신규 {eok(st.median(nw))}({len(nw)}건) · 갱신 {eok(st.median(gg))}({len(gg)}건)')
gap = run(202607, 202611, 'D. (B 다시 — 폭 계산용)')
print(f'  전세 가운데 값 폭 {eok(min(x[3] for x in gap))}~{eok(max(x[3] for x in gap))} · 매매 가운데 값 폭 {eok(min(x[5] for x in gap))}~{eok(max(x[5] for x in gap))}')
for x in (gap[0], gap[len(gap)//2], gap[-1]): print(f'  {x[1]} 전세가율 {x[0]*100:.0f}% → 집값이 {(1-x[0])*100:.0f}% 넘게 내리면 전세금보다 낮아짐')
