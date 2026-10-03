import sys; sys.path.insert(0, r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
import blogimg as B
P = r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work/research/pibu1003/pkg/img/'
SRC = '국민건강보험법 시행규칙 별표 1의2'
B.table(P+'01.png', '재산에 따라 달라지는 소득 기준',
        ['재산세 과세표준 합', '1년 소득 기준', '한 달로 치면'],
        [['5억 4천만원 이하', '2천만원 이하', '약 166만 6천원'],
         ['5억 4천만원 초과 9억원 이하', '1천만원 이하', '약 83만 3천원'],
         ['9억원 초과', '소득 없어도 탈락', '-']],
        hl_col=1, src=SRC)
B.table(P+'02.png', '피부양자 소득에 더하는 것',
        ['소득', '어떻게 보나'],
        [['국민연금 등 공적연금', '1년 받은 돈 전부'],
         ['근로소득', '더한다'],
         ['사업소득', '없어야 한다(등록 없으면 1년 500만원 이하는 없는 것으로)'],
         ['주택임대소득', '500만원 예외 없음'],
         ['분리과세 금융소득', '1년 1천만원 이하면 빼고, 넘으면 전부']],
        src=SRC)
