import { findEarliestRetirementAge, defaultInputs } from 'file:///C:/Users/강영준/Documents/GitHub/retire-age-kr/src/utils/retirementSimulator.js';
const base = { ...defaultInputs, currentAge: 35, financialAsset: 100000000, monthlyInvestment: 3000000, monthlyLivingCost: 3000000 };
const out = {};
for (const r of [3, 4, 5, 6, 7, 8]) out[r] = findEarliestRetirementAge({ ...base, annualReturnRate: r });
console.log(JSON.stringify({ inputs: { currentAge: 35, financialAsset: 1e8, monthlyInvestment: 3e6, monthlyLivingCost: 3e6, inflationRate: base.inflationRate, expectedPensionAge: base.expectedPensionAge, expectedMonthlyPension: base.expectedMonthlyPension, simulationUntilAge: base.simulationUntilAge }, earliestAgeByReturn: out }));
