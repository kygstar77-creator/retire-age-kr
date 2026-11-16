# KOSPI 일별 종가 — 한국은행 ECOS 802Y001/0001000 (원자료 KRX). 키는 apis.key로만 읽고 출력하지 않는다.
import json, sys
sys.path.insert(0, r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
import apis
rows = []
for y0, y1 in [(1995,2002),(2003,2010),(2011,2018),(2019,2026)]:
    r = apis.ecos('802Y001','D',f'{y0}0101',f'{y1}1231','0001000',3000)
    rows += [(t, float(v)) for t, v, _ in r]
rows = sorted(set(rows))
json.dump(rows, open('kospi_daily_ecos.json','w'), ensure_ascii=False)
print(len(rows), rows[0], rows[-1])
