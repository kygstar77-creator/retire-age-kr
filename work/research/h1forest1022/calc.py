# 2026-10-22 write-b: 입주 첫해 전세 — 헬리오시티(2018.12 입주) vs 올림픽파크포레온(2024.11 입주)
# 84㎡대 = 전용 80~85㎡, 전세 = 월세 0원, 매매는 해제 건 뺌. 가운데 값(중앙값).
import json, glob, os, statistics as st, sys
sys.stdout.reconfigure(encoding='utf-8')
def load(pat):
    out = []
    for f in sorted(set(glob.glob(pat))):
        out += json.load(open(f, encoding='utf-8'))
    return out
def n(s): return int((s or '0').replace(',', '') or 0)
def is84(x): return 80 <= float(x['excluUseAr']) <= 85
def ym(x): return int(x['dealYear']) * 100 + int(x['dealMonth'])
def rows(name, lawd, pats):
    R = [x for p in pats for x in load(p.format(l=lawd)) if x['aptNm'] == name and is84(x)]
    return R
res = {}
for name, lawd, rent_p, trade_p, movein in [
    ('헬리오시티', '11710', ['raw/{l}_??????_rent.json'], ['raw/{l}_??????_trade.json'], 201812),
    ('올림픽파크포레온', '11740', ['raw/{l}_*_rent.json'], ['raw/{l}_*_trade.json'], 202411)]:
    rent = rows(name, lawd, rent_p); trade = [x for x in rows(name, lawd, trade_p) if not (x.get('cdealType') or '').strip()]
    # 중복 제거(같은 파일 두 번 방지)
    rent = list({json.dumps(x, sort_keys=True): x for x in rent}.values()); trade = list({json.dumps(x, sort_keys=True): x for x in trade}.values())
    jeon = [x for x in rent if n(x['monthlyRent']) == 0]
    print(f'== {name} 84㎡대 전세 {len(jeon)}건 · 매매 {len(trade)}건')
    def mi(a, b):  # 입주 달 기준 a~b번째 달(0=입주 달)
        y0, m0 = divmod(movein, 100)
        def idx(v): y, m = divmod(v, 100); return (y - y0) * 12 + (m - m0)
        J = [n(x['deposit']) for x in jeon if a <= idx(ym(x)) <= b]
        T = [n(x['dealAmount']) for x in trade if a <= idx(ym(x)) <= b]
        J2 = [n(x['deposit']) for x in jeon if a <= idx(ym(x)) <= b and x.get('contractType') == '신규']
        return J, T, J2
    for lab, a, b in [('입주 0~5달', 0, 5), ('입주 6~11달', 6, 11), ('입주 12~17달', 12, 17), ('입주 18~23달', 18, 23)]:
        J, T, J2 = mi(a, b)
        if not J: print(lab, '전세 0건'); continue
        mj = st.median(J); mt = st.median(T) if T else None
        print(f'{lab}: 전세 {len(J)}건 가운데 {mj/1e4:.2f}억 (최저 {min(J)/1e4:.2f} 최고 {max(J)/1e4:.2f}) · 신규만 {len(J2)}건 {st.median(J2)/1e4 if J2 else 0:.2f}억 · 매매 {len(T)}건 가운데 {mt/1e4 if mt else 0:.2f}억 · 전세/매매 {mj/mt*100 if mt else 0:.1f}%')
    # 최근 1년(2025-11~2026-10)
    J = [n(x['deposit']) for x in jeon if 202511 <= ym(x) <= 202610]; T = [n(x['dealAmount']) for x in trade if 202511 <= ym(x) <= 202610]
    if J: print(f'최근 1년 2025.11~2026.10: 전세 {len(J)}건 가운데 {st.median(J)/1e4:.2f}억 · 매매 {len(T)}건 가운데 {st.median(T)/1e4 if T else 0:.2f}억 · {st.median(J)/st.median(T)*100 if T else 0:.1f}%')
    # 월별 전세 가운데
    from collections import defaultdict
    d = defaultdict(list)
    for x in jeon: d[ym(x)].append(n(x['deposit']))
    print('월별 전세 가운데:', ' '.join(f'{k}:{st.median(v)/1e4:.1f}({len(v)})' for k, v in sorted(d.items())))
    res[name] = 1
