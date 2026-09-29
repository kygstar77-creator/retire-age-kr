# 인천 오피스텔 9월 매매·전월세 실거래 수집 — rtmolit.fetch 재사용
import sys, os, json; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work'); sys.stdout.reconfigure(encoding='utf-8')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import rtmolit as R
IC={'28125':'','28155':'','28177':'미추홀구','28185':'연수구','28200':'남동구','28237':'부평구','28245':'계양구','28275':'','28290':'','28710':'강화군'}
out={}
for c,n in IC.items():
    for k in ('offi_trade','offi_rent'):
        for ym in ('202609','202608'):
            try: rows=R.fetch(k,c,ym)
            except Exception as e: print('실패',c,k,ym,e); rows=[]
            out[f'{c}_{ym}_{k}']=rows
    print(n, len(out[f'{c}_202609_offi_trade']), len(out[f'{c}_202609_offi_rent']))
json.dump({'sgg':IC,'data':out},open('raw.json','w',encoding='utf-8'),ensure_ascii=False)
