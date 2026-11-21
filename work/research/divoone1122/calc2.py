# divoone1122 — DIVO 해마다 12월 분배 vs 나머지 달 평균 (야후 10년, write-b 2026-11-21)
import json, datetime, sys
sys.stdout.reconfigure(encoding='utf-8')
j = json.load(open('raw/DIVO_10y_20261121.json'))['chart']['result'][0]
dv = sorted((datetime.datetime.fromtimestamp(int(k), datetime.UTC).date(), v['amount']) for k, v in j['events']['dividends'].items())
by = {}
for d, a in dv: by.setdefault(d.year, []).append((d, a))
for y, l in by.items():
    s = sum(a for _, a in l); dec = [a for d, a in l if d.month == 12]; o = [a for d, a in l if d.month != 12]
    print(f'{y}\t회차 {len(l)}\t합 {s:.4f}\t12월 {dec}\t나머지 평균 {sum(o)/len(o):.4f}\t12월÷평균 {(dec[0]/(sum(o)/len(o)) if dec else 0):.1f}배')
