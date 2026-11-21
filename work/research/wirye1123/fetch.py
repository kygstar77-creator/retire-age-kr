# 국토교통부 아파트 매매 실거래(rtmolit) — 위례신도시가 걸친 세 곳: 서울 송파구 11710 · 성남시 수정구 41131 · 하남시 41450
# 계약 2021-01~2026-11, 2026-11-22 firemap-write 받음 (bundang1122/fetch.py 틀)
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, W)
import rtmolit as R
out = os.path.join(os.path.dirname(__file__), 'raw')
yms = [f'{y}{m:02d}' for y in (2021, 2022, 2023, 2024, 2025) for m in range(1, 13)] + [f'2026{m:02d}' for m in range(1, 12)]
for lawd in sys.argv[1:] or ['11710', '41131', '41450']:
    for ym in yms:
        p = os.path.join(out, f'{lawd}_{ym}_trade.json')
        if os.path.exists(p) and not ym.startswith('20261'): continue
        rows = R.fetch('trade', lawd, ym)
        json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
        print(lawd, ym, len(rows), flush=True)
