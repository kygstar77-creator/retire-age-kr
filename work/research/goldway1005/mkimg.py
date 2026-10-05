import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
rows=[['KRX 금시장','-2.4%','약 975만 8천원','없음'],['ACE KRX금현물 ETF','-3.2%','약 968만원','없음(손해)'],
      ['골드뱅킹(어림)','+1.3%','약 1,011만원','차익의 15.4%']]
B.table('pkg/img/01.png','1년 전 금 1천만원, 지금 얼마',['사는 곳','1년 수익(세전)','세금 떼고 지금','세금'],rows,hl_col=2,
        note='2025-10-02 → 2026-10-02 · 골드뱅킹은 1년 전 값을 국제 금값×환율로 어림, 은행이 사고팔 때 떼는 1%씩 반영',src='네이버 금융 KRX 금 일별 · 야후 파이낸스 · KB국민은행 골드뱅킹 고시')
rows2=[['KRX 금시장','면제','없음','없음'],['금 ETF','-','15.4%(배당소득)','2천만원 넘으면 합산'],
       ['골드뱅킹','-','15.4%(배당소득)','2천만원 넘으면 합산'],['골드바·금은방','살 때 10%','없음','없음']]
B.table('pkg/img/02.png','금 사는 길마다 붙는 세금',['사는 곳','부가세','판 차익 세금','금융소득 종합과세'],rows2,hl_col=2,
        note='KRX 금도 실물로 찾으면 그때 부가세 10%',src='조세특례제한법 제126조의7 · 부가가치세법 제30조 · 소득세법 제14·17·94·129조')
json.dump({'01.png':{'rows':rows},'02.png':{'rows':rows2}},open('pkg/tables.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
