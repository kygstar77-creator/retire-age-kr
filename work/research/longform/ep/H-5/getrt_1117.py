# H-5 실거래 다시 받기(11/17) — 인천 연수구 28185, 2025.06~2026.11 계약월 매매·전월세(신고 30일·해제 반영)
import os, sys, json
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); RT = os.path.join(HERE, 'raw', 'rt')
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..', '..', '..')))
import rtmolit
MONTHS = [f'2025{m:02d}' for m in range(6, 13)] + [f'2026{m:02d}' for m in range(1, 12)]
for ym in MONTHS:
    for kind in ('trade', 'rent'):
        p = os.path.join(RT, f'28185_{ym}_{kind}.json')
        rows = rtmolit.fetch(kind, '28185', ym)
        old = len(json.load(open(p, encoding='utf-8'))) if os.path.exists(p) else None
        json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
        print(ym, kind, old, '->', len(rows))
