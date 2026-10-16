# soxl1016 표 — calc_out.txt 값만 (3칸 이하)
import sys, json, os; sys.path.insert(0, r'C:\Users\강영준\Documents\GitHub\retire-age-kr\work')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import blogimg as B
r1 = [['1년 전', '180만원', '269만원'], ['3년 전', '329만원', '576만원'], ['5년 전', '353만원', '265만원']]
B.table('pkg/img/01.png', '100만원을 넣고 10월 15일까지 뒀다면', ['넣은 때', 'SOXX (1배)', 'SOXL (3배)'], r1, hl_col=2,
        note='같은 NYSE 반도체 지수 · 분배금은 다시 넣었다고 침 · 세금 떼기 전 · 환율 변화·수수료 계산 안 함(달러 수익률을 100만원에 곱함)',
        src='야후 파이낸스 일별 수정종가(2026.10.15까지), 직접 계산', W=1640)
r2 = [['2024년 6월 4일', '100만원', '100만원'], ['2025년 4월 8일', '67만원', '18만원'], ['2025년 6월 11일', '98만원', '46만원']]
B.table('pkg/img/02.png', '지수가 1년 동안 제자리였을 때', ['날짜', 'SOXX (1배)', 'SOXL (3배)'], r2, hl_col=2,
        note='2024년 6월 4일 종가에 100만원씩 넣었다고 침 · SOXX는 1년 뒤 거의 제자리, SOXL은 절반 아래',
        src='야후 파이낸스 일별 수정종가, 직접 계산', W=1640)
json.dump({'01.png': {'rows': r1}, '02.png': {'rows': r2}}, open('pkg/tables.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
