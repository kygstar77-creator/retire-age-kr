# S-1 발표 '전' 20거래일(선반영 질문용) — youtube-loop 2026-11-02 · 주가는 calc.py와 같은 px(다음 금융, 거래정지 3일 뺌, 분할 전 /50)
import json, os, statistics, sys
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
import calc
px, days = calc.px, calc.days
rows = json.load(open(os.path.join(D, 'calc_out.json'), encoding='utf-8'))
pre = []
for r in rows:
    i = days.index(r['date'])
    if i - 21 < 0: continue
    a, b = px[days[i - 21]], px[days[i - 1]]
    pre.append(dict(date=r['date'], from_date=days[i - 21], pre_pct=round((b / a - 1) * 100, 2), day_pct=r['day_pct']))
n = len(pre); up = [p for p in pre if p['pre_pct'] > 0]
print(f'[PRE1] 발표 전날까지 20거래일(전날 종가 ÷ 21거래일 전 종가) 비교 가능 = {n}')
print(f'[PRE2] 그중 올라 있던 횟수 = {len(up)} ({len(up)/n*100:.1f}%) · 중앙 {statistics.median(p["pre_pct"] for p in pre):+.2f}%')
# 평소 아무 20거래일(같은 기간) — calc N2와 같은 방식
s0 = days.index('2016-01-08'); base = [(px[days[k + 20]] / px[days[k]] - 1) for k in range(s0, len(days) - 20)]
print(f'[PRE3] 같은 기간(2016-01-08~) 아무 20거래일 오른 비율 = {sum(x > 0 for x in base)/len(base)*100:.1f}% ({len(base)}구간)')
upd = [p for p in up if p['day_pct'] < 0]; dnn = [p for p in pre if p['pre_pct'] <= 0]
print(f'[PRE4] 발표 전 20일 올라 있던 {len(up)}번 중 발표 날 내림 = {len(upd)} · 발표 전 20일 오르지 않은 {len(dnn)}번 중 발표 날 내림 = {sum(p["day_pct"] < 0 for p in dnn)}')
for p in pre[-6:]: print('  ', p)
# v3(11/2): 발표 전 가장 많이 올라 있던 때·올해 네 번
for p in sorted(pre, key=lambda p: -p['pre_pct'])[:3]: print('[PRE5] 전 20일 상위', p)
y = [p for p in pre if p['date'].startswith('2026')]
print(f'[PRE6] 2026년 {len(y)}번: 전 20일 올라 있음 {sum(p["pre_pct"] > 0 for p in y)} · 그중 발표 날 내림 {sum(p["pre_pct"] > 0 and p["day_pct"] < 0 for p in y)}')
