# deprise1010 finlife 정기예금 오늘 받기 + 10/04·10/06 저장분과 비교
import sys, json; sys.path.insert(0, '../..'); sys.stdout.reconfigure(encoding='utf-8')
import apis
for g in ('020000', '030300'):
    rows = []
    for p in range(1, 8):
        try: r = apis.finlife('deposit', g, p)
        except Exception as e: print('page', p, e); break
        if not r: break
        rows += r
    json.dump(rows, open(f'raw_{g}_1010.json', 'w', encoding='utf-8'), ensure_ascii=False)
    print(g, len(rows))
