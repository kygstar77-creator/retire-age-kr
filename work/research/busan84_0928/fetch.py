# 부산 16개 구·군 아파트 매매 실거래(국토부 RTMSDataSvcAptTradeDev) 2026-07~09 신고분 → raw/<코드>_<월>.json
import sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..'))
from rtmolit import fetch
CODES = ['26110','26140','26170','26200','26230','26260','26290','26320','26350','26380','26410','26440','26470','26500','26530','26710']
for c in CODES:
    for ym in ('202607','202608','202609'):
        p = os.path.join(HERE, 'raw', f'{c}_{ym}.json')
        if os.path.exists(p) and ym != '202609': continue
        rows = fetch('trade', c, ym)
        json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
        print(c, ym, len(rows), flush=True); time.sleep(0.3)
