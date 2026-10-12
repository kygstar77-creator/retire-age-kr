# w1cafe1013 본문 그림 — c1cafe1011 mkimg 틀(blogimg.table) · 숫자는 W-1 calc_out만
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1=[['삼성전자 100주','2,760만원 → 2,620만원','−140만원 (−5.07%)'],['코스피 그대로 1천만원','1천만원 → 946만원','−53만 9,440원 (−5.39%)'],['미국 SPY 1만 달러','1,359.6만원 → 1,354.7만원','원화 −4만 9,138원 (달러 +1.16%)']]
B.table('pkg/img/01.png','10월 2일 → 8일 (SPY만 9일 종가)',['가진 것','평가액','바뀐 것'],r1,hl_col=2,
        note='평가액 기준(팔지 않으면 확정 아님) · 수수료·보수 뺌 · SPY는 10월 9일 종가, 환율은 10월 8일 매매기준율',src='야후 파이낸스 종가 · 한국은행 ECOS 코스피·원달러')
json.dump({'01.png':{'rows':r1}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
B.bignum('pkg/img/02.png','삼성전자 100주, 사흘 평가액 감소 ÷ 2분기 배당금(세후 3만 1,640원)','44번치',sub='−140만원 = 분기 배당 44.2번치',src='DART 배당결정 공시·야후 파이낸스 종가로 계산')
