# 코스닥·코스피 일별 종가 — 한국은행 ECOS 802Y001 (0089000 코스닥, 0001000 코스피; 원자료 KRX). 키는 apis가 읽고 출력하지 않는다.
import json, sys
sys.path.insert(0, r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
import apis
out = {}
for name, code in [('kosdaq','0089000'),('kospi','0001000')]:
    rows = []
    for y0, y1 in [(1995,2002),(2003,2010),(2011,2018),(2019,2026)]:
        r = apis.ecos('802Y001','D',f'{y0}0101',f'{y1}1231',code,3000)
        rows += [(t, float(v)) for t, v, _ in r]
    out[name] = sorted(set(rows))
    print(name, len(out[name]), out[name][0], out[name][-1])
json.dump(out, open('raw_ecos.json','w'), ensure_ascii=False)
