# cc200vol1021 본문 그림 2장 — 숫자는 calc_out.txt(네이버 일별 종가·삼성자산운용 분배금)에서만
import sys, json, os
sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1 = [['3% 이상 빠진 42일 평균', '−5.8%', '−5.5%'], ['3% 이상 오른 42일 평균', '+5.5%', '+5.2%'],
      ['10월 20일', '−3.5%', '−3.6%'], ['10월 21일', '+3.4%', '+3.4%']]
B.table('pkg/img/01.png', '크게 움직인 날, 하루 등락률', ['', 'KODEX 200', '타겟위클리커버드콜'], r1,
        note='2024년 12월 3일 상장일부터 456거래일 · 분배금 받은 날은 분배금을 더해 셈', src='네이버 증권 일별 시세, 삼성자산운용 분배금 내역 · 파이어맵 직접 셈')
r2 = [['주식 평가액', '약 1,684만원', '약 1,535만원'], ['받은 분배금', '약 16만원', '약 300만원'], ['합계', '약 1,700만원', '약 1,835만원']]
B.table('pkg/img/02.png', '1년 전 오늘 1천만원씩 샀다면', ['', 'KODEX 200', '타겟위클리커버드콜'], r2,
        note='2025년 10월 21일 종가에 사서 2026년 10월 21일 종가로 셈 · 분배금은 재투자 안 함 · 세금·수수료 전', src='네이버 증권 일별 시세, 삼성자산운용 분배금 내역, 야후 파이낸스 · 파이어맵 직접 셈')
json.dump({'01.png': {'rows': r1}, '02.png': {'rows': r2}}, open('pkg/tables.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
