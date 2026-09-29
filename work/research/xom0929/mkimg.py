import sys, json; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
d='pkg/img/'; D=json.load(open('data.json',encoding='utf-8'))
B.table(d+'00.png','엑슨모빌(XOM) 최근 분기 배당금 (한 주 기준)',['배당락일','금액','전 분기 대비'],
 [['2026-08-17','1.03달러','같음'],['2026-05-15','1.03달러','같음'],['2026-02-12','1.03달러','같음'],['2025-11-14','1.03달러','+4.0%'],
  ['2025-08-15','0.99달러','같음'],['2024-11-14','0.99달러','+4.2%'],['2024-08-15','0.95달러','-']],
 hl_col=1, note='미국 날짜 · 미국 현지 원천징수 15% 떼기 전 금액 · 인상은 해마다 11월 배당에서', src='야후 파이낸스 배당 기록 · 엑슨모빌 2분기 실적 발표문 (2026-09-29 조회)')
B.table(d+'01.png','엑슨모빌 분기 실적 (2026년)',['항목','1분기','2분기'],
 [['순이익','41억 8,300만달러','145억 2,500만달러'],['주당순이익','1.00달러','3.48달러'],['조정 주당순이익','2.09달러','3.52달러']],
 hl_col=2, note='조정 주당순이익은 일회성 항목을 뺀 회사 기준 숫자', src='엑슨모빌 홀딩스 2분기 실적 발표문(SEC 8-K, 2026-07-31)')
xs=[t[2:7].replace('-','.') for t in D['ts']]; ys=D['close']; last=len(ys)-1
while ys[last] is None: last-=1
B.line(d+'02.png','엑슨모빌 주가 5년 (주간 종가)',xs[:last+1],ys[:last+1],marks=[(0,ys[0],f'{ys[0]:.0f}달러','ink'),(last,ys[last],f'{ys[last]:.0f}달러','red')],unit='달러',src='야후 파이낸스 (2026-09-29 조회)')
dv=D['divs']
B.line(d+'03.png','엑슨모빌 분기 배당금 6년 (한 주 기준)',[x[2:7].replace('-','.') for x,_ in dv],[v for _,v in dv],marks=[(0,dv[0][1],f'{dv[0][1]:.2f}달러','ink'),(len(dv)-1,dv[-1][1],f'{dv[-1][1]:.2f}달러','red')],unit='달러',src='야후 파이낸스 배당 기록 (2026-09-29 조회)')
print('ok')
