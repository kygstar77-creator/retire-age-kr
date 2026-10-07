import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows=[['바로~2개월 뒤','270일','0원'],['3개월 뒤(10월 1일)','266일','약 27만원'],['4개월 뒤(11월 1일)','235일','약 238만원'],['6개월 뒤(1월 1일)','174일','약 654만원'],['8개월 뒤(3월 1일)','115일','약 1,056만원']]
B.table('pkg/img/01.png','6월 30일에 퇴사한 270일 수급자, 신청을 미루면',['신청한 때','받을 수 있는 날','못 받는 돈'],rows,hl_col=2,
        note='50세 이상·가입 10년 이상·하루 6만 8,100원 기준 · 7일 대기 포함',src='고용보험법 제48·49·50조로 계산')
json.dump({'01.png':{'rows':rows}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
rows2=[['1','회사에 이직확인서 발급 요청','회사는 10일 안에 발급'],['2','고용24에서 구직신청','work24.go.kr'],['3','수급자격 신청 전 교육','온라인 가능'],['4','고용센터 방문, 신분증 지참','수급자격 인정신청서·재취업활동계획서'],['5','접수 뒤 14일 안에 통지','수급자격 인정 여부'],['6','실업인정일마다 구직활동 신고','1~4주 사이에 지정']]
B.table('pkg/img/02.png','실업급여 신청 순서 6단계',['순서','할 일','메모'],rows2,hl_col=2,note='고용노동부 FAQ·고용24 안내 기준',src='고용노동부 자주 하는 질문, 고용24 구직급여 신청 안내(2026-10-07 조회)')
d=json.load(open('pkg/tables.json',encoding='utf-8')); d['02.png']={'rows':rows2}; json.dump(d,open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
