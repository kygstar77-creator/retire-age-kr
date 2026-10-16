# H-4 재료 받기 — 국토부 아파트 매매·전월세 실거래(공공데이터포털 1613000), 후보 4개 구 2025.11~2026.10 계약월
#   py -3.12 work/research/longform/ep/H-4/getrt.py   → raw/rt/<구코드>_<월>_{trade,rent}.json
# 후보: 마포구 11440(공덕동, 4-2 순서 10) · 광명시 41210(철산동) · 서초구 11650(방배동) · 용산구 11170(한남동)
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(HERE, 'raw', 'rt'); os.makedirs(RT, exist_ok=True)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '..', '..')))
import rtmolit
MONTHS = ['202511', '202512'] + [f'2026{m:02d}' for m in range(1, 11)]
for lawd in ['11440', '41210', '11650', '11170']:
    for ym in MONTHS:
        for kind in ('trade', 'rent'):
            p = os.path.join(RT, f'{lawd}_{ym}_{kind}.json')
            if os.path.exists(p) and ym != '202610': continue
            rows = rtmolit.fetch(kind, lawd, ym)
            json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
    print(lawd, 'ok')

# 서울 25개 구 매매 2026.07~09 계약 — '광명이 서울보다 비싼가' 같은 창 비교용(공용 work/research/rt는 8월분이 9/23에 받혀 늦은 신고가 빠져서 여기 새로 받음, 2026-10-16)
SGG = json.load(open(os.path.normpath(os.path.join(HERE, '..', '..', '..', 'seoul_sgg.json')), encoding='utf-8'))
for lawd in SGG:
    for ym in ('202607', '202608', '202609'):
        p = os.path.join(RT, f'{lawd}_{ym}_trade.json')
        if os.path.exists(p): continue
        json.dump(rtmolit.fetch('trade', lawd, ym), open(p, 'w', encoding='utf-8'), ensure_ascii=False)
print('seoul ok', len(SGG))
