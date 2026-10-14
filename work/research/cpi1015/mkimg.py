# cpi1015 본문 표 그림 — 숫자는 calc_out.txt(FRED BLS 지수)만
import sys, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows=[['1월','2.4%','2.5%','-0.1%'],['2월','2.4%','2.5%','0.5%'],['3월','3.3%','2.6%','12.5%'],['5월','4.2%','2.9%','23.5%'],['8월','3.4%','2.4%','16.3%'],['9월','3.7%','2.6%','20.4%']]
B.table('pkg/img/01.png','미국 소비자물가 1년 전 대비 상승률, 2026년',['달','전체','근원(식품·에너지 제외)','에너지'],rows,hl_col=1,src='미국 노동통계국 CPI-U(계절조정 전) · FRED 2026.10.15 조회 · 파이어맵 계산',W=1640)
B.bignum('pkg/img/02.png','9월 한 달 동안 오른 폭(전월 대비, 계절조정)','휘발유 9.1%',sub='에너지 5.2% · 전체 물가 0.6% · 근원물가 0.3%',src='미국 노동통계국 CPI-U 계절조정 지수 · FRED 2026.10.15 조회 · 파이어맵 계산')
