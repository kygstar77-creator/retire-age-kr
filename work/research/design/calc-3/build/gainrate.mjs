// calc-3 [지시] ② 숫자 줄('N년 앞당겨져요')이 뜨는 비율 — 배포 전 추정(product-dev 10/2)
// 분모: 저장된 내 입력이 있는 사람(inputsIsReal)만. 입력 격자는 균등 가정(실측 분포 아님 — 저장 입력은 서버에 없다).
import { buildSimulation, defaultInputs } from '../../../../../src/utils/retirementSimulator.js';
import { unemploymentBenefit } from '../../../../../src/utils/unemploymentBenefit.js';
import { severancePay } from '../../../../../src/utils/severancePay.js';

const ub = unemploymentBenefit({ lastWorkDay: '2026-10-02', monthlyWage: 3000000, insuredMonths: 36, over50: false, dailyHours: 8 }).total;
const sev = severancePay({ hireDate: '2023-10-02', retireDate: '2026-10-02', wages3m: 9000000, weeklyHours: 40, annualBonus: 0, annualLeavePay: 0 }).amount;
const grid = [];
for (const currentAge of [28, 33, 38, 43, 48, 53])
  for (const financialAsset of [0, 3e7, 1e8, 2e8, 4e8])
    for (const monthlyInvestment of [3e5, 1e6, 2e6])
      for (const monthlyLivingCost of [2e6, 3e6])
        grid.push({ ...defaultInputs, currentAge, financialAsset, monthlyInvestment, monthlyLivingCost });

function rate(amount) {
  let shown = 0, firable = 0, ex = null;
  for (const inp of grid) {
    const b = buildSimulation(inp).earliestRetirementAge;
    const a = buildSimulation({ ...inp, financialAsset: inp.financialAsset + amount }).earliestRetirementAge;
    if (b && a) { firable++; if (b - a >= 1) { shown++; ex = ex || { inp, gain: b - a }; } }
  }
  return { amount, n: grid.length, firable, shown, pct: +(100 * shown / grid.length).toFixed(1), ex };
}
console.log(JSON.stringify({ unemployment: rate(ub), severance: rate(sev) }, null, 1));
