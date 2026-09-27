# -*- coding: utf-8 -*-
# 2026-09-27 회차 블로그 묶음: 해외 파이어족 3가구 실제 지출(원문 블로그 3곳)
import os, sys
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import blogimg

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, 'pkg'); I = os.path.join(P, 'img')
os.makedirs(I, exist_ok=True)
FX = 1354  # 원/달러, Yahoo Finance KRW=X, 2026-09-27 조회
def won(usd):
    m = round(usd * FX / 10000)
    return f'{m // 10000}억 {m % 10000:,}만원' if m >= 10000 else f'{m:,}만원'

SRC = '출처: Go Curry Cracker(2019-10) · Retire by 40(2026-04-05) · Root of Good(2026-01-15, 2026-09-15)'
blogimg.table(os.path.join(I, '01.png'), '해외 파이어족 3가구, 원문에 적힌 숫자',
              ['', 'Go Curry Cracker', 'Retire by 40', 'Root of Good'],
              [['은퇴 나이', '글에 없음', '38세', '33세(2013년)'],
               ['사는 곳', '정착 없이 여행', '미국 포틀랜드', '미국 롤리'],
               ['가족', '부부+아들', '부부+10대 아들', '부부+자녀 셋'],
               ['순자산', '글에 없음', '글에 없음', '395만 8천 달러'],
               ['지출', '연평균 7만 5,200달러', '1분기 1만 6,938달러', '2025년 4만 4,013달러'],
               ['기준 시점', '2013~2019년', '2026년 1~3월', '2025년 1년']],
              note='순자산은 Root of Good만 금액을 적었다(2025년 말, 집 30만 달러 포함).', src=SRC)

gcc = [(2013, 38996), (2014, 59086), (2015, 56900), (2016, 72002), (2017, 93648), (2018, 89000), (2019, 95000)]
blogimg.table(os.path.join(I, '02.png'), 'Go Curry Cracker 연도별 실제 지출',
              ['연도', '지출(달러)', '원화 환산'],
              [[f'{y}년' + (' (추정)' if y == 2019 else ''), f'{v:,}', won(v)] for y, v in gcc],
              note=f'환산은 1달러 {FX:,}원(2026-09-27 Yahoo Finance). 2019년은 글쓴이 추정치.',
              src='출처: gocurrycracker.com/expenses (Last updated: October 2019)')

blogimg.table(os.path.join(I, '03.png'), 'Retire by 40, 2026년 1분기 지출 항목',
              ['항목', '달러', '원화 환산'],
              [['주거', '4,971', won(4971)], ['여행', '4,417', won(4417)], ['외식·오락', '2,382', won(2382)],
               ['식료품', '1,573', won(1573)], ['자녀', '1,024', won(1024)], ['건강', '1,008', won(1008)],
               ['개인 지출', '887', won(887)], ['교통', '503', won(503)], ['합계(글에 적힌 값)', '16,938', won(16938)]],
              note='항목을 더하면 16,765달러로 글의 합계와 173달러 차이가 난다. 글에 설명은 없다.',
              src='출처: retireby40.org/q1-2026-fire-update (2026-04-05)')

def photo(name, out):
    im = Image.open(os.path.join(D, 'photos', name)).convert('RGB')
    w, h = im.size; nw = 900; im = im.resize((nw, int(h * nw / w)))
    im.save(out, quality=88)
photo('family_budget_notebook_3_6963888.jpg', os.path.join(I, '04.jpg'))
photo('family_budget_notebook_2_4475473.jpg', os.path.join(I, '05.jpg'))
for v in (75200, 75200 / 12, 200, 16938, 16938 / 3, 10630, 9901, 3593, 80000, 60000, 44013, 44013 / 12, 40000, 3958000, 300000, 1900000, 526409):
    print(v, won(v))
print('ok')
