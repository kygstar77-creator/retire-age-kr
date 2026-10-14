import sys, os, json, io, zipfile, urllib.request, re
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
import apis
k=apis.key('dart')
cc='00126362'
u=f'https://opendart.fss.or.kr/api/company.json?crtfc_key={k}&corp_code={cc}'
print(apis._j(u))
out={}
for y in (2024,2025,2026):
    for rc in ('11013','11012','11014','11011'):
        u=f'https://opendart.fss.or.kr/api/fnlttSinglAcnt.json?crtfc_key={k}&corp_code={cc}&bsns_year={y}&reprt_code={rc}'
        d=apis._j(u)
        if d.get('status')!='000': print(y,rc,d.get('status'),d.get('message')); continue
        out[f'{y}_{rc}']=d['list']
        for x in d['list']:
            if x['fs_div']=='CFS' and x['account_nm'] in ('매출액','영업이익','당기순이익','당기순이익(손실)','영업이익(손실)'):
                print(y,rc,x['account_nm'],x['thstrm_nm'],x['thstrm_amount'],x.get('thstrm_add_amount'),x.get('rcept_no'))
json.dump(out,open('dart_fin.json','w',encoding='utf-8'),ensure_ascii=False)
