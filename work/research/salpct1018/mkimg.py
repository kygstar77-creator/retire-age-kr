import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
B.steps('pkg/img/01.png', '엑셀 쓰는 법', ['원천징수영수증에서 「총급여」 찾기(비과세 뺀 세전 1년 금액)', '첫 장 노란 칸에 만원 단위로 넣기(5,000만원이면 5000)', '아래 칸에 나온 「두 구간 평균 사이」 읽기'],
        note='파일은 이 글 맨 아래에 있어요', src='국세청 근로소득 백분위(천분위) 자료 2024년분으로 만든 엑셀')
r2 = [['3,000만원', '상위 58% 칸 ~ 상위 57% 칸 평균 사이'], ['5,000만원', '상위 31% 칸 ~ 상위 30% 칸 평균 사이'], ['1억원', '상위 8% 칸 ~ 상위 7% 칸 평균 사이']]
B.table('pkg/img/02.png', '넣으면 이렇게 나와요', ['총급여', '결과'], r2, hl_col=1,
        note='국세청 자료는 칸 합계뿐이라 정확한 경계값 대신 두 칸 평균 사이로 알려 줘요', src='국세청 근로소득 백분위(천분위) 자료, 공공데이터포털 15082063(2024년분)')
json.dump({'02.png': {'rows': r2}}, open('pkg/tables.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
