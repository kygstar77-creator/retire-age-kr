# 적금 월 100만원 1년 세후 이자 계산 — saving1011b
# 정액(또는 매달 같은 날 같은 금액) 단리: 이자 = 월 납입 × 연금리 × (12+11+…+1)/12 = 월 납입 × 연금리 × 6.5
# 세금: 소득세법 제129조①1호라 이자소득 14% + 지방세법 제103조의13① 지방소득세(소득세의 10%) = 15.4%
#       원천징수 실제 계산은 소득세·지방소득세 각각 10원 미만 절사(국세징수법·지방세법 끝수 처리) → '약'으로 씀
import sys, json, statistics; sys.stdout.reconfigure(encoding='utf-8')
def tax(i):
    it = int(i * 0.14) // 10 * 10; lt = int(it * 0.10) // 10 * 10
    return it, lt, i - it - lt
M = 1_000_000
print('월 100만원 12개월, 원금 합계', f'{M*12:,}')
for nm, r in [('은행 1년 적금 기본금리 1위 KDB 자유적금(금감원 공시)', 3.86), ('한은 8월 예금은행 정기적금(1~2년) 신규 평균', 3.46), ('은행 1년 적금 57줄 기본금리 가운데값', 2.80)]:
    i = M * r / 100 * 6.5; it, lt, net = tax(i)
    print(f'{nm} {r}%: 세전 {i:,.0f} / 소득세 {it:,} 지방세 {lt:,} / 세후 {net:,.0f} / 원금 대비 {net/(M*12)*100:.2f}%')
# 금리를 1,200만원 전체에 곱한 잘못된 기대
print(f'잘못된 기대(1,200만원 × 3.86%) {12_000_000*0.0386:,.0f}')
# 첫 달·마지막 달 돈이 받는 이자
print(f'첫 달 100만원 이자(12개월) {M*0.0386:,.0f} / 마지막 달 100만원(1개월) {M*0.0386/12:,.0f}')
# 한도 30만원 상품(케이뱅크 코드K 자유적금 3.80%)
i = 300_000 * 0.038 * 6.5; print(f'코드K 월 30만원 3.80%: 세전 {i:,.0f} 세후 {tax(i)[2]:,.0f}')
# 목돈 1,200만원이 이미 있다면 1년 정기예금 1위 3.92%
i = 12_000_000 * 0.0392; print(f'정기예금 1,200만원 3.92%: 세전 {i:,.0f} 세후 {tax(i)[2]:,.0f}')
# 금감원 공시 중앙값(재계산)
s = json.load(open('fin_saving.json', encoding='utf-8')); d = json.load(open('fin_deposit.json', encoding='utf-8'))
sv = [o['intr_rate'] for o in s['opt'] if o['save_trm'] == '12']; dv = [o['intr_rate'] for o in d['opt'] if o['save_trm'] == '12']
print(f'적금 12개월 {len(sv)}줄 가운데값 {statistics.median(sv)} 최고 {max(sv)} / 3.5% 이상 {sum(v>=3.5 for v in sv)}줄')
print(f'예금 12개월 {len(dv)}줄 가운데값 {statistics.median(dv)} 최고 {max(dv)} / 3.5% 이상 {sum(v>=3.5 for v in dv)}줄')
print('조회', s['at'], '공시월', {b['dcls_month'] for b in s['base']})
