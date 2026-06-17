// 완주 엔진 — 목표 자산(G)까지 목표 나이에 도달하려면 매달/매일 얼마를 모아야 하는지.
// 적립식 미래가치 역산. 외부 자동연동 없이도 작동(현재 자산 + 가정 수익률).
export function firePlan(simulation, opts = {}) {
  const inp = (simulation && simulation.inputs) || {};
  const A = Math.max(0, Number(inp.financialAsset) || 0);
  const curAge = Number(inp.currentAge) || 0;
  const targetAge = Number(inp.targetRetirementAge) || 0;
  const G = Math.max(0, Math.round((simulation && simulation.requiredFireAssetByFourPercent) || 0));
  const annual = (opts.annualReturn != null ? opts.annualReturn : (Number(inp.annualReturnRate) || 5)) / 100;
  const months = Math.max(1, Math.round((targetAge - curAge) * 12));
  const i = Math.pow(1 + annual, 1 / 12) - 1;
  const fvCurrent = A * Math.pow(1 + i, months);
  const gap = Math.max(0, G - fvCurrent);
  let pmt = 0;
  if (gap > 0) {
    pmt = (i > 0) ? gap * i / (Math.pow(1 + i, months) - 1) : gap / months;
  }
  const daily = pmt / 30.4;
  const progress = G > 0 ? Math.max(0, Math.min(100, Math.round((A / G) * 100))) : 0;
  const remaining = Math.max(0, G - A);
  const alreadyOnTrack = G > 0 && fvCurrent >= G;
  const planMonthly = Math.max(0, Number(inp.monthlyInvestment) || 0);
  const shortfall = Math.max(0, Math.round(pmt) - planMonthly);
  return {
    A, G, curAge, targetAge, months, annual,
    pmt: Math.round(pmt), daily: Math.round(daily),
    progress, remaining, fvCurrent: Math.round(fvCurrent), alreadyOnTrack,
    planMonthly, shortfall, yearsLeft: Math.max(0, targetAge - curAge)
  };
}
