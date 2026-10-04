import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
from calc import cases
SRC='국민연금공단 2026년 연금액 조정 공지(2026-01-13) · 국민연금법 제52조'
rows=[[n, f'{y:,}원', f'약 {round(y/12):,}원'] for n,y in cases]
B.table('pkg/img/01.png','2026년 부양가족연금, 가족 구성별',['가족 구성','연 금액','월로 나누면'],rows,hl_col=2,
        note='배우자 연 306,630원 · 자녀·부모 1명당 연 204,360원 · 2026년 1월분부터',src=SRC)
rows2=[['일찍 받기(조기노령연금)','1년에 6%씩 깎임','안 깎임'],['늦춰 받기(연기연금)','한 달에 0.6%씩 늘어남','연기 중 안 나옴·가산 없음'],
       ['일하면서 받기(소득 감액)','소득 따라 깎임','안 깎임'],['이혼 뒤 나누기(분할연금)','혼인 기간 몫을 나눔','나누지 않음']]
B.table('pkg/img/02.png','기본 연금은 달라지고 부양가족연금은 따로',['받는 방식','기본 연금','부양가족연금'],rows2,hl_col=2,
        note='법 제62·63·63조의2·64조 모두 부양가족연금액은 빼고 계산',src='국민연금법 제62조·제63조·제63조의2·제64조')
json.dump({'01.png':{'rows':rows},'02.png':{'rows':rows2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(rows)
