import sys; sys.path.insert(0, r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
import blogimg as B
P = r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work/research/sevtax1003/pkg/img/'
B.steps(P+'02.png', '퇴직금 세금 계산 세 단계',
        [('다닌 햇수만큼 공제를 뺀다', '5년이면 500만원, 30년이면 7,000만원'),
         ('남은 돈 ÷ 다닌 햇수 × 12로 1년치 급여로 바꾼다', '여기서 한 번 더 공제를 빼고 세율을 매긴다'),
         ('그 세금 ÷ 12 × 다닌 햇수', '1년 미만 기간은 1년으로 센다')],
        src='소득세법 제48·55조')
