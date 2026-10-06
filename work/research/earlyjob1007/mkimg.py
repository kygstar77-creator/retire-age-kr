# earlyjob1007 본문 표 2장 — parking1007 mkimg 틀. firemap-write 2026-10-07
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows=[['240일','8,172,000원'],['180일','6,129,000원'],['135일(딱 절반)','4,596,750원'],['134일','0원']]
B.table('pkg/img/01.png','남은 실업급여 날수별 조기재취업수당',['남은 날수','받는 수당'],rows,hl_col=1,
        note='50세 이상·고용보험 10년 이상(270일) · 하루 68,100원 × 남은 날수 × 1/2',src='고용보험법 별표 1·같은 법 시행령 제85조 (2026.10.7 조회)')
rows2=[['지급 제외 월급','574만원 이상','300만원 이상'],['적용 대상','10월 31일까지 신청자(확정 시)','11월 1일 이후 신청자(확정 시)'],['상태','시행 중','행정예고(의견 10월 18일까지)']]
B.table('pkg/img/02.png','조기재취업수당 월급 기준, 지금과 개정안',['','지금','개정안'],rows2,hl_col=2,
        note='새 직장 월급이 기준 이상이면 수당이 없음 · 10월 31일은 토요일이라 고용센터는 30일까지',src='고용노동부 고시 제2024-60호·공고 제2026-458호')
json.dump({'01.png':{'rows':rows},'02.png':{'rows':rows2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok')
