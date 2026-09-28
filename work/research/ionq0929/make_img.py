# 아이온큐 카페 이미지. 실행: PYTHONPATH=work py -3.12 work/research/ionq0929/make_img.py
import os, json, urllib.request, datetime
from blogimg import table, line
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pkg', 'img'); os.makedirs(D, exist_ok=True)
table(os.path.join(D, '01.png'), '아이온큐(IONQ)는 어떤 회사',
      ['항목', '내용'],
      [['하는 일', '양자컴퓨터(이온 트랩 방식)'], ['상장', '뉴욕증권거래소 IONQ'],
       ['시가총액', '179억달러 남짓'], ['배당', '없음'], ['9월 25일 종가', '45.48달러']],
      hl_col=1, src='출처: Nasdaq 요약 API·Yahoo 시세 (2026-09-29 조회)')
table(os.path.join(D, '02.png'), '매출은 늘고, 장부 손실은 컸다',
      ['항목', '2분기(2026)'],
      [['매출', '8,010만달러 (1년 전 대비 +287%)'], ['순손실', '18억 6,770만달러'],
       ['그중 워런트 평가손실', '16억 4,912만달러'], ['조정 EBITDA', '-1억 2,030만달러'],
       ['현금·투자자산(6월 말)', '30억달러'], ['올해 매출 전망', '4억 5,000만~4억 6,000만달러']],
      hl_col=1, note='올해 전망은 스카이워터 인수(7월 31일)분을 합친 값', src='출처: 아이온큐 SEC 8-K(2026-08-05)·뉴스룸')
H = {'User-Agent': 'Mozilla/5.0'}
c = json.loads(urllib.request.urlopen(urllib.request.Request('https://query1.finance.yahoo.com/v8/finance/chart/IONQ?range=1y&interval=1d', headers=H), timeout=30).read())['chart']['result'][0]
pts0 = [(datetime.datetime.fromtimestamp(t, datetime.UTC).date(), x) for t, x in zip(c['timestamp'], c['indicators']['quote'][0]['close']) if x]
pts = [p for p in pts0 if p[0] <= datetime.date(2026, 9, 25)]
xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
hi = max(pts, key=lambda p: p[1]); lo = min(pts, key=lambda p: p[1])
line(os.path.join(D, '03.png'), '아이온큐 1년 주가 (종가, 달러)', xs, ys,
     marks=[(hi[0], hi[1], f'최고 {hi[1]:.2f}', 'ink'), (xs[-1], ys[-1], f'9/25 {ys[-1]:.2f}', 'red'), (lo[0], lo[1], f'최저 {lo[1]:.2f}', 'ink')],
     unit='달러', src='출처: Yahoo 차트 API (2026-09-29 조회)')
print(hi, lo, pts[-1])
