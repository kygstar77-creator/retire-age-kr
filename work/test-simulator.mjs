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
check('scenarioA age80 financialAsset', getRow(resultA, 80).financialAsset, -23.07);

const resultB = simulateRetirement(scenarioB);
check('scenarioB age80 financialAsset', getRow(resultB, 80).financialAsset, -45.84);
check('scenarioB age90 financialAsset', getRow(resultB, 90).financialAsset, -67.91);

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

console.log('Simulation regression and invariant tests passed.');
