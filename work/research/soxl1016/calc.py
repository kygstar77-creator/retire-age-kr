# soxl1016 계산 — Yahoo 일별 수정종가(분배금 재투자 반영)
import json, datetime as D, sys
sys.stdout.reconfigure(encoding='utf-8')
def load(t, key='adjclose'):
    r = json.load(open(t + '.json'))['chart']['result'][0]
    ts = [D.datetime.fromtimestamp(x, D.UTC).date() for x in r['timestamp']]
    v = r['indicators']['adjclose'][0]['adjclose'] if key=='adjclose' else r['indicators']['quote'][0]['close']
    return {d: x for d, x in zip(ts, v) if x}
L, X = load('SOXL'), load('SOXX')
Lc, Xc = load('SOXL','close'), load('SOXX','close')
days = sorted(set(L) & set(X)); end = days[-1]
print('마지막', end, 'SOXL 종가', round(Lc[end],2), 'SOXX 종가', round(Xc[end],2))
def at(d):  # d 이전 마지막 거래일
    return max(x for x in days if x <= d)
# 하루 등락 비율 확인
import statistics as S
rat = []
for a, b in zip(days[-260:-1], days[-259:]):
    rx = X[b]/X[a]-1; rl = L[b]/L[a]-1
    if abs(rx) > 0.01: rat.append(rl/rx)
print('최근 1년 하루 등락 배율 중앙값(SOXX 1% 넘게 움직인 날)', round(S.median(rat),2), len(rat))
for yrs in (1, 3, 5):
    s = at(end.replace(year=end.year - yrs))
    rl = L[end]/L[s]-1; rx = X[end]/X[s]-1
    print(f'{yrs}년 {s}~{end}: SOXX {rx*100:+.1f}% SOXL {rl*100:+.1f}% 3배단순 {3*rx*100:+.1f}% | 100만원 SOXX {100*(1+rx):.0f}만 SOXL {100*(1+rl):.0f}만')
# 고점 대비
for t, P in (('SOXL', Lc), ('SOXX', Xc)):
    yr = [d for d in days if d > end.replace(year=end.year-1)]
    hi = max(yr, key=lambda d: P[d]); lo = min(yr, key=lambda d: P[d])
    print(t, '52주 최고', hi, round(P[hi],2), '최저', lo, round(P[lo],2), '지금 최고 대비', f'{(P[end]/P[hi]-1)*100:.1f}%')
# 지수(SOXX)가 제자리인데 SOXL이 빠진 구간: 120~260거래일 창에서 SOXX 변동 ±2% 이내, SOXL 최저
best = None
for i in range(len(days)):
    for j in range(i+60, min(i+260, len(days))):
        a, b = days[i], days[j]
        rx = X[b]/X[a]-1
        if abs(rx) <= 0.02:
            rl = L[b]/L[a]-1
            if best is None or rl < best[0]: best = (rl, rx, a, b)
rl, rx, a, b = best
print(f'제자리 구간 {a}~{b}: SOXX {rx*100:+.1f}% SOXL {rl*100:+.1f}% (100만원→{100*(1+rl):.0f}만)')
# 같은 구간 SOXX 최저점
mn = min((d for d in days if a <= d <= b), key=lambda d: X[d])
print('  그 사이 SOXX 최저', mn, f'{(X[mn]/X[a]-1)*100:.1f}%', 'SOXL', f'{(L[mn]/L[a]-1)*100:.1f}%')
# 10/15 하루
p = days[-2]; print('10/15 하루', p, '->', end, f'SOXX {(Xc[end]/Xc[p]-1)*100:+.2f}% SOXL {(Lc[end]/Lc[p]-1)*100:+.2f}%')
# 분할 이력
r = json.load(open('SOXL.json'))['chart']['result'][0]
print('events', list(r.get('events', {}).keys()))
print('divs 최근', sorted([(str(D.datetime.fromtimestamp(int(k),D.UTC).date()), v['amount']) for k, v in r.get('events',{}).get('dividends',{}).items()])[-5:])
