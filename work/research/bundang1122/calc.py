# bundang1122 — 경기 성남시 분당구 41135 아파트 매매 실거래(S1 raw)로 분당 네 묶음(판교·서현수내정자·야탑이매분당·구미금곡) 같은 집 2021년 고점 무렵·1년 전 대비 · firemap-write-b 2026-11-20 (gimpo1121/calc.py 틀)
# 같은 집 = 같은 단지(aptSeq)·같은 전용면적(1㎡ 반올림). 매매는 해제(cdealType) 뺌.
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
num = lambda s: float(str(s or '0').replace(',', '') or 0)
def grp(u):
    if u in ('삼평동', '백현동', '판교동', '운중동', '대장동'): return '판교'
    if u in ('서현동', '수내동', '정자동'): return '서현수내정자'
    if u in ('야탑동', '이매동', '분당동'): return '야탑이매분당'
    if u in ('구미동', '금곡동'): return '구미금곡'
    return '기타'
def load(kind):
    out = []
    for p in sorted(glob.glob(os.path.join(H, 'raw', f'41135_*_{kind}.json'))):
        for r in json.load(open(p, encoding='utf-8')):
            r['_g'] = grp(r['umdNm'])
            r['_ym'] = int(r['dealYear']) * 100 + int(r['dealMonth']); r['_a'] = round(num(r['excluUseAr']))
            r['_k'] = (r.get('aptSeq') or r['aptNm'], r['_a']); out.append(r)
    return out
TA = load('trade'); T = [r for r in TA if not r.get('cdealType')]
for r in T: r['_p'] = num(r['dealAmount'])
print('분당구 매매(해제 뺌)', len(T), '건 · 해제', len(TA) - len(T), '건 · 단지', len({r['_k'][0] for r in T}))
print('동네별 매매 건수:', C.Counter(r['_g'] for r in T).most_common())
print('기간 처음·끝:', min(r['_ym'] for r in T), max(r['_ym'] for r in T))
PER = {'1년전': (202506, 202510), '최근': (202606, 202610), '고점21': (202107, 202112), '바닥23': (202301, 202306), '상반21': (202101, 202106)}
def inper(r, k): lo, hi = PER[k]; return lo <= r['_ym'] <= hi
def pairs(rows, a, b):
    d = C.defaultdict(lambda: C.defaultdict(list)); nm = {}
    for r in rows:
        nm[r['_k']] = (r['aptNm'], r['umdNm'])
        for k in (a, b):
            if inper(r, k): d[r['_k']][k].append(r['_p'])
    return [(st.median(v[b]) / st.median(v[a]) - 1, st.median(v[b]) - st.median(v[a]), nm[k], k[1], st.median(v[a]), st.median(v[b]), len(v[a]), len(v[b])) for k, v in d.items() if v[a] and v[b]]
def show(lbl, ps):
    if not ps: print(lbl, '0쌍'); return
    rs = [x[0] for x in ps]; ds = [x[1] for x in ps]
    print(f"{lbl}: {len(ps)}쌍 · 가운데 {st.median(rs)*100:+.1f}% · 가운데 금액 {st.median(ds)/10000:+.2f}억 · 오른 쌍 {sum(1 for x in rs if x>0)/len(rs)*100:.0f}% · 넘은 쌍(>=0) {sum(1 for x in rs if x>=0)}개({sum(1 for x in rs if x>=0)/len(rs)*100:.0f}%)")
GS = ['판교', '서현수내정자', '야탑이매분당', '구미금곡']
for a, b, lab in (('고점21', '최근', '2021년 7~12월 → 2026.6~10 (고점 무렵 대비)'), ('1년전', '최근', '1년(2025.6~10 → 2026.6~10)'), ('바닥23', '최근', '2023년 1~6월 → 2026.6~10'), ('상반21', '최근', '2021년 1~6월 → 2026.6~10'), ('고점21', '바닥23', '2021년 7~12월 → 2023년 1~6월 (얼마나 빠졌나)')):
    print(f'\n# 같은 집 매매 {lab}')
    show('분당 전체', pairs(T, a, b))
    for g in GS: show(g, pairs([r for r in T if r['_g'] == g], a, b))
print('\n# 84㎡ 안팎(83~86㎡) 매매 가운데 값')
for g in GS:
    for per in ('고점21', '바닥23', '1년전', '최근'):
        v = [r['_p'] for r in T if r['_g'] == g and inper(r, per) and 83 <= r['_a'] <= 86]
        print(f'{g} {per}: {len(v)}건 {st.median(v)/10000:.2f}억' if v else f'{g} {per}: 0건')
print('\n# 동네별 같은 집 고점 대비 — 84㎡ 안팎, 양쪽 2건 이상, 높은 둘·낮은 둘')
for g in GS:
    ps = sorted([x for x in pairs([r for r in T if r['_g'] == g and 83 <= r['_a'] <= 86], '고점21', '최근') if x[6] >= 2 and x[7] >= 2], reverse=True)
    for x in ps[:2] + ps[-2:]: print('  ', g, f'{x[0]*100:+.1f}%', x[2][0], x[2][1], f'{x[3]}㎡', f'{x[4]/10000:.2f}억→{x[5]/10000:.2f}억', f'({x[6]}건/{x[7]}건)')
print('\n# 반기별 매매 건수(해제 뺌)')
for y in range(2021, 2027):
    for h, (lo, hi) in (('상', (1, 6)), ('하', (7, 12))):
        v = [r for r in T if r['_ym'] // 100 == y and lo <= r['_ym'] % 100 <= hi]
        if v: print(f'{y}{h}', len(v), ' '.join(f"{g}{sum(1 for r in v if r['_g']==g)}" for g in GS))
for lab, lo, hi in (('2021년 6~10월', 202106, 202110), ('2024년 6~10월', 202406, 202410), ('2025년 6~10월', 202506, 202510), ('2026년 6~10월', 202606, 202610)):
    v = [r for r in T if lo <= r['_ym'] <= hi]; print(f'{lab}: {len(v)}건 · 월평균 {len(v)/5:.0f}')
print('\n# 2026년 11월 계약(최근에서 뺌):', sum(1 for r in T if r['_ym'] == 202611), '건')
print('\n# 동네별 단지·건수(최근 6~10월)')
for g in GS:
    v = [r for r in T if r['_g'] == g and inper(r, '최근')]; print(g, len(v), '건 · 단지', len({r['_k'][0] for r in v}))
print('\n# 확인: 고점 대비 넘은 쌍 목록(분당 전체)')
for x in sorted(pairs(T, '고점21', '최근'), reverse=True):
    if x[0] >= 0: print('  ', f'{x[0]*100:+.1f}%', x[2], f'{x[3]}㎡', x[4], x[5], x[6], x[7])
print('\n# 직거래 몫(최근)', C.Counter(r.get('dealingGbn') for r in T if inper(r, '최근')).most_common())
print('\n# 확인: 2021년 하반기가 고점 무렵인가 — 같은 집 반기 사슬(앞 반기 → 다음 반기 가운데 변화)')
HS = [(f'{y}{h}', (y*100+lo, y*100+hi)) for y in range(2021, 2027) for h, lo, hi in (('상', 1, 6), ('하', 7, 12))]
for (la, pa), (lb, pb) in zip(HS, HS[1:]):
    PER['_a'], PER['_b'] = pa, pb
    ps = pairs(T, '_a', '_b')
    if ps: print(f'{la}→{lb}: {len(ps)}쌍 가운데 {st.median([x[0] for x in ps])*100:+.1f}%')
print('\n# 준공 연도로 나눔(1996년 이전 준공 vs 1997년 이후) — 같은 집 고점21→최근, 1년전→최근')
for lab, f in (('1996년 이전 준공', lambda r: int(r.get('buildYear') or 0) <= 1996), ('1997년 이후 준공', lambda r: int(r.get('buildYear') or 0) >= 1997)):
    v = [r for r in T if f(r)]
    show(lab + ' 고점', pairs(v, '고점21', '최근')); show(lab + ' 1년', pairs(v, '1년전', '최근'))
    print(lab, '최근 거래', sum(1 for r in v if inper(r, '최근')), '건')
print('\n# 묶음별 1996 이전 준공 몫(최근 거래)')
for g in GS:
    v = [r for r in T if r['_g'] == g and inper(r, '최근')]
    if v: print(g, f"{sum(1 for r in v if int(r.get('buildYear') or 0) <= 1996)/len(v)*100:.0f}%", len(v))
print('\n# 재건축 선도지구(2024-11-27 국토부 발표 — 샛별마을 동성 등·양지마을 금호 등·시범단지 우성 등, 단지 구성은 뉴시스·헤럴드 2차) vs 나머지 1996년 이전 준공')
SD = {'샛별마을(동성)', '샛별마을(라이프)', '샛별마을(삼부)', '샛별마을(우방)',
      '양지마을(금호1)', '양지마을(2단지)(청구)', '양지마을(3단지)(금호)', '양지마을(5단지)(한양501-514)', '양지마을(5단지)(한양515-529)', '양지마을(6단지)(금호,청구)', '양지마을(6단지)(한양603동)',
      '시범우성', '시범현대', '장안타운(건영)'}
sd = [r for r in T if r['aptNm'] in SD and r['umdNm'] in ('분당동', '수내동', '서현동')]
ot = [r for r in T if r['aptNm'] not in SD and int(r.get('buildYear') or 0) <= 1996]
print('선도지구 단지 수', len({r['aptNm'] for r in sd}), '건', len(sd))
for lab, v in (('선도지구', sd), ('나머지 옛 단지', ot)):
    show(lab + ' 1년', pairs(v, '1년전', '최근')); show(lab + ' 고점', pairs(v, '고점21', '최근')); show(lab + ' 바닥23', pairs(v, '바닥23', '최근'))
    for per in ('1년전', '최근'):
        x = [r['_p'] for r in v if inper(r, per) and 83 <= r['_a'] <= 86]
        print(f'  {lab} 84㎡ {per}: {len(x)}건', f'{st.median(x)/10000:.2f}억' if x else '')
print('\n# 판교(1997년 이후) 84㎡ vs 서현수내정자 84㎡ — 언제 뒤집혔나(반기 가운데 값)')
for y in range(2021, 2027):
    for h, (lo, hi) in (('상', (1, 6)), ('하', (7, 12))):
        row = []
        for g in ('판교', '서현수내정자'):
            x = [r['_p'] for r in T if r['_g'] == g and r['_ym'] // 100 == y and lo <= r['_ym'] % 100 <= hi and 83 <= r['_a'] <= 86]
            row.append(f'{g} {len(x)}건 {st.median(x)/10000:.2f}억' if x else f'{g} 0건')
        print(f'{y}{h}', ' · '.join(row))
print('\n# 84㎡ 최근 가운데 값 구간(대출 한도 15억·25억 기준) 몫')
x = [r['_p'] for r in T if inper(r, '최근') and 83 <= r['_a'] <= 86]
print(len(x), '건 · 15억 이하', sum(1 for p in x if p <= 150000), '· 15억 초과~25억', sum(1 for p in x if 150000 < p <= 250000), '· 25억 초과', sum(1 for p in x if p > 250000))
print('# 10/20 토허 지정 전후 계약 건수: 2025.7~9 월평균', round(sum(1 for r in T if 202507 <= r['_ym'] <= 202509)/3), '· 2025.11~2026.1 월평균', round(sum(1 for r in T if 202511 <= r['_ym'] <= 202601)/3))
print('\n# 확인: 선도지구 구성에서 장안타운(건영)을 뺐을 때(이름이 보도 \'장안건영3\'과 딱 맞지 않음)')
SD2 = SD - {'장안타운(건영)'}
sd2 = [r for r in T if r['aptNm'] in SD2 and r['umdNm'] in ('분당동', '수내동', '서현동')]
ot2 = [r for r in T if r['aptNm'] not in SD and int(r.get('buildYear') or 0) <= 1996]
show('선도지구(장안 뺌) 1년', pairs(sd2, '1년전', '최근')); show('나머지 옛 단지 1년', pairs(ot2, '1년전', '최근'))
print('선도지구 구역별 1년:')
for nm, keys in (('샛별', '샛별'), ('양지', '양지'), ('시범', '시범')):
    show('  ' + nm, pairs([r for r in sd2 if keys in r['aptNm']], '1년전', '최근'))
print('# 확인: 2021년 하반기 대비 지금 값 아래인 쌍 수(분당 전체)', sum(1 for x in pairs(T, '고점21', '최근') if x[0] < 0))
