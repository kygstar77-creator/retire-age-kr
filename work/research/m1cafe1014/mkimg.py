# m1cafe1014 본문 그림 — w1cafe1013 mkimg 틀 · 숫자는 M-1 facts [J1][K1][S1]·calc_out만
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1=[['JEPQ (매달)','0.46572달러 (26년 2월)','0.70497달러 (26년 8월)','1.51배'],['ACE 미국배당다우존스 (매달)','21원 (25년 11월)','53원 (25년 12월)','2.52배'],['SCHD (3달에 한 번)','—','—','1년 4회']]
B.table('pkg/img/01.png','지난 12번 분배금, 한 주당 가장 적은 달과 많은 달',['상품','가장 적은 달','가장 많은 달','차이'],r1,hl_col=3,
        note='JEPQ는 배당락일 기준(2025.11~2026.10), ACE는 지급기준일 기준(2025.10~2026.09)',src='나스닥 배당 이력 · 한국투자신탁운용 ACE 분배 내역 · 찰스 슈왑')
json.dump({'01.png':{'rows':r1}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
B.bignum('pkg/img/02.png','ACE 미국배당다우존스로 매달 100만원(세금·건보료 뒤), 가장 적게 나온 달 기준','8.92억원',sub='평균 기준 5.10억원의 1.75배',src='2026.10.2 종가·지난 12회 분배로 계산 · 2천만원 넘는 추가 세금 빼서 최소값')
