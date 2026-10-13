# dcpension1014 본문 그림 — cheongyak1012 mkimg 틀 · 숫자는 calc_out.txt 그대로
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1=[['2%','1억 2,140만','1억 3,455만','1억 6,213만'],['3%','1억 4,613만','1억 4,734만','1억 7,650만'],['4%','1억 7,557만','1억 6,171만','1억 9,257만']]
B.table('pkg/img/01.png','20년 뒤 받는 퇴직금, 월급 인상률별로 보면',['연봉 인상률','DB형','DC형 연 3.09%','DC형 연 5%'],r1,hl_col=2,
        note='첫해 연봉 5,000만원 · 20년 근속 · DC 부담금 매년 말 연봉의 12분의 1 · 3.09%는 2025년 원리금보장형 평균 · 세전 단순 계산',src='근로자퇴직급여 보장법 제15조·제20조 · 2025년 퇴직연금 투자백서')
json.dump({'01.png':{'rows':r1}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
B.bignum('pkg/img/02.png','임금피크 직전 DC형 전환이 열리면 더 받는 돈(예시)','3,605만원',sub='마지막 5년 연봉 80% · DB형 1억 84만 → DC형 전환 1억 3,689만(원리금보장 3.09%)',src='근로자퇴직급여 보장법 제32조 제5항 · 첫해 연봉 5,000만원·20년 근속 단순 계산')
