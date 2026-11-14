# 국토교통부 아파트 매매 실거래(공공데이터포털 1613000) — 양천구, 계약 2024-11~2026-11, 2026-11-15 받음 (rtmolit.fetch 그대로)
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, W)
import rtmolit as R
out = os.path.join(os.path.dirname(__file__), 'raw')
yms = ['202411','202412'] + [f'2025{m:02d}' for m in range(1, 13)] + [f'2026{m:02d}' for m in range(1, 12)]
for ym in yms:
    p = os.path.join(out, f'11470_{ym}_trade.json')
    if os.path.exists(p): continue
    rows = R.fetch('trade', '11470', ym)
    json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
    print(ym, len(rows), flush=True)
