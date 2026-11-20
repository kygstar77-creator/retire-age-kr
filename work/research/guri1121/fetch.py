# 국토교통부 아파트 매매·전월세 실거래(RTMSDataSvcAptTradeDev·RTMSDataSvcAptRent) — 경기 구리시 41310 + 비교 하남시 41450
# 계약 2023-01~2026-11, 2026-11-20 firemap-write-b 받음 (hanam1120/fetch.py 틀)
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, W)
import rtmolit as R
out = os.path.join(os.path.dirname(__file__), 'raw')
yms = [f'{y}{m:02d}' for y in (2023, 2024, 2025) for m in range(1, 13)] + [f'2026{m:02d}' for m in range(1, 12)]
kinds = [a for a in sys.argv[1:] if not a.isdigit()] or ['trade']
codes = [a for a in sys.argv[1:] if a.isdigit()] or ['41310']
for code in codes:
    for kind in kinds:
        for ym in yms:
            p = os.path.join(out, f'{code}_{ym}_{kind}.json')
            if os.path.exists(p): continue
            rows = R.fetch(kind, code, ym)
            json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
            print(code, kind, ym, len(rows), flush=True)
