import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
P = [l for l in open('../longform/ep/N-2/calc_out.txt', encoding='utf-8').read().split('[Q]')[0].splitlines()[2:] if l.strip()]
P = [[' '.join(l.split()[:-7])] + l.split()[-7:] for l in P]
SRC = '국가데이터처 「2024년 임금근로일자리 소득(보수) 결과」 표7·표8, 2024년 12월 세전 월 보수·일자리 기준'
want = ['20~24세', '25~29세', '30~34세', '35~39세', '40~44세', '45~49세', '50~54세', '55~59세', '60~64세']
r1 = [[p[0], p[3] + '%', p[2] + '%'] for p in P if p[0] in want]
B.table('pkg/img/01.png', '같은 나이대 일자리 중 이 월급 이상 비율', ['나이', '월 450만원 이상', '월 350만원 이상'], r1, hl_col=1,
        note='비율이 곧 "상위 몇 %"입니다. 예) 35~39세 월 450만원 이상 36.2% = 상위 36% 안(2024년 12월 일자리 기준)', src=SRC)
cols = ['나이', '250만↑', '350만↑', '450만↑', '550만↑', '650만↑', '800만↑', '1000만↑']
r2 = [[p[0]] + [x + '%' for x in p[1:]] for p in P]
B.table('pkg/img/02.png', '자세한 표 · 나이별 「월 ○만원 이상」 일자리 비율(2024년 12월)', cols, r2, W=1640,
        note='단위 % · 세전 월 보수 · 시간제·단기 일자리 포함', src=SRC)
r3 = [['상위 10% 선', '8,770만~9,117만원 사이'], ['상위 30% 선', '4,947만~5,063만원 사이'], ['한가운데(50%) 선', '3,358만~3,417만원 사이']]
B.table('pkg/img/03.png', '1년 연봉(국세청)으로 본 선 · 월급 표와 다른 자료', ['자리', '연봉'], r3, hl_col=1,
        note='국세청 자료는 칸마다 평균만 있어 선은 위아래 두 칸 평균 사이로만 말할 수 있어요 · 몇 달만 일한 사람 포함',
        src='국세청 근로소득 백분위(천분위) 자료, 공공데이터포털 15082063(2024년분)')
json.dump({'01.png': {'rows': r1}, '02.png': {'rows': r2}, '03.png': {'rows': r3}}, open('pkg/tables.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(r1[:2], r2[0])
