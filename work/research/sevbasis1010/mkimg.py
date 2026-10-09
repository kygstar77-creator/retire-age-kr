# sevbasis1010 본문 표 2장 — firemap-write helper 10/9
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1=[['이듬해 11월 1일','11월 2일','364일','법정 퇴직금 없음'],['이듬해 11월 2일','11월 3일','365일','300만원'],['1년 반 뒤 5월 2일','5월 3일','546일','448만 7천원']]
B.table('pkg/img/01.png','퇴직금 1년, 마지막 근무일 하루 차이',['마지막 근무일','퇴직일','재직일수','퇴직금'],r1,hl_col=3,
        note='가정: 2025년 11월 3일 입사 · 1일 평균임금 10만원 · 퇴직일 = 마지막 근무일 다음 날',src='근로자퇴직급여 보장법 제4조·제8조 · 고용노동부 퇴직금 계산 (2026.10.9 조회)')
r2=[['근무표 A','16 · 14 · 16 · 14시간','15시간','퇴직금 대상'],['근무표 B','15 · 14 · 15 · 14시간','14.5시간','대상 아님']]
B.table('pkg/img/02.png','주 15시간은 4주 평균으로',['구분','4주 소정근로시간','1주 평균','결과'],r2,hl_col=3,
        note='소정근로시간 = 근로계약으로 정한 시간(실제 일한 시간 아님)',src='근로자퇴직급여 보장법 제4조① · 근로기준법 제2조 (2026.10.9 조회)')
json.dump({'01.png':{'rows':r1},'02.png':{'rows':r2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
