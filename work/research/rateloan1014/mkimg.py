# rateloan1014 표 — calc_out.json(finlife 2026.09 공시)만
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
out = json.load(open('calc_out.json', encoding='utf-8'))
rows = [[b, f'{v:.2f}%', f'{f:.2f}%' + (' (혼합)' if b == '국민은행' else ''), f'{g:.2f}%p', f'{d:,}원'] for b, _, v, _, f, g, pv, pf, d in out]
B.table('pkg/img/01.png', '은행 15곳 주담대 변동·고정 최저 금리와 3억 한 달 상환액 차이', ['은행', '변동 최저', '고정 최저', '차이', '3억 한 달 차이'], rows, hl_col=4,
        note='2026년 9월 공시 · 아파트 담보 · 분할상환 · 은행마다 가장 낮은 상품 · 변동·고정을 둘 다 공시한 은행만(SC제일·iM뱅크는 변동만) · 한 달 차이 = 3억원 30년 원리금균등 상환액(고정 − 변동) · 국민은행 고정 칸은 혼합금리 상품',
        src='금융감독원 금융상품통합비교공시(은행 주택담보대출)')
json.dump({'01.png': {'rows': rows}}, open('pkg/tables.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
