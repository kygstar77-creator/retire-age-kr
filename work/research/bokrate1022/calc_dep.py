# 금감원 금융상품 한눈에 정기예금 공시(2026-10-22 조회) — 기간별 기본금리 가운데 값
import json,statistics as st
from collections import defaultdict
d=json.load(open('raw/finlife_deposit_1022.json',encoding='utf-8'))
p=defaultdict(dict)
for r in d: p[(r['은행'],r['상품'])][r['기간']]=r
print('공시월',set(r['공시월'] for r in d),'상품',len(p),'은행',len(set(k[0] for k in p)))
for t in ['6','12','24','36']:
    v=[x[t]['금리'] for x in p.values() if t in x]; print(t,'개월 n',len(v),'기본 중앙',st.median(v))
