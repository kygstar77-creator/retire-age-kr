import sys, json; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
SRC='한국농어촌공사 농지은행 예상연금 조회(2026-10-05 조회)'
T1=[('60세','93만 7,610원'),('65세','105만 1,330원'),('70세','119만 4,390원'),('75세','137만 9,800원'),('80세','163만 1,380원')]
B.table('pkg/img/01.png','같은 3억원 농지, 나이별 월 지급액',['가입 나이','종신정액형 월 지급액'],[list(x) for x in T1],hl_col=1,
        note='공시지가 3억원 · 종신정액형 · 우대 지급 없음 · 배우자 승계 없음',src=SRC)
T2=[('1억','35만 440원'),('2억','70만 880원'),('3억','105만 1,330원'),('4억','140만 1,770원'),('5억','175만 2,220원'),('6억','210만 2,660원')]
B.table('pkg/img/02.png','65세, 농지 가격별 월 지급액',['농지 가격','종신정액형 월 지급액'],[list(x) for x in T2],hl_col=1,
        note='공시지가 기준 · 종신정액형 · 우대 지급 없음 · 배우자 승계 없음',src=SRC)
json.dump({'01.png':{'cols':['가입 나이','월 지급액'],'rows':[list(x) for x in T1]},'02.png':{'cols':['농지 가격','월 지급액'],'rows':[list(x) for x in T2]}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok')
