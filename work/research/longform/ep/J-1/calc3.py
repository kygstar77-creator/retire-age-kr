# J-1 계산 3(2026-10-19 롱폼 대본 담당) — 대본을 11분으로 늘리며 새로 넣는 장의 숫자. calc.py 함수를 그대로 쓴다.
# 실행: py -3.12 work/research/longform/ep/J-1/calc3.py > work/research/longform/ep/J-1/calc3_out.txt
# 원문: 현행 종합부동산세법 §8①(1세대1주택 12억·그 밖 9억, 공정시장가액비율 60~100% 시행령)·§9①(세율표)·§9③(재산세 공제)·§9⑤~⑧(연령·보유 공제, 합계 80%)
#       ·§10의2(공동명의 특례 9.16~9.30 신청)·§16(납부 12.1~12.15, 고지서 납부기간 5일 전까지 발급) — raw/law1019/*.txt(2026-10-19 법제처 API)
#       · 정부안 의안 2221046 주요내용(raw/bill_2221046.md) · 상세본 세율표(calc.RATES)
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calc as C
class C2:  # calc2.joint_person과 같은 식(calc2는 불러오면 표를 찍어서 옮겨 둠)
    @staticmethod
    def joint_person(share, year, prev=None, reside=True):
        ded = 9 * C.EOK if (year == 2026 or reside) else 6 * C.EOK
        if share <= 9 * C.EOK: return 0.0
        base = (share - ded) * C.FMV[year]
        calc = max(0.0, C.progressive(base, C.RATES[year]) - base * C.PROP_FMV * .004)
        return calc * 1.2
E = C.EOK


def man(x):
    return round(x / 10_000, 1)


def steps(price, year, age, held, lived, label):
    """고지서 계산 순서를 한 칸씩. calc.jongbu와 같은 식을 풀어 쓴다(마지막에 jongbu 값과 맞는지 확인)."""
    reside = lived > 0
    ded = 12 * E if year == 2026 else (14 * E if reside else 12 * E)
    fmv = C.FMV[year]
    base = (price - ded) * fmv
    calc = C.progressive(base, C.RATES[year])
    overlap = base * C.PROP_FMV * .004
    after = calc - overlap
    a = C.rate_of(age, C.AGE)
    if year == 2026:
        l = C.rate_of(held, C.LONG)
    elif year == 2027:
        l = max(C.rate_of(held, C.LONG) / 2, C.rate_of(lived, C.LONG))
    else:
        l = C.rate_of(lived, C.LONG)
    rate = min(.8, a + l)
    credit = after * rate
    cap = C.CREDIT_CAP[year]
    if cap is not None:
        credit = min(credit, cap)
    jong_wo = after - credit
    rural = jong_wo * .2
    jong = jong_wo + rural
    prop = C.property_tax(price)[1]
    chk = C.jongbu(price, year, age, held, lived, 'final')
    print(f"\n[고지서 계산 순서] {label} · {year}년분 · 단위 만원")
    print(f"① 공시가격 {price/E:.0f}억 − 공제 {ded/E:.0f}억 = {(price-ded)/E:.1f}억")
    print(f"② × 공정시장가액비율 {fmv*100:.0f}% = 과세표준 {base/E:.2f}억")
    print(f"③ 세율표: 산출세액 {man(calc)} (3억까지 0.5%=150.0 + 나머지 {man(base-3*E)/10000:.2f}억 × {C.RATES[year][1][1]*100:.1f}% = {man((base-3*E)*C.RATES[year][1][1])})")
    print(f"④ 재산세로 이미 낸 겹친 몫 빼기 {man(overlap)} → {man(after)}")
    print(f"⑤ 세액공제 {rate*100:.0f}%(나이 {a*100:.0f}% + {'보유' if year == 2026 else '거주'} {l*100:.0f}%) = {man(credit)} → {man(jong_wo)}")
    print(f"⑥ 농어촌특별세 20% {man(rural)} → 종부세 고지액 {man(jong)} (calc.jongbu {man(chk['jong'])})")
    print(f"⑦ 같은 해 재산세(지방교육세·도시지역분 포함) {man(prop)} · 보유세 합계 {man(prop + jong)} (calc {man(chk['total'])})")
    assert abs(man(jong) - man(chk['jong'])) <= 0.1, '풀어 쓴 식이 calc.jongbu와 다름'
    return jong


# 1) 올해(2026) 고지서 — 지금 법. 55세·10년 보유·10년 거주(C1과 같은 사람)
steps(20 * E, 2026, 55, 10, 10, '공시 20억 · 55세 · 10년 보유·거주 · 지금 법')
# 2) 같은 집 2028 정부안(거주)
steps(20 * E, 2028, 55, 12, 12, '공시 20억 · 55세 · 12년 거주 · 정부안(국회 통과 전)')

# 3) 공동명의 반반 · 비거주: 각자 몫이 9억을 넘으면(안 §7① '그 밖 9억 초과') 공제는 6억 → 문턱
print('\n[공동명의 반반 · 비거주 문턱] 2028년 종부세 둘 합(만원) · 정부안(국회 통과 전) · 각자 납부(특례 안 함)')
for p in (17.9, 18.0, 18.02, 19, 20):
    j = C2.joint_person(p * E / 2, 2028, reside=False) * 2
    jr = C2.joint_person(p * E / 2, 2028, reside=True) * 2
    print(f"공시 {p}억: 비거주 {man(j)} · 거주 {man(jr)}")

# 4) 갈래표: '종부세가 0원인 공시가격 상한' (1세대 1주택·부부 반반)
print('\n[갈래표] 종부세가 나오기 시작하는 공시가격(이 값 이하면 0원)')
rows = [
    ('혼자 명의 1주택 · 그 집에 산다', '12억', '14억'),
    ('혼자 명의 1주택 · 안 산다(세 줌·빈집)', '12억', '14억(넘으면 12억 공제 → 문턱)'),
    ('부부 반반 · 각자 냄 · 산다', '18억(각 9억)', '18억(각 9억)'),
    ('부부 반반 · 각자 냄 · 안 산다', '18억(각 9억)', '18억(각 9억 넘으면 6억 공제 → 문턱)'),
    ('부부 반반 · 특례 신청(한 사람으로)', '12억', '산다 14억 · 안 산다 14억'),
]
print('경우 | 2026(지금 법) | 2027~(정부안)')
for r in rows:
    print(' | '.join(r))
for p in (12, 14, 18):
    s26 = C.jongbu(p * E + 1e6, 2026, 55, 10, 10, 'final')['jong']
    s27 = C.jongbu(p * E + 1e6, 2027, 55, 10, 10, 'final')['jong']
    n27 = C.jongbu(p * E + 1e6, 2027, 55, 10, 0, 'final')['jong']
    j27 = C2.joint_person((p * E + 1e6) / 2, 2027, reside=True) * 2
    jn27 = C2.joint_person((p * E + 1e6) / 2, 2027, reside=False) * 2
    print(f"검산 공시 {p}억+100만원: 1주택 2026 {man(s26)} · 2027 거주 {man(s27)} · 2027 비거주 {man(n27)} · 반반 2027 거주 {man(j27)} · 반반 2027 비거주 {man(jn27)}")

# 5) 이해 시험 1차 '내년(2027) 고지서는?' — 안 사는 20억(55세·보유 10년) 2026→2027→2028 보유세
s = C.series(20 * E, 55, 10, 0, 'final')
print(f"\n[안 사는 20억 · 55세·보유 10년] 보유세 2026 {man(s[0]['total'])} → 2027 {man(s[1]['total'])}(+{man(s[1]['total']-s[0]['total'])}) → 2028 {man(s[2]['total'])}(+{man(s[2]['total']-s[0]['total'])}) · 종부세 {man(s[0]['jong'])} → {man(s[1]['jong'])} → {man(s[2]['jong'])}")
