# H-3 '우리만' 계산 2(2026-10-17 자료조사 담당) — calc.py와 같은 재료·같은 거르기, 새 숫자만 여기서.
# 실행: py -3.12 work/research/longform/ep/H-3/calc2.py > work/research/longform/ep/H-3/calc2_out.txt
# 재료: raw/rt(국토교통부 아파트 매매·전월세 실거래, 2026-10-16 12:4x 받음 — calc.py와 같은 파일)
#       세대수: 국토교통부 건축HUB 건축물대장 총괄표제부(apis.building, 공공데이터포털 1613000/BldRgstHubService, 2026-10-17 조회) → raw/bld_1017.json
import json, os, sys, glob, re, statistics as st, collections
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(HERE, 'raw', 'rt')
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..', '..', '..')))
PY = 3.305785
def num(s): return float(str(s or '0').replace(',', '') or 0)
def eok(m): return f'{m/10000:.2f}억'
def med(v): return st.median(v) if v else 0
def load(lawd, kind):
    out = []
    for p in sorted(glob.glob(os.path.join(RT, f'{lawd}_*_{kind}.json'))): out += [r for r in json.load(open(p, encoding='utf-8')) if isinstance(r, dict) and 'aptNm' in r]
    return out
def ok(r): return not r.get('cdealType') and r.get('buyerGbn') != '공공기관'
def ar(r): return num(r['excluUseAr'])
def pp(r): return num(r['dealAmount']) / ar(r) * PY
def ymk(r): return int(r['dealYear']) * 100 + int(r['dealMonth'])
DONG = [('11680', '압구정동'), ('11710', '신천동'), ('11470', '목동'), ('11470', '신정동')]
T = {u: [r for r in load(l, 'trade') if r['umdNm'] == u and ok(r)] for l, u in DONG}
R = {u: [r for r in load(l, 'rent') if r['umdNm'] == u] for l, u in DONG}
print('# H-3 calc2_out — 단위 만원·㎡(전용). 매매는 해제·공공기관 매수 제외. 계약 2025.11~2026.10\n')

# §1 세대수와 1년 동안 팔린 비율(회전율) — 지번(본번·부번)마다 건축물대장 총괄표제부 세대수
BF = os.path.join(HERE, 'raw', 'bld_1017.json')
cache = json.load(open(BF, encoding='utf-8')) if os.path.exists(BF) else {}
import apis
lots = collections.defaultdict(lambda: {'names': collections.Counter(), 'n': 0})
for u, rs in T.items():
    for r in rs:
        k = f"{r['sggCd']}-{r['umdCd']}-{r['bonbun']}-{r['bubun']}"
        lots[k]['names'][r['aptNm']] += 1; lots[k]['n'] += 1; lots[k]['umd'] = u
big = {k: v for k, v in lots.items() if v['n'] >= 8}
for k in big:
    if k not in cache:
        s, b, bon, bu = k.split('-'); cache[k] = apis.building(s, b, bon, bu)
json.dump(cache, open(BF, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('## 1. 1년 매매 8건 이상 지번 — 세대수(건축물대장 총괄표제부)와 1년 매매 ÷ 세대수')
rows = []
for k, v in big.items():
    b = cache.get(k) or {}
    hh = b.get('세대수') or 0
    rows.append((v['umd'], ' / '.join(n for n, _ in v['names'].most_common(3)), v['n'], hh, b.get('준공', ''), b.get('단지') or '', k))
for umd in ['압구정동', '신천동', '목동', '신정동']:
    sub = sorted([x for x in rows if x[0] == umd], key=lambda x: -x[2])
    for x in sub:
        rate = f'{x[2]/x[3]*100:.1f}%' if x[3] else '세대수 없음'
        print(f'- {x[0]} {x[1]} · 지번 {x[6]} · 대장 {x[5]} 준공 {x[4]} · 세대 {x[3]:,} · 1년 매매 {x[2]}건 → {rate}')
    hh = sum(x[3] for x in sub if x[3]); n = sum(x[2] for x in sub if x[3])
    if hh: print(f'  ▶ {umd} 위 단지 합: 세대 {hh:,} · 매매 {n}건 → 백 집에 {n/hh*100:.1f}집')

# §2 같은 집, 앞 6개월(2025.11~2026.04) vs 뒤 6개월(2026.05~10) 매매 중앙 — 거래 많은 대표 면적
print('\n## 2. 같은 단지 같은 면적 — 앞 6개월(2025.11~2026.04) vs 뒤 6개월(2026.05~10) 매매 중앙')
PICK = [('신천동', '파크리오', 84, 85.5), ('신천동', '장미2', 81, 83), ('목동', '목동신시가지7', 66, 68), ('목동', '목동신시가지3', 64, 66),
        ('신정동', '목동신시가지11', 65, 67), ('압구정동', '한양1차(영동한양)', 49, 51), ('압구정동', '신현대12차', 107, 113)]
for umd, nm, lo, hi in PICK:
    rs = [r for r in T[umd] if r['aptNm'] == nm and lo <= ar(r) < hi]
    a = [num(r['dealAmount']) for r in rs if ymk(r) <= 202604]; b = [num(r['dealAmount']) for r in rs if ymk(r) >= 202605]
    if a and b: print(f'- {umd} {nm} {lo}~{hi}㎡: 앞 {len(a)}건 {eok(med(a))} → 뒤 {len(b)}건 {eok(med(b))} ({med(b)/med(a)*100-100:+.1f}%)')
    else: print(f'- {umd} {nm} {lo}~{hi}㎡: 앞 {len(a)}건 · 뒤 {len(b)}건 (한쪽 없음)')

# §3 전세 — 같은 집 신규 전세(보증금만, 월세 0, 계약구분 '신규') 중앙과 매매 중앙의 비율
print('\n## 3. 같은 집 전세(월세 0, 계약구분 신규) 보증금 중앙 vs 매매 중앙')
for umd, nm, lo, hi in PICK:
    rr = [r for r in R[umd] if r['aptNm'] == nm and lo <= ar(r) < hi and num(r['monthlyRent']) == 0]
    new = [num(r['deposit']) for r in rr if r.get('contractType') == '신규']; ren = [num(r['deposit']) for r in rr if r.get('contractType') == '갱신']
    ss = [num(r['dealAmount']) for r in T[umd] if r['aptNm'] == nm and lo <= ar(r) < hi]
    if new and ss: print(f'- {umd} {nm} {lo}~{hi}㎡: 신규 전세 {len(new)}건 중앙 {eok(med(new))} · 갱신 {len(ren)}건 {eok(med(ren)) if ren else "-"} · 매매 {len(ss)}건 {eok(med(ss))} → 신규 전세 ÷ 매매 {med(new)/med(ss)*100:.0f}% · 차액 {eok(med(ss)-med(new))}')
    else: print(f'- {umd} {nm}: 신규 전세 {len(new)}건 · 매매 {len(ss)}건')

# §4 직거래 비율 — 동네별
print('\n## 4. 동네별 직거래(중개사 없이) 비율')
for u, rs in T.items():
    d = sum(1 for r in rs if r.get('dealingGbn') == '직거래'); print(f'- {u}: {d}/{len(rs)}건 = {d/len(rs)*100:.1f}%')

# §5 실제 질문에 답 — 댓글·자동완성에서 나온 단지·크기
print('\n## 5. 질문 답')
q12 = [r for r in T['신정동'] if r['aptNm'] == '목동신시가지12']
print(f"- Q 목동 12단지 '지금 20억 정도'(4O6trzyjalI 댓글): 1년 {len(q12)}건 · 매매 중앙 {eok(med([num(r['dealAmount']) for r in q12]))} · 면적별 " +
      ', '.join(f"{a}㎡ {len(v)}건 {eok(med(v))}" for a, v in sorted(collections.defaultdict(list, {a: [num(r['dealAmount']) for r in q12 if round(ar(r)) == a] for a in {round(ar(r)) for r in q12}}).items())))
big2 = [r for r in T['압구정동'] if r['aptNm'].startswith('현대1차') or r['aptNm'].startswith('현대2차')]
for a in sorted({round(ar(r)) for r in big2}):
    v = sorted(num(r['dealAmount']) for r in big2 if round(ar(r)) == a)
    print(f"- Q 압구정 현대 1·2차 '65평 130억?'(dCxvZ_P7fNk 댓글): 전용 {a}㎡ {len(v)}건 · " + ', '.join(eok(x) for x in v))
top = max(T['압구정동'], key=lambda r: num(r['dealAmount']))
print(f"  · 압구정동 1년 최고가: {top['aptNm']} {ar(top):.2f}㎡ {eok(num(top['dealAmount']))} {top['dealYear']}.{top['dealMonth']}")
p35 = [num(r['dealAmount']) for r in T['신천동'] if r['aptNm'] == '파크리오' and ar(r) < 40]
print(f"- Q '파크리오 16평'(네이버 자동완성): 전용 35㎡대 {len(p35)}건 · 중앙 {eok(med(p35))} · 최저 {eok(min(p35))} · 최고 {eok(max(p35))}")
for B, lab in [(200000, '20억')]:
    for u in ['압구정동', '신천동', '목동', '신정동']:
        m = [r for r in T[u] if B * 0.9 <= num(r['dealAmount']) <= B * 1.1]
        top2 = collections.Counter(r['aptNm'] for r in m).most_common(3)
        print(f"- Q '총투자금 20억'(QO-6aWpqVm4 댓글) {u} 동 전체 18~22억: {len(m)}건 · 전용 중앙 {med([ar(r) for r in m]):.0f}㎡ · " + ', '.join(f'{n} {c}' for n, c in top2))

# §6 목동신시가지 1~14 합 — 세대(건축물대장) vs 1년 매매 · 압구정 현대·신현대(번호 붙은 '현대') 합
print('\n## 6. 목동신시가지 1~14단지 합 · 압구정 현대·신현대 합(§1 지번 8건 이상만, 장미는 대장 세대수가 단지 전체와 안 맞아 뺌)')
def lotsum(pred):
    hh = n = 0
    for k, v in big.items():
        nm = v['names'].most_common(1)[0][0]; b = cache.get(k) or {}
        if pred(v['umd'], nm) and b.get('세대수'): hh += b['세대수']; n += v['n']
    return hh, n
for lab, pred in [('목동 쪽 1~7단지', lambda u, nm: '목동신시가지' in nm and u == '목동'), ('신정동 쪽 8~14단지', lambda u, nm: '목동신시가지' in nm and u == '신정동'),
                  ('목동신시가지 1~14 전체', lambda u, nm: '목동신시가지' in nm), ('압구정 현대·신현대(8건 이상 지번)', lambda u, nm: u == '압구정동' and '현대' in nm),
                  ('파크리오', lambda u, nm: nm == '파크리오')]:
    hh, n = lotsum(pred); print(f'- {lab}: 세대 {hh:,} · 1년 매매 {n}건 → 백 집에 {n/hh*100:.1f}집 · 세대당 한 번 팔리는 데 걸릴 햇수(단순 역수) {hh/n:.0f}년')

# §7 해제(계약 뒤 취소 신고) — 동네별 비율. calc §0의 해제 건수를 비율로
print('\n## 7. 해제 신고 비율(계약했다가 취소 신고된 거래) — 신고가 뉴스가 나중에 사라질 수 있는 몫')
for l, u in DONG:
    allr = [r for r in load(l, 'trade') if r['umdNm'] == u]
    cx = [r for r in allr if r.get('cdealType')]
    print(f'- {u}: 해제 {len(cx)}/{len(allr)}건 = {len(cx)/len(allr)*100:.1f}% · 해제된 거래 중 그 동네 1년 최고가보다 비쌌던 것 {sum(1 for r in cx if num(r["dealAmount"]) > max(num(x["dealAmount"]) for x in T[u]))}건')
