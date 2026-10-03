import sys; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
SRC='소득세법 제48·55조로 계산(국가법령정보, 2026-10-03) · 지방소득세 10% 포함'
T=[('5년','1,036만원','3,571만원','6,392만원'),('10년','426만원','1,966만원','4,289만원'),('15년','239만원','1,162만원','2,844만원'),
   ('20년','123만원','773만원','1,984만원'),('25년','75만원','558만원','1,361만원'),('30년','26만원','380만원','1,085만원')]
B.table('pkg/img/01.png','퇴직금 일시금 세금, 다닌 햇수별',['근속','퇴직금 1억','퇴직금 2억','퇴직금 3억'],[list(x) for x in T],hl_col=1,
 note='비과세 소득·중간정산 없다고 보고 계산 · 1년 미만 기간은 1년으로 셈', src=SRC)
print('ok')
