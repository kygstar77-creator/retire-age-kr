# ECOS 731Y001(주요국 통화의 대원화환율) 원/달러(0000001) 일별 — FRED DEXKOUS와 대조용. 키는 출력하지 않는다.
import json, sys
sys.path.insert(0, r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
import apis
k = apis.key('ecos')
rows = []
for a, b in (('20000101', '20101231'), ('20110101', '20261127')):
    d = apis._j(f'https://ecos.bok.or.kr/api/StatisticSearch/{k}/json/kr/1/10000/731Y001/D/{a}/{b}/0000001', t=60)
    rows += d['StatisticSearch']['row']
json.dump(rows, open('raw/ecos_731Y001_usd_1127.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(rows), rows[0]['TIME'], rows[-1]['TIME'], rows[-1]['DATA_VALUE'], rows[0].get('STAT_NAME'), rows[0].get('ITEM_NAME1'), rows[0].get('UNIT_NAME'))
