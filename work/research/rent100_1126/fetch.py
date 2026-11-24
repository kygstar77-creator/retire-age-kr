# 국토교통부 아파트 전월세 실거래(RTMSDataSvcAptRent) — 서울 25개 구, 계약 2025-08~10·2026-08~10
# 2026-11-24 firemap-write-b 받음 (geomdan1125/fetch.py 틀). 다시 돌리면 2026년 달만 새로 받는다.
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, W)
import rtmolit as R
out = os.path.join(os.path.dirname(__file__), 'raw')
sgg = json.load(open(os.path.join(W, 'research', 'seoul_sgg.json'), encoding='utf-8'))
yms = ['202508', '202509', '202510', '202608', '202609', '202610']
for lawd in sgg:
    for ym in yms:
        p = os.path.join(out, f'{lawd}_{ym}_rent.json')
        if os.path.exists(p) and not ym.startswith('2026'): continue
        rows = R.fetch('rent', lawd, ym)
        json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
        print(lawd, ym, len(rows), flush=True)
