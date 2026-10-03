# n1cafe1004 표 그림 2장 — facts.txt 표A-위치·표B 값만. firemap-write 2026-10-03
import sys; sys.path.insert(0, r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
import blogimg as B
P = r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work/research/n1cafe1004/pkg/img/'
SRC = '국세청 근로소득 백분위(천분위) 자료 2024년 귀속 · 칸 평균 = 구간 총급여 합계 ÷ 인원'
B.table(P+'01.png', '내 연봉은 위에서 몇 % 칸 사이일까',
        ['연봉', '위에서 몇 % 사이'],
        [['3,000만원', '57%와 58%'], ['4,000만원', '41%와 42%'], ['평균 4,475만원', '35%와 36%'],
         ['5,000만원', '30%와 31%'], ['7,000만원', '17%와 18%'], ['1억원', '7%와 8%'], ['2억원', '상위 1% 안쪽']],
        hl_col=1, src=SRC)
B.table(P+'02.png', '연봉 몫과 근로소득세 몫',
        ['누구', '받은 연봉', '낸 세금'],
        [['상위 1%', '7.7%', '30.3%'], ['상위 10%', '31.7%', '71.7%'], ['아래 절반', '20.4%', '1.43%']],
        hl_col=2, src=SRC + ' · 결정세액 합계 65조 1,605억원')
