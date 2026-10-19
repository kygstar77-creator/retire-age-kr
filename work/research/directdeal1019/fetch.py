# directdeal1019 — 서울 25개 구 아파트 매매 실거래(국토부 RTMSDataSvcAptTradeDev) 2025-10~2026-10 새로 받기 (2026-10-19)
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(H, '..', '..'))
sys.path.insert(0, W)
import rtmolit
SGG = json.load(open(os.path.join(W, 'research', 'seoul_sgg.json'), encoding='utf-8'))
months = ['202510','202511','202512'] + [f'2026{m:02d}' for m in range(1, 11)]
n = 0
for code in SGG:
    for ym in months:
        p = os.path.join(H, 'raw', f'{code}_{ym}_trade.json')
        if os.path.exists(p): continue
        rows = rtmolit.fetch('trade', code, ym); n += 1
        json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
print('calls', n)
