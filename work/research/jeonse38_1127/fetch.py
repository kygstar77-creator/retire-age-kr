# jeonse38_1127 — 국토부 아파트 매매·전월세 실거래 인천 연수구(28185) 2026-07~11 계약월 다시 받기
#   py -3.12 work/research/jeonse38_1127/fetch.py  → raw/28185_<월>_{trade,rent}.json, H-5(11/21)·halfpair(11/24)와 건수 비교
import os, sys, json, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'raw'); os.makedirs(OUT, exist_ok=True)
H5 = os.path.join(HERE, '..', 'longform', 'ep', 'H-5', 'raw', 'rt'); HP = os.path.join(HERE, '..', 'halfpair1126', 'raw')
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..')))
import rtmolit
print('받은 시각', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
for ym in ['202607', '202608', '202609', '202610', '202611']:
    for kind in ('trade', 'rent'):
        rows = rtmolit.fetch(kind, '28185', ym)
        def cnt(d):
            p = os.path.join(d, f'28185_{ym}_{kind}.json')
            return len(json.load(open(p, encoding='utf-8'))) if os.path.exists(p) else None
        json.dump(rows, open(os.path.join(OUT, f'28185_{ym}_{kind}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        print(ym, kind, 'H-5 11/21:', cnt(H5), '· halfpair 11/24:', cnt(HP), '-> 오늘:', len(rows), flush=True)
