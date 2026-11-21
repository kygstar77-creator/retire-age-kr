# 같은 기간(1986~2025) 맞대기·1950년 뒤 대조 (2026-11-21 firemap-write-b) — 원자료 raw/*_20261121.json
import json, datetime, statistics as st, sys
sys.stdout.reconfigure(encoding='utf-8')
def load(n):
    r = json.load(open(f'raw/{n}_20261121.json'))['chart']['result'][0]
    dd = {}
    for t, v in zip(r['timestamp'], r['indicators']['quote'][0]['close']):
        if v is None: continue
        dd[(datetime.datetime(1970,1,1)+datetime.timedelta(seconds=t+9*3600)).date()] = v
    return sorted(dd.items())
def pct(a, b): return (b/a-1)*100
def stats(S, y0, y1):
    last = {}
    for d, v in S: last[(d.year, d.month)] = v
    dec = {y: pct(last[(y,11)], last[(y,12)]) for y in range(y0, y1+1) if (y,11) in last and (y,12) in last}
    nov = {y: pct(last[(y,10)], last[(y,11)]) for y in range(y0, y1+1) if (y,10) in last and (y,11) in last}
    santa = {}
    for y in range(y0, y1+1):
        di = [i for i,(d,v) in enumerate(S) if d.year==y and d.month==12]
        ji = [i for i,(d,v) in enumerate(S) if d.year==y+1 and d.month==1]
        if len(di)<6 or len(ji)<2: continue
        santa[y] = pct(S[di[-5]-1][1], S[ji[1]][1])
    return dec, nov, santa
for name in ['gspc', 'ndx']:
    S = load(name)
    for y0, y1 in ([(1950, 2025), (1986, 2025), (2006, 2025)] if name=='gspc' else [(1986, 2025), (2006, 2025)]):
        dec, nov, santa = stats(S, y0, y1)
        du = sum(1 for v in dec.values() if v>0); su = sum(1 for v in santa.values() if v>0)
        print(f'{name} {y0}~{y1}: 12월 {du}/{len(dec)} ({du/len(dec)*100:.1f}%) 중간 {st.median(dec.values()):.2f} | 산타 {su}/{len(santa)} ({su/len(santa)*100:.1f}%) 평균 {st.mean(santa.values()):.2f} 중간 {st.median(santa.values()):.2f}')
        big = [y for y in nov if nov[y] <= -3 and y in dec]
        if big:
            bu = sum(1 for y in big if dec[y] > 0)
            print(f'   11월 -3% 이하 {len(big)}번 → 12월 오른 {bu}, 12월 중간 {st.median([dec[y] for y in big]):.2f} :', ', '.join(f'{y}({nov[y]:.1f}→{dec[y]:+.1f})' for y in big))
    dec, nov, santa = stats(S, 1986, 2025)
    print('   12월 내린 해:', ' '.join(f'{y}:{v:+.1f}' for y, v in sorted(dec.items()) if v <= 0))
    print('   최근 10년 12월:', ' '.join(f'{y}:{v:+.1f}' for y, v in sorted(dec.items())[-10:]))
# 같은 해에 S&P500은 12월 올랐는데 나스닥100은 내린 해
S1, S2 = load('gspc'), load('ndx')
d1, _, s1 = stats(S1, 1986, 2025); d2, _, s2 = stats(S2, 1986, 2025)
both = [y for y in d1 if y in d2]
print('같은 40년: S&P만 오름', [y for y in both if d1[y]>0 and d2[y]<=0])
print('           나스닥100만 오름', [y for y in both if d2[y]>0 and d1[y]<=0])
print('           12월 나스닥100이 S&P보다 높은 해', sum(1 for y in both if d2[y]>d1[y]), '/', len(both))
