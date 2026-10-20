# loan25_1020 — 서울 25개 구 아파트 매매 실거래 2026-07~10 새로 받기(rtmolit.fetch 재사용). 2026-10-20 firemap-write-b
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.join('..', '..'))
import rtmolit
sgg = json.load(open(os.path.join('..', 'seoul_sgg.json'), encoding='utf-8'))
n = 0
for code, name in sgg.items():
    if not code.startswith('11'): continue
    for ym in ('202607', '202608', '202609', '202610'):
        rows = rtmolit.fetch('trade', code, ym); n += 1
        json.dump(rows, open(os.path.join('raw', f'{code}_{ym}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        print(code, name, ym, len(rows), flush=True)
print('calls', n)
