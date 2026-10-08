# isapen1009 본문 표 2장 — firemap-write 10/9 (hometown1009 mkimg2 틀)
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
S='소득세법 제59조의3 · 시행령 제118조의3 (2026.10.9 조회)'
r1=[['1천만원','100만원','13만2천원','16만5천원'],['2천만원','200만원','26만4천원','33만원'],['3천만원','300만원','39만6천원','49만5천원'],['5천만원','300만원(상한)','39만6천원','49만5천원']]
B.table('pkg/img/01.png','ISA 만기 자금을 연금계좌로 옮기면',['옮긴 돈','늘어나는 한도','공제 13.2%','공제 16.5%'],r1,hl_col=3,
        note='16.5%는 총급여 5,500만원 이하(근로소득만) · 지방소득세 포함',src=S)
r2=[['한 번에 3천만원','300만원','-','300만원'],['12월 2천만원 + 1월 1천만원','200만원','100만원','300만원']]
B.table('pkg/img/02.png','두 해에 나눠 옮기면 한도는',['옮긴 방법','첫해','다음 해','합계'],r2,hl_col=3,
        note='다음 해 한도 = 300만원 − 앞 해에 쓴 한도',src='소득세법 제59조의3 제4항 (2026.10.9 조회)')
json.dump({'01.png':{'rows':r1},'02.png':{'rows':r2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
