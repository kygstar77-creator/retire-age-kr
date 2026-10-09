# evoucher1009 본문 표 2장 — firemap-write 10/9
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1=[['1인','29만5,200원','4만700원','25만4,500원'],['2인','40만7,500원','5만8,800원','34만8,700원'],['3인','53만2,700원','7만5,800원','45만6,900원'],['4인 이상','70만1,300원','10만2천원','59만9,300원']]
B.table('pkg/img/01.png','에너지바우처 2026 세대원 수별 금액',['세대원','한 해 총액','여름 몫(9월까지)','빠지는 겨울 몫'],r1,hl_col=3,
        note='연탄쿠폰·연탄전환 바우처·긴급복지 연료비를 받으면 여름 몫만 인정(9월 30일까지 전기요금)',src='한국에너지공단 에너지바우처 지원기준 (2026.10.9 조회)')
r2=[['요금차감','도시가스·전기·지역난방 중 하나','고지서에서 자동으로 빠짐'],['국민행복카드','등유·LPG·연탄·전기·도시가스','가맹점에서 카드 결제(배달료 포함)']]
B.table('pkg/img/02.png','겨울 몫 쓰는 방법 (둘 중 하나)',['방식','쓸 수 있는 연료','쓰는 법'],r2,hl_col=0,
        note='은행 창구·공과금 수납기에서는 카드 사용 불가',src='한국에너지공단 에너지바우처 사용안내 (2026.10.9 조회)')
json.dump({'01.png':{'rows':r1},'02.png':{'rows':r2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
