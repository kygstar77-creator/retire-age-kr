# npsimui1007 본문 표 2장 — bigwa1006 mkimg 틀. firemap-write 2026-10-06
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows=[['10년','1,154만7,600원','22만6,090원'],['15년','1,732만1,400원','33만9,140원'],['20년','2,309만5,200원','45만2,190원'],['30년','3,464만2,800원','67만8,290원']]
B.table('pkg/img/01.png','임의가입 최저 보험료로 낼 때 받는 연금',['낸 기간','낸 보험료 합계','매달 받는 연금'],rows,hl_col=2,
        note='월 보험료 9만6,230원(기준소득 101만3천원 × 9.5%, 10원 미만 버림)을 계속 낸다고 본 값 · 2026년 A값 기준',src='국민연금공단 중앙노후준비지원센터 예상연금월액표')
rows2=[['2026년','9.5%','9만6,230원'],['2027년','10%','10만1,300원'],['2030년','11.5%','11만6,490원'],['2033년부터','13%','13만1,690원']]
B.table('pkg/img/02.png','보험료율이 오르면 매달 내는 돈',['해','보험료율','기준소득 101만3천원일 때'],rows2,hl_col=2,
        note='10원 미만 버림 · 기준소득은 2026년 4월 기준 값',src='국민연금법 제88조·부칙(2026~2032년 보험료율), 국민연금공단 가입 안내')
json.dump({'01.png':{'rows':rows},'02.png':{'rows':rows2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok')
