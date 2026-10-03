import sys; sys.path.insert(0, r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
import blogimg as B
P = r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work/research/ubjob1003/pkg/img/'
SRC = '고용보험법 제10·40·48조'
B.table(P+'01.png', '65세 기준, 실업급여 받을 수 있나',
        ['경우', '실업급여'],
        [['65세 넘어 새로 고용', '적용 안 됨'],
         ['65세 넘어 자영업 시작', '적용 안 됨'],
         ['65세 전부터 가입 이어 계속 고용', '적용(다른 조건 따로)']],
        hl_col=1, src=SRC)
B.steps(P+'02.png', '실업급여, 나이 말고도 챙길 조건',
        [('그만두기 전 18개월 동안 피보험 단위기간 180일 이상', '고용보험에 가입해 임금을 받은 날'),
         ('그만둔 다음 날부터 12개월 안에만 지급', '신청을 미루면 남은 날수가 있어도 끝난다'),
         ('이직 사유', '정년·계약 만료는 정당한 사유, 자기 사정은 별표 2에 있어야')],
        numbered=False, src=SRC + ' · 시행규칙 별표 2')
