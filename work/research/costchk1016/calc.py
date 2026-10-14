# costchk1016 계산 — 생산자물가(ECOS 404Y014 총지수, ppi.json) · 공사비 검증 수수료(고시 2024-468 별표1·2)
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
rows = json.load(open('ppi.json', encoding='utf-8'))['StatisticSearch']['row']
P = {r['TIME']: float(r['DATA_VALUE']) for r in rows}
NOW = '202608'  # 2026년 9월 증액 신청 → 직전달 8월 (고시 제3조②)
print('생산자물가지수 총지수(2020=100) 최신', NOW, P[NOW], '· 행수', len(P))
INC = 15.0
print(f'\n[A] 공사비 {INC}% 증액 신청(2026년 9월) — 계약 공사비 산정 기준일별 물가 몫')
for base in ['202107', '202207', '202307', '202407', '202507']:
    p = (P[NOW] / P[base] - 1) * 100
    sub = INC - p
    div = ((1 + INC / 100) / (P[NOW] / P[base]) - 1) * 100
    v10 = '검증 의무' if sub >= 10 else '아님'
    v5 = '검증 의무' if sub >= 5 else '아님'
    same = (sub >= 5) == (div >= 5) and (sub >= 10) == (div >= 10)
    print(f'기준일 {int(base[:4])}년 {int(base[4:])+1}월(직전달 {base} {P[base]}) 물가 {p:.2f}% · 빼고 남는 증액 {sub:.2f}% (나눗셈식 {div:.2f}%, 결론 같음 {same}) · 인가 전 선정(10%) {v10} · 인가 후 선정(5%) {v5}')

def fee_inc(x):  # 별표2 증액공사 (원)
    e = 1e8
    if x <= 10 * e: return 5_000_000
    if x <= 50 * e: return 5_000_000 + (x - 10 * e) * 40 / 10000
    if x <= 100 * e: return 21_000_000 + (x - 50 * e) * 25 / 10000
    if x <= 200 * e: return 33_500_000 + (x - 100 * e) * 15 / 10000
    return 48_500_000 + (x - 200 * e) * 5 / 10000
def fee_all(x):  # 별표1 전체공사
    e = 1e8
    if x <= 100 * e: return 5_000_000
    if x <= 500 * e: return 5_000_000 + (x - 100 * e) * 40 / 100000
    if x <= 1000 * e: return 21_000_000 + (x - 500 * e) * 25 / 100000
    if x <= 2000 * e: return 33_500_000 + (x - 1000 * e) * 15 / 100000
    return 48_500_000 + (x - 2000 * e) * 5 / 100000
print('\n[B] 예시 조합: 당초 계약 공사비 4,000억원, 조합원 1,000명, 15% 증액 = 600억원')
e = 1e8; base = 4000 * e; inc = base * INC / 100; n = 1000
print(f'증액 {inc/e:.0f}억원 · 조합원 1인 평균 {inc/n/1e4:,.0f}만원')
f2 = fee_inc(inc); print(f'증액공사 검증 수수료(별표2) {f2:,.0f}원 · 1인 {f2/n:,.0f}원')
for tot in (base, base + inc):
    f1 = fee_all(tot); print(f'전체공사 검증 수수료(별표1, 전체 공사비 {tot/e:,.0f}억) {f1:,.0f}원 · 1인 {f1/n:,.0f}원')
p23 = (P[NOW] / P['202307'] - 1) * 100
print(f'2023년 8월 기준일이면 물가 몫 {p23:.2f}% = {base*p23/100/e:.0f}억원, 물가 빼고 남는 증액 {(INC-p23):.2f}% = {base*(INC-p23)/100/e:.0f}억원')
print('\n[C] 별표2 구간 예시')
for x in (10, 50, 100, 200, 600):
    print(f'증액 {x}억원 → 수수료 {fee_inc(x*e):,.0f}원')
