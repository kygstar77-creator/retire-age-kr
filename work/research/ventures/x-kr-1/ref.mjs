// firemap 운영 식(src/utils/retirementSimulator.js)으로 checks 예시 값을 낸다. 엑셀과 같은 조건: 연금 0·국내·90세.
import { findEarliestRetirementAge, findRequiredAssetNow } from '../../../../src/utils/retirementSimulator.js';
const cases = { 1: [30, 30000000, 5, 3, 3500000, 2000000, 2150000], 2: [35, 100000000, 5, 3, 5000000, 3000000, 3000000], 3: [40, 200000000, 5, 3, 4500000, 2500000, 2800000] };
const run = (age, asset, r, i, inc, m, extra = {}) => ({ currentAge: age, targetRetirementAge: age, financialAsset: asset, annualReturnRate: r, inflationRate: i,
  monthlyInvestment: inc - m, monthlyLivingCost: m, expectedMonthlyPension: 0, simulationUntilAge: 90, ...extra });
const out = {};
for (const [k, [age, asset, r, i, inc, m, mp]] of Object.entries(cases)) {
  out[k] = { earliest: findEarliestRetirementAge(run(age, asset, r, i, inc, m)), earliest_plus100k: findEarliestRetirementAge(run(age, asset, r, i, inc, m + 100000)),
    earliest_prev: findEarliestRetirementAge(run(age, asset, r, i, inc, mp)), required: findRequiredAssetNow(run(age, asset, r, i, inc, m)),
    earliest_webdefault_pension: findEarliestRetirementAge(run(age, asset, r, i, inc, m, { expectedMonthlyPension: 1000000 })) };
}
console.log(JSON.stringify(out));
