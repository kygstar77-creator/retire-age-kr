# H-4 계산 재현 — 광명(철산·하안·광명동). 숫자는 전부 여기서 나온다. 실행: py -3.12 work/research/longform/ep/H-4/calc.py > calc_out.txt
# 재료: raw/rt/<구코드>_<월>_{trade,rent}.json = 국토교통부 아파트 매매·전월세 실거래(공공데이터포털 1613000, getrt.py로 2026-10-16 20:4x~21:0x 받음)
# 네이버 부동산 등 민간 화면·호가·매물·분양권 웃돈·재건축 전망은 쓰지 않는다. 분양권 전매는 이 자료에 없다(입주 전 새 단지 매매 0건인 까닭).
import json, os, sys, glob, collections, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(HERE, 'raw', 'rt')
SGG = json.load(open(os.path.normpath(os.path.join(HERE, '..', '..', '..', 'seoul_sgg.json')), encoding='utf-8'))
PY = 3.305785
def num(s): return float(str(s or '0').replace(',', '') or 0)
def eok(m): return f'{m/10000:.2f}억'
def load(lawd, kind, months=None):
    out = []
    for p in sorted(glob.glob(os.path.join(RT, f'{lawd}_*_{kind}.json'))):
        if months and os.path.basename(p).split('_')[1] not in months: continue
        out += json.load(open(p, encoding='utf-8'))
    return out
def ok(r): return not r.get('cdealType') and r.get('buyerGbn') != '공공기관'
def is84(r): return 80 <= num(r['excluUseAr']) <= 85.99
def med(v): return st.median(v) if v else 0
def ym(r): return (int(r['dealYear']), int(r['dealMonth']))
GM = '41210'; DONG = ['철산동', '하안동', '광명동']
T = [r for r in load(GM, 'trade') if ok(r)]
R = load(GM, 'rent')
print('# H-4 calc_out — 단위 만원. 84㎡대 = 전용 80~85㎡. 해제·공공기관 매수 제외. 전세 = 월세 0인 전월세 신고(신규·갱신 섞임 — 구분 칸 contractType로 따로 셈)\n')

print('## 0. 거래량 관문(최근 3개월 = 2026.07~10 계약, 매매 20건 미만 동네는 뺀다)')
for u in DONG:
    t = [r for r in T if r['umdNm'] == u]
    print(f'- {u}: 1년(2025.11~2026.10 계약) 매매 {len(t)}건 · 2026.07~10 {sum(1 for r in t if ym(r) >= (2026, 7))}건')

print('\n## 1. 광명시 vs 서울 25개 구 — 84㎡대 매매 가운데 값, 같은 창(2026.07~09 계약)')
W = ('202607', '202608', '202609')
rows = []
for code, name in list(SGG.items()) + [(GM, '광명시')]:
    nm = name if isinstance(name, str) else (name.get('name') or str(name))
    t = [r for r in load(code, 'trade', W) if ok(r) and is84(r)]
    if code == GM: t = [r for r in t if r['umdNm'] in DONG + ['일직동', '소하동', '노온사동', '가학동', '옥길동']]
    rows.append((med([num(r['dealAmount']) for r in t]), nm, len(t)))
rows.sort(reverse=True)
for i, (m, nm, n) in enumerate(rows, 1): print(f'{i:2}. {nm} {eok(m)} ({n}건){"  ◀" if nm == "광명시" else ""}')
gm = [x for x in rows if x[1] == '광명시'][0]
print(f'→ 광명시 84㎡대 가운데 값 {eok(gm[0])} · 서울 25개 구 중 광명보다 가운데 값이 낮은 구 {sum(1 for x in rows if x[1] != "광명시" and x[0] < gm[0])}개')
gt = [r for r in load(GM, 'trade', W) if ok(r) and is84(r)]
for u in DONG:
    v = [num(r['dealAmount']) for r in gt if r['umdNm'] == u]
    print(f'   - {u} 84㎡대 {len(v)}건 가운데 {eok(med(v))}')
NEW = [num(r['dealAmount']) for r in gt if int(r['buildYear'] or 0) >= 2019]
print(f'   - 광명시 2019년 이후 지은 단지 84㎡대 {len(NEW)}건 가운데 {eok(med(NEW))}')

print('\n## 2. 철산동 84㎡대 단지별 1년 매매 가운데 값(5건 이상, 비싼 순)')
c = collections.defaultdict(list)
for r in T:
    if r['umdNm'] == '철산동' and is84(r): c[(r['aptNm'], r['buildYear'])].append(num(r['dealAmount']))
CH = sorted(((med(v), k, len(v)) for k, v in c.items() if len(v) >= 5), reverse=True)
for m, (nm, by), n in CH: print(f'- {nm}({by}) {n}건 가운데 {eok(m)}')

print('\n## 3. 새 단지 전세 vs 옆 단지 매매 — 철산자이더헤리티지(2025 입주) 84㎡대 전세')
H = [r for r in R if r['aptNm'] == '철산자이더헤리티지' and num(r.get('monthlyRent')) == 0 and is84(r)]
hd = [num(r['deposit']) for r in H]
print(f'- 전세 {len(H)}건(신규 {sum(1 for r in H if r.get("contractType") == "신규")}건) · 가운데 {eok(med(hd))} · 최저 {eok(min(hd))} · 최고 {eok(max(hd))} · 계약 {sorted({f"{a}.{b:02d}" for a, b in map(ym, H)})}')
print(f'- 같은 단지 84㎡대 매매 신고 {sum(1 for r in T if r["aptNm"] == "철산자이더헤리티지")}건(분양권 전매는 이 자료에 없음)')
under = [(m, k, n) for m, k, n in CH if m <= med(hd)]
print(f'- 철산동 84㎡대 단지(5건 이상 {len(CH)}곳) 중 매매 가운데 값이 이 전세 가운데 값({eok(med(hd))}) 이하인 곳 {len(under)}곳:')
for m, (nm, by), n in under: print(f'    {nm}({by}) {eok(m)} ({n}건)')

print('\n## 4. 새 단지 전세가 옆 옛 단지 전세보다 얼마나 — 철산동 84㎡대 신규 전세 가운데 값(5건 이상, 갱신은 옛 값이 남아 뺌)')
rc = collections.defaultdict(list)
for r in R:
    if r['umdNm'] == '철산동' and is84(r) and num(r.get('monthlyRent')) == 0 and r.get('contractType') == '신규': rc[(r['aptNm'], r['buildYear'])].append(num(r['deposit']))
for m, (nm, by), n in sorted(((med(v), k, len(v)) for k, v in rc.items() if len(v) >= 5), reverse=True): print(f'- {nm}({by}) 전세 {n}건 가운데 {eok(m)}')

print('\n## 5. 광명시 새 입주 단지(2023년 이후) 전월세 신고 건수 — 입주 몰림')
cn = collections.Counter((r['aptNm'], r['umdNm'], r['buildYear']) for r in R if int(r['buildYear'] or 0) >= 2023)
for (nm, u, by), n in cn.most_common(8): print(f'- {nm}({u}, {by}) {n}건')
