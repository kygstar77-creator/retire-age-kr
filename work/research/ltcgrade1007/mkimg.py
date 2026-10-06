# ltcgrade1007 본문 표 2장 — pensavbreak1007 mkimg 틀. firemap-write 2026-10-06
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows=[['1등급','95점 이상','251만2,900원','37만6,935원'],['2등급','75~95점 미만','233만1,200원','34만9,680원'],['3등급','60~75점 미만','152만8,200원','22만9,230원'],
      ['4등급','51~60점 미만','140만9,700원','21만1,455원'],['5등급','45~51점 미만(치매)','120만8,900원','18만1,335원'],['인지지원','45점 미만(치매)','67만6,320원','10만1,448원']]
B.table('pkg/img/01.png','장기요양등급별 집에서 받는 서비스 한도',['등급','점수','한 달 한도','다 쓰면 내는 돈(15%)'],rows,hl_col=2,
        note='재가급여(복지용구 제외) 월 한도, 2026.1.1. 기준',src='국민건강보험공단, 노인장기요양보험법 시행령 제7조·제15조의8')
rows2=[['2등급','233만1,200원','0원','34만9,680원'],['3등급','152만8,200원','80만3,000원','103만2,230원']]
B.table('pkg/img/02.png','같은 서비스 233만원어치를 쓰면',['등급','한도','한도 넘는 돈','본인이 내는 돈'],rows2,hl_col=3,
        note='한도 안은 15%, 넘는 돈은 전액 본인부담',src='노인장기요양보험법 제40조, 국민건강보험공단 월 한도액')
json.dump({'01.png':{'rows':rows},'02.png':{'rows':rows2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok')
