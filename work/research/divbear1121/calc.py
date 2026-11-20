# divbear1121 직접 계산 — 야후 adjclose(배당 재투자·분할 반영) 기준
# ① 2022년 안 최대 낙폭(고점→바닥) ② 2020 코로나: 2020-01-01 뒤 고점→2020년 바닥 ③ 회복: 바닥 뒤 처음으로 그 고점 adjclose를 넘은 날
# ④ 2022년 한 해 수익(2021 마지막 거래일 → 2022 마지막 거래일, 배당 재투자)
import json, datetime, sys
sys.stdout.reconfigure(encoding='utf-8')
T = ['SPY','SCHD','JEPI','HDV','SPYD','VYM','DGRO','VIG','402970.KS']
def load(t):
    r = json.load(open(f'raw/{t}_chart_20261120.json', encoding='utf-8'))['chart']['result'][0]
    ts = r['timestamp']; ad = r['indicators']['adjclose'][0]['adjclose']; cl = r['indicators']['quote'][0]['close']
    off = r['meta'].get('gmtoffset', -18000)
    return [(datetime.datetime.utcfromtimestamp(a+off).date(), c, x) for a, c, x in zip(ts, cl, ad) if x is not None]
def mdd(rows):
    pk = rows[0]; best = (0, None, None)
    for r in rows:
        if r[2] > pk[2]: pk = r
        dd = r[2]/pk[2]-1
        if dd < best[0]: best = (dd, pk, r)
    return best
def recover(rows, peak, trough):
    for r in rows:
        if r[0] > trough[0] and r[2] >= peak[2]: return r
    return None
out = []
w = out.append
w('# divbear1121 calc_out — 야후 chart API adjclose(배당 재투자) · 2026-11-20 받음 raw/*_chart_20261120.json')
w('티커 | 2022 안 낙폭%(고점일→바닥일) | 회복일(거래일 수·달 수) | 2022 한 해 수익% | 코로나 낙폭%(고점일→바닥일) | 회복일(거래일·달) | 마지막 날 종가')
for t in T:
    px = load(t)
    s = ''
    r22 = [p for p in px if datetime.date(2022,1,1) <= p[0] <= datetime.date(2022,12,31)]
    if r22 and r22[0][0] < datetime.date(2022,2,1):
        dd, pk, tr = mdd(r22); rc = recover(px, pk, tr)
        n = [p for p in px if tr[0] < p[0] <= rc[0]] if rc else []
        prev = [p for p in px if p[0] <= datetime.date(2021,12,31)][-1]
        yr = r22[-1][2]/prev[2]-1
        mo = (rc[0]-tr[0]).days/30.44 if rc else None
        mo_pk = (rc[0]-pk[0]).days/30.44 if rc else None
        s += f"{dd*100:.1f}({pk[0]}→{tr[0]}) | {rc[0] if rc else '아직'}({len(n)}거래일·바닥에서 {mo:.1f}달·고점에서 {mo_pk:.1f}달) | {yr*100:.1f}"
    else:
        s += '- | - | -'
    r20 = [p for p in px if datetime.date(2020,1,1) <= p[0] <= datetime.date(2020,12,31)]
    if r20 and r20[0][0] < datetime.date(2020,1,10):
        dd, pk, tr = mdd(r20); rc = recover(px, pk, tr)
        n = [p for p in px if tr[0] < p[0] <= rc[0]] if rc else []
        mo = (rc[0]-tr[0]).days/30.44 if rc else None
        mo_pk = (rc[0]-pk[0]).days/30.44 if rc else None
        s += f" | {dd*100:.1f}({pk[0]}→{tr[0]}) | {rc[0] if rc else '아직'}({len(n)}거래일·바닥에서 {mo:.1f}달·고점에서 {mo_pk:.1f}달)"
    else:
        s += ' | - | -'
    s += f" | {px[-1][0]} {px[-1][1]:.2f}"
    w(f'{t} | {s}')
print('\n'.join(out))
open('calc_out.txt','w',encoding='utf-8').write('\n'.join(out)+'\n')

# ⑤ 지금(2026-11 하락): 사상 최고 adjclose → 마지막 거래일, 그리고 최근 한 달(약 21거래일 전 → 마지막)
w('')
w('## 지금 — 사상 최고(배당 재투자) 대비 마지막 거래일 · 최근 21거래일 수익')
for t in T:
    px = load(t)
    hi = max(px, key=lambda p: p[2]); last = px[-1]; m1 = px[-22]
    w(f"{t} | 최고 {hi[0]} → {last[0]} {(last[2]/hi[2]-1)*100:.1f}% | 21거래일({m1[0]}→{last[0]}) {(last[2]/m1[2]-1)*100:.1f}%")
print('\n'.join(out[-(len(T)+2):]))
open('calc_out.txt','w',encoding='utf-8').write('\n'.join(out)+'\n')
