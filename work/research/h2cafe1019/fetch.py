# h2cafe1019 올리기 전 확인 — 국토부 아파트 매매·전월세 실거래 다시 받기(2026-10-19 밤). rtmolit.fetch 그대로.
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.stdout.reconfigure(encoding='utf-8')
import rtmolit
H = os.path.dirname(os.path.abspath(__file__))
for lawd in ('11680', '11710', '11650'):
    for ym in ('202608', '202609', '202610'):
        for kind in ('trade', 'rent'):
            rows = rtmolit.fetch(kind, lawd, ym)
            json.dump(rows, open(os.path.join(H, 'raw', f'{lawd}_{ym}_{kind}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
            print(lawd, ym, kind, len(rows))
