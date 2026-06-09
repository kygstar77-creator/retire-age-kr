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
