# -*- coding: utf-8 -*-
# 2026-09-27 19시 회차 블로그 묶음: 청년미래적금 2차 가입 조건과 날짜
import os, sys
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import blogimg

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, 'pkg'); I = os.path.join(P, 'img')
os.makedirs(I, exist_ok=True)
SRC = '출처: 금융위원회 보도자료(2026.9.16) · 정책브리핑'

blogimg.steps(os.path.join(I, '01.png'), '청년미래적금 2차, 신청부터 계좌 개설까지',
              ['10월 7일 출생연도 끝자리 홀수 신청',
               '10월 8일 짝수 신청',
               '10월 12~16일 누구나 신청',
               '10월 19일~11월 13일 심사',
               '11월 16~27일 통과자 계좌 개설'],
              note='10월 9일은 한글날, 10~11일은 주말이다.', src=SRC)
blogimg.table(os.path.join(I, '02.png'), '일반형과 우대형, 소득 기준 비교(2025년 소득)',
              ['구분', '일반형', '우대형'],
              [['근로소득(총급여)', '7,500만원 이하', '3,600만원 이하(중소기업)'],
               ['종합소득', '6,300만원 이하', '2,600만원 이하'],
               ['소상공인 연매출', '3억원 이하', '1억원 이하'],
               ['가구 소득', '중위소득 200% 이하', '중위소득 150% 이하'],
               ['정부 기여금', '납입액의 6%', '납입액의 12%']],
              note='우대형 가구 기준은 맞벌이 2인 가구면 200% 이하.',
              src='출처: 금융위원회 보도자료(2026.9.16) · 카카오뱅크 상품 안내')
blogimg.table(os.path.join(I, '03.png'), '월 50만원씩 3년 넣으면 받는 기여금',
              ['기여금 비율', '원금', '정부 기여금'],
              [['일반형 6%', '1,800만원', '108만원'],
               ['우대형 12%', '1,800만원', '216만원'],
               ['개편안 15%(국회 승인 필요)', '1,800만원', '270만원'],
               ['개편안 25%(지방 중소기업)', '1,800만원', '450만원']],
              note='은행 이자는 따로. 만기 전 해지하면 기여금을 받지 못한다.', hl_col=2, src=SRC)
blogimg.steps(os.path.join(I, '04.png'), '청년도약계좌에서 갈아타는 순서',
              ['청년미래적금 가입 신청',
               '심사 통과, 가입 가능 안내 받기',
               '청년미래적금 계좌 개설',
               '청년도약계좌 특별중도해지 신청'],
              note='순서대로 하면 도약계좌 기존 납입분의 기여금·비과세를 받고 해지한다.',
              src='출처: 금융위원회 보도자료(2026.6.15, 2026.9.16)')

def photo(name, out):
    im = Image.open(os.path.join(D, 'photos', name)).convert('RGB')
    w, h = im.size; nw = 900; im = im.resize((nw, int(h * nw / w)))
    im.save(out, quality=88)
photo('young_adult_saving_money_1_7009866.jpg', os.path.join(I, '05.jpg'))
photo('young_adult_saving_money_3_7009596.jpg', os.path.join(I, '06.jpg'))
print('ok')
