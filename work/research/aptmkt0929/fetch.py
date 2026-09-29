import sys,json,os
sys.path.insert(0,'.'); import rtmolit as r
C={'수원 장안':'41111','수원 권선':'41113','수원 팔달':'41115','수원 영통':'41117','성남 수정':'41131','성남 중원':'41133','성남 분당':'41135',
'용인 처인':'41461','용인 기흥':'41463','용인 수지':'41465','평택':'41220','안양 만안':'41171','안양 동안':'41173','광명':'41210','과천':'41290',
'오산':'41370','군포':'41410','의왕':'41430','안산 상록':'41271','안산 단원':'41273','화성':'41590'}
out={}
for n,c in C.items():
    for ym in ('202609','202608'):
        try: rows=r.fetch('trade',c,ym)
        except Exception as e: rows=None; print(n,ym,'ERR',e)
        out[f'{n}|{ym}']=rows
        print(n,ym,len(rows) if rows is not None else None, flush=True)
json.dump(out,open('research/aptmkt0929/raw.json','w',encoding='utf-8'),ensure_ascii=False)
