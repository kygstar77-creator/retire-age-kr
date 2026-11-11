import sys,json
sys.path.insert(0,'../..')
import apis
out={}
# 시장금리(월) 721Y001: 국고채3년 5020000 ; 예금은행 신규취급 정기예금 121Y002 BEABAA21? try candidates
out['ktb3_m']=apis.ecos('721Y001','M','200101','202610','5020000',n=400)
for it in ['BEABAA2','BEABAA21','BEABAA211']:
    r=apis.ecos('121Y002','M','200101','202610',it,n=400)
    if r: out['dep_'+it]=r
out['base_m']=apis.ecos('722Y001','M','200101','202610','0101000',n=400)
out['ktb3_d']=apis.ecos('817Y002','D','20260901','20261111','010200000',n=100)
json.dump(out,open('raw/ecos_1111.json','w',encoding='utf-8'),ensure_ascii=False)
for k,v in out.items(): print(k,len(v),v[:1],v[-2:])
