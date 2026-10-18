# K-1 미국 국채금리 5% → 한국 국채·정기예금·주담대 금리는 얼마나 따라왔나 (원자료: FRED GS10/DGS10, 한국은행 ECOS)
import sys, json, urllib.request, os
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.stdout.reconfigure(encoding='utf-8')
import apis
K = apis.key('ecos'); F = apis.key('fred')
os.makedirs('raw', exist_ok=True)
def ecos(stat, cyc, s, e, item):
    u = f'https://ecos.bok.or.kr/api/StatisticSearch/{K}/json/kr/1/100000/{stat}/{cyc}/{s}/{e}/{item}'
    rows = json.load(urllib.request.urlopen(u, timeout=40))['StatisticSearch']['row']
    return {r['TIME']: float(r['DATA_VALUE']) for r in rows}
def fred(sid, start='1996-01-01'):
    u = f'https://api.stlouisfed.org/fred/series/observations?series_id={sid}&api_key={F}&file_type=json&observation_start={start}'
    obs = json.load(urllib.request.urlopen(u, timeout=40))['observations']
    return {o['date']: float(o['value']) for o in obs if o['value'] != '.'}
us_m = {d[:4]+d[5:7]: v for d, v in fred('GS10').items()}
us_d = fred('DGS10', '2023-01-01')
kr10 = ecos('721Y001', 'M', '200010', '202609', '5050000')
kr3 = ecos('721Y001', 'M', '199601', '202609', '5020000')
dep = ecos('121Y002', 'M', '199601', '202608', 'BEABAA211')     # 정기예금 신규취급액 가중평균
dep1 = ecos('121Y002', 'M', '201201', '202608', 'BEABAA2118')   # 정기예금(1년)
mtg = ecos('121Y006', 'M', '200109', '202608', 'BECBLA0302')    # 주택담보대출
mfix = ecos('121Y006', 'M', '201301', '202608', 'BECBLA030201')
mvar = ecos('121Y006', 'M', '201301', '202608', 'BECBLA030202')
kr10d = ecos('817Y002', 'D', '20230101', '20261016', '010210000')
json.dump(dict(us_m=us_m, us_d=us_d, kr10=kr10, kr3=kr3, dep=dep, dep1=dep1, mtg=mtg, mfix=mfix, mvar=mvar, kr10d=kr10d), open('raw/series.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('받은 끝:', 'US GS10', max(us_m), '| DGS10', max(us_d), '| KR10 월', max(kr10), '| KR10 일', max(kr10d), '| 예금', max(dep), '| 주담대', max(mtg))

print('\n== 1. 미국 10년 5% 넘은 날 (DGS10, 2023~)')
over = [d for d, v in sorted(us_d.items()) if v >= 5.0]
print(' 5% 이상 날 수', len(over), '처음', over[:3], '마지막', over[-3:])
print(' 최근 10일', [(d, us_d[d]) for d in sorted(us_d)[-10:]])
print(' 2026 최고', max((v, d) for d, v in us_d.items() if d >= '2026'))
print(' 한국 10년 최근 10일', [(d, kr10d[d]) for d in sorted(kr10d)[-10:]])

print('\n== 2. 월별 나란히 (최근 18개월)')
ms = sorted(m for m in us_m if m >= '202503')
print(' 월     미10년 한10년 한3년 예금(전체) 예금1년 주담대 고정 변동')
for m in ms:
    g = lambda s: f'{s[m]:.2f}' if m in s else '  -  '
    print(f' {m} {g(us_m)} {g(kr10)} {g(kr3)} {g(dep)} {g(dep1)} {g(mtg)} {g(mfix)} {g(mvar)}')

def ch(s, a, b): return round(s[b] - s[a], 2) if a in s and b in s else None
last = max(dep)
for a in ('202508', '202601', '202606'):
    print(f'\n== 3. {a} → {last} 변화(%p): 미10년', ch(us_m, a, last), '한10년', ch(kr10, a, last), '한3년', ch(kr3, a, last), '예금', ch(dep, a, last), '예금1년', ch(dep1, a, last), '주담대', ch(mtg, a, last), '고정', ch(mfix, a, last), '변동', ch(mvar, a, last))

print('\n== 4. 누가 더 닮았나: 월 변화끼리 상관 (2013.01~끝, 같은 달)')
def diffs(s, months): return [s[months[i]] - s[months[i-1]] for i in range(1, len(months))]
def corr(x, y):
    n = len(x); mx = sum(x)/n; my = sum(y)/n
    sxy = sum((a-mx)*(b-my) for a, b in zip(x, y)); sx = sum((a-mx)**2 for a in x)**.5; sy = sum((b-my)**2 for b in y)**.5
    return round(sxy/(sx*sy), 2)
def beta(x, y):
    n = len(x); mx = sum(x)/n; my = sum(y)/n
    return round(sum((a-mx)*(b-my) for a, b in zip(x, y)) / sum((a-mx)**2 for a in x), 2)
months = sorted(m for m in mfix if m in us_m and m in kr10 and m in dep1 and m in kr3)
for name, s in (('예금1년', dep1), ('주담대 고정', mfix), ('주담대 변동', mvar)):
    y = diffs(s, months)
    print(f' {name}: 미10년 상관 {corr(diffs(us_m, months), y)} 기울기 {beta(diffs(us_m, months), y)} | 한10년 상관 {corr(diffs(kr10, months), y)} 기울기 {beta(diffs(kr10, months), y)} | 한3년 상관 {corr(diffs(kr3, months), y)} 기울기 {beta(diffs(kr3, months), y)}  (n={len(y)})')
print(' 미10년 vs 한10년 월 변화 상관', corr(diffs(us_m, months), diffs(kr10, months)), '기울기', beta(diffs(us_m, months), diffs(kr10, months)))

print('\n== 5. 지난번 미 10년 5% 근처: 2023.10 (월평균) 앞뒤')
for m in ('202305', '202307', '202309', '202310', '202311', '202312', '202402', '202404'):
    g = lambda s: f'{s[m]:.2f}' if m in s else '-'
    print(f' {m} 미10년 {g(us_m)} 한10년 {g(kr10)} 예금1년 {g(dep1)} 주담대 {g(mtg)} 고정 {g(mfix)} 변동 {g(mvar)}')
print(' 2007 미10년 월평균', {m: us_m[m] for m in sorted(us_m) if '200701' <= m <= '200712'})
for m in ('200701', '200706', '200707', '200712', '200806'):
    g = lambda s: f'{s[m]:.2f}' if m in s else '-'
    print(f' {m} 미10년 {g(us_m)} 한10년 {g(kr10)} 예금 {g(dep)} 주담대 {g(mtg)}')

print('\n== 6. 내 돈으로 (계산)')
def pay(P, r, yrs=30):
    i = r/100/12; n = yrs*12; return P*i/(1-(1+i)**-n)
for a in ('202508', '202601'):
    if a in mfix:
        p0, p1 = pay(3e8, mfix[a]), pay(3e8, mfix[last])
        print(f' 3억·30년 원리금균등 고정형: {a} {mfix[a]}% 월 {p0:,.0f}원 → {last} {mfix[last]}% 월 {p1:,.0f}원 (차 {p1-p0:+,.0f}원, 한 해 {12*(p1-p0):+,.0f}원)')
    if a in dep1:
        i0, i1 = 1e8*dep1[a]/100*(1-.154), 1e8*dep1[last]/100*(1-.154)
        print(f' 1억 1년 정기예금 세후(15.4%): {a} {dep1[a]}% {i0:,.0f}원 → {last} {dep1[last]}% {i1:,.0f}원 (차 {i1-i0:+,.0f}원)')
