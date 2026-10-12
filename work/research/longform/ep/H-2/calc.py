# H-2 계산 재현 — 숫자는 전부 여기서 나온다(대본·카페·쇼츠 공통). 실행: py -3.12 work/research/longform/ep/H-2/calc.py > calc_out.txt
# 재료: work/research/rt/<구코드>_<월>_{trade,rent}.json = 국토교통부 아파트 매매·전월세 실거래(공공데이터포털 1613000, rtmolit.py)
#       raw/tour_{daechi,jamsil}.json = work/research/sonpum2/tour.py 출력(2026-10-12, 걸어서 거리·입주·세대수)
#       반포는 Overpass 4회 실패(10/12 밤 3서버·10/13 08:5x 2서버)라 tour 없음 → 걷는 거리·세대수 '확인 안 함'
# 네이버 부동산 등 민간 화면·매물·경매 자료는 쓰지 않는다. 단지명은 국토부 aptNm 그대로(공백 뺌).
import json, os, sys, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(HERE, '..', '..', '..', 'rt')
PY = 3.305785
MS = ['202511', '202512', '202601', '202602', '202603', '202604', '202605', '202606', '202607', '202608', '202609', '202610']
DONG = [('11680', '대치동', 'daechi'), ('11710', '잠실동', 'jamsil'), ('11650', '반포동', None)]
def num(s): return float(str(s or '0').replace(',', '') or 0)
def eok(m): return f'{m/10000:.2f}억'
def load_rt(lawd, kind):
    out, miss = [], []
    for m in MS:
        p = os.path.join(RT, f'{lawd}_{m}_{kind}.json')
        if not os.path.exists(p): miss.append(m); continue
        d = json.load(open(p, encoding='utf-8'))
        out += [r for r in d if isinstance(r, dict) and 'aptNm' in r] if isinstance(d, list) else []
    return out, miss
def ok(r, umd): return r['umdNm'] == umd and not r.get('cdealType') and r.get('buyerGbn') != '공공기관'
def is84(r): return 80 <= num(r['excluUseAr']) < 85
def nm(r): return r['aptNm'].replace(' ', '')
def ym(r): return f"{r['dealYear']}.{str(r['dealMonth']).zfill(2)}"

print('# H-2 calc_out — 단위 만원(금액), 평당 = 전용면적 기준 3.305785㎡. 매매는 해제·공공기관 매수 제외, 84㎡대 = 전용 80~85㎡\n')
DATA = {}
for lawd, umd, tk in DONG:
    T, mt = load_rt(lawd, 'trade'); R, mr = load_rt(lawd, 'rent')
    T = [r for r in T if ok(r, umd)]; R = [r for r in R if r['umdNm'] == umd]
    DATA[umd] = (T, R)
    yms = sorted({ym(r) for r in T})
    print(f'## {umd}: 매매 {len(T)}건(모든 면적) · 84㎡대 {sum(map(is84, T))}건 · 계약월 {yms[0] if yms else "-"}~{yms[-1] if yms else "-"} · 없는 월 파일 trade {mt or "없음"} rent {mr or "없음"}')

print('\n## 1. 84㎡대 단지별(거래 3건 이상) — 매매 중앙·평당 중앙·최저·최고·직거래·신규 순수전세 중앙·전세가율')
B = {}
for lawd, umd, tk in DONG:
    T, R = DATA[umd]
    g = collections.defaultdict(list)
    for r in T:
        if is84(r): g[nm(r)].append(r)
    print(f'### {umd}')
    for apt, rows in sorted(g.items(), key=lambda kv: -len(kv[1])):
        if len(rows) < 3: continue
        amts = [num(r['dealAmount']) for r in rows]; med = st.median(amts)
        ppy = st.median(num(r['dealAmount']) / (num(r['excluUseAr']) / PY) for r in rows)
        js = [num(r['deposit']) for r in R if nm(r) == apt and is84(r) and r.get('contractType') == '신규' and num(r['monthlyRent']) == 0]
        jm = st.median(js) if len(js) >= 3 else None
        built = rows[0].get('buildYear', '?')
        direct = sum(r.get('dealingGbn') == '직거래' for r in rows)
        B[(umd, apt)] = dict(n=len(rows), med=med, ppy=ppy, built=built, jm=jm, rows=rows)
        print(f"- {apt}(건축 {built}) {len(rows)}건 중앙 {eok(med)} · 평당 {ppy:,.0f}만원 · 최저 {eok(min(amts))} 최고 {eok(max(amts))} · 직거래 {direct} · 순수전세 {len(js)}건 {eok(jm) if jm else '-'}" + (f' · 전세가율 {jm/med*100:.1f}%' if jm else ''))

print('\n## 2. 같은 동네 오래된 단지 vs 새 단지(84㎡대 평당 중앙) — 건축 1990 이전을 오래된 단지로')
for umd in ('대치동', '잠실동', '반포동'):
    items = [(a, v) for (u, a), v in B.items() if u == umd and v['n'] >= 5]
    old = [(a, v) for a, v in items if str(v['built']).isdigit() and int(v['built']) < 1990]
    new = [(a, v) for a, v in items if str(v['built']).isdigit() and int(v['built']) >= 2000]
    for a, v in old:
        for b, w in new:
            print(f"- {umd}: {a}({v['built']}) {v['ppy']:,.0f} vs {b}({w['built']}) {w['ppy']:,.0f} → 오래된 쪽이 {(v['ppy']/w['ppy']-1)*100:+.1f}% · 84㎡ 중앙 {eok(v['med'])} vs {eok(w['med'])}")
    if not old: print(f'- {umd}: 5건 이상 오래된 단지 없음')

print('\n## 3. 대표 단지 달별 중앙(84㎡대)')
for (umd, apt), v in sorted(B.items(), key=lambda kv: -kv[1]['n'])[:9]:
    bym = collections.defaultdict(list)
    for r in v['rows']: bym[ym(r)].append(num(r['dealAmount']))
    print(f"- {apt}({umd}): " + ' · '.join(f"{k} {eok(st.median(x))}({len(x)})" for k, x in sorted(bym.items())))

print('\n## 4. 같은 단지 같은 달 최고-최저(84㎡대, 그 달 3건 이상) — 상위 6')
gaps = []
for (umd, apt), v in B.items():
    bym = collections.defaultdict(list)
    for r in v['rows']: bym[ym(r)].append(r)
    for k, rs in bym.items():
        if len(rs) >= 3:
            rs.sort(key=lambda r: num(r['dealAmount']))
            gaps.append((num(rs[-1]['dealAmount']) - num(rs[0]['dealAmount']), apt, k, rs))
for gap, apt, k, rs in sorted(gaps, key=lambda x: -x[0])[:6]:
    print(f"- {apt} {k} {len(rs)}건 차이 {eok(gap)}: " + ' / '.join(f"{r['dealDay']}일 {eok(num(r['dealAmount']))} {r['floor']}층 {r.get('dealingGbn','')}" for r in rs))

print('\n## 5. 걸어서 거리(tour.py, OSM 보행로) — 대치·잠실만')
for k in ('daechi', 'jamsil'):
    d = json.load(open(os.path.join(HERE, 'raw', f'tour_{k}.json'), encoding='utf-8'))
    for c in sorted(d['complexes'], key=lambda c: -(c.get('nTop') or 0))[:6]:
        w = c['walk']; kp = c.get('kapt') or {}
        f = lambda x: f"{x['name']} {x['m']}m" if x else '-'
        print(f"- {c['name']}({d['umd']}) 입주 {kp.get('use') or c.get('built')} · {kp.get('hh') or '?'}세대 · 역 {f(w.get('station'))} · 초등 {f(w.get('school'))} · 마트 {f(w.get('mart'))}")
print('- 반포동: 확인 안 함(Overpass 막힘)')

print('\n## 6. 사는 값과 빌려 사는 값(84㎡대 매매 중앙 − 신규 순수전세 중앙) — 오래된 단지 vs 새 단지')
for umd, a, b in [('잠실동', '주공아파트5단지', '리센츠'), ('잠실동', '주공아파트5단지', '잠실엘스'), ('대치동', '은마', '래미안대치팰리스'), ('반포동', '반포미도', '래미안원베일리')]:
    v, w = B.get((umd, a)), B.get((umd, b))
    if not v or not w or not v['jm'] or not w['jm']: print(f'- {umd} {a}/{b}: 자료 부족'); continue
    print(f"- {umd}: {a} 매매 {eok(v['med'])} 전세 {eok(v['jm'])} 차이 {eok(v['med']-v['jm'])}(전세가율 {v['jm']/v['med']*100:.1f}%) vs {b} 매매 {eok(w['med'])} 전세 {eok(w['jm'])} 차이 {eok(w['med']-w['jm'])}({w['jm']/w['med']*100:.1f}%)")
