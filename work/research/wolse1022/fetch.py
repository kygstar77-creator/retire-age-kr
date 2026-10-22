# 서울 25개 구 아파트 전월세 실거래(국토부 RTMSDataSvcAptRent) — work/rtmolit.py 의 fetch 그대로 쓴다. 저장은 이 폴더 raw/ 에만.
import sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); W = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, W)
from rtmolit import fetch
sgg = json.load(open(os.path.join(W, 'research', 'seoul_sgg.json'), encoding='utf-8'))
months = sys.argv[1:] or ['202507', '202508', '202509', '202607', '202608', '202609']
for lawd, name in sgg.items():
    for ym in months:
        p = os.path.join(HERE, 'raw', 'rent', f'{lawd}_{ym}_rent.json')
        if os.path.exists(p): continue
        try:
            rows = fetch('rent', lawd, ym); json.dump(rows, open(p, 'w', encoding='utf-8'), ensure_ascii=False)
            print(name, ym, len(rows), time.strftime('%H:%M:%S'), flush=True)
        except Exception as e: print(name, ym, '실패', e, flush=True)
        time.sleep(0.2)
print('완료', time.strftime('%Y-%m-%d %H:%M:%S'))
