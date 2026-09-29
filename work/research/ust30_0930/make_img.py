# 미국 30년 국채 금리 카페 이미지. 실행: PYTHONPATH=work py -3.12 work/research/ust30_0930/make_img.py
import os, csv
from blogimg import line, table
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, 'pkg', 'img'); os.makedirs(D, exist_ok=True)
r = list(csv.DictReader(open(os.path.join(H, 't26.csv'))))[::-1]
xs = [x['Date'][:5].replace('/', '.') for x in r]; ys = [float(x['30 Yr']) for x in r]
line(os.path.join(D, '01.png'), '미국 30년 국채 금리, 올해 움직임', xs, ys,
     marks=[(0, 4.86, '1월 2일 4.86%', 'ink'), ('02.27', 4.64, '2월 27일 4.64%', 'ink'), (len(xs) - 1, 5.56, '9월 28일 5.56%', 'red')],
     unit='%', src='출처: 미 재무부 일별 국채 금리표 (종가 기준, 9월 28일까지)')
table(os.path.join(D, '02.png'), '만기별 미국 국채 금리, 연초와 지금',
      ['만기', '1월 2일', '9월 28일', '오른 폭'],
      [['2년', '3.47%', '4.92%', '+1.45%p'], ['10년', '4.19%', '5.24%', '+1.05%p'], ['30년', '4.86%', '5.56%', '+0.70%p']],
      hl_col=3, src='출처: 미 재무부 일별 국채 금리표')
table(os.path.join(D, '03.png'), '미국 30년 고정 주택담보대출 금리',
      ['시점', '금리'],
      [['1년 전 (2025.9.25)', '6.30%'], ['올해 최저 (2.26)', '5.98%'], ['최근 (9.24)', '7.03%']],
      hl_col=1, src='출처: 프레디맥 주간 조사(PMMS), 세인트루이스 연준 FRED')
