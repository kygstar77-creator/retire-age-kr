import { simulateRetirement } from '../src/utils/retirementSimulator.js';

const toEok = (value) => value / 100000000;

function check(label, actual, expected, tolerance = 0.05) {
  const actualEok = toEok(actual);
  if (Math.abs(actualEok - expected) > tolerance) {
    console.error(`${label}: expected ${expected} eok, got ${actualEok.toFixed(2)} eok`);
    process.exit(1);
  }
}

function getRow(result, age) {
  return result.rows.find((row) => row.age === age);
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

console.log('Simulation regression tests passed.');
