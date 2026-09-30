// E-1 끝 장면: 35세·1억(월 300만원 저축·생활비 300만원·수익률 5%)에서 시작 자산이 1년 안 최대 낙폭만큼 줄면 은퇴 나이가 몇 살이 되나
import { findEarliestRetirementAge, defaultInputs } from 'file:///C:/Users/강영준/Documents/GitHub/retire-age-kr/src/utils/retirementSimulator.js';
const base = { ...defaultInputs, currentAge: 35, financialAsset: 100000000, monthlyInvestment: 3000000, monthlyLivingCost: 3000000, annualReturnRate: 5 };
const dd = { none: 0, mu: 39.1, samsung: 42.9, hynix: 54.7 };
const out = {};
for (const [k, d] of Object.entries(dd)) { const a = Math.round(1e8 * (1 - d / 100)); out[k] = { drawdown: d, asset: a, age: findEarliestRetirementAge({ ...base, financialAsset: a }) }; }
console.log(JSON.stringify({ inputs: { currentAge: 35, financialAsset: 1e8, monthlyInvestment: 3e6, monthlyLivingCost: 3e6, annualReturnRate: 5, inflationRate: base.inflationRate, expectedPensionAge: base.expectedPensionAge, expectedMonthlyPension: base.expectedMonthlyPension }, out }));
