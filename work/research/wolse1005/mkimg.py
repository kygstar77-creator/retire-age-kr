import sys, json; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
SRC='조세특례제한법 제95조의2 · 정책브리핑 2026-08-13 세제개편안'
T1=[('총급여 5,500만원 이하','170만원','204만원'),('5,500만원 초과 · 35세 이상','150만원','180만원'),('5,500만원 초과 · 15~34세','150만원','204만원')]
B.table('pkg/img/01.png','월세 월 100만원, 공제액 비교',['총급여 구간','현행(한도 1,000만원)','개편안(한도 1,200만원)'],[list(x) for x in T1],hl_col=2,
        note='월세 연 1,200만원 · 종합소득금액 조건 별도 · 개편안은 정부안(국회 심의 전)',src=SRC)
T2=[('월 60만원','122만 4,000원','122만 4,000원'),('월 80만원','163만 2,000원','163만 2,000원'),('월 100만원','170만원','204만원'),('월 120만원','170만원','204만원')]
B.table('pkg/img/02.png','월세별 공제액(공제율 17% 기준)',['월세','현행','개편안'],[list(x) for x in T2],hl_col=2,
        note='공제율 17% · 월세 12개월 기준 · 개편안은 정부안',src=SRC)
import json
json.dump({'01.png':{'cols':['총급여 구간','현행','개편안'],'rows':[list(x) for x in T1]},'02.png':{'cols':['월세','현행','개편안'],'rows':[list(x) for x in T2]}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok')
