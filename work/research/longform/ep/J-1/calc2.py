# J-1 '우리만' 계산 2(2026-10-17 자료조사 담당) — calc.py 함수를 그대로 쓰고 새 질문만 더 계산한다.
# 실행: py -3.12 work/research/longform/ep/J-1/calc2.py > work/research/longform/ep/J-1/calc2_out.txt
# 원문: 의안 2221046 주요내용(raw/bill_2221046.md: §8① 부부공동명의 거주 9억·비거주 6억) · 9/1 수정안(raw/mofe_0901.txt 3번: 비거주 각 4억→6억)
#       · 문답자료 p.41(raw/mofe_0803_8.txt 1090행: 공동명의는 개별 납부 또는 1세대 1주택 특례 '신청 필요') · 국세청 공동명의 특례(9.16~9.30 신청, 다음 해부터 계속 적용)
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import calc as C
E = C.EOK; m = C.m

def joint_person(share, year, prev=None, reside=True):
    """부부 공동명의 각자 납부(특례 신청 안 함) — 한 사람 몫. 세액공제(연령·보유) 없음, 공제 2026 9억 / 정부안 거주 9억·비거주 6억.
    납세의무: 2026 공시 지분 9억 초과 · 정부안 '그 밖' 9억 초과(안 §7①). 세율 2026·2027은 1·2주택 표, 2028은 단일 표(calc.RATES와 같음).
    재산세는 집 전체로 계산해 지분대로 나눈다(공정시장가액비율 45% 가정은 calc와 같음)."""
    ded = 9 * E if (year == 2026 or reside) else 6 * E
    if share <= 9 * E: return 0.0
    base = (share - ded) * C.FMV[year]
    calc = max(0.0, C.progressive(base, C.RATES[year]) - base * C.PROP_FMV * .004)
    return calc * 1.2

def couple(price, age, lived, reside=True):
    print(f"\n[부부 공동명의 1주택 · 공시 {price/E:.0f}억 · 반반 · {age}세 · 그 집 {lived}년 {'거주' if reside else '비거주'}] 단위 만원 · 정부안(국회 통과 전)")
    prop = C.property_tax(price)[1]
    for y in (2026, 2027, 2028):
        j = joint_person(price / 2, y, reside=reside) * 2
        s = C.jongbu(price, y, age, lived + (y - 2026), (lived + (y - 2026)) if reside else 0, 'final')
        print(f"- {y}: 각자 납부(둘 합) 종부세 {m(j)} · 보유세 {m(prop + j)} | 특례 신청(한 사람 1주택으로) 종부세 {m(s['jong'])} · 보유세 {m(s['total'])} → 더 적은 쪽: {'각자' if j < s['jong'] else '특례'} (차이 {m(abs(j - s['jong']))})")

for p in (16, 20, 25, 30):
    couple(p * E, 55, 10)
for p in (20, 30):
    couple(p * E, 70, 15)
for p in (20, 30):
    couple(p * E, 55, 10, reside=False)

print('\n[댓글 질문] "9억에 산 집이 40억 됐음, 20년 보유 실거주"(SLh90bWU7Tw) — 시가 40억이면 공시가격은? 정부 사례 짝(시가 30억↔공시 20억, 시가 50억↔공시 35억)의 비율 67~70%를 써 공시 27억·28억 두 가지로')
for p in (27, 28):
    for age in (60, 65, 70):
        s = C.series(p * E, age, 20, 20, 'final')
        print(f"- 공시 {p}억 · {age}세 · 20년 거주: 보유세 2026 {m(s[0]['total'])} → 2028 {m(s[2]['total'])} ({m(s[2]['total'] - s[0]['total']):+}) · 종부세 2026 {m(s[0]['jong'])} → 2028 {m(s[2]['jong'])} · 2028 세액공제 한도 걸림 {'예' if s[2]['credit_raw'] > s[2]['credit'] else '아니오'}")

print('\n[댓글 질문] "한집에 30년 산 게 죄입니까"(SLh90bWU7Tw) — 거주공제율은 15년 이상이 상한(50%) → 15년과 30년이 같은지')
for lived in (15, 30):
    s = C.series(20 * E, 70, lived, lived, 'final')
    print(f"- 공시 20억 · 70세 · {lived}년 거주: 2028 종부세 {m(s[2]['jong'])} · 보유세 {m(s[2]['total'])}")

print('\n[정부 사례③ 2027 불일치 원인] 공시 50억·70세·10년 거주(8월안). 정부 표 같은 칸: 세액공제 한도 전 2,141.1 · 한도 800 · 종부세 1,942.1')
r = C.jongbu(50 * E, 2027, 70, 10, 10, 'aug', 1788.3 * 1e4)
print(f"- calc 산출세액(공제할 재산세 뺀 뒤) {m(r['calc'])} · 세액공제 한도 전 {m(r['credit_raw'])}(정부 2,141.1과 같음) · 한도 뒤 {m(r['credit'])} · 종부세 (산출 − 800) × 1.2 = {m(r['jong'])}")
print(f"- 정부 2,141.1 ÷ 80% = {2141.1/0.8:.1f} → 정부도 산출세액을 {2141.1/0.8:.1f}로 잡았다는 뜻. 여기서 800을 빼고 농특세 20%를 붙이면 {(2141.1/0.8-800)*1.2:.1f}")
print(f"- 정부 종부세 1,942.1 ÷ 1.2 + 800 = {1942.1/1.2+800:.1f} → 이 산출세액이면 세액공제 한도 전은 {(1942.1/1.2+800)*0.8:.1f}이어야 하는데 정부 표는 2,141.1 → 같은 칸 두 숫자가 서로 안 맞음")
alt = C.RATES[2027][:]; alt[3] = (25, .013)
g = C.progressive((50 - 14) * E * .7, alt) - (50 - 14) * E * .7 * .45 * .004
print(f"- 가장 가까운 설명: 12~25억 구간을 현행 1.3%로 둔 계산 → 종부세 {m((g - 800e4) * 1.2)}(정부 1,942.1과 {abs(m((g - 800e4) * 1.2) - 1942.1):.1f} 차) — 0.2 안에 안 들어 단정하지 않음")
print(f"- 사례③ 2028(같은 정부 표): calc {m(C.jongbu(50*E, 2028, 70, 10, 10, 'aug')['jong'])} = 정부 3,295.7 → 2028 세율표·한도 600은 맞음")
