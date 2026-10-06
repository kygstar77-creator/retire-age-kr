# parking1007 본문 표 2장 — bigwa1006 mkimg 틀. firemap-write 2026-10-06
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows=[['저축은행 156개 가운데값','0.2%','7,050원'],['토스뱅크 통장','1.0%','35,250원'],['카카오뱅크 세이프박스(1억까지)','1.8%','63,450원'],['다올저축 Fi 저축예금','2.8%','98,700원'],['고려저축 보고파플러스','3.1%','109,275원']]
B.table('pkg/img/01.png','파킹통장 5천만원, 한 달 세후 이자',['통장','기본금리','한 달 이자'],rows,hl_col=2,
        note='세후 15.4% 뗀 값 · 1년 이자를 12로 나눔 · 금리는 변동',src='저축은행중앙회 입출금자유예금 공시·각 은행 상품안내 2026.10.6 조회')
rows2=[['200만원까지','최고 6%','12만원'],['나머지 4,800만원','기본 2%','96만원'],['5천만원 전체','2.16%','108만원']]
B.table('pkg/img/02.png','최고 6% 통장에 5천만원 넣으면',['금액','금리','1년 이자(세전)'],rows2,hl_col=1,
        note='대신저축은행 더더더파킹 · 첫 거래 고객 + 문자 수신 동의 유지 시',src='저축은행중앙회 입출금자유예금 공시 2026.10.6 조회')
json.dump({'01.png':{'rows':rows},'02.png':{'rows':rows2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok')
