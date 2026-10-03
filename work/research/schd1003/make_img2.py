import sys; sys.path.insert(0, r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
import blogimg as B
P = r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work/research/schd1003/pkg/img/'
B.table(P+'02.png', 'SCHD 배당률, 1년 새 어떻게 달라졌나',
        ['언제 기준', '최근 1년 배당 ÷ 주가'],
        [['1년 전 10월 1일 주가로', '3.76%'],
         ['올해 10월 1일 주가로', '3.23%'],
         ['1년 전에 산 사람(산 가격 기준)', '3.83%']],
        hl_col=1, src='슈왑 자산운용 SCHD 분배금 내역 · 종가 야후 파이낸스')
