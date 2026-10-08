# isapen1009 본문 표 2장 — firemap-write 10/9 (hometown1009 mkimg2 틀)
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
S='소득세법 제59조의3 · 시행령 제118조의2 (2026.10.9 조회)'
r1=[['1천만원','16만5천원','165만원'],['2천만원','33만원','181만5천원'],['3천만원','49만5천원','198만원'],['5천만원','49만5천원','198만원']]
B.table('pkg/img/01.png','ISA 만기 자금을 IRP로 옮기면 돌려받는 세금',['옮긴 돈','900만원 이미 채운 분(더 받는 몫)','다른 납입 없는 분'],r1,hl_col=2,
        note='공제율 16.5% 기준(종합소득금액 4,500만원 이하) · 13.2%면 표 금액의 80%',src=S)
r2=[['한 번에 5천만원','1,200만원','-','198만원'],['12월 2천만원 + 1월 3천만원','1,100만원','1,000만원','346만5천원']]
B.table('pkg/img/02.png','다른 납입 없이 IRP로 옮길 때 나누면',['옮긴 방법','첫해 공제 대상','다음 해 공제 대상','돌려받는 돈 합계'],r2,hl_col=3,
        note='늘어나는 한도는 두 해 합쳐 300만원 · 기본 한도 900만원은 해마다 따로 · 16.5%, 두 해 모두 낼 세금이 있을 때',src='소득세법 제59조의3 제1·3·4항 (2026.10.9 조회)')
json.dump({'01.png':{'rows':r1},'02.png':{'rows':r2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
