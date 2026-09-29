import sys; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
def w(m):
    m=int(round(m)); e,r=divmod(m,10000)
    return ((f'{e}억' + (f' {r:,}만원' if r else '원')) if e else f'{r:,}만원')
SRC='국토교통부 실거래가 공개 오픈API(송파구 11710, 2026-09-29 조회)'
H=[('39',201000,84000,2),('60',228850,111500,4),('85',295000,135000,21),('100',336000,160000,3),('111',349500,170000,3)]
B.table('pkg/img/02.png','헬리오시티 면적별 매매·전세 가운데 값 (2026년 7~9월)',['전용㎡','매매','신규 전세','전세가율'],
 [[a,w(b),f'{w(c)} ({n}건)',f'{c/b*100:.1f}%'] for a,b,c,n in H],hl_col=3,
 note='전세는 월세 0원 신규 계약만 · 9월은 12일 계약분까지 신고됨', src=SRC)
