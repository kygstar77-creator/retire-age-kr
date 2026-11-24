# 서울 아파트 월세 실거래 — 계약 2025-08~10 vs 2026-08~10 (국토부 RTMSDataSvcAptRent, raw/). 11/24 write-b
import json, os, glob, statistics as st, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
sgg = json.load(open(os.path.join(H, '..', 'seoul_sgg.json'), encoding='utf-8'))
def n(s): return int((s or '0').replace(',', '') or 0)
P = {'2025': ['202508', '202509', '202510'], '2026': ['202608', '202609', '202610']}
data = {}
for y, yms in P.items():
    rows = []
    for f in glob.glob(os.path.join(H, 'raw', '*_rent.json')):
        lawd, ym = os.path.basename(f).split('_')[:2]
        if ym in yms:
            for r in json.load(open(f, encoding='utf-8')): r['_g'] = lawd; rows.append(r)
    data[y] = rows
def pct(a, b): return f'{a/b*100:.1f}%' if b else '-'
for y, rows in data.items():
    mon = [r for r in rows if n(r['monthlyRent']) > 0]
    m = [n(r['monthlyRent']) for r in mon]
    print(f'== {y} 8~10월 계약: 전체 {len(rows):,} · 월세(월세>0) {len(mon):,} ({pct(len(mon), len(rows))})')
    print(f'  월세 중간 {st.median(m)}만원 · 평균 {st.mean(m):.1f}만원 · 100만원 이상 {sum(x>=100 for x in m):,} ({pct(sum(x>=100 for x in m), len(m))}) · 200만원 이상 {pct(sum(x>=200 for x in m), len(m))} · 300만원 이상 {pct(sum(x>=300 for x in m), len(m))} · 50만원 미만 {pct(sum(x<50 for x in m), len(m))}')
    q = st.quantiles(m, n=10); print('  10분위', q)
    print(f'  월세 계약 보증금 중간 {st.median([n(r["deposit"]) for r in mon]):,}만원')
    a84 = [n(r['monthlyRent']) for r in mon if 80 <= float(r['excluUseAr']) <= 86]
    a59 = [n(r['monthlyRent']) for r in mon if 55 <= float(r['excluUseAr']) <= 61]
    print(f'  84㎡대(80~86) 월세 {len(a84):,}건 중간 {st.median(a84)} · 100만원 이상 {pct(sum(x>=100 for x in a84), len(a84))} | 59㎡대(55~61) {len(a59):,}건 중간 {st.median(a59)} · 100만원 이상 {pct(sum(x>=100 for x in a59), len(a59))}')
    ct = collections.Counter(r.get('contractType') or '빈칸' for r in mon); print('  계약구분', dict(ct))
    for t in ('신규', '갱신'):
        mt = [n(r['monthlyRent']) for r in mon if r.get('contractType') == t]
        if mt: print(f'   {t} {len(mt):,}건 중간 {st.median(mt)} · 100만원 이상 {pct(sum(x>=100 for x in mt), len(mt))}')
    big = sorted(mon, key=lambda r: -n(r['monthlyRent']))[:3]
    print('  가장 비싼', [(sgg[r['_g']], r['aptNm'], r['excluUseAr'], r['deposit'], r['monthlyRent']) for r in big])
print('\n== 구별 (2026 월세 중간 · 100만원 이상 몫 | 2025 같은 값 · 건수)')
rowsg = []
for g, name in sgg.items():
    v = {}
    for y in P:
        m = [n(r['monthlyRent']) for r in data[y] if r['_g'] == g and n(r['monthlyRent']) > 0]
        v[y] = (st.median(m), sum(x>=100 for x in m)/len(m)*100, len(m))
    rowsg.append((name, v))
for name, v in sorted(rowsg, key=lambda x: -x[1]['2026'][0]):
    print(f'  {name:6} 2026 중간 {v["2026"][0]:>6} · 100↑ {v["2026"][1]:5.1f}% ({v["2026"][2]:,}건) | 2025 중간 {v["2025"][0]:>6} · 100↑ {v["2025"][1]:5.1f}% ({v["2025"][2]:,}건)')
print('  중간 100만원 넘는 구 2026:', sum(v['2026'][0] > 100 for _, v in rowsg), '· 100만원 이상:', sum(v['2026'][0] >= 100 for _, v in rowsg), '· 2025:', sum(v['2025'][0] >= 100 for _, v in rowsg))
print('  100만원 이상 계약이 절반 넘는 구 2026:', [nm for nm, v in rowsg if v['2026'][1] > 50], '| 2025:', [nm for nm, v in rowsg if v['2025'][1] > 50])
