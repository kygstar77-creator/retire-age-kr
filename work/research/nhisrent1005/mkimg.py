import sys, json; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
def w(n):
    s=f'{n:,}'; return s
def man(n):
    a,b=divmod(n,10000); return (f'{a}만 ' if a else '')+(f'{b:,}원' if b else '원') if b else f'{a}만원'
from calc import prem
def mm(n):
    a,b=divmod(n,10000)
    return (f'{a}억 ' if a else '')+(f'{b:,}만원' if b else '')
    
SRC='국민건강보험법 시행령 별표 4·시행규칙 별표 8 대입 계산(2026-10-05)'
rows=[]
for label,gp in (('1억원 이하',10000),('1억 5,000만원',15000),('2억원',20000),('3억원',30000),('4억원',40000),('5억 4,000만원',54000),('7억원',70000),('9억원',90000)):
    a=prem(0,gp); b=prem(750000,gp)
    rows.append([label, f"{a['pts']}점", man(a['total']), man(b['total'])])
B.table('pkg/img/01.png','집 있는 퇴직자, 재산세 과세표준별 월 건강보험료',['과세표준','재산 점수','소득 없음','연금 월 150만원'],rows,hl_col=2,
        note='지역가입자 1인 · 장기요양보험료 포함 · 자동차 제외 · 10원 미만 버림',src=SRC)
rows2=[]
for label,dep,mon in (('전세 3억원',30000,0),('보증금 1억원 + 월세 100만원',10000,100),('전세 5억원',50000,0),('보증금 5억원 + 월세 100만원',50000,100),('전세 7억원',70000,0)):
    ev=(dep+mon*40)*0.3; a=prem(0,ev)
    rows2.append([label, mm(int(ev)), f"{a['pts']}점", man(a['total'])])
B.table('pkg/img/02.png','집이 없는 퇴직자, 전월세 보증금별 월 건강보험료',['임차 조건','재산 평가액','재산 점수','소득 없음 월 보험료'],rows2,hl_col=3,
        note='평가액 = (보증금 + 월세 × 40) × 30% · 지역가입자 1인 · 장기요양보험료 포함',src=SRC)
json.dump({'01.png':{'cols':['과세표준','재산 점수','소득 없음','연금 월 150만원'],'rows':rows},'02.png':{'cols':['임차 조건','재산 평가액','재산 점수','소득 없음 월 보험료'],'rows':rows2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(rows); print(rows2)
