import sys; sys.path.insert(0, r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
import blogimg as B
P = r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work/research/deadfin1003/pkg/img/'
SRC = '행정안전부·금융위원회 보도자료(2026년 9월 7일)'
B.table(P+'01.png', '사망자 계좌, 무엇이 막히고 무엇은 되나',
        ['거래', '사망신고 다음 날부터'],
        [['고인 명의 출금·금융거래', '정지'],
         ['입금', '계속된다'],
         ['치료비·장례비', '예외 인출로 병원·장례식장에 직접'],
         ['고인 계좌의 자동이체', '함께 멈출 수 있음'],
         ['그 밖의 돈', '상속 절차를 밟은 뒤']],
        src=SRC + ' · 조회 금융회사 4,890곳')
B.steps(P+'02.png', '장례비 예외 인출은 이렇게',
        [('가족관계증명서 같은 서류를 금융회사에 낸다', '필요한 서류는 거래하던 금융회사에 먼저 묻기'),
         ('금융회사가 확인한다', ''),
         ('병원·요양원·장례식장에 직접 보낸다', '유가족 통장으로는 들어오지 않는다')],
        src=SRC)
