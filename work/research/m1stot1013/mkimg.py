# m1stot1013 본문 그림 — w1cafe1013 mkimg 틀(blogimg.table) · 숫자는 M-1 calc_out·facts만
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1=[['SCHD','+15.73%','3.73%','+19.46%','119,456,864원'],['ACE 미국배당다우존스','+15.01%','3.54%','+18.55%','118,547,352원'],['JEPQ','+3.03%','11.62%','+14.65%','114,649,910원']]
B.table('pkg/img/01.png','1억 넣고 1년 뒤 (2025년 10월 2일 → 2026년 10월 2일, 원화)',['상품','가격 변화','분배금','합','1억이 1년 뒤'],r1,hl_col=3,
        note='세전 · 분배금 다시 사지 않음 · 분배금은 2026년 10월 2일 환율(1달러 1,359.6원)로 바꾼 어림값 · 지난 기록',src='나스닥 배당 이력 · 찰스 슈왑 · 한국투자신탁운용 · 야후 파이낸스 · 한국은행 ECOS')
json.dump({'01.png':{'rows':r1}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
B.bignum('pkg/img/02.png','JEPQ 1년(원화) — 분배금 11.62% · 가격 변화','+3.03%',sub='달러 종가 57.29 → 61.04달러(+6.55%) · 환율 1,406.0 → 1,359.6원',src='야후 파이낸스 종가 · 한국은행 ECOS 731Y001')
