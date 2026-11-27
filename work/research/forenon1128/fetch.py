# forenon1128 — 강동구(11740) 아파트 매매 2024.11~2026.11 국토부 실거래(rtmolit) 받아 raw/ 저장
import sys, os, json, datetime
sys.stdout.reconfigure(encoding='utf-8')
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE,'..','..'))
import rtmolit
OUT=os.path.join(HERE,'raw')
ms=[]; y,m=2024,11
while (y,m)<=(2026,11):
    ms.append(f'{y}{m:02d}'); m+=1
    if m==13: y,m=y+1,1
log=open(os.path.join(HERE,'fetch_log.txt'),'a',encoding='utf-8')
log.write(f'# {datetime.datetime.now():%Y-%m-%d %H:%M} 받음\n')
for mm in ms:
    rows=rtmolit.fetch('trade','11740',mm)
    json.dump(rows,open(os.path.join(OUT,f'11740_{mm}_trade.json'),'w',encoding='utf-8'),ensure_ascii=False)
    print(mm,len(rows)); log.write(f'{mm} trade {len(rows)}\n')
