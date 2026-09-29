# 내부자 매수 카페 이미지. 실행: PYTHONPATH=work py -3.12 work/research/insider0930/make_img.py
import os
from blogimg import table
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pkg', 'img'); os.makedirs(D, exist_ok=True)
S = '출처: SEC EDGAR Form 4 (9/28~29 접수), 주가 9/28 종가'
table(os.path.join(D, '01.png'), '이번 주 임원이 직접 산 금액 순위',
      ['회사', '산 사람', '금액'],
      [['인히브릭스(INBX)', 'CEO', '99.9만 달러'], ['인피니티(INR)', 'CFO', '30.0만 달러'],
       ['다모라(DMRA)', 'CEO', '25.3만 달러'], ['데이브앤버스터스(PLAY)', '임시 CFO', '2.6만 달러']], hl_col=2, src=S)
table(os.path.join(D, '02.png'), '두경부암 2상 결과 (9월 8일 발표)',
      ['', '키트루다만', '같이 쓴 쪽'],
      [['반응한 비율', '26.5%', '48.3%'], ['악화 없이 버틴 기간(중앙값)', '4.9개월', '9.6개월']],
      hl_col=2, src='출처: 인히브릭스 보도자료 (2026-09-08), 평가 환자 63명')
table(os.path.join(D, '03.png'), '산 값과 지금 주가',
      ['회사', '산 값', '9/28 종가', '1년 고점 대비'],
      [['인히브릭스', '99.88달러', '101.71달러', '-28%'], ['인피니티', '13.44달러', '12.53달러', '-35%'],
       ['다모라', '20.23달러', '20.75달러', '-39%'], ['데이브앤버스터스', '6.50달러', '6.41달러', '-70%']],
      hl_col=3, src='출처: SEC Form 4, 야후 파이낸스 (2026-09-28 미국 종가)')
