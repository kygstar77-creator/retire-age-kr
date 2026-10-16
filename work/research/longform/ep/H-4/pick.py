# H-4 동네 고르기 — 후보 동네별 1년·최근 3개월 매매 건수, 대표 단지 거래 수(검색수 큰 단지가 실거래에 얼마나 잡히나)
#   py -3.12 work/research/longform/ep/H-4/pick.py > pick_out.txt
import json, os, sys, glob, collections, statistics as st
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(HERE, 'raw', 'rt')
def num(s): return float(str(s or '0').replace(',', '') or 0)
def load(lawd, kind):
    out = []
    for p in sorted(glob.glob(os.path.join(RT, f'{lawd}_*_{kind}.json'))): out += json.load(open(p, encoding='utf-8'))
    return out
def ok(r): return not r.get('cdealType') and r.get('buyerGbn') != '공공기관'
print('# H-4 pick_out — 국토부 아파트 매매 실거래, 계약월 2025.11~2026.10, 해제·공공기관 매수 제외. 최근 3개월 = 2026.07~10 계약')
for lawd, umds in [('11440', ['공덕동', '아현동', '염리동', '도화동']), ('41210', ['철산동', '하안동', '광명동']), ('11650', ['방배동']), ('11170', ['한남동', '이촌동', '서빙고동'])]:
    T = [r for r in load(lawd, 'trade') if ok(r)]
    R = load(lawd, 'rent')
    print(f'\n## {lawd}')
    for u in umds:
        t = [r for r in T if r['umdNm'] == u]
        rec = [r for r in t if (int(r['dealYear']), int(r['dealMonth'])) >= (2026, 7)]
        rn = [r for r in R if r['umdNm'] == u and num(r.get('monthlyRent')) == 0]
        print(f'- {u}: 1년 매매 {len(t)}건 · 7~10월 {len(rec)}건 · 순수전세 {len(rn)}건')
        c = collections.Counter(r['aptNm'] for r in t)
        for name, n in c.most_common(8):
            rs = [r for r in t if r['aptNm'] == name]
            a = [num(r['dealAmount']) for r in rs]; ar = [num(r['excluUseAr']) for r in rs]
            print(f'    {name}({rs[0].get("buildYear")}) {n}건 · 매매 중앙 {st.median(a)/10000:.2f}억 · 전용 중앙 {st.median(ar):.1f}㎡')
