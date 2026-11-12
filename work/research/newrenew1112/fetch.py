# 국토교통부 아파트 매매·전월세 실거래(공공데이터포털 1613000) — 강남·송파·양천, 계약 2025-11~2026-11, 2026-11-12 받음 (rtmolit.fetch 그대로)
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, W)
import rtmolit as R
out = os.path.join(os.path.dirname(__file__), 'raw')
yms = ['202511','202512'] + [f'2026{m:02d}' for m in range(1, 12)]
for code in ('11680', '11710', '11470'):
    for ym in yms:
        for kind in ('trade', 'rent'):
            p = os.path.join(out, f'{code}_{ym}_{kind}.json')
            if os.path.exists(p): continue
            rows = R.fetch(kind, code, ym)
            json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
            print(code, ym, kind, len(rows), flush=True)
