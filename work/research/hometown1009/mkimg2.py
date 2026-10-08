# hometown1009 본문 표 2번째 장 (구간별 공제율) — firemap-write 10/9
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows=[['10만원까지','100%','10만원 기부하면 세금 10만원'],['10만원 넘고 20만원까지','44%','10만원 더 내면 4만4천원'],['20만원 넘는 부분','16.5%','10만원 더 내면 1만6천500원']]
B.table('pkg/img/02.png','기부액 구간별 세액공제율',['구간','공제율','10만원 더 낼 때'],rows,hl_col=1,
        note='특별재난지역에 기부하면 20만원 넘는 부분은 33%',src='조세특례제한법 제58조·고향사랑e음 안내 (2026.10.9 조회)')
t=json.load(open('pkg/tables.json',encoding='utf-8')); t['02.png']={'rows':rows}
json.dump(t,open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
