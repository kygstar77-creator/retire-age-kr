// E-2 끝 장면(2026-10-01): E-1과 같은 35세·1억 가정 + E-1 끝에서 예고한 '은퇴 가까운 사람'(50세·5억·월 200만원 저축·생활비 300만원)
// 시작 자산이 테슬라 최고가 대비 지금 낙폭(-27.6%)·5년 중 최대 낙폭(-73.6%, facts [11])만큼 줄면 은퇴 나이가 몇 살이 되나
import { findEarliestRetirementAge, defaultInputs } from 'file:///C:/Users/강영준/Documents/GitHub/retire-age-kr/src/utils/retirementSimulator.js';
const people = {
  p35: { ...defaultInputs, currentAge: 35, financialAsset: 1e8, monthlyInvestment: 3e6, monthlyLivingCost: 3e6, annualReturnRate: 5 },
  p50: { ...defaultInputs, currentAge: 50, financialAsset: 5e8, monthlyInvestment: 2e6, monthlyLivingCost: 3e6, annualReturnRate: 5 },
};
const dd = { none: 0, now: 27.6, max5y: 73.6 };
const out = {};
for (const [p, base] of Object.entries(people)) {
  out[p] = { inputs: { currentAge: base.currentAge, financialAsset: base.financialAsset, monthlyInvestment: base.monthlyInvestment, monthlyLivingCost: base.monthlyLivingCost, annualReturnRate: base.annualReturnRate, inflationRate: base.inflationRate, expectedPensionAge: base.expectedPensionAge, expectedMonthlyPension: base.expectedMonthlyPension } };
  for (const [k, d] of Object.entries(dd)) { const a = Math.round(base.financialAsset * (1 - d / 100)); out[p][k] = { drawdown: d, asset: a, age: findEarliestRetirementAge({ ...base, financialAsset: a }) }; }
}
console.log(JSON.stringify(out));
