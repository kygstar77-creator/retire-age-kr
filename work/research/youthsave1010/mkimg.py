# youthsave1010 본문 표 — schdacct1007 mkimg 틀. firemap-write 2026-10-10
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows=[['도약계좌 총급여 2,400만 이하','2만 7,000원','60개월','162만원'],
      ['도약계좌 총급여 3,600만 이하','2만 3,000원','60개월','138만원'],
      ['도약계좌 총급여 4,800만 이하','1만 8,500원','60개월','111만원'],
      ['도약계좌 총급여 6,000만 이하','1만 5,000원','60개월','90만원'],
      ['미래적금 일반형 6%','3만원','36개월','108만원'],
      ['미래적금 우대형 12%','6만원','36개월','216만원']]
B.table('pkg/img/01.png','월 50만원 넣을 때 정부기여금',['상품·소득 구간','월 기여금','기간','합계'],rows,hl_col=3,
        note='정부기여금만 비교 · 이자 제외 · 도약계좌는 2025년 1월 납입분 기준표 · 기간과 원금이 달라 같은 조건 비교 아님',src='금융위원회 2026-10-07·2024-12-26 보도자료, 서민금융진흥원')
json.dump({'01.png':{'rows':rows}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok')
