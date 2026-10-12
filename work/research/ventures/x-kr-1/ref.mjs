// firemap 운영 식(src/utils/retirementSimulator.js)으로 checks 예시 값을 낸다. 엑셀과 같은 조건: 국내·90세. 10/12부터 국민연금 월액은 예시마다(make_xlsx.py CASES 8번째 값).
import { findEarliestRetirementAge, findRequiredAssetNow } from '../../../../src/utils/retirementSimulator.js';
const cases = { 1: [30, 30000000, 5, 3, 3500000, 2000000, 2150000, 0], 2: [35, 100000000, 5, 3, 5000000, 3000000, 3000000, 0], 3: [40, 200000000, 5, 3, 4500000, 2500000, 2800000, 0],
  4: [30, 30000000, 5, 3, 3500000, 2000000, 2150000, 1000000], 5: [45, 150000000, 5, 3, 6000000, 3500000, 3300000, 1500000], 6: [58, 400000000, 4, 3, 5000000, 3000000, 3200000, 1200000] };
const run = (age, asset, r, i, inc, m, pen, extra = {}) => ({ currentAge: age, targetRetirementAge: age, financialAsset: asset, annualReturnRate: r, inflationRate: i,
  monthlyInvestment: inc - m, monthlyLivingCost: m, expectedMonthlyPension: pen, simulationUntilAge: 90, ...extra });
const out = {};
for (const [k, [age, asset, r, i, inc, m, mp, pen]] of Object.entries(cases)) {
  out[k] = { earliest: findEarliestRetirementAge(run(age, asset, r, i, inc, m, pen)), earliest_plus100k: findEarliestRetirementAge(run(age, asset, r, i, inc, m + 100000, pen)),
    earliest_prev: findEarliestRetirementAge(run(age, asset, r, i, inc, mp, pen)), required: findRequiredAssetNow(run(age, asset, r, i, inc, m, pen)),
    earliest_webdefault_pension: findEarliestRetirementAge(run(age, asset, r, i, inc, m, 1000000)) };
}
console.log(JSON.stringify(out));
