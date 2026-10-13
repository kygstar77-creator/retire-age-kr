# cheongyak1012 본문 그림 — reitetf1013 mkimg 틀 · 숫자는 calc_out.txt 그대로
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1=[['6%','21만 6천원','54만원','21만 6천원'],['15%','54만원','54만원','54만원']]
B.table('pkg/img/01.png','청약통장 3년 공제받고 5년 안에 해지하면',['세율 구간','3년 동안 줄어든 세금','은행이 떼는 돈','증명하면 내는 돈'],r1,hl_col=3,
        note='1년 300만원씩 · 총급여 7천만원 이하만 공제라 두 구간만 · 소득세만(지방소득세 별도) · 공제 120만원이 한 세율 구간 안에 든다고 본 단순 계산',src='조세특례제한법 제87조 · 소득세법 제55조')
json.dump({'01.png':{'rows':r1}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
B.bignum('pkg/img/02.png','퇴직하고 이 기간 안에 해지하면 추징 없음','6개월',sub='폐업·3개월 넘는 입원·요양·천재지변도 같음 · 특별해지사유신고서 제출',src='조세특례제한법 시행령 제81조 제11항·제12항')
