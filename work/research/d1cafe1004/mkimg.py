# d1cafe1004 표 그림 2장 — facts.txt [계산] 값만. firemap-write 2026-10-03
import sys; sys.path.insert(0, r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work')
import blogimg as B
P = r'C:/Users/강영준/Documents/GitHub/retire-age-kr/work/research/d1cafe1004/pkg/img/'
SRC = '국민건강보험법 시행령 제44조·시행규칙 제44조 · 지역가입자 1인·재산 0·다른 소득 0·2026년 · 장기요양 포함, 10원 미만 버림'
B.table(P+'01.png', '1년 배당·이자에 따른 월 건강보험료',
        ['1년 배당·이자', '월 건보료'],
        [['1,000만원 이하', '2만 2,800원'], ['1,001만원', '6만 7,850원'], ['1,200만원', '8만 1,340원'],
         ['2,000만원', '13만 5,570원']],
        hl_col=1, src=SRC)
B.table(P+'02.png', '국민연금 월 150만원을 받을 때',
        ['1년 배당·이자', '월 건보료'],
        [['없음', '6만 1,000원'], ['1,000만원', '6만 1,000원'], ['1,001만원', '12만 8,860원']],
        hl_col=1, src=SRC + ' · 연금은 절반만 소득으로 반영')
