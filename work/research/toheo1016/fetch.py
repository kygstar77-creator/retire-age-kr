# 서울 25개 구 아파트 매매 실거래 2026-04~09 새로 받기(조회 2026-10-15) → raw/<구>_<월>.json
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.stdout.reconfigure(encoding='utf-8')
from rtmolit import fetch
H = os.path.dirname(os.path.abspath(__file__))
sgg = json.load(open(os.path.join(H, '..', 'seoul_sgg.json'), encoding='utf-8'))
for lawd, name in sgg.items():
    for ym in ['202604', '202605', '202606', '202607', '202608', '202609']:
        p = os.path.join(H, 'raw', f'{lawd}_{ym}.json')
        if os.path.exists(p): continue
        try:
            rows = fetch('trade', lawd, ym); json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False); print(name, ym, len(rows), flush=True)
        except Exception as e: print(name, ym, '실패', e, flush=True)
        time.sleep(0.3)
print('끝', time.strftime('%H:%M'))
