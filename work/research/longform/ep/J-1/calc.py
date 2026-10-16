# J-1 1주택 종부세 2026→2027→2028 계산기 (정부안 원문 기준)
# 원문: raw/mofe_0803_6.txt(상세본 p.60~65), raw/mofe_0803_8.txt(문답 p.39~45 적용사례),
#       raw/mofe_0901.txt(9/1 국무회의 수정: 비거주 1주택 공제 12억 유지·세부담 상한 150% 유지)
# 모드 aug = 8/3 발표안(정부 적용사례 재현용), final = 9/1 국무회의 수정 정부안(국회 심사 중, 법 아님 — 10/17 이해 시험: '확정'이라 쓰면 법이 정해진 것으로 읽혀 라벨 바꿈)
import sys

EOK = 100_000_000

# 종부세 세율표 (과표 상한, 세율) — 1·2주택 기준. 1세대 1주택만 다룬다.
RATES = {
    2026: [(3, .005), (6, .007), (12, .010), (25, .013), (50, .015), (94, .020), (None, .027)],
    2027: [(3, .005), (6, .007), (12, .013), (25, .015), (50, .020), (94, .027), (None, .035)],
    2028: [(3, .005), (6, .007), (12, .013), (25, .020), (50, .030), (94, .040), (None, .050)],
}
FMV = {2026: .60, 2027: .70, 2028: .70}           # 1세대 1주택 종부세 공정시장가액비율
CREDIT_CAP = {2026: None, 2027: 8_000_000, 2028: 6_000_000}
PROP_FMV = .45   # 재산세 공정시장가액비율(1주택 공시 6억 초과) — 정부 사례 재현으로 확인한 값, 2027년 이후는 시행령 가정
AGE = [(70, .40), (65, .30), (60, .20)]
LONG = [(15, .50), (10, .40), (5, .20)]           # 거주(2028~)·보유(2026) 기간 공제율


def progressive(base, table):
    tax, lo = 0.0, 0.0
    for hi, r in table:
        top = base if hi is None else min(base, hi * EOK)
        if top > lo:
            tax += (top - lo) * r
        if hi is None or base <= hi * EOK:
            break
        lo = hi * EOK
    return tax


def property_tax(price):
    """재산세(표준세율)·도시지역분·지방교육세. 공시 9억 넘는 1주택이라 특례세율 없음."""
    base = price * PROP_FMV
    std = progressive(base, [(0.6, .001), (1.5, .0015), (3, .0025), (None, .004)])
    return std, std + base * .0014 + std * .2


def rate_of(years, table):
    for y, r in table:
        if years >= y:
            return r
    return 0.0


def jongbu(price, year, age, held, lived, mode="final", prev_total=None):
    """1세대 1주택 한 해 종부세(농특세 포함)와 보유세. held=보유 연수, lived=거주 연수(그 집)."""
    reside = lived > 0
    if year == 2026:
        ded = 12 * EOK
    elif reside:
        ded = 14 * EOK
    else:
        ded = (9 if mode == "aug" else 12) * EOK
    threshold = 12 * EOK if year == 2026 else 14 * EOK
    std, prop_total = property_tax(price)
    if price <= threshold:
        return dict(jong=0, credit=0, credit_raw=0, total=prop_total, prop=prop_total, calc=0)
    base = max(0.0, (price - ded) * FMV[year])
    calc = progressive(base, RATES[year])
    overlap = base * PROP_FMV * .004 if base > 0 else 0   # 공제할 재산세(과표 3억 초과 구간 0.4%)
    calc = max(0.0, calc - overlap)
    a = rate_of(age, AGE)
    if year == 2026:
        l = rate_of(held, LONG)
    elif year == 2027:
        l = max(rate_of(held, LONG) / 2, rate_of(lived, LONG))
    else:
        l = rate_of(lived, LONG)
    credit_raw = calc * min(.8, a + l)
    credit = credit_raw if CREDIT_CAP[year] is None else min(credit_raw, CREDIT_CAP[year])
    jong = (calc - credit) * 1.2                          # 농어촌특별세 20%
    total = prop_total + jong
    cap = 2.0 if (mode == "aug" and year >= 2027) else 1.5
    if prev_total is not None and total > prev_total * cap:
        jong = max(0.0, jong - (total - prev_total * cap))
        total = prop_total + jong
    return dict(jong=jong, credit=credit, credit_raw=credit_raw, total=total, prop=prop_total, calc=calc)


def m(x):
    return round(x / 10_000, 1)


def series(price, age, held, lived, mode, cap_chain=True):
    out, prev = [], None
    for y in (2026, 2027, 2028):
        r = jongbu(price, y, age, held + (y - 2026), lived + (y - 2026) if lived else 0, mode,
                   prev if cap_chain else None)
        out.append(r)
        prev = r["total"]
    return out


def verify():
    # 정부 문답자료 p.45 적용사례(8월안, 공시가 변동 없음, 단위 만원): 종부세 합계·보유세
    # 사례에는 매년 보유 연수가 늘지 않는다(10년 고정) — 정부 표 그대로 재현하려고 같은 가정
    cases = [
        ("① 공시 30억 70세 10년 거주", 30, 70, 10, 10, [(154.9, 916.3), (200.3, 961.7), (281.3, 1042.7)]),
        ("② 공시 30억 70세 10년 보유(비거주)", 30, 70, 10, 0, [(154.9, 916.3), (614.6, 1376.0), (1019.1, 1780.5)]),
        ("③ 공시 50억 70세 10년 거주", 50, 70, 10, 10, [(468.9, 1788.3), (1942.1, 3261.5), (3295.7, 4615.1)]),
    ]
    bad = 0
    for name, p, age, held, lived, want in cases:
        prev = None
        for y, (wj, wt) in zip((2026, 2027, 2028), want):
            r = jongbu(p * EOK, y, age, held, lived, "aug", prev)
            prev = r["total"]
            ok = abs(m(r["jong"]) - wj) <= 0.2 and abs(m(r["total"]) - wt) <= 0.2
            bad += not ok
            print(f"{name} {y}: 종부세 {m(r['jong'])}(정부 {wj}) 보유세 {m(r['total'])}(정부 {wt}) {'OK' if ok else 'X'}")
    print("재현 불일치", bad)
    return bad


def table(age=55, held=10, lived=10):
    print(f"\n[9/1 정부안·국회 통과 전] 1세대 1주택 {age}세·보유 {held}년·거주 {lived}년(그 뒤 해마다 +1년), 공시가격 그대로, 단위 만원")
    print("공시가 | 26 종부세 | 27 종부세 | 28 종부세 | 26 보유세 | 28 보유세 | 28-26")
    for p in (12, 13, 14, 15, 16, 18, 20, 22, 25, 30, 40):
        s = series(p * EOK, age, held, lived, "final")
        print(f"{p}억 | {m(s[0]['jong'])} | {m(s[1]['jong'])} | {m(s[2]['jong'])} | "
              f"{m(s[0]['total'])} | {m(s[2]['total'])} | {m(s[2]['total'] - s[0]['total'])}")


def recheck_final():
    """정부 적용사례 3건(8월안)을 9/1 수정 정부안(의안 2221046: 비거주 공제 12억·상한 150%)으로 다시 계산."""
    cases = [("① 30억 70세 10년 거주", 30, 70, 10, 10), ("② 30억 70세 10년 보유·비거주", 30, 70, 10, 0),
             ("③ 50억 70세 10년 거주", 50, 70, 10, 10)]
    print("\n[9/1 수정 정부안(국회 통과 전)으로 다시 계산] 정부 사례 가정 그대로(보유·거주 10년 고정), 단위 만원: 8월안 → 9월 정부안")
    for name, p, age, held, lived in cases:
        pa = pf = None
        for y in (2026, 2027, 2028):
            a = jongbu(p * EOK, y, age, held, lived, "aug", pa); pa = a["total"]
            f = jongbu(p * EOK, y, age, held, lived, "final", pf); pf = f["total"]
            print(f"{name} {y}: 종부세 {m(a['jong'])} → {m(f['jong'])} · 보유세 {m(a['total'])} → {m(f['total'])}")


def cliff(age=55, held=10):
    """비거주 1주택: 납세의무 문턱 14억(안 §7①)인데 공제는 12억(안 §8①) — 문턱 앞뒤 2028년."""
    print(f"\n[비거주 문턱] {age}세·보유 {held}년·거주 0, 2028년 종부세(만원)")
    for p in (13.9, 14.0, 14.01, 14.5, 15):
        s = series(p * EOK, age, held, 0, "final")
        r = series(p * EOK, age, held, 10, "final")
        print(f"공시 {p}억: 비거주 {m(s[2]['jong'])} · 10년 거주 {m(r[2]['jong'])}")


if __name__ == "__main__":
    if verify() and "--force" not in sys.argv:
        sys.exit(1)
    table(55, 10, 10)
    table(55, 10, 0)
    table(70, 15, 15)
    table(45, 3, 3)
    recheck_final()
    cliff()
