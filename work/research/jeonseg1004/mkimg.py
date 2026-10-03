import sys, json; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
SRC = '주택도시보증공사 전세보증금반환보증 상품개요(2026-10-03 조회)'
T1 = [('1순위', 'KB시세·부동산원 시세', '공시가격 × 140%'), ('2순위', '공시가격 × 140%', '안심전세 앱 시세 하한가'),
      ('3순위', '안심전세 앱 시세 하한가', '1년 안 매매가'), ('보증 한도', '집값 × 90% − 앞선 빚', '집값 × 90% − 앞선 빚')]
B.table('pkg/img/01.png', '전세보증보험, 집값을 잡는 순서', ['', '아파트·오피스텔', '연립·다세대 빌라'], [list(x) for x in T1], hl_col=2,
        note='감정평가서(6개월 안)가 있으면 그 값을 가장 먼저 씀', src=SRC)
T2 = [('아파트 · 부채비율 70% 이하', '연 0.107%', '64만 2천원'), ('아파트 · 80% 초과', '연 0.154%', '92만 4천원'),
      ('빌라 등 · 70% 이하', '연 0.124%', '74만 4천원'), ('빌라 등 · 80% 초과', '연 0.197%', '118만 2천원')]
B.table('pkg/img/02.png', '전세금 3억원 2년 계약, 보증료는 얼마', ['집 · 부채비율', '보증료율', '2년 보증료'], [list(x) for x in T2], hl_col=2,
        note='부채비율 = (앞선 빚 + 전세금) ÷ (집값 × 90%) · 할인·할증 전 금액', src=SRC + ' · 2억 초과~5억 이하 구간')
json.dump({'01.png': {'cols': ['', '아파트·오피스텔', '연립·다세대 빌라'], 'rows': [list(x) for x in T1]},
           '02.png': {'cols': ['집 · 부채비율', '보증료율', '2년 보증료'], 'rows': [list(x) for x in T2]}},
          open('pkg/tables.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok')
