# 2026-10-22 firemap-write: 서울 25개 구 아파트 매매 실거래(해제 포함) 2025-07~2026-10 받기 (rtmolit.fetch)
import sys, os, json, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
sys.stdout.reconfigure(encoding='utf-8')
import rtmolit
HERE = os.path.dirname(os.path.abspath(__file__))
sgg = json.load(open(os.path.join(HERE, '..', 'seoul_sgg.json'), encoding='utf-8'))
months = ['202507','202508','202509','202510','202511','202512','202601','202602','202603','202604','202605','202606','202607','202608','202609','202610']
for lawd in sgg:
    for ym in months:
        p = os.path.join(HERE, 'raw', f'{lawd}_{ym}_trade.json')
        if os.path.exists(p): continue
        try:
            rows = rtmolit.fetch('trade', lawd, ym)
            json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
            print(lawd, ym, len(rows), flush=True)
        except Exception as e:
            print(lawd, ym, 'FAIL', e, flush=True)
        time.sleep(0.2)
print('done')
