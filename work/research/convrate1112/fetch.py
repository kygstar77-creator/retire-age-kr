# 서울 25개 구 아파트 전월세 실거래 2026-08~10 (11/12 받음) — rtmolit.fetch 그대로
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
W = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, W)
import rtmolit as R
sgg = json.load(open(os.path.join(W, 'research', 'seoul_sgg.json'), encoding='utf-8'))
out = os.path.join(os.path.dirname(__file__), 'raw')
for code, name in sgg.items():
    for ym in ('202608', '202609', '202610'):
        p = os.path.join(out, f'{code}_{ym}.json')
        if os.path.exists(p): continue
        rows = R.fetch('rent', code, ym)
        json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
        print(code, name, ym, len(rows), flush=True)
