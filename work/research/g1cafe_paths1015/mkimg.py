import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows=[['낸 돈','10,000,000원','10,000,000원','10,000,000원'],['그중 금값 몫','10,000,000원','-','9,090,909원'],['1년 뒤 받는 돈','9,556,861원','9,472,686원','8,688,055원'],['달라진 폭','-4.43%','-5.27%','-13.12%']]
B.table('pkg/img/01.png','같은 날(2025-10-02) 산 금 1천만원, 2026-10-06에 팔면',['','KRX 금시장','금 ETF','골드바(어림)'],rows,hl_col=1,note='골드바는 금값 몫이 KRX 금값만큼 움직였다고 본 어림 · 모든 수수료·되팔 때 값 차이 제외 · 지난 기록',src='네이버 증권 KRX 금 종가 · 야후 파이낸스 · 파이어맵 계산')
json.dump({'01.png':{'rows':rows}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
B.bignum('pkg/img/02.png','KRX 금시장 956만원 − 골드바 869만원','868,806원',sub='골드바 금 몫이 낸 돈의 90.9%뿐 · 같은 -4.43% 적용한 어림',src='국가법령정보센터 · 파이어맵 계산')
