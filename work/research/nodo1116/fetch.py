# 국토교통부 아파트 매매 실거래(공공데이터포털 1613000, rtmolit.fetch) — 서울 25개 구, 계약 2024-11~2026-11, 2026-11-15 받음
# 인자 없으면 노원(11350)·도봉(11320)·강북(11305)만, 'all'이면 서울 25개 구
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(H, '..', '..'))
sys.path.insert(0, W)
import rtmolit as R
out = os.path.join(H, 'raw')
yms = ['202411','202412'] + [f'2025{m:02d}' for m in range(1, 13)] + [f'2026{m:02d}' for m in range(1, 12)]
if len(sys.argv) > 1 and sys.argv[1] == 'all':
    sgg = json.load(open(os.path.join(W, 'research', 'seoul_sgg.json'), encoding='utf-8'))
    codes = ['11350', '11320', '11305'] + [c for c in sgg if c not in ('11350', '11320', '11305')]
else:
    codes = ['11350', '11320', '11305']
for code in codes:
    for ym in yms:
        p = os.path.join(out, f'{code}_{ym}_trade.json')
        if os.path.exists(p): continue
        rows = R.fetch('trade', code, ym)
        json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
        print(code, ym, len(rows), flush=True)
