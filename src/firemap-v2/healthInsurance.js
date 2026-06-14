// 건강보험 피부양자 자격 판정 (현행 제도 근사, 참고용 — 출처: 국민건강보험 제도).
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

// 지역가입자 월 건강보험료 근사 추정 (2025: 건보료율 7.09%, 점수단가 208.4원, 재산 1억 공제, 자동차 폐지, 장기요양 건보료의 12.95%)
// 정확한 금액은 국민건강보험공단 확인 필요 — 참고용 근사치.
export function estimateLocalPremium({ chargeableIncomeManwon = 0, propertyTaxBaseEok = 0 }) {
  const RATE = 0.0709;   // 2025 건강보험료율
  const LTC = 0.1295;    // 장기요양보험료(건보료 대비)
  const MIN = 19780;     // 2025 지역 최저보험료(근사)
  const incomeMonthly = (Math.max(0, Number(chargeableIncomeManwon) || 0) * 10000) * RATE / 12;
  const base = Math.max(0, (Number(propertyTaxBaseEok) || 0) - 1); // 억, 재산 1억 기본공제
  let propMonthly = 0;
  if (base > 0) {
    const pts = base <= 1 ? base * 280
      : base <= 3 ? 280 + (base - 1) * 220
      : base <= 5 ? 720 + (base - 3) * 160
      : 1040 + (base - 5) * 120;
    propMonthly = pts * 208.4;
  }
  const health = Math.max(MIN, incomeMonthly + propMonthly);
  return { incomeMonthly: Math.round(incomeMonthly), propMonthly: Math.round(propMonthly), monthly: Math.round(health * (1 + LTC)) };
}
