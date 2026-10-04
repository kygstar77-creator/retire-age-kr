import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
from calc import couple, BASE
def man(n):
    a,b=divmod(n,10000); return f'{a}만원' if not b else (f'{a}만 {b:,}원' if a else f'{b:,}원')
SRC='기초연금법 제8조·시행령 제11조 대입 계산(2026-10-05)'
rows=[['혼자 받을 때',man(BASE),'-'],['부부 중 한 명만 받을 때',man(BASE),'20% 감액 없음'],['부부가 둘 다 받을 때',man(couple(0)[1]),f'1인 {man(couple(0)[0])}']]
B.table('pkg/img/01.png','2026년 기초연금 월액, 누가 받느냐에 따라',['경우','월 받는 돈(합계)','비고'],rows,hl_col=1,
        note='기준연금액 34만 9,700원 · 국민연금 연계감액 없는 경우 · 소득역전방지 감액 전',src=SRC)
rows2=[]
for x in (3000000,3392480,3500000,3700000,3900000):
    rows2.append([man(x),man(couple(x)[1])])
B.table('pkg/img/02.png','부부 소득인정액별 기초연금 부부 합계',['부부 소득인정액(월)','부부 합계(월)'],rows2,hl_col=1,
        note='부부 선정기준액 395만 2,000원 · 최저 부부 6만 9,940원 · 연계감액 없는 경우',src=SRC)
json.dump({'01.png':{'rows':rows},'02.png':{'rows':rows2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(rows);print(rows2)
