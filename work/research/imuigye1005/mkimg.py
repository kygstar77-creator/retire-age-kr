import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
from calc import prem
from calc2 import imui
def man(n):
    a,b=divmod(n,10000); return f'{a}만원' if not b else (f'{a}만 {b:,}원' if a else f'{b:,}원')
SRC='국민건강보험법 제110조·시행령 별표 4 대입 계산(2026-10-05)'
rows=[]
for x in (2000000,3000000,4000000,5000000,6000000,8000000):
    h,l,t=imui(x); rows.append([f'{x//10000}만원',man(h),man(l),man(t)])
B.table('pkg/img/01.png','임의계속가입 월 보험료, 평균 보수월액별',['평균 보수월액','건강보험료','장기요양','합계'],rows,hl_col=3,
        note='보수월액 × 7.19% + 장기요양 0.9448% · 본인 전액 부담 · 10원 미만 버림 · 상하한·경감 제외',src=SRC)
BR={20000:157,30000:200,40000:228,54000:258,70000:287,90000:310}
rows2=[]
for label,gp in (('2억원',20000),('3억원',30000),('4억원',40000),('5억 4,000만원',54000),('7억원',70000),('9억원',90000)):
    a=prem(0,gp); rows2.append([label,man(a['total']),f'{BR[gp]}만원 이하'])
B.table('pkg/img/02.png','지역가입자 월 보험료와 임의계속이 더 싼 경우',['재산세 과세표준','지역가입자 월 보험료','임의계속이 더 싼 보수월액'],rows2,hl_col=2,
        note='지역가입자 1인 · 소득 없음 · 자동차 제외 · 장기요양 포함 · 10원 미만 버림',src=SRC)
json.dump({'01.png':{'rows':rows},'02.png':{'rows':rows2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(rows);print(rows2)
