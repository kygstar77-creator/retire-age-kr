# H-2 '우리만' 계산(2026-10-17 자료조사 담당) — calc.py와 같은 재료·같은 거르기, 새 숫자만 여기서.
# 실행: py -3.12 work/research/longform/ep/H-2/calc2.py > work/research/longform/ep/H-2/calc2_out.txt
# 재료: work/research/rt/<구코드>_<월>_{trade,rent}.json(국토교통부 아파트 매매·전월세 실거래, rtmolit.py) · raw/tour_*.json(OSM 보행로, tour.py)
# 기준 하나: 대본 본값은 calc_out(2026-10-12 받음). 여기 ①~④는 2026-10-16 23:18 재수신 파일까지 읽는다(잠실 10월 2건 늘어남 — §0에 차이 표시).
import json, os, sys, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(HERE, '..', '..', '..', 'rt')
PY = 3.305785
Y1 = ['202511', '202512', '202601', '202602', '202603', '202604', '202605', '202606', '202607', '202608', '202609', '202610']
DONG = [('11680', '대치동'), ('11710', '잠실동'), ('11650', '반포동')]
FOCUS = {'잠실동': ['주공아파트5단지', '리센츠', '잠실엘스', '트리지움', '우성아파트'],
         '대치동': ['은마', '래미안대치팰리스', '대치르엘', '한보미도맨션1'],
         '반포동': ['래미안원베일리', '아크로리버파크', '래미안퍼스티지', '반포자이', '반포미도']}
def num(s): return float(str(s or '0').replace(',', '') or 0)
def eok(m): return f'{m/10000:.2f}억'
def load(lawd, kind, months):
    out = []
    for m in months:
        p = os.path.join(RT, f'{lawd}_{m}_{kind}.json')
        if os.path.exists(p):
            d = json.load(open(p, encoding='utf-8')); out += [r for r in d if isinstance(r, dict) and 'aptNm' in r]
    return out
def nm(r): return r['aptNm'].replace(' ', '')
def is84(r): return 80 <= num(r['excluUseAr']) < 85
def okT(r, umd): return r['umdNm'] == umd and not r.get('cdealType') and r.get('buyerGbn') != '공공기관' and is84(r)
def pure(r): return num(r['monthlyRent']) == 0
def med(x): return st.median(x) if x else None

print('# H-2 calc2_out — 우리만 숫자. 단위 만원, 84㎡대 = 전용 80~85㎡, 매매는 해제·공공기관 매수 제외\n')
T = {u: [r for r in load(l, 'trade', Y1) if okT(r, u)] for l, u in DONG}
R = {u: [r for r in load(l, 'rent', Y1) if r['umdNm'] == u and is84(r)] for l, u in DONG}

print('## 0. 재수신 차이(2026-10-16 파일 기준 84㎡대 매매 건수) — 대본 본값은 calc_out(10/12)')
for u in T: print(f'- {u} 84㎡대 매매 {len(T[u])}건')

print('\n## 1. 같은 단지 같은 84㎡대, 낮은 층(1~3층) vs 그 위 층 — 매매 중앙(1년)')
for u, apts in FOCUS.items():
    for a in apts:
        rs = [r for r in T[u] if nm(r) == a]
        lo = [num(r['dealAmount']) for r in rs if int(r['floor']) <= 3]
        hi = [num(r['dealAmount']) for r in rs if int(r['floor']) >= 4]
        top = sorted(rs, key=lambda r: -int(r['floor']))
        if len(lo) >= 3 and len(hi) >= 3:
            print(f"- {u} {a}: 1~3층 {len(lo)}건 중앙 {eok(med(lo))} · 4층 이상 {len(hi)}건 중앙 {eok(med(hi))} · 차이 {eok(med(hi)-med(lo))}({(med(lo)/med(hi)-1)*100:+.1f}%) · 최고층 거래 {top[0]['floor']}층")
        else:
            print(f"- {u} {a}: 1~3층 {len(lo)}건 · 4층 이상 {len(hi)}건 — 3건 미만이라 비교 안 함")

print('\n## 2. 보증금 9.50억(손품 씨, H-1 calc_out 8) 안에 든 신규 순수전세 비율(84㎡대, 1년)')
for u, apts in FOCUS.items():
    for a in apts:
        js = [num(r['deposit']) for r in R[u] if nm(r) == a and r.get('contractType') == '신규' and pure(r)]
        if js:
            k = sum(x <= 95000 for x in js)
            print(f"- {u} {a}: 신규 순수전세 {len(js)}건 중 9.50억 이하 {k}건({k/len(js)*100:.0f}%) · 최저 {eok(min(js))} 최고 {eok(max(js))}")
        else: print(f'- {u} {a}: 신규 순수전세 0건')

print('\n## 3. 신규 vs 갱신 순수전세(84㎡대, 1년) — 갱신은 같은 세입자가 다시 계약한 것, 계약갱신요구권 사용 여부 칸 포함')
for u, apts in FOCUS.items():
    for a in apts:
        rs = [r for r in R[u] if nm(r) == a and pure(r)]
        new = [num(r['deposit']) for r in rs if r.get('contractType') == '신규']
        ren = [r for r in rs if r.get('contractType') == '갱신']
        rv = [num(r['deposit']) for r in ren]; used = sum(r.get('useRRRight') == '사용' for r in ren)
        pre = [num(r['deposit']) - num(r['preDeposit']) for r in ren if num(r.get('preDeposit')) > 0]
        if len(new) >= 3 and len(rv) >= 3:
            print(f"- {u} {a}: 신규 {len(new)}건 중앙 {eok(med(new))} · 갱신 {len(rv)}건 중앙 {eok(med(rv))} · 갱신이 {eok(med(new)-med(rv))} 낮음 · 갱신요구권 사용 {used}/{len(rv)} · 갱신 때 올린 보증금 중앙 {eok(med(pre)) if pre else '-'}({len(pre)}건)")
        else: print(f'- {u} {a}: 신규 {len(new)} · 갱신 {len(rv)} — 3건 미만')

print('\n## 4. 같은 석 달(7~9월 계약) 견줌 — 2024 · 2025 · 2026, 84㎡대 매매 중앙·신규 순수전세 중앙')
Q = {'2024': ['202407', '202408', '202409'], '2025': ['202507', '202508', '202509'], '2026': ['202607', '202608', '202609']}
for l, u in DONG:
    TQ = {y: [r for r in load(l, 'trade', ms) if okT(r, u)] for y, ms in Q.items()}
    RQ = {y: [r for r in load(l, 'rent', ms) if r['umdNm'] == u and is84(r) and r.get('contractType') == '신규' and pure(r)] for y, ms in Q.items()}
    for a in FOCUS[u]:
        cells = []
        for y in Q:
            t = [num(r['dealAmount']) for r in TQ[y] if nm(r) == a]; j = [num(r['deposit']) for r in RQ[y] if nm(r) == a]
            cells.append((y, t, j))
        s = ' · '.join(f"{y} 매매 {eok(med(t)) if t else '-'}({len(t)}) 전세 {eok(med(j)) if j else '-'}({len(j)})" for y, t, j in cells)
        (_, t25, j25), (_, t26, j26) = cells[1], cells[2]
        ch = ''
        if len(t25) >= 3 and len(t26) >= 3: ch += f' → 매매 {(med(t26)/med(t25)-1)*100:+.1f}%'
        if len(j25) >= 3 and len(j26) >= 3: ch += f' · 전세 {(med(j26)/med(j25)-1)*100:+.1f}%'
        print(f'- {u} {a}: {s}{ch}')

print('\n## 5. 걸어서 거리(OSM 보행로, 단지 가운데 → 지하철 출입구) — 반포는 2026-10-17 00시 재시도로 처음 받음(raw/tour_banpo.json)')
for k in ('daechi', 'jamsil', 'banpo'):
    d = json.load(open(os.path.join(HERE, 'raw', f'tour_{k}.json'), encoding='utf-8'))
    for c in sorted(d['complexes'], key=lambda c: -(c.get('nTop') or 0))[:8]:
        w = c['walk']; kp = c.get('kapt') or {}
        f = lambda x: f"{x['name']} {x['m']}m" if x else '-'
        print(f"- {c['name']}({d['umd']}) 입주 {kp.get('use') or c.get('built')} · {kp.get('hh') or '?'}세대 · 역 {f(w.get('station'))} · 초등 {f(w.get('school'))}")

print('\n## 6. 갱신 순수전세에서 보증금을 얼마나 올렸나(이전 보증금 칸이 있는 것만) — 5% 이하 비율')
for u, apts in FOCUS.items():
    for a in apts:
        ren = [r for r in R[u] if nm(r) == a and pure(r) and r.get('contractType') == '갱신' and num(r.get('preDeposit')) > 0]
        if len(ren) < 5: continue
        rate = [(num(r['deposit']) / num(r['preDeposit']) - 1) * 100 for r in ren]
        le5 = sum(x <= 5.0001 for x in rate); same = sum(abs(x) < 0.01 for x in rate); down = sum(x < -0.01 for x in rate)
        used = [x for r, x in zip(ren, rate) if r.get('useRRRight') == '사용']
        print(f"- {u} {a}: 갱신 {len(ren)}건 · 5% 이하로 올림(동결·내림 포함) {le5}건({le5/len(ren)*100:.0f}%) · 그대로 {same} · 내림 {down} · 갱신요구권 쓴 {len(used)}건 중 5% 이하 {sum(x <= 5.0001 for x in used)}건")
tot = over = 0
for u, apts in FOCUS.items():
    for a in apts:
        for r in R[u]:
            if nm(r) == a and pure(r) and r.get('contractType') == '갱신' and r.get('useRRRight') == '사용' and num(r.get('preDeposit')) > 0:
                tot += 1; over += (num(r['deposit']) / num(r['preDeposit']) - 1) * 100 > 5.0001
print(f'- 합계: 갱신요구권 사용 갱신 순수전세 {tot}건(14단지) 중 5% 넘게 오른 계약 {over}건')

print('\n## 7. 84㎡대 안에서도 전용면적이 다르다(한 채 값 차이 < 평당 차이인 까닭) — 매매 전용면적 가운데 값')
for u, apts in FOCUS.items():
    for a in apts:
        ar = [num(r['excluUseAr']) for r in T[u] if nm(r) == a]
        if ar: print(f'- {u} {a}: {len(ar)}건 전용 가운데 {med(ar):.2f}㎡ (최소 {min(ar):.2f} 최대 {max(ar):.2f})')
