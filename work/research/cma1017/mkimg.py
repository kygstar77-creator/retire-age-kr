import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1 = [['RP형', '국공채 담보 채권(RP)', '안 됨'], ['발행어음형', '증권사가 발행한 어음', '안 됨'], ['MMF형 · MMW형', '단기 채권 펀드 · 한국증권금융', '안 됨'],
      ['종금형', '종합금융회사 상품', '됨'], ['주식 계좌 예수금', '주식 안 사고 둔 현금', '됨']]
B.table('pkg/img/01.png', 'CMA 종류별 예금자보호', ['종류', '내 돈이 들어가는 곳', '예금자보호'], r1, hl_col=2,
        note='보호되는 것(종금형·예수금)도 한 금융회사에 원금과 이자를 합쳐 1억원까지(2025년 9월부터)',
        src='예금자보호법 제2조·시행령 제3조(10월 17일 조회), 한국투자증권·신한투자증권 CMA 안내', W=1640)
r2 = [['신한투자증권 RP형', '2.45%', '약 1만7천원'], ['한국투자증권 RP형', '2.50%', '약 1만7천원'], ['한국투자증권 발행어음형', '2.85%', '약 2만원']]
B.table('pkg/img/02.png', '1천만원을 CMA에 30일 넣으면 받는 이자', ['상품', '연 금리(세전)', '세후 이자'], r2, hl_col=2,
        note='세금 15.4% 뗀 값 · 한국투자증권 RP형 8월 31일, 발행어음형 9월 4일 기준 · 금리는 회사가 바꿀 수 있음',
        src='한국투자증권·신한투자증권 CMA 안내(10월 17일 조회), 직접 계산', W=1640)
json.dump({'01.png': {'rows': r1}, '02.png': {'rows': r2}}, open('pkg/tables.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
