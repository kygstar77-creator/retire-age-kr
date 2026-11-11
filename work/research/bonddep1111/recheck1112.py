# 발행 당일(11/12) 올리기 전 확인 — finlife·ECOS 다시 받아 11/11 값과 비교
import sys,json,statistics as st
sys.path.insert(0,'../..'); import apis
r=apis.finlife_all('deposit','020000')
json.dump(r,open('raw/finlife_bank_1112.json','w',encoding='utf-8'),ensure_ascii=False)
def stats(rows):
    base=rows['baseList'] if isinstance(rows,dict) else None
    return rows
old=json.load(open('raw/finlife_bank_1111.json',encoding='utf-8'))
def twelve(d):
    out={}
    for o in d:
        if str(o.get('기간'))=='12':
            out[(o['은행'],o['상품'],o.get('금리유형'))]=(o.get('금리'),o.get('최고금리'),o.get('공시월'))
    return out
try:
    a,b=twelve(old),twelve(r)
except Exception as e:
    print('form',type(old),str(old)[:300]); raise
ba=[v[0] for v in a.values() if v[0] is not None]; bb=[v[0] for v in b.values() if v[0] is not None]
print('finlife 12개월 11/11',len(a),'중앙',st.median(ba),'최고',max(ba),'| 11/12',len(b),'중앙',st.median(bb),'최고',max(bb),'공시월',{v[2] for v in b.values()})
diff=[(k,a.get(k),b.get(k)) for k in set(a)|set(b) if a.get(k)!=b.get(k)]
print('바뀐 상품',len(diff)); [print(x) for x in diff[:10]]
d=apis.ecos('817Y002','D','20261101','20261112','010200000',n=30)
print('국고채3년 일별',d[-4:])
m=apis.ecos('121Y002','M','202607','202611','BEABAA211',n=10)
print('예금은행 정기예금 신규 월',m[-3:])
k=apis.ecos('722Y001','D','20261101','20261112','0101000',n=30)
print('기준금리',k[-2:])
json.dump({'ktb3_d':d,'dep_m':m,'base':k},open('raw/ecos_1112.json','w',encoding='utf-8'),ensure_ascii=False)
