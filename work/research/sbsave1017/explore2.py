import json, sys
sys.stdout.reconfigure(encoding='utf-8')
d = json.load(open('raw/finlife_saving_1017.json', encoding='utf-8'))
for g in ('020000','030300'):
    seen=0
    for b in d[g]['base']:
        if b['max_limit'] and seen<6:
            seen+=1; print(g, b['kor_co_nm'], b['fin_prdt_nm'], b['max_limit'], '|', (b['etc_note'] or '').replace('\n',' / ')[:200])
