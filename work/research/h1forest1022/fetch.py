# 2026-10-22 write-b: 국토부 아파트 매매·전월세 실거래 다시 받기 (rtmolit.fetch)
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
sys.stdout.reconfigure(encoding='utf-8')
import rtmolit
def months(a, b):
    y, m = int(a[:4]), int(a[4:]); out = []
    while f'{y}{m:02d}' <= b:
        out.append(f'{y}{m:02d}'); m += 1
        if m > 12: y, m = y + 1, 1
    return out
jobs = [('11710', months('201811', '202001') + months('202510', '202610')), ('11740', months('202410', '202610'))]
for lawd, ms in jobs:
    for ym in ms:
        for kind in ('trade', 'rent'):
            p = f'raw/{lawd}_{ym}_{kind}.json'
            if os.path.exists(p): continue
            rows = rtmolit.fetch(kind, lawd, ym)
            json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
            print(lawd, ym, kind, len(rows), flush=True)
