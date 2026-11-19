# 국토교통부 아파트 매매·전월세 실거래(RTMSDataSvcAptTradeDev·RTMSDataSvcAptRent) — 경기 하남시 41450
# 계약 2021-01~2026-11, 2026-11-19 firemap-write-b 받음 (rtmolit.fetch 그대로, songdo1119/fetch.py 틀)
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, W)
import rtmolit as R
out = os.path.join(os.path.dirname(__file__), 'raw')
yms = [f'{y}{m:02d}' for y in (2021, 2022, 2023, 2024, 2025) for m in range(1, 13)] + [f'2026{m:02d}' for m in range(1, 12)]
kinds = sys.argv[1:] or ['trade']
for kind in kinds:
    for ym in yms:
        p = os.path.join(out, f'41450_{ym}_{kind}.json')
        if os.path.exists(p) and not ym.startswith('20261'): continue
        rows = R.fetch(kind, '41450', ym)
        json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
        print(kind, ym, len(rows), flush=True)
