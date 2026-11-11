import sys,json,statistics as st
sys.path.insert(0,'../..'); import apis
r=apis.finlife_all('deposit','020000')
json.dump(r,open('raw/finlife_bank_1111.json','w',encoding='utf-8'),ensure_ascii=False)
print(type(r), len(r)); print(json.dumps(r[0],ensure_ascii=False)[:600])
