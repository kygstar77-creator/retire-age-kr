# TQQQ·QLD 블로그 이미지. 실행: PYTHONPATH=work py -3.12 work/research/levetf/make_img.py (repo 루트에서)
import os
from blogimg import table, steps
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pkg', 'img')
os.makedirs(D, exist_ok=True)
SRC_P = '출처: ProShares 공식 펀드 페이지 TQQQ·QLD (2026-09-23 조회, NAV·시장가격은 2026-09-22 기준)'
SRC_Y = '출처: 거래소 시세·배당 기록 (Yahoo Finance chart API, 2026-09-23 조회)'

table(os.path.join(D, 'b1.png'), '1년 수익률과 산술 배수의 차이',
      ['상품', '일간 목표', '1년(배당 포함)', '산술 배수', '차이'],
      [['QQQ', '1배', '+24.53%', '-', '-'],
       ['QLD', '2배', '+41.33%', '+49.07%', '-7.74%p'],
       ['TQQQ', '3배', '+54.80%', '+73.60%', '-18.79%p']],
      [0.18, 0.16, 0.24, 0.21, 0.21], hl_col=2,
      note='2025년 9월 23일 종가 → 2026년 9월 21일 종가. 배당은 받은 것으로 넣었고 세금·거래비용은 넣지 않았다.', src=SRC_Y)

table(os.path.join(D, 'b2.png'), 'TQQQ와 QLD 기본 정보',
      ['항목', 'TQQQ', 'QLD'],
      [['운용사', 'ProShares', 'ProShares'],
       ['기초지수', 'Nasdaq-100 Index', 'Nasdaq-100 Index'],
       ['일간 목표', '3배', '2배'],
       ['설정일', '2010년 2월 9일', '2006년 6월 19일'],
       ['순자산', '401억 7,400만 달러', '153억 6,000만 달러'],
       ['순자산가치(9/22)', '80.87달러', '97.84달러'],
       ['시장가격(9/22)', '80.83달러', '97.82달러']],
      [0.3, 0.35, 0.35], hl_col=1, src=SRC_P)

table(os.path.join(D, 'b3.png'), '총보수는 면제 전후로 두 줄이 적혀 있다',
      ['항목', 'TQQQ', 'QLD'],
      [['면제 전(gross)', '0.97%', '0.98%'],
       ['면제 후(net)', '0.82%', '0.95%'],
       ['면제 기한', '2026년 9월 30일', '2026년 9월 30일']],
      [0.3, 0.35, 0.35], hl_col=1,
      note='ProShares 각주 원문: "This fund has a fee waiver through September 30, 2026, without this fee waiver fees may have been higher." QLD는 "Expenses with Contractual Waiver through September 30, 2026." 9월 30일 이후 보수가 어떻게 되는지는 확인하지 못했다.',
      src=SRC_P)

steps(os.path.join(D, 'b4.png'), '지수가 제자리로 와도 3배는 제자리가 아니다',
      [('첫째 날 지수 +10%', '1배는 1.10이 된다. 일간 3배는 +30%라 1.30이 된다.'),
       ('둘째 날 지수 -10%', '1배는 1.10 × 0.90 = 0.99. 1% 손실이다.'),
       ('같은 이틀, 일간 3배', '1.30 × 0.70 = 0.91. 9% 손실이다.'),
       ('매일 다시 계산하기 때문', '운용사가 약속한 것은 하루다. 하루를 넘기면 오르내린 경로가 결과를 바꾼다.'),
       ('한 방향으로만 오르면 반대', '계속 오르는 구간에서는 산술 배수를 넘기도 한다. 구간에 따라 달라진다.')],
      note='이 예시는 사실이 아니라 산수다. 실제 지수 움직임이 아니다.',
      src='설명 근거: ProShares 공식 문구 "For any holding period other than a day, your return may be higher or lower than the Daily Target. These differences may be significant."')

table(os.path.join(D, 'b5.png'), '최근 12개월 배당 — 셋 다 분기 배당',
      ['배당락일', 'TQQQ', 'QLD', 'QQQ'],
      [['2025년 9월 24일', '0.0490달러', '0.0205달러', '-'],
       ['2025년 12월', '0.0860달러', '0.0230달러', '0.7940달러'],
       ['2026년 3월', '0.0720달러', '0.0130달러', '0.7330달러'],
       ['2026년 6월', '0.1710달러', '0.0610달러', '0.8130달러'],
       ['2026년 9월 21일', '-', '-', '0.7510달러'],
       ['12개월 합', '0.3780달러', '0.1175달러', '3.0910달러'],
       ['현재가 기준 배당률', '0.47%', '0.12%', '-']],
      [0.28, 0.24, 0.24, 0.24], hl_col=1,
      note='TQQQ 현재가 80.83달러, QLD 97.82달러 기준. 배당락일이 3·6·9·12월 같은 주에 몰린다.', src=SRC_Y)

table(os.path.join(D, 'b6.png'), '1,000만원을 넣었다고 놓으면',
      ['상품', '1년 뒤', '산술 배수대로 갔다면'],
      [['QQQ', '1,245만원', '-'],
       ['QLD', '1,413만원', '1,490만원'],
       ['TQQQ', '1,548만원', '1,736만원']],
      [0.3, 0.35, 0.35], hl_col=1,
      note='세금·환율·거래 비용은 넣지 않은 단순 계산이다. 지난 1년 한 구간의 결과이며 앞으로의 방향은 이 표에 없다.',
      src=SRC_Y)
print('ok')
