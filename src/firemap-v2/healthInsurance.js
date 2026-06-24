// 건강보험 피부양자 자격 판정 (현행 제도 근사, 참고용 — 출처: 국민건강보험공단).
// 단위: 소득 만원, 재산세 과세표준 억원.
export function assessDependentEligibility({ otherIncomeManwon = 0, financialIncomeManwon = 0, propertyTaxBaseEok = 0, hasBusinessIncome = false, hasRentalIncome = false }) {
  const finIncome = Math.max(0, Number(financialIncomeManwon) || 0);
  const other = Math.max(0, Number(otherIncomeManwon) || 0);
  const prop = Math.max(0, Number(propertyTaxBaseEok) || 0);
  // 금융소득 1,000만원 이하면 합산서 전액 제외, 초과 시 전액 합산
  const combinedIncome = other + (finIncome > 1000 ? finIncome : 0);

  const reasons = [];
  let eligible = true;
  if (hasBusinessIncome) { eligible = false; reasons.push('사업자등록 + 소득 발생 → 즉시 자격 박탈'); }
  if (hasRentalIncome) { eligible = false; reasons.push('주택임대소득 발생 → 즉시 자격 박탈'); }
  if (prop > 9) { eligible = false; reasons.push('재산세 과표 9억 초과 → 소득과 무관하게 박탈'); }
  else if (prop > 5.4) {
    if (combinedIncome > 1000) { eligible = false; reasons.push('재산과표 5.4억~9억 구간은 합산소득 1,000만원 이하만 유지'); }
  } else if (combinedIncome > 2000) {
    eligible = false; reasons.push('합산소득 2,000만원 초과 → 박탈');
  }
  if (finIncome > 1000) reasons.push(`금융소득 ${finIncome.toLocaleString()}만원(1,000만원 초과) → 전액 합산소득에 포함`);
  if (eligible) reasons.unshift('현재 조건에서는 피부양자 자격 유지 가능');
  return { eligible, combinedIncome, reasons };
}

// 2026 기준 요율 (출처: 보건복지부·국민건강보험공단)
const RATE_2026 = 0.0719;           // 2026 건강보험료율 7.19%
const LTC_2026 = 0.9448 / 7.19;     // 2026 장기요양보험료(건보료 대비) ≈ 13.14%
const POINT_2026 = 211.5;           // 2026 재산보험료 부과점수당 금액(원)
const EMP_SHARE = 0.5;              // 직장가입자 보수월액보험료 근로자 부담 50%
const LOCAL_MIN = 19780;            // 지역 최저보험료(근사)

// 지역가입자 월 건강보험료 근사 추정 (2026: 7.19%, 점수단가 211.5원, 재산 1억 공제, 장기요양 포함)
// 정확한 금액은 국민건강보험공단 확인 필요 — 참고용 근사치.
export function estimateLocalPremium({ chargeableIncomeManwon = 0, propertyTaxBaseEok = 0 }) {
  const incomeMonthly = (Math.max(0, Number(chargeableIncomeManwon) || 0) * 10000) * RATE_2026 / 12;
  const base = Math.max(0, (Number(propertyTaxBaseEok) || 0) - 1); // 억, 재산 1억 기본공제
  let propMonthly = 0;
  if (base > 0) {
    const pts = base <= 1 ? base * 280
      : base <= 3 ? 280 + (base - 1) * 220
      : base <= 5 ? 720 + (base - 3) * 160
      : 1040 + (base - 5) * 120;
    propMonthly = pts * POINT_2026;
  }
  const health = Math.max(LOCAL_MIN, incomeMonthly + propMonthly);
  return { incomeMonthly: Math.round(incomeMonthly), propMonthly: Math.round(propMonthly), monthly: Math.round(health * (1 + LTC_2026)) };
}

// 바리스타 파이어(파트타임 4대보험 → 직장가입자) 월 건강보험료 근사 추정 (2026 기준).
// - 보수월액보험료: 보수월액 × 7.19% × 50%(근로자부담) + 장기요양
// - 소득월액보험료(보수외): 금융소득 1,000만원 이하면 합산 제외, 초과 시 전액 합산 →
//   합산 보수외소득(금융소득+임대·연금·사업 등)이 연 2,000만원 초과 시 그 초과분에만
//   ((합산−2,000만)÷12) × 7.19%(본인 100%) + 장기요양 추가.
// - 분리과세 등 일부 예외는 단순화. 정확한 금액은 국민건강보험공단 확인 — 참고용 근사치.
export function estimateBaristaPremium({ wageMonthlyManwon = 0, otherIncomeManwon = 0, financialIncomeManwon = 0 }) {
  const wage = Math.max(0, Number(wageMonthlyManwon) || 0) * 10000; // 원/월 보수월액
  const fin = Math.max(0, Number(financialIncomeManwon) || 0);      // 만원/년 금융소득
  const other = Math.max(0, Number(otherIncomeManwon) || 0);        // 만원/년 금융 외 보수외소득
  const finCounted = fin > 1000;                                    // 1,000만원 게이트
  const combinedOther = other + (finCounted ? fin : 0);            // 만원/년 합산 보수외소득
  const overThreshold = combinedOther > 2000;                       // 2,000만원 임계
  const overManwon = Math.max(0, combinedOther - 2000);            // 초과분(만원/년)

  const wagePremiumBase = wage * RATE_2026 * EMP_SHARE;            // 보수월액보험료(본인 50%)
  const incomePremiumBase = ((overManwon * 10000) / 12) * RATE_2026; // 소득월액보험료(본인 100%)
  const wagePremium = Math.round(wagePremiumBase * (1 + LTC_2026));
  const incomePremium = Math.round(incomePremiumBase * (1 + LTC_2026));
  return {
    combinedOther,
    overThreshold,
    finCounted,
    wagePremium,
    incomePremium,
    monthly: Math.round((wagePremiumBase + incomePremiumBase) * (1 + LTC_2026)),
  };
}
