# 같은 동(법정동) 안에서 신축(≤5년) vs 21~30년, 84㎡ 안팎 · 신축 단지 이름 · 31년+ 비싼 구 단지
import json, glob, os, re, statistics as st, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
SGG = json.load(open(os.path.join(H, '..', 'seoul_sgg.json'), encoding='utf-8'))
def num(s): return float(re.sub(r'[^\d.]', '', str(s) or '0') or 0)
R = []
for f in sorted(glob.glob(os.path.join(H, 'raw', '*_2026*.json'))):
    code = os.path.basename(f).split('_')[0]
    for r in json.load(open(f, encoding='utf-8')):
        if r.get('cdealType'): continue
        by = int(num(r.get('buildYear')) or 0); a = num(r.get('excluUseAr'))
        if not by or not (80 <= a <= 86): continue
        R.append(dict(gu=SGG.get(code, code), dong=r.get('umdNm'), age=2026 - by, by=by, p=num(r.get('dealAmount')) / 1e4, apt=r.get('aptNm'), d=r.get('dealingGbn')))
g = collections.defaultdict(lambda: collections.defaultdict(list))
for r in R:
    k = 'new' if r['age'] <= 5 else 'old' if 21 <= r['age'] <= 30 else None
    if k: g[(r['gu'], r['dong'])][k].append(r['p'])
out = []
for (gu, dong), v in g.items():
    if len(v['new']) >= 3 and len(v['old']) >= 3:
        out.append((gu, dong, st.median(v['new']), st.median(v['old']), len(v['new']), len(v['old'])))
print('== 같은 동 안 신축(≤5년, 3건+) vs 21~30년(3건+) 84㎡ 안팎')
rat = []
for gu, dong, a, b, na, nb in sorted(out, key=lambda x: -x[2] / x[3]):
    rat.append(a / b); print(f'  {gu} {dong}: 신축 {a:.2f}억({na}) · 21~30년 {b:.2f}억({nb}) · {a/b:.2f}배 · 차이 {a-b:.2f}억')
print(f'  동 {len(rat)}곳 · 배수 중간값 {st.median(rat):.2f} · 신축이 더 비싼 동 {sum(1 for x in rat if x > 1)}곳 · 차이 중간값 {st.median([x[2]-x[3] for x in out]):.2f}억')
print('\n== 신축(≤5년) 84㎡ 거래 많은 단지 상위 10')
c = collections.Counter((r['gu'], r['apt'], r['by']) for r in R if r['age'] <= 5)
for (gu, apt, by), n in c.most_common(10):
    ps = [r['p'] for r in R if r['apt'] == apt and r['gu'] == gu and r['age'] <= 5]
    print(f'  {gu} {apt}({by}) {n}건 중간값 {st.median(ps):.2f}억')
print('\n== 31년 이상이 21~30년보다 비싼 구: 31년+ 거래 많은 단지')
for gu in ['강남구', '서초구', '송파구', '양천구', '강동구', '용산구']:
    c = collections.Counter((r['apt'], r['by']) for r in R if r['gu'] == gu and r['age'] > 30)
    print(' ', gu, ' · '.join(f"{a}({b}) {n}건 {st.median([r['p'] for r in R if r['gu']==gu and r['apt']==a and r['age']>30]):.1f}억" for (a, b), n in c.most_common(4)))
print('\n== 서울 전체 연식 띠별 건수 비중(84㎡ 안팎)')
tot = len(R)
for lo, hi, nm in [(0, 5, '5년 이내'), (6, 10, '6~10년'), (11, 20, '11~20년'), (21, 30, '21~30년'), (31, 99, '31년 이상')]:
    n = sum(1 for r in R if lo <= r['age'] <= hi); print(f'  {nm}: {n}건 {n/tot*100:.1f}%')
