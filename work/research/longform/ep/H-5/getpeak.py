# H-5 고점 재료 — 인천 연수구 28185 아파트 매매 실거래 2021.01~2025.10 계약월(2021~22 고점·그 뒤 바닥 확인용)
#   py -3.12 work/research/longform/ep/H-5/getpeak.py → raw/rt/28185_<월>_trade.json
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(HERE, 'raw', 'rt'); os.makedirs(RT, exist_ok=True)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '..', '..')))
import rtmolit
MONTHS = [f'{y}{m:02d}' for y in range(2021, 2026) for m in range(1, 13) if (y, m) <= (2025, 10)]
n = 0
for ym in MONTHS:
    p = os.path.join(RT, f'28185_{ym}_trade.json')
    if os.path.exists(p): continue
    rows = rtmolit.fetch('trade', '28185', ym); n += len(rows)
    json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
print('ok', len(MONTHS), 'months', n, 'rows')
