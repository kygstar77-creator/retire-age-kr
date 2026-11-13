# 서울 25개 구 아파트 매매 실거래 2026-08~10 — 08월은 newold1112/raw(11/13 15시 받음) 복사, 09·10월은 11/13 23시 새로 받음(늦은 신고) — rtmolit.fetch 그대로
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
        rows = R.fetch('trade', code, ym)
        json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
        print(code, name, ym, len(rows), flush=True)
