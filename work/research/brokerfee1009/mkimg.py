# brokerfee1009 본문 표 2장 — firemap-write 10/9
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1=[['12억원에 팔 때','0.6%','720만원'],['7억원에 살 때','0.4%','280만원'],['두 번 합계','','1,000만원'],['부가세 10% 붙으면','','1,100만원']]
B.table('pkg/img/01.png','집 팔고 작은 집 살 때 중개보수 상한',['거래','상한 요율','상한 금액'],r1,hl_col=2,
        note='파는 쪽·사는 쪽 각각 받음 · 상한 안에서 협의해 정함',src='공인중개사법 시행규칙 별표 1·서울시 주택중개보수 조례 (2026.10.9 조회)')
r2=[['8억9천만원 → 9억원','0.4% → 0.5%','356만 → 450만원','+94만원'],['11억9천만원 → 12억원','0.5% → 0.6%','595만 → 720만원','+125만원'],['14억9천만원 → 15억원','0.6% → 0.7%','894만 → 1,050만원','+156만원']]
B.table('pkg/img/02.png','매매 요율 경계 바로 아래와 위',['거래금액','상한 요율','상한 금액','차이'],r2,hl_col=3,
        note='요율은 거래금액 전체에 곱함 · 부가세 별도',src='공인중개사법 시행규칙 별표 1 (2026.10.9 조회)')
json.dump({'01.png':{'rows':r1},'02.png':{'rows':r2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
