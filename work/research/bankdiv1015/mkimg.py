# bankdiv1015 본문 그림 — 숫자는 calc_out.txt·facts.txt만
import sys, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows = [['BNK금융지주', '14,240원', '5.2%'], ['우리금융지주', '31,150원', '4.4%'], ['하나금융지주', '122,400원', '3.4%'], ['KB금융', '156,700원', '2.8%'], ['신한지주', '94,200원', '2.7%']]
B.table('pkg/img/01.png', '은행 지주회사 배당수익률 (작년 배당금 ÷ 오늘 종가)', ['회사', '10월 15일 종가', '배당수익률'], rows, hl_col=2,
        src='한국거래소 2026.10.15 종가 · DART 2025년 사업보고서 주당 현금배당금 · 파이어맵 계산', W=1640)
B.bignum('pkg/img/02.png', '10월 15일 하루 주가 변화', '코스피 −7.57%', sub='은행 지주 5곳은 −2.9% ~ +0.7%',
         src='코스피: 한국거래소(연합뉴스 보도) · 은행주: 한국거래소 종가 2026.10.14→10.15')
