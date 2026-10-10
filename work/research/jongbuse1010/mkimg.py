# jongbuse1010 본문 표 2장 — firemap-write 10/10
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1=[['60~64세','20%','40%','60%','70%'],['65~69세','30%','50%','70%','80%'],['70세 이상','40%','60%','80%','80% (90%→한도)']]
B.table('pkg/img/01.png','종부세 1주택 공제율 합계',['나이 · 보유기간','5년 미만','5~9년','10~14년','15년 이상'],r1,hl_col=4,
        note='고령자 20·30·40% + 장기보유 20·40·50%, 합계는 80%까지 · 나이·보유기간은 6월 1일 기준',src='종합부동산세법 제9조⑤⑥⑧ (2026.10.10 조회)')
r2=[['1956년 6월 2일 출생','만 69세','30%','40%'],['2011년 7월 1일 취득','14년 11개월','40%','50%']]
B.table('pkg/img/02.png','6월 1일 하루로 세는 나이와 보유기간',['예','2026년 6월 1일','올해 공제율','2027년 공제율'],r2,hl_col=2,
        note='과세기준일 = 매년 6월 1일 · 2027년 공제율은 지금 법 그대로일 때',src='종합부동산세법 제3조·제9조⑥⑧ (2026.10.10 조회)')
json.dump({'01.png':{'rows':r1},'02.png':{'rows':r2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
