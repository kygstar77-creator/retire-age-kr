import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1=[['간병 보상 인정 없음','6억원','1억 5천만원'],['4억원을 간병 보상으로 인정','2억원','5천만원'],['6억원 전부 보상으로 인정','0원','0원']]
B.table('pkg/img/01.png','언니가 받은 아파트 6억원, 동생 유류분은',['가정법원 판단','계산에 들어가는 증여','동생 유류분'],r1,hl_col=2,
        note='자녀 둘·배우자 없음 · 8년 전 증여 · 남은 재산과 빚 없음 · 손해를 알고 한 증여 아님 · 4억원은 계산용 가정',src='민법 제1008조·제1112조~제1114조(2026.3.17 시행) · 대법원 95다17885')
r2=[['간병·부양 보상은 빼고 계산','2024년 4월 25일 이후 상속'],['부족한 몫은 돈으로 청구 + 청구일부터 이자','2026년 3월 17일 이후 상속'],['형제자매 유류분 없음','2024년 9월 20일 삭제'],['부양 외면·학대한 상속인 상속권 상실','가정법원 선고 확정 시']]
B.table('pkg/img/02.png','유류분, 무엇이 언제부터 바뀌었나',['바뀐 것','적용'],r2,hl_col=1,
        note='돌아가신 날짜 기준',src='민법 부칙(법률 제21454호) · 법령정보센터 2026.10.11 조회')
json.dump({'01.png':{'rows':r1},'02.png':{'rows':r2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
