// 국민연금 조기노령연금 감액 (연 6%, 최대 5년 = 30% 감액 → 70% 수령, 평생 미복원). 참고용.
export function earlyClaim(normalMonthly, normalAge, claimAge) {
  const nm = Math.max(0, Number(normalMonthly) || 0);
  const yearsEarly = Math.min(5, Math.max(0, (Number(normalAge) || 0) - (Number(claimAge) || 0)));
  const reductionPct = yearsEarly * 6;
  const factor = Math.max(0.7, 1 - reductionPct / 100);
  return { claimAge: Number(claimAge) || 0, yearsEarly, reductionPct, factor, monthly: Math.round(nm * factor) };
}
