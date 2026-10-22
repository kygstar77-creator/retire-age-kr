# H-5 calc2 — calc.py의 '고점 최고가 ÷ 최근 중앙'은 최고 한 건과 가운데 값을 견줘 회복을 낮게 보이게 한다 → 같은 잣대(가운데 값끼리)로 다시 셈
#   py -3.12 work/research/longform/ep/H-5/calc2.py > calc2_out.txt
# 고점 반기 = 2021.07~2022.06(calc §2 반기 중앙 9.00억·8.95억, 가장 높은 두 반기) · 바닥 반기 = 2022.07~2023.06(6.80억·6.73억) · 최근 = 2026.07~10
import json, os, sys, glob, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(HERE, 'raw', 'rt')
def num(s): return float(str(s or '0').replace(',', '') or 0)
def ym(r): return int(r['dealYear']) * 100 + int(r['dealMonth'])
T = []
for p in sorted(glob.glob(os.path.join(RT, '28185_*_trade.json'))): T += json.load(open(p, encoding='utf-8'))
T = [r for r in T if not r.get('cdealType') and r.get('buyerGbn') != '공공기관' and r['umdNm'] == '송도동']
S = [r for r in T if 80 <= num(r['excluUseAr']) <= 86]
eok = lambda v: f'{v/10000:.2f}억'
PK, LO, RC = (202107, 202206), (202207, 202306), (202607, 202612)
inw = lambda r, w: w[0] <= ym(r) <= w[1]
print('# H-5 calc2_out — 송도동 84㎡대, 가운데 값끼리 견줌(고점 반기 2021.07~2022.06 · 바닥 반기 2022.07~2023.06 · 최근 2026.07~10)')
a = lambda w: [num(r['dealAmount']) for r in S if inw(r, w)]
p, l, c = a(PK), a(LO), a(RC)
print(f'\n## 1 동 전체 84㎡대: 고점 반기 {len(p)}건 중앙 {eok(st.median(p))} · 바닥 반기 {len(l)}건 중앙 {eok(st.median(l))} · 최근 {len(c)}건 중앙 {eok(st.median(c))}')
print(f'  바닥 ÷ 고점 = {st.median(l)/st.median(p)*100:.0f}% · 최근 ÷ 고점 = {st.median(c)/st.median(p)*100:.0f}% · 최근 ÷ 바닥 = {st.median(c)/st.median(l)*100:.0f}%')
rows = []
for name in sorted({r['aptNm'] for r in S}):
    rs = [r for r in S if r['aptNm'] == name]
    pk = [num(r['dealAmount']) for r in rs if inw(r, PK)]
    lo = [num(r['dealAmount']) for r in rs if inw(r, LO)]
    rc = [num(r['dealAmount']) for r in rs if inw(r, RC)]
    if len(rc) >= 3 and len(pk) >= 3:
        rows.append((st.median(rc)/st.median(pk), name, int(rs[0].get('buildYear') or 0), st.median(pk), len(pk), st.median(lo) if len(lo) >= 3 else None, len(lo), st.median(rc), len(rc)))
rows.sort(reverse=True)
print(f'\n## 2 단지별(고점 반기·최근 각 3건 이상): 최근 중앙 ÷ 고점 반기 중앙')
for r in rows:
    lo = f'바닥 {eok(r[5])}({r[6]}건)' if r[5] else f'바닥 -({r[6]}건)'
    print(f'  {r[1]}({r[2]}) 고점 {eok(r[3])}({r[4]}건) · {lo} · 최근 {eok(r[7])}({r[8]}건) → {r[0]*100:.0f}%')
pc = [r[0] for r in rows]
print(f'  단지 {len(rows)}곳 · 중앙 {st.median(pc)*100:.0f}% · 최저 {min(pc)*100:.0f}% · 최고 {max(pc)*100:.0f}% · 100% 넘은 곳 {sum(x>=1 for x in pc)} · 90% 넘은 곳 {sum(x>=.9 for x in pc)} · 70% 밑 {sum(x<.7 for x in pc)} · 50% 밑 {sum(x<.5 for x in pc)}')
print('\n## 3 지은 해로 묶음(위 단지들, 단지 중앙의 중앙)')
for lab, lo_, hi_ in (('2010년 이전', 0, 2010), ('2011~2016년', 2011, 2016), ('2017년 이후', 2017, 2100)):
    g = [r for r in rows if lo_ <= r[2] <= hi_]
    if g: print(f'  {lab}: {len(g)}곳 · 최근÷고점 중앙 {st.median([r[0] for r in g])*100:.0f}% · 최근 값 중앙 {eok(st.median([r[7] for r in g]))} · 고점 값 중앙 {eok(st.median([r[3] for r in g]))}')
print('\n## 4 "반값" 확인 — 2022.07~2026.10 84㎡대 거래 중 그 단지 고점 반기 중앙의 절반 이하로 팔린 건수')
pkm = {r[1]: r[3] for r in rows}
after = [r for r in S if ym(r) >= 202207 and r['aptNm'] in pkm]
half = [r for r in after if num(r['dealAmount']) <= pkm[r['aptNm']] * .5]
print(f'  대상 {len(after)}건 중 {len(half)}건({len(half)/len(after)*100:.1f}%)')
for r in sorted(half, key=lambda r: num(r['dealAmount'])/pkm[r['aptNm']])[:12]:
    print(f"   {r['aptNm']} {r['dealYear']}.{int(r['dealMonth']):02d} {num(r['excluUseAr']):.1f}㎡ {r.get('floor')}층 {eok(num(r['dealAmount']))} (고점 {eok(pkm[r['aptNm']])}의 {num(r['dealAmount'])/pkm[r['aptNm']]*100:.0f}%) {r.get('dealingGbn','')}")
low60 = [r for r in after if num(r['dealAmount']) <= pkm[r['aptNm']] * .6]
print(f'  60% 이하: {len(low60)}건({len(low60)/len(after)*100:.1f}%)')
print('\n## 5 매매 − 전세(최근, 단지별 가운데 값끼리, 전세 3건 이상)')
R = []
for p_ in sorted(glob.glob(os.path.join(RT, '28185_2026*_rent.json'))): R += json.load(open(p_, encoding='utf-8'))
R = [r for r in R if r['umdNm'] == '송도동' and 80 <= num(r['excluUseAr']) <= 86 and num(r.get('monthlyRent')) == 0 and int(r['dealMonth']) >= 7]
gs = []
for r in rows:
    d = [num(x['deposit']) for x in R if x['aptNm'] == r[1]]
    if len(d) >= 3: gs.append((r[7] - st.median(d), r[1], r[7], st.median(d), len(d)))
gs.sort()
for g in gs: print(f'  {g[1]} 매매 {eok(g[2])} − 전세 {eok(g[3])}({g[4]}건) = {eok(g[0])}')
if gs: print(f'  {len(gs)}곳 · 차 중앙 {eok(st.median([g[0] for g in gs]))} · 최소 {eok(gs[0][0])} · 최대 {eok(gs[-1][0])}')
print('\n## 6 직거래(중개 없이) 비율 — 2022.07~2026.10 84㎡대, 위 30곳')
dj = lambda xs: sum(1 for r in xs if r.get('dealingGbn') == '직거래')
print(f'  전체 {len(after)}건 중 직거래 {dj(after)}건({dj(after)/len(after)*100:.1f}%) · 고점 반기의 60% 이하 {len(low60)}건 중 직거래 {dj(low60)}건 · 절반 이하 {len(half)}건 중 직거래 {dj(half)}건')
print('\n## 7 전세 4억 안팎(3.8~4.2억) 순수전세가 있었던 단지(2026.07~10, 84㎡대)')
near = {}
for x in R:
    if 38000 <= num(x['deposit']) <= 42000: near[x['aptNm']] = near.get(x['aptNm'], 0) + 1
print(f'  {sum(near.values())}건 · {len(near)}곳: ' + ' · '.join(f'{k} {v}' for k, v in sorted(near.items(), key=lambda kv: -kv[1])[:10]))
print(f'  2026.07~10 순수전세 84㎡대 전체 {len(R)}건 중앙 {eok(st.median([num(x["deposit"]) for x in R]))}')
