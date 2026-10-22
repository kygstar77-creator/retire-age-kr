# H-5 재료 받기 — 국토부 아파트 매매·전월세 실거래(공공데이터포털 1613000), 후보 구 2025.11~2026.10 계약월
#   py -3.12 work/research/longform/ep/H-5/getrt.py   → raw/rt/<구코드>_<월>_{trade,rent}.json
# 후보: 강동구 11740(고덕동, 4-2 순서 3) · 인천 연수구 28185(송도동, 4-2 경기 줄)
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(HERE, 'raw', 'rt'); os.makedirs(RT, exist_ok=True)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '..', '..')))
import rtmolit
MONTHS = ['202511', '202512'] + [f'2026{m:02d}' for m in range(1, 11)]
for lawd in sys.argv[1:] or ['11740', '28185']:
    for ym in MONTHS:
        for kind in ('trade', 'rent'):
            p = os.path.join(RT, f'{lawd}_{ym}_{kind}.json')
            if os.path.exists(p) and ym != '202610': continue
            rows = rtmolit.fetch(kind, lawd, ym)
            json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
    print(lawd, 'ok')
