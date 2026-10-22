# H-5 송도 계산 — 국토부 아파트 매매·전월세 실거래(1613000), 인천 연수구 28185 송도동, 해제·공공기관 매수 제외
#   py -3.12 work/research/longform/ep/H-5/calc.py > calc_out.txt
# 84㎡대 = 전용 80~86㎡. 고점 창 = 2021.01~2022.12 계약. 최근 = 2026.07~10 계약. 바닥 창 = 2023.01~2024.12.
import json, os, sys, glob, collections, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(HERE, 'raw', 'rt')
def num(s): return float(str(s or '0').replace(',', '') or 0)
def ym(r): return int(r['dealYear']) * 100 + int(r['dealMonth'])
T = []
for p in sorted(glob.glob(os.path.join(RT, '28185_*_trade.json'))): T += json.load(open(p, encoding='utf-8'))
T = [r for r in T if not r.get('cdealType') and r.get('buyerGbn') != '공공기관' and r['umdNm'] == '송도동']
S = [r for r in T if 80 <= num(r['excluUseAr']) <= 86]
eok = lambda v: f'{v/10000:.2f}억'
print('# H-5 calc_out — 송도동 84㎡대(전용 80~86㎡) 매매, 계약 2021.01~2026.10, 해제·공공기관 매수 제외')
print(f'\n## 0 표본: 송도동 매매 전체 {len(T)}건 · 84㎡대 {len(S)}건')
# 1 해마다 가운데 값·건수
print('\n## 1 해마다 84㎡대 거래 가운데 값(중앙)·건수')
for y in range(2021, 2027):
    a = [num(r['dealAmount']) for r in S if int(r['dealYear']) == y]
    if a: print(f'  {y}: {len(a)}건 · 중앙 {eok(st.median(a))}')
# 2 반기마다
print('\n## 2 반기마다 84㎡대 중앙')
for y in range(2021, 2027):
    for h, ms in ((1, range(1, 7)), (2, range(7, 13))):
        a = [num(r['dealAmount']) for r in S if int(r['dealYear']) == y and int(r['dealMonth']) in ms]
        if a: print(f'  {y}H{h}: {len(a)}건 · 중앙 {eok(st.median(a))}')
# 3 단지별: 고점 창 최고가 vs 최근 중앙·최근 최고
print('\n## 3 단지별 84㎡대 — 2021~22 최고가 · 2023~24 최저가 · 2026.07~10 중앙(최근 3건 이상인 단지만), 최근 중앙 ÷ 고점 최고')
rows = []
for name in sorted({r['aptNm'] for r in S}):
    rs = [r for r in S if r['aptNm'] == name]
    pk = [num(r['dealAmount']) for r in rs if 202101 <= ym(r) <= 202212]
    lo = [num(r['dealAmount']) for r in rs if 202301 <= ym(r) <= 202412]
    rc = [num(r['dealAmount']) for r in rs if ym(r) >= 202607]
    if len(rc) >= 3 and pk:
        rows.append((st.median(rc) / max(pk), name, rs[0].get('buildYear'), max(pk), min(lo) if lo else None, st.median(rc), len(rc), max(rc)))
rows.sort(reverse=True)
for r in rows:
    print(f'  {r[1]}({r[2]}) 고점 {eok(r[3])} · 바닥 {eok(r[4]) if r[4] else "-"} · 최근 중앙 {eok(r[5])}({r[6]}건, 최고 {eok(r[7])}) → 고점의 {r[0]*100:.0f}%')
pc = [r[0] for r in rows]
print(f'  단지 {len(rows)}곳 · 고점 대비 중앙 {st.median(pc)*100:.0f}% · 90% 넘은 단지 {sum(1 for x in pc if x >= .9)}곳 · 70% 밑 {sum(1 for x in pc if x < .7)}곳')
# 4 전세 — 2026.07~10 신규 순수전세 84㎡대 중앙, 같은 단지 매매 최근 중앙과 비율
R = []
for p in sorted(glob.glob(os.path.join(RT, '28185_2026*_rent.json'))): R += json.load(open(p, encoding='utf-8'))
R = [r for r in R if r['umdNm'] == '송도동' and 80 <= num(r['excluUseAr']) <= 86 and num(r.get('monthlyRent')) == 0 and int(r['dealMonth']) >= 7]
print(f'\n## 4 2026.07~10 순수전세 84㎡대 {len(R)}건(신규 {sum(1 for r in R if r.get("contractType") == "신규")}건) · 전체 중앙 {eok(st.median([num(r["deposit"]) for r in R]))}')
for r0 in rows[:0]: pass
gap = []
for r in rows:
    d = [num(x['deposit']) for x in R if x['aptNm'] == r[1]]
    if len(d) >= 3: gap.append((st.median(d) / r[5], r[1], st.median(d), r[5], len(d)))
gap.sort(reverse=True)
for g in gap: print(f'  {g[1]} 전세 중앙 {eok(g[2])}({g[4]}건) ÷ 매매 중앙 {eok(g[3])} = {g[0]*100:.0f}%')
if gap: print(f'  단지 {len(gap)}곳 전세가율 중앙 {st.median([g[0] for g in gap])*100:.0f}%')
