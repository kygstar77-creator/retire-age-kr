# m1snhis1013 본문 그림 — w1cafe1013 mkimg 틀(blogimg) · 숫자는 M-1 calc_out·facts만
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
if os.path.exists('pkg/tables.json'): os.remove('pkg/tables.json')
r1=[['1,000만원 이하','미국 상장 70만 8,333원 · 국내 상장 70만 5,000원','안 넣음','2만 2,800원(최저)'],['1,561만원','보험료까지 떼고 100만원(미국 상장)','전부 넣음','10만 5,832원']]
B.table('pkg/img/01.png','배당 받으면 건강보험료 얼마부터 (지역가입자)',['1년 이자·배당(세전)','세금 뗀 한 달','보험료 소득에','월 보험료'],r1,hl_col=3,
        note='재산·다른 소득 없을 때 · 세금 미국 상장 15%, 국내 상장 15.4% · 보험료율 8.1348%(장기요양 포함) · 2026년 10월 2일 기준',src='국민건강보험법 시행규칙 제44조 · 국민건강보험공단 보험료율')
B.bignum('pkg/img/02.png','2026년에 받은 배당이 반영되는 보험료','2027년 11월분',sub='11~12월분은 전년도, 1~10월분은 전전년도 소득 자료',src='국민건강보험법 시행령 제41조')
