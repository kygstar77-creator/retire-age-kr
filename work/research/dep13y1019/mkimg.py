import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1 = [['KB국민 KB Star', '3.6%', '2.6%'], ['신한 쏠편한', '3.5%', '2.6%'], ['하나 하나의정기예금', '3.6%', '2.7%'], ['우리 WON플러스', '3.6%', '2.7%'], ['농협 NH올원e', '3.65%', '2.7%']]
B.table('pkg/img/01.png', '5대 은행 정기예금, 1년이 3년보다 높다', ['상품', '1년', '3년'], r1, hl_col=None,
        note='최고금리(우대 포함) · 2026년 9월 공시 · 10월 19일 조회', src='금융감독원 금융상품 통합비교공시')
r2 = [['3년짜리 2.7% 한 번', '약 685만원', '기준'], ['1년짜리 3.6% 세 번', '약 942만원', '257만원 더'], ['1년짜리, 2년째부터 3.0%', '약 834만원', '149만원 더'], ['1년짜리, 2년째부터 2.5%', '약 745만원', '60만원 더'], ['1년짜리, 2년째부터 약 2.2%', '약 685만원', '같아짐']]
B.table('pkg/img/02.png', '1억을 3년 맡기면 세후 이자', ['넣는 법', '3년 이자', '3년짜리와'], r2, hl_col=None,
        note='우리은행 WON플러스예금 · 이자소득세 15.4% 뗌 · 1년짜리는 원금+이자 다시 넣기', src='금융감독원 공시 금리로 직접 계산')
json.dump({'01.png': {'rows': r1}, '02.png': {'rows': r2}}, open('pkg/tables.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
