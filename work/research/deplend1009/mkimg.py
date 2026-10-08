# deplend1009 본문 표 2장 — earlyjob1007 mkimg 틀. firemap-write 2026-10-08
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
os.makedirs('pkg/img', exist_ok=True)
rows=[['우리 WON플러스','698,230원','1,020,861원','1,064,061원'],['하나의 정기예금','576,825원','972,299원','1,064,061원']]
B.table('pkg/img/01.png','5천만원 예금, 6개월 뒤 2천만원이 필요할 때',['','통째로 해지','2천만원 일부해지','예금담보대출'],rows,hl_col=3,
        note='2027년 4월 8일 기준 세후 이자 · 그대로 두면 두 곳 모두 1,522,800원',src='각 은행 상품설명서·10월 8일 고시 금리를 가입 금리로 가정 (2026.10.8 조회)')
rows2=[['기본이율 / 적용금리','3.60% / 3.60%','2.3% / 3.6%'],['6개월 지난 중도해지이율','연 약 1.26%','연 0.691%'],['일부해지 횟수','만기해지 포함 3회','만기 전 2회'],['예금담보대출 금리','수신금리 + 1.0%p','예금금리 + 1.0%p(영업점 1.2%p)']]
B.table('pkg/img/02.png','계산에 쓴 두 상품의 조건',['','우리 WON플러스','하나의 정기예금'],rows2,hl_col=None,
        note='중도해지이율은 기본이율에 구간 비율과 경과 비율을 곱한 값',src='우리은행 상품설명서(2026.7.16)·하나은행 공시(2025.8.26) (2026.10.8 조회)')
json.dump({'01.png':{'rows':rows},'02.png':{'rows':rows2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok')
