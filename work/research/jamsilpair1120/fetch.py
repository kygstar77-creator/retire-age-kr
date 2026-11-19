# 국토교통부 아파트 매매·전월세 실거래 — 서울 송파구 11710(잠실동 포함)
# 계약 2020-01~2026-11, 2026-11-20 firemap-write 받음 (rtmolit.fetch 그대로)
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, W)
import rtmolit as R
out = os.path.join(os.path.dirname(__file__), 'raw')
yms = [f'{y}{m:02d}' for y in range(2020, 2026) for m in range(1, 13)] + [f'2026{m:02d}' for m in range(1, 12)]
for kind in ('trade', 'rent'):
    for ym in (yms if kind == 'trade' else yms[-12:]):
        p = os.path.join(out, f'11710_{ym}_{kind}.json')
        if os.path.exists(p) and ym < '202609': continue
        rows = R.fetch(kind, '11710', ym)
        json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
        print(kind, ym, len(rows), flush=True)
