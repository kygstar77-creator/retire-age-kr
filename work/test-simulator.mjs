import { simulateRetirement } from '../src/utils/retirementSimulator.js';

const toEok = (value) => value / 100000000;

function fail(message) {
  console.error(message);
  process.exit(1);
}

function check(label, actual, expected, tolerance = 0.05) {
  const actualEok = toEok(actual);
  if (Math.abs(actualEok - expected) > tolerance) {
    fail(`${label}: expected ${expected} eok, got ${actualEok.toFixed(2)} eok`);
  }
}

function assert(condition, message) {
  if (!condition) fail(message);
}

function getRow(result, age) {
  return result.rows.find((row) => row.age === age);
}

function comparableEndAge(result, untilAge) {
  return result.depletionAge ?? untilAge + 1;
}

const scenarioA = {
  currentAge: 34,
  targetRetirementAge: 36,
  startYear: 2026,
  financialAsset: 270000000,
  realEstateValue: 240000000,
  debt: 90000000,
  monthlyInvestment: 1000000,
  monthlyLivingCost: 3000000,
  annualReturnRate: 10,
  inflationRate: 3,
  expectedPensionAge: 65,
  expectedMonthlyPension: 1000000,
  partTimeIncomeAfterRetirement: 0,
  simulationUntilAge: 80
};

const scenarioB = {
  currentAge: 34,
  targetRetirementAge: 39,
  startYear: 2026,
  financialAsset: 230000000,
  realEstateValue: 240000000,
  debt: 90000000,
  monthlyInvestment: 1000000,
  monthlyLivingCost: 5000000,
  annualReturnRate: 8,
  inflationRate: 3,
  expectedPensionAge: 65,
  expectedMonthlyPension: 1000000,
  partTimeIncomeAfterRetirement: 0,
  simulationUntilAge: 90
};

const resultA = simulateRetirement(scenarioA);
check('scenarioA age80 financialAsset', getRow(resultA, 80).financialAsset, -24.44);

const resultB = simulateRetirement(scenarioB);
check('scenarioB age80 financialAsset', getRow(resultB, 80).financialAsset, -46.51);
check('scenarioB age90 financialAsset', getRow(resultB, 90).financialAsset, -68.59);

const base = { ...scenarioB };
const workLonger = simulateRetirement(base, base.targetRetirementAge + 1);
assert(
  comparableEndAge(workLonger, base.simulationUntilAge) >= comparableEndAge(resultB, base.simulationUntilAge),
  'Invariant failed: working longer should not shorten asset runway.'
);

const lowerLivingCost = simulateRetirement({ ...base, monthlyLivingCost: base.monthlyLivingCost - 1000000 });
assert(
  comparableEndAge(lowerLivingCost, base.simulationUntilAge) >= comparableEndAge(resultB, base.simulationUntilAge),
  'Invariant failed: lower living cost should not shorten asset runway.'
);

const higherLivingCost = simulateRetirement({ ...base, monthlyLivingCost: base.monthlyLivingCost + 1000000 });
assert(
  comparableEndAge(higherLivingCost, base.simulationUntilAge) <= comparableEndAge(resultB, base.simulationUntilAge),
  'Invariant failed: higher living cost should not extend asset runway.'
);

const higherReturn = simulateRetirement({ ...base, annualReturnRate: base.annualReturnRate + 2 });
assert(
  higherReturn.finalFinancialAsset >= resultB.finalFinancialAsset,
  'Invariant failed: higher return should not reduce final financial asset.'
);

const morePartTimeIncome = simulateRetirement({ ...base, partTimeIncomeAfterRetirement: 1000000 });
assert(
  comparableEndAge(morePartTimeIncome, base.simulationUntilAge) >= comparableEndAge(resultB, base.simulationUntilAge),
  'Invariant failed: retirement side income should not shorten asset runway.'
);

// --- 추가 불변식 (물가·연금·음수복리) ---

// (1) 생활비 = 기준 × (1+물가)^경과연수  — 인플레 인덱싱 정확성
{
  const r = simulateRetirement(scenarioB); // 물가 3%, 퇴사 39
  const c50 = getRow(r, 50).baseLivingCost;
  const c70 = getRow(r, 70).baseLivingCost;
  const ratio = c70 / c50;
  const expected = Math.pow(1 + scenarioB.inflationRate / 100, 20);
  assert(Math.abs(ratio - expected) < 0.01, `Invariant failed: 생활비 인플레 인덱싱 어긋남 (ratio ${ratio.toFixed(3)} vs ${expected.toFixed(3)})`);
}

// (2) 물가를 올리면 자산수명이 절대 늘어나지 않는다
{
  const base = simulateRetirement(scenarioB);
  const higherInf = simulateRetirement({ ...scenarioB, inflationRate: scenarioB.inflationRate + 2 });
  assert(
    comparableEndAge(higherInf, scenarioB.simulationUntilAge) <= comparableEndAge(base, scenarioB.simulationUntilAge),
    'Invariant failed: 물가가 오르면 자산수명이 늘어나면 안 됨.'
  );
}

// (3) 고갈 이후 자산은 수익률로 음수 복리되지 않는다 (연 감소폭 ≈ 인출액)
{
  const r = simulateRetirement(scenarioB);
  if (r.depletionAge && r.depletionAge < scenarioB.simulationUntilAge) {
    const age = r.depletionAge + 2; // 고갈 이후 확실한 연도
    const cur = getRow(r, age), prev = getRow(r, age - 1);
    if (cur && prev && prev.financialAsset < 0) {
      const delta = cur.financialAsset - prev.financialAsset; // 음수
      assert(Math.abs(delta + cur.withdrawal) < 1, 'Invariant failed: 고갈 후 자산이 수익률로 음수 복리됨(감소폭≠인출액).');
    }
  }
}

// (4) 국민연금 개시 후 인출액이 줄어든다 (연금>0)
{
  const r = simulateRetirement(scenarioB); // 연금 65세 월100만
  const before = getRow(r, scenarioB.expectedPensionAge - 1).withdrawal;
  const after = getRow(r, scenarioB.expectedPensionAge).withdrawal;
  assert(after < before, `Invariant failed: 연금 개시 후 인출이 줄지 않음 (before ${Math.round(before)} after ${Math.round(after)}).`);
}

// (5) 적립 기간: 0(기본)=퇴사까지와 동일, 기간을 줄이면 최종자산이 늘지 않는다
{
  const full = simulateRetirement({ ...scenarioB, savingYears: 0 });
  const untilRetire = simulateRetirement({ ...scenarioB, savingYears: scenarioB.targetRetirementAge - scenarioB.currentAge });
  assert(Math.abs(full.finalFinancialAsset - untilRetire.finalFinancialAsset) < 1, 'Invariant failed: savingYears 0이 퇴사까지 저축과 다름.');
  const shorter = simulateRetirement({ ...scenarioB, savingYears: 3 });
  assert(shorter.finalFinancialAsset <= full.finalFinancialAsset + 1, 'Invariant failed: 적립 기간을 줄였는데 최종자산이 늘어남.');
}

// (6) 첫해(시작 시점) 자산은 시작 자산 그대로 — 수익률·저축 미적용
{
  const r = simulateRetirement(scenarioB);
  assert(Math.abs(r.rows[0].financialAsset - scenarioB.financialAsset) < 1, 'Invariant failed: 첫해 자산이 시작 자산과 다름(첫해 성장/저축이 적용됨).');
  assert(r.rows[0].investmentAdded === 0, 'Invariant failed: 첫해에 저축이 적용됨.');
}

console.log('Simulation regression and invariant tests passed.');
