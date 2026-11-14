# -*- coding: utf-8 -*-
"""S-1 6장 — 10/8 발표 20거래일 뒤 값(2026-11-15 youtube-loop). calc.py 기준 그대로: 발표 전날 종가 → 20거래일 뒤 종가, 거래량 0 행 뺌.
주가: 다음 금융 일별 종가 raw/daum_005930_daily_1115.json(11/15 04시대 받음, 마지막 행 11/13) — calc.py와 같은 출처(KRX 정규장 종가)."""
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__))
px = {r['date'][:10]: r['tradePrice'] for r in json.load(open(os.path.join(D, 'raw/daum_005930_daily_1115.json'), encoding='utf-8')) if r['accTradeVolume']}
days = sorted(px); i = days.index('2026-10-08')
prev, d20 = days[i - 1], days[i + 20]
c0, c20 = px[prev], px[d20]
pct = (c20 / c0 - 1) * 100
print(f'발표 2026-10-08 · 전날 {prev} {c0:,.0f}원 → 20거래일 뒤 {d20} {c20:,.0f}원 · {pct:+.2f}%')
print(f'100주 {c0*100:,.0f}원 → {c20*100:,.0f}원 · {(c20-c0)*100:+,.0f}원')
print('사이 거래일:', ' '.join(days[i + 1:i + 21]))
for d in ('2026-10-07', '2026-10-08', '2026-10-13'): print('옛 calc_out 대조', d, px[d])
