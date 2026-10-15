# deposit1016 본문 그림 — 숫자는 calc_out.txt·finlife_deposit.json만
import sys, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows = [['농협 NH올원e예금', '3.65% · 30만 9천원', '3.65% · 30만 9천원'], ['우리 WON플러스예금', '3.60% · 30만 5천원', '3.60% · 30만 5천원'],
        ['하나 하나의정기예금', '2.30% · 19만 5천원', '3.60% · 30만 5천원'], ['신한 쏠편한 정기예금', '2.55% · 21만 6천원', '3.50% · 29만 6천원'],
        ['국민 KB Star 정기예금', '2.40% · 20만 3천원', '3.50% · 29만 6천원']]
B.table('pkg/img/01.png', '12개월 정기예금 1천만원, 세후 이자', ['상품', '공시 저축 금리 · 이자', '공시 최고우대금리 · 이자'], rows, hl_col=2,
        src='금융감독원 금융상품통합비교공시 9월분 · 단리, 세금 15.4% 뗀 값 · 파이어맵 계산', W=1640)
B.bignum('pkg/img/02.png', '하나의정기예금, 공시 금리 두 칸 사이 1년 세후 이자 차이', '약 11만원', sub='연 2.3%와 3.6% · 1천만원 12개월 · 우대 조건란은 해당사항없음',
         src='금융감독원 금융상품통합비교공시 9월분 · 단리, 세금 15.4%')
