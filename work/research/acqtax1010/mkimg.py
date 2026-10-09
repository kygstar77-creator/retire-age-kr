# acqtax1010 본문 표 2장 — firemap-write 10/9 (brokerfee1009 틀)
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1=[['6억원','660만원','5,040만원','+4,380만원'],['10억원','3,300만원','8,400만원','+5,100만원'],['15억원','4,950만원','1억2,600만원','+7,650만원']]
B.table('pkg/img/01.png','기한 안에 못 팔면 새 집 취득세',['새 집 값','기한 안에 팔면','못 팔면(8%)','더 내는 돈'],r1,hl_col=3,
        note='전용 85㎡ 이하 · 지방교육세 포함 · 차액은 기간 끝난 날부터 60일 안에 신고',src='지방세법 제11조·제13조의2·제151조 (2026.10.9 조회)')
r2=[['8월 3일까지','3년','3년'],['8월 4일 ~ 26일','2년','3년'],['8월 27일 이후','2년','2년']]
B.table('pkg/img/02.png','두 집 다 조정대상지역일 때 계약일별 기한',['새 집 계약·계약금','양도세','취득세'],r2,hl_col=2,
        note='취득세 2년은 10월 1일 이후 잔금(취득)분부터 · 계약금 낸 서류가 있어야 함',src='지방세법 시행령·소득세법 시행령 부칙 (2026.9.30 공포)')
json.dump({'01.png':{'rows':r1},'02.png':{'rows':r2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
