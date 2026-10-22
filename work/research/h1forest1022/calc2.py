# 2026-10-22 write-b: 갱신 vs 신규 전세 — 84㎡대(전용 80~85㎡), 월세 0원, 계약 2025-11~2026-10
import json, glob, statistics as st, sys
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding='utf-8')
def n(s): return int((s or '0').replace(',', '') or 0)
def load(l, k): return [x for f in sorted(glob.glob(f'raw/{l}_??????_{k}.json')) for x in json.load(open(f, encoding='utf-8'))]
for name, l in [('올림픽파크포레온', '11740'), ('헬리오시티', '11710')]:
    R = [x for x in load(l, 'rent') if x['aptNm'] == name and 80 <= float(x['excluUseAr']) <= 85 and n(x['monthlyRent']) == 0]
    R = list({json.dumps(x, sort_keys=True): x for x in R}.values())
    yy = lambda x: int(x['dealYear']) * 100 + int(x['dealMonth'])
    Y = [x for x in R if 202511 <= yy(x) <= 202610]
    print(f'== {name} 전세 {len(Y)}건 · 계약 종류', Counter(x.get('contractType') or '(빈칸)' for x in Y), '· 갱신권 사용', Counter(x.get('useRRRight') or '(빈칸)' for x in Y))
    for t in ['신규', '갱신', '']:
        S = [x for x in Y if (x.get('contractType') or '') == t]
        if not S: continue
        d = [n(x['deposit']) for x in S]
        print(f'  [{t or "빈칸"}] {len(S)}건 가운데 {st.median(d)/1e4:.2f}억 최저 {min(d)/1e4:.2f} 최고 {max(d)/1e4:.2f}')
        if t == '갱신':
            pre = [(n(x['preDeposit']), n(x['deposit']), x.get('useRRRight'), n(x.get('preMonthlyRent'))) for x in S if n(x['preDeposit']) > 0]
            print(f'    종전 보증금 있는 {len(pre)}건 · 종전 가운데 {st.median([p[0] for p in pre])/1e4:.2f}억 · 올린 비율 가운데 {st.median([(b-a)/a*100 for a,b,_,_ in pre]):.1f}% · 종전 월세 있던 건 {sum(1 for p in pre if p[3]>0)}')
            for u in ['사용', '']:
                P = [(a, b) for a, b, uu, _ in pre if (uu or '') == u]
                if P: print(f'    갱신권 [{u or "빈칸"}] {len(P)}건 올린 비율 가운데 {st.median([(b-a)/a*100 for a,b in P]):.1f}% · 5% 넘게 올린 건 {sum(1 for a,b in P if (b-a)/a>0.0501)} · 새 보증금 가운데 {st.median([b for a,b in P])/1e4:.2f}억')
    # 월별 신규/갱신
    m = defaultdict(lambda: [[], []])
    for x in Y: m[yy(x)][0 if x.get('contractType') == '신규' else 1].append(n(x['deposit']))
    print('  월별 신규(건)/갱신(건):', ' '.join(f"{k%100}월 {st.median(v[0])/1e4 if v[0] else 0:.1f}({len(v[0])})/{st.median(v[1])/1e4 if v[1] else 0:.1f}({len(v[1])})" for k, v in sorted(m.items())))
    # 신규 최근 6개월
    S6 = [n(x['deposit']) for x in Y if x.get('contractType') == '신규' and yy(x) >= 202605]
    if S6: print(f'  신규 2026-05~10: {len(S6)}건 가운데 {st.median(S6)/1e4:.2f}억')
    S6 = [n(x['deposit']) for x in Y if x.get('contractType') == '갱신' and yy(x) >= 202605]
    if S6: print(f'  갱신 2026-05~10: {len(S6)}건 가운데 {st.median(S6)/1e4:.2f}억')
    # 매매 최근 1년
    T = [n(x['dealAmount']) for x in load(l, 'trade') if x['aptNm'] == name and 80 <= float(x['excluUseAr']) <= 85 and not (x.get('cdealType') or '').strip() and 202511 <= int(x['dealYear'])*100+int(x['dealMonth']) <= 202610]
    print(f'  매매 {len(T)}건 가운데 {st.median(T)/1e4:.2f}억')
