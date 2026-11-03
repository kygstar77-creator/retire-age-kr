# K-1 calc5 (youtube-loop 2026-11-03): 한은 9월분(10월 말 공표) 나온 뒤 8월 비교를 9월 비교로 다시 셈
import sys, json, urllib.request
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
sys.stdout.reconfigure(encoding='utf-8')
import apis
K = apis.key('ecos'); F = apis.key('fred')
def ecos(stat, cyc, s, e, item):
    u = f'https://ecos.bok.or.kr/api/StatisticSearch/{K}/json/kr/1/100000/{stat}/{cyc}/{s}/{e}/{item}'
    rows = json.load(urllib.request.urlopen(u, timeout=40))['StatisticSearch']['row']
    return {r['TIME']: float(r['DATA_VALUE']) for r in rows}
def fred(sid, start):
    u = f'https://api.stlouisfed.org/fred/series/observations?series_id={sid}&api_key={F}&file_type=json&observation_start={start}'
    return {o['date'][:4]+o['date'][5:7]: float(o['value']) for o in json.load(urllib.request.urlopen(u, timeout=40))['observations'] if o['value'] != '.'}
S = dict(dep=ecos('121Y002', 'M', '202001', '202610', 'BEABAA211'), dep1=ecos('121Y002', 'M', '202001', '202610', 'BEABAA2118'),
         mtg=ecos('121Y006', 'M', '202001', '202610', 'BECBLA0302'), mfix=ecos('121Y006', 'M', '202001', '202610', 'BECBLA030201'),
         mvar=ecos('121Y006', 'M', '202001', '202610', 'BECBLA030202'), kr10=ecos('721Y001', 'M', '202001', '202610', '5050000'),
         kr3=ecos('721Y001', 'M', '202001', '202610', '5020000'), us=fred('GS10', '2020-01-01'))
json.dump(S, open('raw/series_1103.json', 'w', encoding='utf-8'), ensure_ascii=False)
cf = json.load(open('raw/cofix.json', encoding='utf-8'))['rows']
print('받은 끝:', {k: max(v) for k, v in S.items()})
a, b, f5 = '202509', '202609', '202109'
print('== 1. 9월끼리(2025.09 → 2026.09)')
for k in ('dep1', 'dep', 'mtg', 'mfix', 'mvar', 'kr10', 'kr3', 'us'):
    print(f' {k}: {S[k][a]} → {S[k][b]} ({S[k][b]-S[k][a]:+.2f}%p)')
print(' 4월 이후 고정−변동:', {m: round(S['mfix'][m]-S['mvar'][m], 2) for m in sorted(S['mfix']) if m >= '202509'})
print('== 2. 1억·2억 1년 정기예금 세후(15.4%)')
for m in (f5, a, b):
    print(f" {m} {S['dep1'][m]}% 1억 {1e8*S['dep1'][m]/100*.846:,.0f}원 · 2억 {2e8*S['dep1'][m]/100*.846:,.0f}원")
d1 = 1e8*(S['dep1'][b]-S['dep1'][a])/100*.846
print(f' 차: 1억 {d1:,.0f}원(월 {d1/12:,.0f}) · 2억 {2*d1:,.0f}원')
print('== 3. 주담대 − 정기예금(전체)')
for m in (f5, a, b):
    print(f" {m}: {S['mtg'][m]} − {S['dep'][m]} = {S['mtg'][m]-S['dep'][m]:.2f}%p")
def pay(P, r, n): r /= 1200; return P*r/(1-(1+r)**-n)
def bal(P, r, n, k):
    i = r/1200; m = pay(P, r, n); return P*(1+i)**k - m*((1+i)**k-1)/i
print('== 4. 3억·30년 새로 빌리기')
for k in ('mfix', 'mvar'):
    p0, p1 = pay(3e8, S[k][a], 360), pay(3e8, S[k][b], 360)
    print(f' {k}: {S[k][a]}% {p0:,.0f} → {S[k][b]}% {p1:,.0f} (차 {p1-p0:+,.0f})')
print('== 5. 2021.08 고정형 3억·30년 → 5년 뒤 지금(2026.09) 평균으로 다시 정함')
r0 = 2.98; m0 = pay(3e8, r0, 360); B = bal(3e8, r0, 360, 60)
for k in ('mfix', 'mvar'):
    m1 = pay(B, S[k][b], 300); print(f' {k} {S[k][b]}%: 처음 {m0:,.0f} · 남은 원금 {B:,.0f} · 월 {m1:,.0f} (차 {m1-m0:+,.0f}, 한 해 {12*(m1-m0):+,.0f})')
print('== 6. COFIX 신규·잔액 2025/09 → 2026/09', cf.get('2025/09'), cf['2026/09'])
