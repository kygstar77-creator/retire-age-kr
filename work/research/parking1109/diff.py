# 10/6 vs 11/9 저축은행 입출금자유예금 공시 비교 (parking1109, write 11/9 21시)
import json,sys,statistics as st
sys.stdout.reconfigure(encoding='utf-8')
def load(p):
    d=json.load(open(p,encoding='utf-8'))['ANYM_REC']
    return {(r['BANK_CODE'],r['FINAN_PROD_CODE']):r for r in d}
a=load('../parking1007/fsb_anym_20261006.json'); b=load('raw/fsb_anym_20261109.json')
def nm(r): return f"{r.get('FINAN_COMP_NAME') or r.get('BANK_NAME') or r['BANK_CODE']} {r['PRODUCT_NAME']}"
print('10/6',len(a),'11/9',len(b))
up=[];dn=[]
for k in b:
    if k in a:
        x,y=a[k],b[k]
        if (x['RATE_LOW'],x['RATE_HIGH'])!=(y['RATE_LOW'],y['RATE_HIGH']) or x['ETC_NOTE_MATTER']!=y['ETC_NOTE_MATTER']:
            print('CHG',nm(y),x['RATE_LOW'],x['RATE_HIGH'],'->',y['RATE_LOW'],y['RATE_HIGH'],'|',y['ETC_NOTE_MATTER'][:150].replace('\n',' '), '| 공시', y.get('FINAN_COMP_SUBMIT_DATE'))
print('NEW:')
for k in b:
    if k not in a: y=b[k]; print('NEW',nm(y),y['RATE_LOW'],y['RATE_HIGH'],'|',y['ETC_NOTE_MATTER'][:150].replace('\n',' '))
for k in a:
    if k not in b: print('GONE',nm(a[k]))
for lab,d in (('10/6',a),('11/9',b)):
    lo=[float(r['RATE_LOW']) for r in d.values()]; hi=[float(r['RATE_HIGH']) for r in d.values()]
    print(lab,'기본 중앙',st.median(lo),'최고 중앙',st.median(hi),'최고 최대',max(hi), '최고>=3', sum(h>=3 for h in hi))
