import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows=[['달러 금값 (금 선물)','3,897.5 → 4,156.8달러/온스','+6.65%'],['원/달러 환율','1,406.0 → 1,358.5원','-3.38%'],['KRX 웃돈 (어림)','+6.3% → -1.4%','-7.26%'],['KRX 금 (세 가지 곱)','187,300 → 179,000원/g','-4.43%']]
B.table('pkg/img/01.png','2025-10-02에 산 금, 2026-10-06에 팔면',['무엇이','얼마에서 얼마로','변한 정도(비율)'],rows,hl_col=2,note='달러 금값은 산·판 날 전날(10/1, 10/5) 뉴욕 종가 · 웃돈 칸 -7.26%는 6.3과 -1.4를 뺀 값이 아니라 비율로 따진 값 · 세 가지는 곱해서 -4.43%',src='네이버 증권 · 야후 파이낸스 · 한국은행 ECOS · 파이어맵 계산',W=900)
json.dump({'01.png':{'rows':rows}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)

