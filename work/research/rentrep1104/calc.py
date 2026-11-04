# rentrep1104 계산 — 서울 25개 구 아파트 전월세 실거래(국토부 RTMSDataSvcAptRent, rawrt/ 11/4 10:55 받음, 계약월 2026-09·10)
# 질문: 월세 계약은 과태료 '계약금액'을 보증금 + 월세×200으로 센다(시행령 별표3 비고 2). 보증금만 볼 때와 칸이 얼마나 달라지나
import sys, os, json, glob, re, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
def num(s): return int(re.sub(r'[^\d]', '', s or '0') or 0)
rows = []
for f in glob.glob(os.path.join(H, 'rawrt', '*_2026*_rent.json')):
    for r in json.load(open(f, encoding='utf-8')):
        rows.append((num(r['deposit']), num(r['monthlyRent']), r.get('contractType', ''), r['dealMonth']))  # 만원
# 별표3 마. 1) 칸(만원) — 1억 미만 / 1~3억 / 3~5억 / 5억 이상
FINE = {'3개월 이하': (2, 3, 4, 5), '6개월 이하': (4, 8, 12, 15), '1년 이하': (6, 10, 16, 20), '2년 이하': (8, 13, 20, 25), '2년 초과·공동신고 거부': (10, 15, 25, 30)}
NAMES = ('1억 미만', '1억~3억', '3억~5억', '5억 이상')
def band(a): return 0 if a < 10000 else 1 if a < 30000 else 2 if a < 50000 else 3
def amt(d, m): return d + m * 200
def need(d, m): return d > 6000 or m > 30   # 시행령 4조의3 ①
print(f'전체 계약 {len(rows):,}건 (9월 {sum(r[3]=="9" for r in rows):,} · 10월 {sum(r[3]=="10" for r in rows):,} — 10월은 신고 기한 30일이라 덜 들어옴)')
w = [r for r in rows if r[1] > 0]; j = [r for r in rows if r[1] == 0]
print(f'월세(월세 0원 초과) {len(w):,}건 {100*len(w)/len(rows):.1f}% · 전세 {len(j):,}건')
print(f'신고 대상 아님(보증금 6천만원 이하이면서 월세 30만원 이하) {sum(not need(d,m) for d,m,_,_ in rows):,}건')
bd = collections.Counter(band(d) for d, m, _, _ in w); ba = collections.Counter(band(amt(d, m)) for d, m, _, _ in w)
print('\n월세 계약 칸 — 보증금만 볼 때 → 보증금+월세×200')
for i, n in enumerate(NAMES): print(f'  {n}: {bd[i]:,}건 ({100*bd[i]/len(w):.1f}%) → {ba[i]:,}건 ({100*ba[i]/len(w):.1f}%)')
up = [r for r in w if band(amt(r[0], r[1])) > band(r[0])]
print(f'칸이 한 칸 이상 올라간 월세 계약 {len(up):,}건 = {100*len(up)/len(w):.1f}%')
print(f'월세 계약 중앙: 보증금 {st.median(r[0] for r in w):g}만원 · 월세 {st.median(r[1] for r in w):g}만원 · 계약금액 중앙 {st.median(amt(r[0], r[1]) for r in w):g}만원')
print(f'전세 계약 보증금 중앙 {st.median(r[0] for r in j):g}만원 · 칸 {collections.Counter(NAMES[band(r[0])] for r in j).most_common()}')
print('\n예시(만원) — 계약금액 · 칸 · 늦은 기간별 과태료')
for d, m in ((1000, 100), (3000, 50), (5000, 150), (10000, 100), (20000, 150), (30000, 0)):
    a = amt(d, m); b = band(a)
    print(f'  보증금 {d:,} 월세 {m}: 계약금액 {a:,} ({NAMES[b]}) · 보증금만이면 {NAMES[band(d)]} · ' + ' / '.join(f'{k} {v[b]}만' for k, v in FINE.items()))
print('\n일반기준: 신고관청이 동기·결과·횟수로 개별기준의 2분의 1 범위에서 늘리거나 줄임 — 1억~3억 6개월 이하 8만원이면 4만~12만원')
