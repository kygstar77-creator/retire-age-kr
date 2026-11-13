# 11/13 올리기 전 확인 — 국토부 전월세·매매 실거래 다시 받기(raw1113: 7곳 3개 구 2026-09~11, raw1113b: 서울 25개 구 전월세 2026-08~10)
import sys, os, json, glob, shutil
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(H, '..', '..'))
sys.path.insert(0, W)
import rtmolit as R
a = os.path.join(H, 'raw1113'); b = os.path.join(H, 'raw1113b')
if not os.path.exists(a): shutil.copytree(os.path.join(H, 'raw'), a)
os.makedirs(b, exist_ok=True)
for code in ('11680', '11710', '11470'):
    for ym in ('202609', '202610', '202611'):
        for kind in ('trade', 'rent'):
            rows = R.fetch(kind, code, ym)
            json.dump(rows, open(os.path.join(a, f'{code}_{ym}_{kind}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
            print('A', code, ym, kind, len(rows), flush=True)
codes = sorted({os.path.basename(p)[:5] for p in glob.glob(os.path.join(H, '..', 'convrate1112', 'raw', '1*_2026*.json'))})
for code in codes:
    for ym in ('202608', '202609', '202610'):
        p = os.path.join(b, f'{code}_{ym}.json')
        if os.path.exists(p): continue
        rows = R.fetch('rent', code, ym)
        json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
        print('B', code, ym, len(rows), flush=True)
