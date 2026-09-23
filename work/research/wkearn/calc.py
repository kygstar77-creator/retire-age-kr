# 이번 주 실적 발표(2026-09-24~25) 파생값 계산. 실행: py -3.12 work/research/wkearn/calc.py
import json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(os.path.join(D, 'raw.json'), encoding='utf-8'))

def num(s):
    s = (s or '').strip().replace('$', '').replace(',', '')
    neg = s.startswith('(') and s.endswith(')')
    s = s.strip('()')
    if not s or s == 'N/A': return None
    try: v = float(s)
    except ValueError: return None
    return -v if neg else v

rows = []
for day, rs in raw['earnings'].items():
    for r in rs:
        rows.append(dict(day=day, sym=r['symbol'], name=r['name'], cap=num(r.get('marketCap')),
                         t=r.get('time'), last=num(r.get('lastYearEPS')), fc=num(r.get('epsForecast')),
                         q=r.get('fiscalQuarterEnding'), n=r.get('noOfEsts')))
print('발표 종목 수 %d (9/24 %d · 9/25 %d)' % (len(rows), len(raw['earnings']['2026-09-24']), len(raw['earnings']['2026-09-25'])))
print('시총 1,000억 달러 이상: %s' % [r['sym'] for r in rows if r['cap'] and r['cap'] >= 100e9])
print('시총 100억 달러 이상: %s' % [r['sym'] for r in rows if r['cap'] and r['cap'] >= 10e9])
print('예상 EPS 없는 곳: %d곳' % sum(1 for r in rows if r['fc'] is None))
print('추정치 10명 이상: %s' % [(r['sym'], r['n']) for r in rows if str(r['n']).isdigit() and int(r['n']) >= 10])
print('시총 합계: %.1f억 달러' % (sum(r['cap'] or 0 for r in rows) / 1e8))
cost = next(r for r in rows if r['sym'] == 'COST')
print('코스트코 시총 비중: %.1f%%' % (cost['cap'] / sum(r['cap'] or 0 for r in rows) * 100))
up = [r for r in rows if r['fc'] is not None and r['last'] is not None and r['fc'] > r['last']]
print('예상 EPS가 작년보다 높은 곳 %d곳: %s' % (len(up), [(r['sym'], r['last'], r['fc']) for r in up]))
print('배당락일 건수: 9/24 %d · 9/25 %d · 합 %d' % (len(raw['div']['2026-09-24']), len(raw['div']['2026-09-25']),
                                                len(raw['div']['2026-09-24']) + len(raw['div']['2026-09-25'])))
print()
# --- 코스트코 ---
P, FX = 900.76, 1366.43
SH = 444.430          # Q3 FY2026 희석 주식수(백만 주)
print('[코스트코] 주가 %.2f달러 = %s원' % (P, format(round(P * FX), ',')))
print('  52주 최고 1,096.50 대비 %+.2f%% · 52주 최저 844.06 대비 %+.2f%%' % (P / 1096.50 * 100 - 100, P / 844.06 * 100 - 100))
print('  4분기 예상 EPS 6.48 vs 작년 4분기 5.87 → %+.2f%%' % (6.48 / 5.87 * 100 - 100))
print('  36주 실적 14.01 + 4분기 예상 6.48 = %.2f달러' % (14.01 + 6.48))
print('  작년 연간 18.21 대비 %+.2f%%' % ((14.01 + 6.48) / 18.21 * 100 - 100))
m = 2610 / 84432
print('  작년 4분기 순이익률 2,610 / 84,432 = %.3f%%' % (m * 100))
ni = 93900 * m
print('  올해 4분기 매출 93,900에 같은 마진 → 순이익 %.0f백만 달러, EPS %.2f달러' % (ni, ni / SH))
print('  예상 PER: %.1f배(예상 20.49) · %.1f배(작년 18.21)' % (P / (14.01 + 6.48), P / 18.21))
print('  배당 연 5.88달러 ÷ %.2f = %.3f%%' % (P, 5.88 / P * 100))
print('  분기 배당 1.30 → 1.47달러 %+.1f%%' % (1.47 / 1.30 * 100 - 100))
print('  회원수수료 36주 4,057 vs 작년 3,599 → %+.2f%%' % (4057 / 3599 * 100 - 100))
print('  창고 939개 − 914개 = %d개' % (939 - 914))
print('  4분기 16주 매출 93.9 / 16 = 주당 %.2f억 달러' % (93.9 / 16 * 10))
