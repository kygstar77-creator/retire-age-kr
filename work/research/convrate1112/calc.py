# 갱신 계약 중 '전세 → 보증금 줄이고 월세'로 바꾼 서울 아파트 계약의 실제 전환율 (2026-08~10 계약, 11/12 받음)
import json, glob, os, statistics as st, sys
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__))
sgg = json.load(open(os.path.join(D, '..', 'seoul_sgg.json'), encoding='utf-8'))
def n(s):
    s = (s or '').replace(',', '').strip()
    return int(s) if s else 0
def cap(y, m, d):   # 계약일 기준 상한 = 기준금리 + 2%p (시행령 제9조, 연 10%보다 낮음)
    dt = (y, m, d)
    base = 3.00 if dt >= (2026, 8, 27) else (2.75 if dt >= (2026, 7, 16) else 2.50)
    return base + 2
rows = []
tot = {'all': 0, 'renew': 0, 'renew_pre_jeonse': 0}
for f in sorted(glob.glob(os.path.join(D, 'raw', '*.json'))):
    code = os.path.basename(f).split('_')[0]
    for r in json.load(open(f, encoding='utf-8')):
        tot['all'] += 1
        if r.get('contractType') != '갱신': continue
        tot['renew'] += 1
        pd, pm, dp, mr = n(r['preDeposit']), n(r['preMonthlyRent']), n(r['deposit']), n(r['monthlyRent'])
        if pm != 0 or pd == 0: continue
        tot['renew_pre_jeonse'] += 1
        if mr == 0: continue              # 전세 그대로 갱신
        if dp >= pd: continue             # 보증금은 그대로/올리고 월세를 더 얹은 경우 — 전환율 식이 안 맞음
        rate = mr * 12 / (pd - dp) * 100
        y, m, d = int(r['dealYear']), int(r['dealMonth']), int(r['dealDay'])
        rows.append(dict(gu=sgg.get(code, code), rate=rate, cut=pd - dp, pre=pd, dep=dp, mr=mr,
                         cap=cap(y, m, d), rr=r.get('useRRRight', ''), ym=f'{y}{m:02d}', apt=r['aptNm'], ar=r['excluUseAr']))
print('전체 전월세', tot['all'], '· 갱신', tot['renew'], '· 갱신 중 종전 전세', tot['renew_pre_jeonse'])
both = [x for x in rows]
print('전세→보증금 줄이고 월세로 바꾼 갱신', len(both))
# 보증금 그대로/올리고 월세 붙인 경우 수
r_all = [x['rate'] for x in rows]
def desc(xs, lab):
    xs = sorted(xs)
    if not xs: print(lab, 0); return
    q = st.quantiles(xs, n=4)
    print(f"{lab}: {len(xs)}건 · 중앙 {st.median(xs):.2f}% · 1사분위 {q[0]:.2f} 3사분위 {q[2]:.2f} · 평균 {st.mean(xs):.2f}")
desc(r_all, '전체')
over = [x for x in rows if x['rate'] > x['cap'] + 1e-9]
print(f"계약일 상한보다 높음 {len(over)}/{len(rows)} ({len(over)/len(rows)*100:.1f}%)")
over5 = [x for x in rows if x['rate'] > 5.0 + 1e-9]
print(f"5% 넘음 {len(over5)}/{len(rows)} ({len(over5)/len(rows)*100:.1f}%)")
for lab, f in (('4% 미만', lambda r: r < 4), ('4~5%', lambda r: 4 <= r <= 5), ('5~6%', lambda r: 5 < r <= 6), ('6% 초과', lambda r: r > 6)):
    k = sum(1 for x in rows if f(x['rate'])); print(f"  {lab}: {k} ({k/len(rows)*100:.1f}%)")
print('-- 갱신요구권')
for v in ('사용', ''):
    desc([x['rate'] for x in rows if x['rr'] == v], f"useRRRight='{v}'")
    sub = [x for x in rows if x['rr'] == v]
    if sub: print('   상한 넘음', sum(1 for x in sub if x['rate'] > x['cap'] + 1e-9), '/', len(sub))
print('-- 월별')
for ym in ('202608', '202609', '202610'):
    sub = [x for x in rows if x['ym'] == ym]; desc([x['rate'] for x in sub], ym)
print('-- 줄인 보증금 크기')
for lab, lo, hi in (('5천만 미만', 0, 5000), ('5천~1억', 5000, 10000), ('1~2억', 10000, 20000), ('2억 이상', 20000, 10**9)):
    sub = [x for x in rows if lo <= x['cut'] < hi]
    desc([x['rate'] for x in sub], lab)
    if sub: print('   5% 넘음', sum(1 for x in sub if x['rate'] > 5), '/', len(sub))
print('-- 구별 (20건 이상)')
by = {}
for x in rows: by.setdefault(x['gu'], []).append(x['rate'])
for g, xs in sorted(by.items(), key=lambda kv: -st.median(kv[1])):
    if len(xs) >= 20: print(f"  {g:5s} {len(xs):4d}건 중앙 {st.median(xs):.2f}%")
print('-- 보증금 줄인 폭 중앙(만원)', st.median([x['cut'] for x in rows]), '· 월세 중앙', st.median([x['mr'] for x in rows]), '· 종전 전세 중앙', st.median([x['pre'] for x in rows]))
# 갱신 중 종전 전세였던 계약에서: 전세 유지/보증금 줄이고 월세/보증금 그대로·올리고 월세
pj = 0; keep = 0; addm = 0
for f in glob.glob(os.path.join(D, 'raw', '*.json')):
    for r in json.load(open(f, encoding='utf-8')):
        if r.get('contractType') != '갱신': continue
        pd, pm, dp, mr = n(r['preDeposit']), n(r['preMonthlyRent']), n(r['deposit']), n(r['monthlyRent'])
        if pm != 0 or pd == 0: continue
        pj += 1
        if mr == 0: keep += 1
        elif dp >= pd: addm += 1
print(f"종전 전세 갱신 {pj}: 전세 유지 {keep} ({keep/pj*100:.1f}%) · 보증금 줄이고 월세 {len(rows)} ({len(rows)/pj*100:.1f}%) · 보증금 그대로·올리고 월세 {addm}")
json.dump(rows, open(os.path.join(D, 'rows.json'), 'w', encoding='utf-8'), ensure_ascii=False)
