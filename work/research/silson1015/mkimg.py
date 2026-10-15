# silson1015 본문 그림 — 숫자는 facts.txt·calc_out.txt만
import sys, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows = [['그대로 두기', '178,489원', '약 643만원'], ['선택형 할인 특약(셋 다)', '107,093원', '약 386만원'], ['5세대로 전환(3년 할인)', '21,270원', '약 77만원']]
B.table('pkg/img/01.png', '1세대 실손 60대 여성, 3년 동안 내는 보험료', ['고르는 길', '월 보험료', '3년 합계'], rows, hl_col=2,
        src='금융위원회 2026.5.6 보도자료 예시(대형 손해보험사 6곳) · 보험료가 오르지 않는다고 가정 · 파이어맵 계산', W=1640)
B.bignum('pkg/img/02.png', '5세대 실손, 큰 병이 아닌 비급여 치료로 입원하면', '내 돈 50%', sub='예전(4세대)은 30% · 도수치료·체외충격파·비급여 주사는 보장 안 함',
         src='금융위원회 2026.5.6 보도자료 참고1(비중증 비급여 특약2) · 중증 특약은 30% 그대로')
