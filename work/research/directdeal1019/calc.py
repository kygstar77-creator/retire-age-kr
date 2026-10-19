# directdeal1019 계산 — 서울 아파트 직거래가 같은 단지·같은 면적 중개거래보다 얼마나 쌌나
# 자료: raw/ 국토부 아파트 매매 실거래(2026-10-19 받음), 계약 2025-10~2026-09(10월은 신고 기한 안이라 뺌)
# 짝: 같은 구·같은 단지(aptSeq 없으면 이름+법정동)·전용면적 소수 첫째 자리까지 같음, 계약일 ±90일 중개거래 중앙값
import sys, os, json, glob, re, statistics as st, collections, datetime as dt
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(H, '..', '..'))
SGG = json.load(open(os.path.join(W, 'research', 'seoul_sgg.json'), encoding='utf-8'))
def num(s): return int(re.sub(r'[^\d]', '', s or '0') or 0)
R = []
for f in glob.glob(os.path.join(H, 'raw', '*_trade.json')):
    ym = os.path.basename(f).split('_')[1]
    if ym == '202610': continue
    for r in json.load(open(f, encoding='utf-8')):
        r['_p'] = num(r['dealAmount']); r['_d'] = dt.date(int(r['dealYear']), int(r['dealMonth']), int(r['dealDay']))
        r['_k'] = (r['sggCd'], r.get('aptSeq') or (r['umdNm'] + r['aptNm']), round(float(r['excluUseAr']), 1))
        R.append(r)
print('전체 행', len(R), '필드 예', {k: R[0][k] for k in ('dealingGbn','cdealType','buyerGbn','slerGbn') if k in R[0]})
print('거래유형', collections.Counter(r.get('dealingGbn') for r in R))
V = [r for r in R if not r.get('cdealType')]
print('해제 빼고', len(V), '해제', len(R) - len(V))
D = [r for r in V if r.get('dealingGbn') == '직거래']; M = [r for r in V if r.get('dealingGbn') == '중개거래']
print(f'직거래 {len(D):,} / {len(V):,} = {100*len(D)/len(V):.1f}%')
print('직거래 매수자', collections.Counter(r.get('buyerGbn') for r in D), '매도자', collections.Counter(r.get('slerGbn') for r in D))
# 월별
bym = collections.defaultdict(lambda: [0, 0])
for r in V:
    k = r['_d'].strftime('%Y-%m'); bym[k][1] += 1; bym[k][0] += r.get('dealingGbn') == '직거래'
for k in sorted(bym): a, b = bym[k]; print(' ', k, f'{a}/{b} {100*a/b:.1f}%')
# 구별
bg = collections.defaultdict(lambda: [0, 0])
for r in V: bg[r['sggCd']][1] += 1; bg[r['sggCd']][0] += r.get('dealingGbn') == '직거래'
print('구별 직거래 비율'); [print(' ', SGG[c], f'{a}/{b} {100*a/b:.1f}%') for c, (a, b) in sorted(bg.items(), key=lambda x: -x[1][0]/x[1][1])]
# 짝 비교
idx = collections.defaultdict(list)
for r in M: idx[r['_k']].append(r)
pairs = []
for r in D:
    if r.get('buyerGbn') == '공공기관' or r.get('slerGbn') == '공공기관': continue
    c = [m['_p'] for m in idx[r['_k']] if abs((m['_d'] - r['_d']).days) <= 90]
    if len(c) >= 3:
        med = st.median(c); pairs.append((r, med, (r['_p'] / med - 1) * 100, len(c)))
gaps = [g for _, _, g, _ in pairs]
print(f'\n짝 지은 직거래 {len(pairs):,}건 (같은 단지·면적, ±90일 중개 3건 이상) · 전체 직거래 {len(D):,}')
print(f'  차이 중앙값 {st.median(gaps):+.1f}% · 평균 {st.mean(gaps):+.1f}%')
for lo, hi, lab in ((-1e9, -30, '30% 넘게 쌈'), (-30, -10, '10~30% 쌈'), (-10, -5, '5~10% 쌈'), (-5, 5, '±5% 안'), (5, 1e9, '5% 넘게 비쌈')):
    n = sum(lo < g <= hi if hi != 5 else lo < g < hi for g in gaps) if False else sum((g > lo) and (g <= hi) for g in gaps)
    print(f'  {lab}: {n:,}건 {100*n/len(gaps):.1f}%')
n30 = sum(g <= -30 for g in gaps); n5 = sum(g <= -5 for g in gaps)
print(f'  30% 이상 쌈 {n30} ({100*n30/len(gaps):.1f}%) · 5% 이상 쌈 {n5} ({100*n5/len(gaps):.1f}%)')
# 차액 3억 이상
d3 = [(r, med) for r, med, g, _ in pairs if med - r['_p'] >= 30000]
print(f'  중개 중앙값보다 3억 이상 싸게: {len(d3)}건')
# 예시: 차이 큰 순 5건
print('\n가장 싸게 된 직거래 10건')
for r, med, g, n in sorted(pairs, key=lambda x: x[2])[:10]:
    print(f"  {SGG[r['sggCd']]} {r['umdNm']} {r['aptNm']} {r['excluUseAr']}㎡ {r['_d']} {r['floor']}층 직거래 {r['_p']:,}만 vs 중개중앙 {med:,.0f}만({n}건) {g:+.1f}%")
# 같은 기간 중개거래끼리 '자기 빼고 중앙값' 대비 퍼짐(대조군)
ctrl = []
for k, L in idx.items():
    for r in L:
        c = [m['_p'] for m in L if m is not r and abs((m['_d'] - r['_d']).days) <= 90]
        if len(c) >= 3: ctrl.append((r['_p'] / st.median(c) - 1) * 100)
print(f'\n대조군 중개거래 {len(ctrl):,}건: 중앙 {st.median(ctrl):+.1f}% · 30% 이상 쌈 {100*sum(g<=-30 for g in ctrl)/len(ctrl):.1f}% · 5% 이상 쌈 {100*sum(g<=-5 for g in ctrl)/len(ctrl):.1f}%')
