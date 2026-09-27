# -*- coding: utf-8 -*-
# 2026-09-27 17시 회차 블로그 묶음: ISA 만기 자금 연금계좌 이전 세액공제
import os, sys, shutil
from PIL import Image
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import blogimg

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, 'pkg'); I = os.path.join(P, 'img')
os.makedirs(I, exist_ok=True)
SRC = '출처: 소득세법 제59조의3 · 소득세법 시행령 제118조의2'

rows = []
for amt in (1000, 2000, 3000, 5000):
    add = min(amt * 0.10, 300)
    rows.append([f'{amt:,}만원', f'{add:,.0f}만원', f'{add*0.15:,.0f}만원', f'{add*0.12:,.0f}만원'])
blogimg.table(os.path.join(I, '01.png'), 'ISA 만기 자금을 옮기면 늘어나는 공제 한도',
              ['옮긴 금액', '늘어나는 한도', '공제 15%일 때', '공제 12%일 때'], rows,
              note='추가 한도는 옮긴 돈의 10%, 300만원까지. 소득세 기준(지방소득세 제외).', src=SRC)
blogimg.steps(os.path.join(I, '02.png'), 'ISA 만기 자금이 연금계좌로 가는 순서',
              ['ISA 계약기간 만료(3년 이상 유지)',
               '만기일부터 60일 안에 연금저축·IRP로 입금',
               '옮긴 돈의 10%(최대 300만원)가 그해 공제 한도에 추가',
               '그해 연말정산이나 종합소득세 신고 때 공제'],
              note='60일을 넘기면 일반 납입으로 처리된다.', src=SRC)
blogimg.table(os.path.join(I, '03.png'), '연금계좌 세액공제 한도, 옮긴 해와 평소 비교',
              ['구분', '평소', 'ISA 만기 자금을 옮긴 해'],
              [['연금저축 한도', '600만원', '600만원'],
               ['연금저축+IRP 한도', '900만원', '최대 1,200만원'],
               ['연간 납입 한도', '1,800만원', '전환금은 따로 센다']],
              src='출처: 소득세법 제59조의3 · 소득세법 시행령 제40조의2')

def photo(name, out):
    im = Image.open(os.path.join(D, 'photos', name)).convert('RGB')
    w, h = im.size; nw = 900; im = im.resize((nw, int(h * nw / w)))
    im.save(out, quality=88)
photo('연금_저축_노후_3_20376766.jpg', os.path.join(I, '04.jpg'))
photo('연금_저축_노후_4_6120252.jpg', os.path.join(I, '05.jpg'))
print('ok')
