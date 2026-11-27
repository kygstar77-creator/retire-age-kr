# elsjeonse1129 — 국토부 아파트 매매·전월세 실거래 서울 송파구(11710) 2025-06~2026-11 계약월 받기
#   py -3.12 work/research/elsjeonse1129/fetch.py → raw/11710_<월>_{trade,rent}.json
import os, sys, json, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'raw'); os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '..', '..')))
import rtmolit
print('받은 시각', datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
yms = []
y, m = 2025, 6
while (y, m) <= (2026, 11):
    yms.append(f'{y}{m:02d}'); m += 1
    if m == 13: y, m = y + 1, 1
for ym in yms:
    for kind in ('trade', 'rent'):
        rows = rtmolit.fetch(kind, '11710', ym)
        json.dump(rows, open(os.path.join(OUT, f'11710_{ym}_{kind}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        els = [r for r in rows if '엘스' in r.get('aptNm', '')]
        print(ym, kind, len(rows), '엘스', len(els), flush=True)
