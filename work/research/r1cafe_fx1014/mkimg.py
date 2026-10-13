# r1cafe_fx1014 본문 그림 — m1stot1013 mkimg 틀(blogimg.table) · 숫자는 R-1 facts·calc2_out만
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1=[['2025-10-02 산 날','1,406.0원','100,000,000원'],['2026-07-02 환율 최고','1,554.4원','123,037,245원'],['2026-09-10 환율 최저','1,337.9원','107,755,946원'],['2026-10-02 판 날','1,359.6원','111,210,188원']]
B.table('pkg/img/01.png','S&P500 ETF(SPY) 1억, 언제 꺼냈느냐에 따라 (원화)',['날짜','원/달러 환율','SPY 1억의 원화 값'],r1,hl_col=2,
        note='분배금 빼고 가격만 · 환전 수수료 넣지 않음 · 지난 기록',src='한국은행 ECOS 731Y001 · 야후 파이낸스 종가')
json.dump({'01.png':{'rows':r1}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
B.bignum('pkg/img/02.png','2026년 7월 2일 → 9월 10일(70일) SPY 1억의 원화 값','−1,528만원',sub='달러 가격 744.78 → 757.83달러(+1.75%) · 환율 1,554.4 → 1,337.9원(−13.93%)',src='야후 파이낸스 종가 · 한국은행 ECOS 731Y001')
