# bigwa1006 본문 표 2장 — yangdo1006 mkimg 틀. firemap-write 2026-10-06
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows=[['65세 이상 대상','나이만 맞으면','65세 이상 + 기초연금 수급자'],['가입 기한','2025년 12월 31일','2028년 12월 31일'],['한도(1명)','5천만원','5천만원'],['장애인·유공자 등','가입 가능','그대로 가입 가능'],['작년까지 든 통장','—','만기까지 예전 규정']]
B.table('pkg/img/01.png','비과세종합저축, 2026년부터 달라진 것',['항목','2025년까지','2026년부터'],rows,hl_col=2,
        note='기초연금 수급자 = 지금 기초연금을 받고 있는 사람 · 금융소득종합과세 대상자는 예나 지금이나 제외',src='조세특례제한법 제88조의2, 부칙(제21223호) 제41조')
rows2=[['1년 이자','166만5천원','166만5천원'],['세금 15.4%','25만6천원','0원'],['손에 쥐는 돈','140만9천원','166만5천원']]
B.table('pkg/img/02.png','5천만원 1년 맡기면 손에 쥐는 이자',['','일반 예금','비과세종합저축'],rows2,hl_col=2,
        note='세전 연 3.33%(1년 정기예금 기본금리 중간값) · 단리',src='금융감독원 금융상품통합비교공시 2026년 9월, 소득세법 제129조')
json.dump({'01.png':{'rows':rows},'02.png':{'rows':rows2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok')
