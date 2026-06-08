export const defaultInputs = {
  currentAge: 35,
  targetRetirementAge: 55,
  startYear: 2026,
  financialAsset: 0,
  realEstateValue: 0,
  debt: 0,
  monthlyInvestment: 0,
  monthlyLivingCost: 3000000,
  annualReturnRate: 5,
  inflationRate: 3,
  expectedPensionAge: 65,
  expectedMonthlyPension: 0,
  partTimeIncomeAfterRetirement: 0,
  simulationUntilAge: 90,
  healthInsuranceEnabled: 0,
  monthlyHealthInsurance: 0,
  overseasInsurancePauseEnabled: 0,
  overseasStayEnabled: 0,
  overseasMonthsPerYear: 0,
  overseasContinuousDays: 0,
  overseasMonthlyCostLocal: 0,
  overseasExchangeRate: 40,
  overseasAnnualExtraCost: 0,
  overseasApplyYears: 10
};

const toRate = (value) => Number(value || 0) / 100;
const yearly = (monthly) => Number(monthly || 0) * 12;
const enabled = (value) => Number(value || 0) === 1;
const clamp = (value, min, max) => Math.max(min, Math.min(max, Number(value || 0)));

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
    const yearsFromRetirement = Math.max(0, age - retirementAge);
    const inflationFactor = Math.pow(1 + inflation, yearsFromStart);
    const baseLivingCost = isRetired ? yearly(data.monthlyLivingCost) * inflationFactor : 0;
    const overseasAdjustment = isRetired ? calculateOverseasAdjustment(data, inflationFactor, yearsFromRetirement) : null;
    const adjustedLivingCost = overseasAdjustment ? overseasAdjustment.adjustedLivingCost : baseLivingCost;
    const healthInsuranceExpense = isRetired ? calculateHealthInsuranceExpense(data, inflationFactor) : 0;
    const livingCost = adjustedLivingCost + healthInsuranceExpense;
    const partTimeIncome = isRetired ? yearly(data.partTimeIncomeAfterRetirement) * inflationFactor : 0;
    const pensionIncome = isRetired && age >= data.expectedPensionAge
      ? yearly(data.expectedMonthlyPension) * inflationFactor
      : 0;
    const withdrawal = isRetired ? Math.max(0, livingCost - partTimeIncome - pensionIncome) : 0;
    const investmentAdded = isRetired ? 0 : yearly(data.monthlyInvestment);
    const assetAfterCashFlow = financialAsset + investmentAdded - withdrawal;
    const investmentReturn = assetAfterCashFlow > 0 ? assetAfterCashFlow * annualReturn : 0;

    financialAsset = assetAfterCashFlow + investmentReturn;

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
      livingCost,
      baseLivingCost,
      healthInsuranceExpense,
      overseasLivingCost: overseasAdjustment?.overseasLivingCost ?? 0,
      overseasSavings: overseasAdjustment?.annualSavings ?? 0,
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
  const baselineForAdjustments = buildBaselineForAdjustments(data);
  const earliestRetirementAge = findEarliestRetirementAge(data);
  const scenarios = compareWorkMoreScenarios(data);
  const status = getRiskStatus(targetResult, data);
  const gainedYears = estimateGainedYears(scenarios[0], scenarios[1], data.simulationUntilAge);
  const extraAssetFromOneMoreYear = (scenarios[1]?.finalFinancialAsset ?? 0) - (scenarios[0]?.finalFinancialAsset ?? 0);
  const retirementRow = targetResult.rows.find((row) => row.age === data.targetRetirementAge);
  const pensionStartRow = targetResult.rows.find((row) => row.age === data.expectedPensionAge);
  const finalRow = targetResult.rows.at(-1);
  const firstRetirementExpense = retirementRow?.withdrawal ?? 0;
  const retirementFinancialAsset = retirementRow?.financialAsset ?? data.financialAsset;
  const safeWithdrawalRate = retirementFinancialAsset > 0
    ? (firstRetirementExpense / retirementFinancialAsset) * 100
    : 0;
  const requiredFireAssetByFourPercent = firstRetirementExpense / 0.04;
  const fireGap = requiredFireAssetByFourPercent - retirementFinancialAsset;
  const bridgeYears = Math.max(0, data.expectedPensionAge - data.targetRetirementAge);
  const runwayYears = targetResult.depletionAge
    ? Math.max(0, targetResult.depletionAge - data.targetRetirementAge)
    : Math.max(0, data.simulationUntilAge - data.targetRetirementAge);
  const survivalScore = calculateSurvivalScore({
    depletionAge: targetResult.depletionAge,
    targetRetirementAge: data.targetRetirementAge,
    simulationUntilAge: data.simulationUntilAge
  });

  return {
    inputs: data,
    targetResult,
    baselineForAdjustments,
    earliestRetirementAge,
    scenarios,
    status,
    gainedYears,
    extraAssetFromOneMoreYear,
    fireAssetWithoutRealEstate: data.financialAsset - data.debt,
    netWorth: data.financialAsset + data.realEstateValue - data.debt,
    firstRetirementExpense,
    firstYearLivingCost: retirementRow?.livingCost ?? 0,
    firstYearBaseLivingCost: retirementRow?.baseLivingCost ?? 0,
    firstYearHealthInsurance: retirementRow?.healthInsuranceExpense ?? 0,
    firstYearOverseasSavings: retirementRow?.overseasSavings ?? 0,
    firstYearPartTimeIncome: retirementRow?.partTimeIncome ?? 0,
    firstYearPensionIncome: retirementRow?.pensionIncome ?? 0,
    pensionStartWithdrawal: pensionStartRow?.withdrawal ?? null,
    retirementFinancialAsset,
    finalFinancialAsset: finalRow?.financialAsset ?? targetResult.finalFinancialAsset,
    safeWithdrawalRate,
    requiredFireAssetByFourPercent,
    fireGap,
    fourPercentReferenceGap: fireGap,
    bridgeYears,
    runwayYears,
    depletionStatus: status,
    survivalScore,
    marginStatus: getReferenceStatus({ targetResult, safeWithdrawalRate, simulationUntilAge: data.simulationUntilAge }),
    marginScore: survivalScore,
    healthScore: survivalScore
  };
}

export function normalizeInputs(inputs) {
  const merged = { ...defaultInputs, ...inputs };
  return Object.fromEntries(
    Object.entries(merged).map(([key, value]) => [key, Number(String(value ?? '').replace(/[^\d.-]/g, '')) || 0])
  );
}

function calculateHealthInsuranceExpense(data, inflationFactor) {
  if (!enabled(data.healthInsuranceEnabled)) return 0;
  const overseasMonths = getInsurancePausedMonths(data);
  const chargedMonths = 12 - overseasMonths;
  return data.monthlyHealthInsurance * chargedMonths * inflationFactor;
}

function getInsurancePausedMonths(data) {
  if (!enabled(data.overseasInsurancePauseEnabled)) return 0;
  if (!enabled(data.overseasStayEnabled)) return 0;
  if (data.overseasContinuousDays < 90) return 0;
  return clamp(data.overseasMonthsPerYear, 0, 12);
}

function calculateOverseasAdjustment(data, inflationFactor, yearsFromRetirement) {
  if (!enabled(data.overseasStayEnabled)) return null;
  if (yearsFromRetirement >= Math.max(0, data.overseasApplyYears)) return null;

  const overseasMonths = clamp(data.overseasMonthsPerYear, 0, 12);
  if (overseasMonths <= 0) return null;

  const domesticMonths = 12 - overseasMonths;
  const domesticMonthlyCost = data.monthlyLivingCost * inflationFactor;
  const overseasMonthlyCost = data.overseasMonthlyCostLocal * data.overseasExchangeRate * inflationFactor;
  const annualExtraCost = data.overseasAnnualExtraCost * inflationFactor;
  const adjustedLivingCost = (domesticMonthlyCost * domesticMonths) + (overseasMonthlyCost * overseasMonths) + annualExtraCost;
  const baseLivingCost = yearly(data.monthlyLivingCost) * inflationFactor;

  return {
    adjustedLivingCost,
    overseasLivingCost: overseasMonthlyCost * overseasMonths,
    annualSavings: baseLivingCost - adjustedLivingCost
  };
}

function buildBaselineForAdjustments(data) {
  const baselineInputs = {
    ...data,
    healthInsuranceEnabled: 0,
    overseasInsurancePauseEnabled: 0,
    overseasStayEnabled: 0
  };
  return simulateRetirement(baselineInputs, data.targetRetirementAge);
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
