# 서울 25개 구 아파트 매매 실거래 2026-08~10(11/12 23시 받음)으로 신축·구축 가격 차이
# 연식 = 2026 − buildYear. 해제(cdealType 있음) 뺌. 전용 80~86㎡(84㎡ 안팎)만 같은 크기로 비교.
import json, glob, os, re, statistics as st, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
SGG = json.load(open(os.path.join(H, '..', 'seoul_sgg.json'), encoding='utf-8'))
def num(s): return float(re.sub(r'[^\d.]', '', str(s) or '0') or 0)
def band(age):
    if age <= 5: return 'A 5년 이내'
    if age <= 10: return 'B 6~10년'
    if age <= 20: return 'C 11~20년'
    if age <= 30: return 'D 21~30년'
    return 'E 31년 이상'
allr = []; cancel = 0; direct = 0
for f in sorted(glob.glob(os.path.join(H, 'raw', '*_2026*.json'))):
    code = os.path.basename(f).split('_')[0]
    for r in json.load(open(f, encoding='utf-8')):
        if r.get('cdealType'): cancel += 1; continue
        by = int(num(r.get('buildYear')) or 0)
        if not by: continue
        a = num(r.get('excluUseAr')); p = num(r.get('dealAmount')) / 1e4  # 억
        d = r.get('dealingGbn')
        if d == '직거래': direct += 1
        allr.append(dict(gu=SGG.get(code, code), age=2026 - by, by=by, area=a, p=p, d=d, apt=r.get('aptNm'), m=r.get('dealMonth'), fl=num(r.get('floor'))))
print('해제 뺀 거래', len(allr), '· 해제', cancel, '· 직거래', direct)
k84 = [r for r in allr if 80 <= r['area'] <= 86]
print('전용 80~86㎡', len(k84))
def show(rows, title):
    print('\n==', title)
    g = collections.defaultdict(list)
    for r in rows: g[band(r['age'])].append(r['p'])
    for b in sorted(g): print(f'  {b}: {len(g[b])}건 · 중간값 {st.median(g[b]):.2f}억')
show(k84, '서울 전체 84㎡ 안팎 연식별')
show([r for r in k84 if r['d'] != '직거래'], '서울 전체 84㎡ 중개거래만')
# 구별: 같은 구 안 신축(≤5) vs 21~30년 vs 31년+
print('\n== 구별 84㎡ 중간값(억) 신축≤5 / 6~10 / 11~20 / 21~30 / 31+ (건수)')
res = []
for gu in sorted(set(r['gu'] for r in k84)):
    g = collections.defaultdict(list)
    for r in k84:
        if r['gu'] == gu: g[band(r['age'])].append(r['p'])
    cell = [(f"{st.median(g[b]):.2f}({len(g[b])})" if g[b] else '-') for b in ['A 5년 이내', 'B 6~10년', 'C 11~20년', 'D 21~30년', 'E 31년 이상']]
    print(' ', gu, ' / '.join(cell))
    if len(g['A 5년 이내']) >= 5 and len(g['D 21~30년']) >= 5:
        res.append((gu, st.median(g['A 5년 이내']), st.median(g['D 21~30년']), len(g['A 5년 이내']), len(g['D 21~30년'])))
print('\n== 신축(≤5년)·21~30년 둘 다 5건 이상인 구: 신축/구축 배수')
rat = []
for gu, a, d, na, nd in sorted(res, key=lambda x: -x[1] / x[2]):
    rat.append(a / d); print(f'  {gu}: 신축 {a:.2f}억({na}) · 21~30년 {d:.2f}억({nd}) · {a/d:.2f}배 · 차이 {a-d:.2f}억')
if rat: print(f'  구 {len(rat)}곳 배수 중간값 {st.median(rat):.2f} · 신축이 더 비싼 구 {sum(1 for x in rat if x>1)}곳')
