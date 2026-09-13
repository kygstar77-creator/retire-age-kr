// 국민연금 수령 시기 조정 — 조기수령은 연 6% 감액(최대 5년 30%), 연기수령은 연 7.2% 가산(최대 5년 36%).
// 둘 다 평생 유지된다. 참고용 계산이에요.
export function earlyClaim(normalMonthly, normalAge, claimAge) {
  const nm = Math.max(0, Number(normalMonthly) || 0);
  const na = Number(normalAge) || 0;
  const ca = Number(claimAge) || 0;
  const yearsEarly = Math.min(5, Math.max(0, na - ca));
  const yearsLate = Math.min(5, Math.max(0, ca - na));
  const reductionPct = yearsEarly * 6;
  const bonusPct = yearsLate * 7.2;
  const factor = yearsLate > 0 ? 1 + bonusPct / 100 : Math.max(0.7, 1 - reductionPct / 100);
  return { claimAge: ca, yearsEarly, yearsLate, reductionPct, bonusPct, factor, monthly: Math.round(nm * factor) };
}
