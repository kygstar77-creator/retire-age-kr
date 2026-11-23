# halfpair1126 — 국토부 아파트 매매 실거래 인천 연수구(28185) 2021-01~2026-11 계약월 전부 다시 받기 + 전월세 2026-07~11
#   py -3.12 work/research/halfpair1126/fetch.py   → raw/28185_<월>_{trade,rent}.json (H-5 raw/rt와 같은 꼴, 건수 비교 출력)
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'raw'); os.makedirs(OUT, exist_ok=True)
H5 = os.path.join(HERE, '..', 'longform', 'ep', 'H-5', 'raw', 'rt')
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..')))
import rtmolit
MONTHS = [f'{y}{m:02d}' for y in range(2021, 2027) for m in range(1, 13) if f'{y}{m:02d}' <= '202611']
for ym in MONTHS:
    kinds = ('trade', 'rent') if ym >= '202607' else ('trade',)
    for kind in kinds:
        rows = rtmolit.fetch(kind, '28185', ym)
        old_p = os.path.join(H5, f'28185_{ym}_{kind}.json')
        old = len(json.load(open(old_p, encoding='utf-8'))) if os.path.exists(old_p) else None
        json.dump(rows, open(os.path.join(OUT, f'28185_{ym}_{kind}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        print(ym, kind, 'H-5:', old, '-> 오늘:', len(rows), flush=True)
