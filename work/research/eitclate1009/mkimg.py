# eitclate1009 본문 표 2장 — deplend1009 mkimg 틀. firemap-write 2026-10-08
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
os.makedirs('pkg/img', exist_ok=True)
rows=[['10월','3월 2일'],['11월 30일까지','3월 30일'],['12월 1일','4월 30일']]
B.table('pkg/img/01.png','기한 후 신청, 언제 내면 늦어도 언제 받나',['신청한 때','늦어도 받는 날 (2027년)'],rows,hl_col=1,
        note='신청한 달 말일 + 3개월 안에 결정, 결정일 + 30일 안에 환급 (연장 단서 빼고)',src='조세특례제한법 제100조의7·제100조의8 (2026.10.8 조회)')
rows2=[['단독 · 총급여 1,500만원','약 88만9천원','약 84만4천원','약 4만4천원'],['홑벌이 · 2,000만원','190만원','180만5천원','9만5천원'],['맞벌이 · 3,000만원','약 171만1천원','약 162만6천원','약 8만6천원'],['맞벌이 최대','330만원','313만5천원','16만5천원']]
B.table('pkg/img/02.png','기한 후 신청으로 깎이는 5%',['가구','정기 신청','기한 후 신청','차이'],rows2,hl_col=3,
        note='재산 1억7천만원 미만·체납 없음 가정, 법 계산식 기준(실제는 시행령 산정표)',src='조세특례제한법 제100조의5·제100조의7 (2026.10.8 조회)')
json.dump({'01.png':{'rows':rows},'02.png':{'rows':rows2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('ok')
