# H-5 calc4 — 레드팀 v1(10/23) 지적 확인: '반값' 표본 범위·30곳 기준 최고 한 건 잣대·뺀 단지·전세 가격대 분포
#   py -3.12 work/research/longform/ep/H-5/calc4.py > calc4_out.txt
import json, os, sys, glob, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(HERE, 'raw', 'rt')
def num(s): return float(str(s or '0').replace(',', '') or 0)
def ym(r): return int(r['dealYear']) * 100 + int(r['dealMonth'])
T = []
for p in sorted(glob.glob(os.path.join(RT, '28185_*_trade.json'))): T += json.load(open(p, encoding='utf-8'))
T = [r for r in T if not r.get('cdealType') and r.get('buyerGbn') != '공공기관' and r['umdNm'] == '송도동']
S = [r for r in T if 80 <= num(r['excluUseAr']) <= 86]
eok = lambda v: f'{v/10000:.2f}억'
PK, RC = (202107, 202206), (202607, 202612)
inw = lambda r, w: w[0] <= ym(r) <= w[1]
names = sorted({r['aptNm'] for r in S})
info = {}
for n in names:
    rs = [r for r in S if r['aptNm'] == n]
    pk = [num(r['dealAmount']) for r in rs if inw(r, PK)]
    rc = [num(r['dealAmount']) for r in rs if inw(r, RC)]
    mx = [num(r['dealAmount']) for r in rs if 202101 <= ym(r) <= 202212]
    info[n] = dict(pk=pk, rc=rc, mx=max(mx) if mx else None, by=int(rs[0].get('buildYear') or 0))
in30 = [n for n, d in info.items() if len(d['rc']) >= 3 and len(d['pk']) >= 3]
print(f'# calc4_out — 84㎡대 거래가 한 건이라도 있는 단지 {len(names)}곳 · 30곳 기준(고점 반기·최근 각 3건 이상) {len(in30)}곳')
after_all = [r for r in S if ym(r) >= 202207]
after30 = [r for r in after_all if r['aptNm'] in in30]
print(f'\n## 1 2022.07~2026.10 84㎡대 거래: 동 전체 {len(after_all)}건 · 그중 30곳 {len(after30)}건')
print('\n## 2 30곳에서 빠진 단지(최근 3건 이상인데 고점 반기 3건 미만 / 최근 3건 미만)')
a = [n for n in names if n not in in30 and len(info[n]['rc']) >= 3]
b = [n for n in names if n not in in30 and len(info[n]['rc']) < 3]
print(f'  최근 3건 이상 · 고점 반기 3건 미만: {len(a)}곳')
for n in a:
    d = info[n]; mx = eok(d['mx']) if d['mx'] else '-'
    print(f'   {n}({d["by"]}) 고점 반기 {len(d["pk"])}건 · 2021~22 최고 {mx} · 최근 {len(d["rc"])}건 중앙 {eok(st.median(d["rc"]))}' + (' ← 최근 중앙이 2021~22 최고보다 높음' if d['mx'] and st.median(d['rc']) > d['mx'] else ''))
print(f'  최근 3건 미만: {len(b)}곳')
print('\n## 3 같은 30곳으로 잣대만 바꿈: 최근 중앙 ÷ 2021~22 최고 한 건')
r1 = sorted(st.median(info[n]['rc']) / info[n]['mx'] for n in in30)
r2 = sorted(st.median(info[n]['rc']) / st.median(info[n]['pk']) for n in in30)
print(f'  최고 한 건 기준 중앙 {st.median(r1)*100:.1f}% ({min(r1)*100:.0f}~{max(r1)*100:.0f}%) · 가운데 값끼리 중앙 {st.median(r2)*100:.1f}%')
print('\n## 4 2026.07~10 순수전세 84㎡대 가격대(0.5억 칸)')
R = []
for p in sorted(glob.glob(os.path.join(RT, '28185_*_rent.json'))): R += json.load(open(p, encoding='utf-8'))
R = [r for r in R if r['umdNm'] == '송도동' and 80 <= num(r['excluUseAr']) <= 86 and num(r.get('monthlyRent')) == 0 and inw(r, RC)]
c = collections.Counter(int(num(r['deposit']) // 5000) for r in R)
for k in sorted(c): print(f'  {k*0.5:.1f}~{k*0.5+0.5:.1f}억 미만: {c[k]}건')
print(f'  합 {len(R)}건 · 3.8~4.2억 {sum(1 for r in R if 38000 <= num(r["deposit"]) <= 42000)}건')
