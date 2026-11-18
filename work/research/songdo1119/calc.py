# songdo1119 — 인천 연수구 28185 중 송도동 아파트 전세(월세 0) 실거래(S1 raw)로 '1억 올랐다'를 같은 집으로 다시 재기 · firemap-write-b 2026-11-18 (gwanggyo1118/calc.py 틀)
# 같은 집 = 같은 단지(aptSeq)·같은 전용면적(1㎡ 반올림). 전세 = monthlyRent 0. 매매는 해제(cdealType) 뺌.
import json, os, glob, statistics as st, sys, collections as C
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
num = lambda s: float(str(s or '0').replace(',', '') or 0)
def load(kind):
    out = []
    for p in sorted(glob.glob(os.path.join(H, 'raw', f'28185_*_{kind}.json'))):
        for r in json.load(open(p, encoding='utf-8')):
            if r['umdNm'] != '송도동': continue
            r['_ym'] = int(r['dealYear']) * 100 + int(r['dealMonth']); r['_a'] = round(num(r['excluUseAr']))
            r['_k'] = (r.get('aptSeq') or r['aptNm'], r['_a']); out.append(r)
    return out
T = [r for r in load('trade') if not r.get('cdealType')]
for r in T: r['_p'] = num(r['dealAmount'])
R = load('rent')
J = [r for r in R if num(r['monthlyRent']) == 0]
for r in J: r['_p'] = num(r['deposit'])
print('송도동 매매(해제 뺌)', len(T), '건 · 전월세', len(R), '건 · 그중 전세', len(J), '건 · 단지', len({r['aptSeq'] for r in J}))
print('전세 계약 구분:', C.Counter(r.get('contractType') or '(빈칸)' for r in J if r['_ym'] >= 202506).most_common())
NEWJ = [r for r in J if r.get('contractType') == '신규']
PER = {'1년전': (202506, 202510), '최근': (202606, 202610), '2년전': (202406, 202410), '고점21': (202107, 202112)}
def inper(r, k): lo, hi = PER[k]; return lo <= r['_ym'] <= hi
def pairs(rows, a, b):
    d = C.defaultdict(lambda: C.defaultdict(list)); nm = {}
    for r in rows:
        nm[r['_k']] = r['aptNm']
        for k in (a, b):
            if inper(r, k): d[r['_k']][k].append(r['_p'])
    return [(st.median(v[b]) / st.median(v[a]) - 1, st.median(v[b]) - st.median(v[a]), nm[k], k[1], st.median(v[a]), st.median(v[b]), len(v[a]), len(v[b])) for k, v in d.items() if v[a] and v[b]]
def show(lbl, ps):
    if not ps: print(lbl, '0쌍'); return
    rs = [x[0] for x in ps]; ds = [x[1] for x in ps]
    print(f"{lbl}: {len(ps)}쌍 · 가운데 {st.median(rs)*100:+.1f}% · 가운데 금액 {st.median(ds)/10000:+.2f}억 · 오른 쌍 {sum(1 for x in rs if x>0)/len(rs)*100:.0f}% · 1억 이상 오른 쌍 {sum(1 for x in ds if x>=10000)}개({sum(1 for x in ds if x>=10000)/len(ds)*100:.0f}%)")
print('\n# 같은 집 전세 보증금 1년(2025.6~10 → 2026.6~10)')
show('전세 전체(신규+갱신)', pairs(J, '1년전', '최근'))
show('전세 신규만', pairs(NEWJ, '1년전', '최근'))
show('전세 2년(2024.6~10→최근) 전체', pairs(J, '2년전', '최근'))
show('전세 2021H2→최근 전체', pairs(J, '고점21', '최근'))
print('\n# 같은 집 매매 1년 · 2021H2→최근')
show('매매 1년', pairs(T, '1년전', '최근'))
show('매매 2021H2→최근', pairs(T, '고점21', '최근'))
print('\n# 84㎡ 안팎(83~86㎡) 전세 신규 1년 같은 집 — 위·아래 예시')
ps = sorted(pairs([r for r in NEWJ if 83 <= r['_a'] <= 86], '1년전', '최근'), reverse=True)
show('84㎡ 신규', ps)
for x in ps[:4] + ps[-3:]: print('  ', f'{x[0]*100:+.1f}%', x[2], f'{x[3]}㎡', f'{x[4]/10000:.2f}억→{x[5]/10000:.2f}억', f'({x[6]}건/{x[7]}건)')
print('\n# 더샵퍼스트파크(기사 예시) 84㎡ 전세 월별')
for r in sorted([r for r in J if '퍼스트파크' in r['aptNm'] and 83 <= r['_a'] <= 86 and r['_ym'] >= 202409], key=lambda r: r['_ym']):
    pass
dd = C.defaultdict(list)
for r in J:
    if '퍼스트파크' in r['aptNm'] and 83 <= r['_a'] <= 86 and r['_ym'] >= 202409: dd[(r['aptNm'], r['_ym'], r.get('contractType') or '-')].append(r['_p'])
for k in sorted(dd, key=lambda k: (k[1], k[0])): print('  ', k, len(dd[k]), '건 가운데', st.median(dd[k])/10000, '억')
print('\n# 갱신 vs 신규 같은 기간(최근) 84㎡ 가운데 보증금')
for ct in ('신규', '갱신'):
    v = [r['_p'] for r in J if inper(r, '최근') and 83 <= r['_a'] <= 86 and r.get('contractType') == ct]
    print(ct, len(v), '건 · 가운데', f'{st.median(v)/10000:.2f}억' if v else '-')
print('갱신 중 계약갱신요구권 쓴 몫(최근):', C.Counter(r.get('useRRRight') or '(빈칸)' for r in J if inper(r, '최근') and r.get('contractType') == '갱신'))
print('\n# 전세가율(같은 집: 같은 기간 전세 가운데 / 매매 가운데)')
for per in ('고점21', '2년전', '1년전', '최근'):
    dt = C.defaultdict(list); dj = C.defaultdict(list)
    for r in T:
        if inper(r, per): dt[r['_k']].append(r['_p'])
    for r in J:
        if inper(r, per): dj[r['_k']].append(r['_p'])
    rs = [st.median(dj[k]) / st.median(dt[k]) for k in dt if k in dj]
    print(f'{per}: {len(rs)}개 집 · 전세가율 가운데 {st.median(rs)*100:.1f}% · 70% 넘는 집 {sum(1 for x in rs if x>0.7)}개')
print('\n# 84㎡ 안팎 가운데 값(기간별)')
for per in PER:
    vt = [r['_p'] for r in T if inper(r, per) and 83 <= r['_a'] <= 86]; vj = [r['_p'] for r in J if inper(r, per) and 83 <= r['_a'] <= 86]
    print(f'{per}: 매매 {len(vt)}건 {st.median(vt)/10000:.2f}억 · 전세 {len(vj)}건 {st.median(vj)/10000:.2f}억')
print('\n# 전세 건수(월평균)·월세 몫')
for lab, lo, hi in (('2024년 6~10월', 202406, 202410), ('2025년 6~10월', 202506, 202510), ('2026년 6~10월', 202606, 202610)):
    v = [r for r in R if lo <= r['_ym'] <= hi]; j = [r for r in v if num(r['monthlyRent']) == 0]
    print(f'{lab}: 전월세 {len(v)}건 · 전세 {len(j)}건(월평균 {len(j)/5:.0f}) · 월세 낀 몫 {(1-len(j)/len(v))*100:.0f}%')
print('\n# 2026년 11월 신고분(최근에서 뺌):', sum(1 for r in J if r['_ym'] == 202611), '건(전세)')
print('\n# 신규 전세 1년 같은 집 오른 금액 구간(전체 넓이)')
ps = pairs(NEWJ, '1년전', '최근'); ds = sorted(x[1] for x in ps)
B = [('내리거나 그대로', lambda d: d <= 0), ('5천만원 미만', lambda d: 0 < d < 5000), ('5천만~1억원 미만', lambda d: 5000 <= d < 10000), ('1억원 이상', lambda d: d >= 10000)]
for lab, f in B:
    n = sum(1 for d in ds if f(d)); print(f'{lab}: {n}개({n/len(ds)*100:.0f}%)')
print('합', len(ds))
print('\n# 84㎡ 안팎 같은 기간 신규 전세 가운데(1년전→최근) — 섞인 값')
for per in ('1년전', '최근'):
    v = [r['_p'] for r in NEWJ if inper(r, per) and 83 <= r['_a'] <= 86]
    print(per, len(v), '건', f'{st.median(v)/10000:.2f}억')
print('\n# 더샵퍼스트파크 84㎡ 안팎 신규 1년 같은 집')
for x in pairs([r for r in NEWJ if '퍼스트파크' in r['aptNm'] and 83 <= r['_a'] <= 86], '1년전', '최근'):
    print('  ', f'{x[0]*100:+.1f}%', x[2], f'{x[3]}㎡', f'{x[4]/10000:.2f}억→{x[5]/10000:.2f}억', f'({x[6]}건/{x[7]}건)')
