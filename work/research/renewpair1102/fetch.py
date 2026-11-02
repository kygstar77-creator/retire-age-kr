# 2026-11-02 firemap-write: 국토부 아파트 전월세 실거래 다시 받기 (rtmolit.fetch) — h2s_renew 짝 글
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.stdout.reconfigure(encoding='utf-8')
import rtmolit
HERE = os.path.dirname(os.path.abspath(__file__))
MS = ['202511', '202512'] + [f'2026{m:02d}' for m in range(1, 12)]
for lawd in ('11680', '11710', '11650'):
    for ym in MS:
        p = os.path.join(HERE, 'raw', f'{lawd}_{ym}_rent.json')
        if os.path.exists(p): continue
        rows = rtmolit.fetch('rent', lawd, ym)
        json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
        print(lawd, ym, len(rows), flush=True)
