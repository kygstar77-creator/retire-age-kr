# cofix1117 계산 — 은행연합회 COFIX 월별 공시(raw/cofix_month_2025.xlsx·2026.xlsx, 11/16 23:1x 받음)
import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')
rows = {}
for y in (2025, 2026):
    ws = openpyxl.load_workbook(f'raw/cofix_month_{y}.xlsx', data_only=True).active
    for r in ws.iter_rows(min_row=3, values_only=True):
        if r[0]: rows[r[1]] = (r[0], float(r[2]), float(r[3]), float(str(r[4]).strip()))
for k in sorted(rows): print(k, rows[k])
now, prev, yago = rows['2026/10'], rows['2026/09'], rows['2025/10']
names = ['신규취급액', '잔액', '신잔액']
P = 300_000_000
print('\n10월 vs 9월 / vs 1년 전(2025/10)')
for i, n in enumerate(names):
    d1 = round(now[i+1] - prev[i+1], 2); d12 = round(now[i+1] - yago[i+1], 2)
    yr = P * d12 / 100
    print(f'{n}: {yago[i+1]} -> {now[i+1]} (전월 {d1:+.2f}%p, 1년 {d12:+.2f}%p) 3억 연 이자 +{yr/1e4:.0f}만원, 월 +{yr/12/1e4:.1f}만원')
# 신규가 잔액을 처음 넘은 달
for k in sorted(rows):
    if rows[k][1] > rows[k][2]: print('신규>잔액 첫 달', k, rows[k]); break
print('1억 신규 1년:', 1e8 * (now[1]-yago[1]) / 100 / 1e4, '만원')
print('기준금리(ECOS 722Y001): 2025/10 2.50 -> 2026/10 3.00, 변경일 2026-07-16 2.75, 2026-08-27 3.00')
print('신규 1년 상승 / 기준금리 상승 =', round((now[1]-yago[1]) / 0.5, 2))
