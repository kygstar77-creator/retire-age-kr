# 잠실주공5단지 vs 리센츠 — 국토부 실거래(raw, 2026-11-20 받음) 직접 계산
# 84㎡대 = 전용 80~85㎡ · 해제(cdealType 'O') 제외 · 공공기관 매수 제외 · 평당 = 전용 3.305785㎡ · 단위 억
import json, glob, os, statistics as st, sys
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
def rows(kind):
    for p in sorted(glob.glob(os.path.join(H, 'raw', f'11710_*_{kind}.json'))):
        for r in json.load(open(p, encoding='utf-8')):
            if r.get('umdNm', '잠실동') != '잠실동': continue
            yield r
NM = {'5단지': lambda n: '주공' in n and '5' in n, '리센츠': lambda n: n == '리센츠'}
def who(n):
    for k, f in NM.items():
        if f(n): return k
T = []
for r in rows('trade'):
    k = who(r['aptNm']);
    if not k: continue
    if r.get('cdealType') == 'O' or r.get('buyerGbn') == '공공기관': continue
    a = float(r['excluUseAr']); amt = int(r['dealAmount'].replace(',', '')) / 1e4
    ym = f"{r['dealYear']}{int(r['dealMonth']):02d}"
    T.append(dict(k=k, a=a, amt=amt, ym=ym, d=f"{ym}{int(r['dealDay']):02d}", fl=int(r['floor']), nm=r['aptNm'], by=r.get('buildYear')))
print('단지 이름:', sorted({(t['k'], t['nm'], t['by']) for t in T}))
B = [t for t in T if 80 <= t['a'] <= 85]
med = lambda xs: st.median(xs) if xs else None
def summ(xs, lab):
    if not xs: print(lab, '없음'); return
    p = [x['amt'] / (x['a'] / 3.305785) for x in xs]
    print(f"{lab}: {len(xs)}건 중앙 {med([x['amt'] for x in xs]):.2f}억 · 평당 {med(p)*1e4:,.0f}만원 · 최저 {min(x['amt'] for x in xs):.2f} 최고 {max(x['amt'] for x in xs):.2f} · 면적 {sorted({x['a'] for x in xs})}")
    return med(p)
print('\n## 1. 최근 1년(계약 2025.12~2026.11) 84㎡대')
p5 = summ([x for x in B if x['k'] == '5단지' and x['ym'] >= '202512'], '5단지')
pr = summ([x for x in B if x['k'] == '리센츠' and x['ym'] >= '202512'], '리센츠')
print(f"평당 차이 5단지가 {(p5/pr-1)*100:+.1f}%")
print('\n## 2. 해마다 84㎡대 중앙(억) — 5단지 / 리센츠 / 차이')
for y in range(2020, 2027):
    a = [x['amt'] for x in B if x['k'] == '5단지' and x['ym'][:4] == str(y)]
    b = [x['amt'] for x in B if x['k'] == '리센츠' and x['ym'][:4] == str(y)]
    if a and b: print(f"{y}: 5단지 {med(a):.2f}({len(a)}) / 리센츠 {med(b):.2f}({len(b)}) / 차이 {med(a)-med(b):+.2f}억 ({(med(a)/med(b)-1)*100:+.1f}%)")
print('\n## 3. 사업시행인가(2026-07-01) 전후 84㎡대 중앙')
for k in NM:
    a = [x['amt'] for x in B if x['k'] == k and '202601' <= x['ym'] <= '202606']
    b = [x['amt'] for x in B if x['k'] == k and '202607' <= x['ym'] <= '202611']
    print(f"{k}: 2026.1~6월 {med(a):.2f}억({len(a)}) → 7~11월 {med(b):.2f}억({len(b)}) {(med(b)/med(a)-1)*100:+.1f}%")
print('\n## 4. 최근 1년 층(84㎡대) 1~3층 / 4층 이상')
for k in NM:
    lo = [x['amt'] for x in B if x['k'] == k and x['ym'] >= '202512' and x['fl'] <= 3]
    hi = [x['amt'] for x in B if x['k'] == k and x['ym'] >= '202512' and x['fl'] >= 4]
    print(f"{k}: 1~3층 {med(lo)}억({len(lo)}) · 4층↑ {med(hi)}억({len(hi)})")
print('\n## 5. 최근 1년 순수전세(월세 0) 84㎡대 중앙 · 전세가율')
R = {}
for r in rows('rent'):
    k = who(r['aptNm'])
    if not k or int(str(r.get('monthlyRent', '0')).replace(',', '') or 0) != 0: continue
    a = float(r['excluUseAr'])
    if not 80 <= a <= 85: continue
    ym = f"{r['dealYear']}{int(r['dealMonth']):02d}"
    if ym < '202512': continue
    R.setdefault(k, []).append(int(r['deposit'].replace(',', '')) / 1e4)
for k in NM:
    s = [x['amt'] for x in B if x['k'] == k and x['ym'] >= '202512']
    print(f"{k}: 전세 {len(R.get(k,[]))}건 중앙 {med(R.get(k,[])):.2f}억 · 매매 중앙 대비 {med(R[k])/med(s)*100:.1f}% · 매매-전세 {med(s)-med(R[k]):.2f}억")
print('\n## 6. 달마다 5단지 최저 vs 리센츠 최고(최근 1년, 84㎡대)')
c = 0; n = 0
for ym in sorted({x['ym'] for x in B if x['ym'] >= '202512'}):
    a = [x['amt'] for x in B if x['k'] == '5단지' and x['ym'] == ym]; b = [x['amt'] for x in B if x['k'] == '리센츠' and x['ym'] == ym]
    if a and b:
        n += 1; c += min(a) > max(b); print(f"{ym}: 5단지 최저 {min(a):.2f} / 리센츠 최고 {max(b):.2f}")
print(f"5단지 최저가 더 높은 달 {c}/{n}")
