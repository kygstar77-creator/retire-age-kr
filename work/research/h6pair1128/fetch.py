# h6pair1128(H-6 은마 카페 짝 글) — 강남구(11680) 아파트 매매·전월세 2025.10~2026.11 국토부 실거래 다시 받아 raw/ 에 저장
import sys, os, json, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE,'..','..'))
import rtmolit
OUT=os.path.join(HERE,'raw')
MS=['202510','202511','202512','202601','202602','202603','202604','202605','202606','202607','202608','202609','202610','202611']
log=open(os.path.join(HERE,'fetch_log.txt'),'a',encoding='utf-8')
log.write(f'# {datetime.datetime.now():%Y-%m-%d %H:%M} 받음\n')
for m in MS:
    for k in ('trade','rent'):
        rows=rtmolit.fetch(k,'11680',m)
        json.dump(rows,open(os.path.join(OUT,f'11680_{m}_{k}.json'),'w',encoding='utf-8'),ensure_ascii=False)
        print(m,k,len(rows)); log.write(f'{m} {k} {len(rows)}\n')
