export const defaultInputs = {
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

const toRate = (value) => Number(value || 0) / 100;
const yearly = (monthly) => Number(monthly || 0) * 12;

export function simulateRetirement(inputs, retirementAge = Number(inputs.targetRetirementAge)) {
  const data = normalizeInputs(inputs);
  const annualReturn = toRate(data.annualReturnRate);
  const inflation = toRate(data.inflationRate);
  let financialAsset = data.financialAsset;
  let depletionAge = null;
  const rows = [];

  for (let age = data.currentAge; age <= data.simulationUntilAge; age += 1) {
    const year = data.startYear + (age - data.currentAge);
    const isRetired = age >= retirementAge;
    const yearsFromStart = age - data.currentAge;
    const inflatedLivingCost = yearly(data.monthlyLivingCost) * Math.pow(1 + inflation, yearsFromStart);
    const partTimeIncome = isRetired ? yearly(data.partTimeIncomeAfterRetirement) * Math.pow(1 + inflation, yearsFromStart) : 0;
    const pensionIncome = isRetired && age >= data.expectedPensionAge
      ? yearly(data.expectedMonthlyPension) * Math.pow(1 + inflation, yearsFromStart)
      : 0;
    const withdrawal = isRetired ? Math.max(0, inflatedLivingCost - partTimeIncome - pensionIncome) : 0;
    const investmentAdded = isRetired ? 0 : yearly(data.monthlyInvestment);

    financialAsset = financialAsset * (1 + annualReturn) + investmentAdded - withdrawal;

    if (financialAsset <= 0 && depletionAge === null) {
      depletionAge = age;
    }

    rows.push({
      year,
      age,
      status: isRetired ? '퇴사 후' : '근무 중',
      financialAsset,
      realEstateValue: data.realEstateValue,
      debt: data.debt,
      netWorth: financialAsset + data.realEstateValue - data.debt,
      livingCost: isRetired ? inflatedLivingCost : 0,
      partTimeIncome,
      pensionIncome,
      withdrawal,
      investmentAdded
    });
  }

  return {
    rows,
    depletionAge,
    finalFinancialAsset: rows.at(-1)?.financialAsset ?? financialAsset,
    finalNetWorth: rows.at(-1)?.netWorth ?? financialAsset + data.realEstateValue - data.debt,
    retirementAge
  };
}

export function findEarliestRetirementAge(inputs) {
  const data = normalizeInputs(inputs);

  for (let age = data.currentAge; age <= 70; age += 1) {
    const result = simulateRetirement(data, age);
    if (!result.depletionAge || result.depletionAge > data.simulationUntilAge) {
      return age;
    }
  }

  return null;
}

export function compareWorkMoreScenarios(inputs) {
  const data = normalizeInputs(inputs);
  return [0, 1, 2, 3].map((extraYears) => {
    const retirementAge = data.targetRetirementAge + extraYears;
    const result = simulateRetirement(data, retirementAge);
    return {
      extraYears,
      retirementAge,
      depletionAge: result.depletionAge,
      finalFinancialAsset: result.finalFinancialAsset,
      status: getRiskStatus(result, data)
    };
  });
}

export function getRiskStatus(result, inputs) {
  const data = normalizeInputs(inputs);
  if (!result.depletionAge || result.depletionAge > data.simulationUntilAge) {
    return 'stable';
  }
  if (result.depletionAge >= data.expectedPensionAge) {
    return 'caution';
  }
  return 'risk';
}

export function buildSimulation(inputs) {
  const data = normalizeInputs(inputs);
  const targetResult = simulateRetirement(data, data.targetRetirementAge);
  const earliestRetirementAge = findEarliestRetirementAge(data);
  const scenarios = compareWorkMoreScenarios(data);
  const depletionStatus = getRiskStatus(targetResult, data);
  const firstScenario = scenarios[0];
  const secondScenario = scenarios[1];
  const gainedYears = estimateGainedYears(firstScenario, secondScenario, data.simulationUntilAge);
  const extraAssetFromOneMoreYear = (secondScenario?.finalFinancialAsset ?? 0) - (firstScenario?.finalFinancialAsset ?? 0);
  const retirementRow = targetResult.rows.find((row) => row.age === data.targetRetirementAge);
  const firstRetirementExpense = retirementRow?.withdrawal ?? 0;
  const retirementFinancialAsset = retirementRow?.financialAsset ?? data.financialAsset;
  const safeWithdrawalRate = retirementFinancialAsset > 0
    ? (firstRetirementExpense / retirementFinancialAsset) * 100
    : 0;
  const requiredFireAssetByFourPercent = firstRetirementExpense / 0.04;
  const fireGap = requiredFireAssetByFourPercent - retirementFinancialAsset;
  const fourPercentReferenceGap = fireGap;
  const bridgeYears = Math.max(0, data.expectedPensionAge - data.targetRetirementAge);
  const targetYears = Math.max(1, data.simulationUntilAge - data.targetRetirementAge);
  const runwayYears = targetResult.depletionAge
    ? Math.max(0, targetResult.depletionAge - data.targetRetirementAge)
    : Math.max(0, data.simulationUntilAge - data.targetRetirementAge);
  const survivalScore = calculateSurvivalScore({
    depletionAge: targetResult.depletionAge,
    targetRetirementAge: data.targetRetirementAge,
    simulationUntilAge: data.simulationUntilAge
  });
  const marginStatus = getReferenceStatus({
    targetResult,
    safeWithdrawalRate,
    simulationUntilAge: data.simulationUntilAge
  });
  const marginScore = survivalScore;
  const status = depletionStatus;
  const healthScore = survivalScore;

  return {
    inputs: data,
    targetResult,
    earliestRetirementAge,
    scenarios,
    status,
    gainedYears,
    extraAssetFromOneMoreYear,
    fireAssetWithoutRealEstate: data.financialAsset - data.debt,
    netWorth: data.financialAsset + data.realEstateValue - data.debt,
    firstRetirementExpense,
    retirementFinancialAsset,
    safeWithdrawalRate,
    requiredFireAssetByFourPercent,
    fireGap,
    fourPercentReferenceGap,
    monthlySavingsGapUntilRetirement: 0,
    bridgeYears,
    targetYears,
    runwayYears,
    depletionStatus,
    survivalScore,
    marginStatus,
    marginScore,
    healthScore
  };
}

export function normalizeInputs(inputs) {
  const merged = { ...defaultInputs, ...inputs };
  return Object.fromEntries(
    Object.entries(merged).map(([key, value]) => [key, Number(value)])
  );
}

function estimateGainedYears(current, next, simulationUntilAge) {
  const currentEnd = current.depletionAge ?? simulationUntilAge;
  const nextEnd = next.depletionAge ?? simulationUntilAge;
  return Math.max(0, nextEnd - currentEnd);
}

function calculateSurvivalScore({ depletionAge, targetRetirementAge, simulationUntilAge }) {
  if (!depletionAge || depletionAge > simulationUntilAge) return 100;

  const targetYears = Math.max(1, simulationUntilAge - targetRetirementAge);
  const coveredYears = Math.max(0, depletionAge - targetRetirementAge);
  return Math.max(5, Math.min(95, Math.round((coveredYears / targetYears) * 100)));
}

function getReferenceStatus({ targetResult, safeWithdrawalRate, simulationUntilAge }) {
  if (targetResult.depletionAge && targetResult.depletionAge <= simulationUntilAge) {
    return targetResult.depletionAge >= simulationUntilAge - 5 ? 'caution' : 'risk';
  }
  if (safeWithdrawalRate >= 8) return 'caution';
  return 'stable';
}
