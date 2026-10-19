import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1 = [['100만원', '연 4%', '0명'], ['150만원', '연 6%', '5명'], ['200만원', '연 8%', '6명'], ['300만원', '연 12%', '17명']]
B.table('pkg/img/01.png', '3억에서 매달 꺼낸 돈별, 37명 중 바닥난 사람', ['매달 꺼낸 돈', '3억 중 1년에', '바닥'], r1, hl_col=None,
        note='1989~2025년 해마다 1월 시작 · 2025년 말까지 · 원화 기준', src='S&P500 총수익 지수 × 한국은행 원/달러 환율')
r2 = [['규칙 없이 월 200만원', '6명', '2011년 바닥'], ['1월 통장이 3억보다 적은 해만 월 100만원', '0명', '2025년 말 약 4억 9천만원']]
B.table('pkg/img/02.png', '1월에 통장 한 번 보는 규칙을 썼다면', ['꺼내는 법', '37명 중 바닥', '1998년 시작 정우 씨'], r2, hl_col=None,
        note='3억 · 1월 초 1년 치를 한 번에 팔기 · 정우 씨는 가상 인물', src='S&P500 총수익 지수 × 한국은행 원/달러 환율')
json.dump({'01.png': {'rows': r1}, '02.png': {'rows': r2}}, open('pkg/tables.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
