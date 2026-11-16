# 국토교통부 아파트 매매 실거래(공공데이터포털 1613000 RTMSDataSvcAptTradeDev) — 성남시 분당구 41135 · 고양시 일산동구 41285 · 일산서구 41287
# 계약 2021-01~2026-11, 2026-11-17 firemap-write-b 받음 (rtmolit.fetch 그대로)
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, W)
import rtmolit as R
out = os.path.join(os.path.dirname(__file__), 'raw')
yms = [f'{y}{m:02d}' for y in (2021, 2022, 2023, 2024, 2025) for m in range(1, 13)] + [f'2026{m:02d}' for m in range(1, 12)]
for code in ('41135', '41285', '41287'):
    for ym in yms:
        p = os.path.join(out, f'{code}_{ym}_trade.json')
        if os.path.exists(p) and ym < '202609': continue
        rows = R.fetch('trade', code, ym)
        json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
        print(code, ym, len(rows), flush=True)
