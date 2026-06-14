export const defaultInputs = {
  currentAge: 35,
  targetRetirementAge: 55,
  startYear: 2026,
  financialAsset: 0,
  realEstateValue: 0,
  debt: 0,
  monthlyInvestment: 0,
  salaryGrowthRate: 0,
  savingYears: 0,
  monthlyLivingCost: 3000000,
  annualReturnRate: 5,
  inflationRate: 3,
  expectedPensionAge: 65,
  expectedMonthlyPension: 1000000,
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
  overseasApplyYears: 10,
  investType: 0,
  dividendYield: 4
};

const toRate = (value) => Number(value || 0) / 100;
const yearly = (monthly) => Number(monthly || 0) * 12;
const enabled = (value) => Number(value || 0) === 1;
const clamp = (value, min, max) => Math.max(min, Math.min(max, Number(value || 0)));

export function simulateRetirement(inputs, retirementAge = Number(inputs.targetRetirementAge), opts = {}) {
  const data = normalizeInputs(inputs);
  const annualReturn = toRate(data.annualReturnRate);
  const inflation = toRate(data.inflationRate);
  const savingYears = data.savingYears > 0 ? data.savingYears : Infinity; // 0 = 파이어할 때까지 저축
  let financialAsset = data.financialAsset;
  let costBasis = data.financialAsset; // 양도세 차익 추정용(취득원가 누적)
  const investType = Math.round(data.investType) || 0; // 0 국내(면제) · 1 해외 양도세22% · 2 배당15.4% · 3 둘 다
  const dividendYield = toRate(data.dividendYield);
  const CG_RATE = 0.22; const DIV_TAX = 0.154; const CG_EXEMPT = 2500000;
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
    // 부업소득은 물가 미반영(명목 고정): 생활비·월급과 달리 자동 인상 주체가 없으므로 입력한 금액 그대로 본다.
    const partTimeIncome = isRetired ? yearly(data.partTimeIncomeAfterRetirement) : 0;
    const pensionIncome = isRetired && age >= data.expectedPensionAge
      ? yearly(data.expectedMonthlyPension) * inflationFactor
      : 0;
    const withdrawal = isRetired ? Math.max(0, livingCost - partTimeIncome - pensionIncome) : 0;
    const salaryGrowth = toRate(data.salaryGrowthRate);
    const stillSaving = !isRetired && yearsFromStart >= 1 && yearsFromStart <= savingYears;
    const investmentAdded = stillSaving ? yearly(data.monthlyInvestment) * Math.pow(1 + salaryGrowth, yearsFromStart) : 0;
    if (investmentAdded > 0) costBasis += investmentAdded;
    // 투자 유형별 세금(파이어 후): 국내=0 · 해외=인출차익 22%(250만 공제) · 배당=배당세 15.4%
    let investTax = 0;
    if (isRetired && financialAsset > 0) {
      if (investType === 1 || investType === 3) { // 해외주식 양도세: 매도 차익분 22%(250만 공제)
        const gainRatio = Math.max(0, (financialAsset - costBasis) / financialAsset);
        const gain = withdrawal * gainRatio;
        investTax += Math.max(0, gain - CG_EXEMPT) * CG_RATE;
      }
      if (investType === 2 || investType === 3) { // 배당세: 연 배당(자산×배당률) 15.4%
        investTax += financialAsset * dividendYield * DIV_TAX;
      }
    }
    const assetAfterCashFlow = financialAsset + investmentAdded - withdrawal - investTax;
    if (isRetired && financialAsset > 0) {
      const sold = withdrawal + investTax;
      costBasis = Math.max(0, costBasis - sold * (costBasis / financialAsset));
    }
    // 첫해(yearsFromStart 0)는 수익률·저축 미적용 — 시작 자산을 그대로 표시(직관성)
    const yearReturn = opts.returnFn ? opts.returnFn(yearsFromStart) : annualReturn;
    const investmentReturn = (yearsFromStart >= 1 && assetAfterCashFlow > 0) ? assetAfterCashFlow * yearReturn : 0;

    financialAsset = assetAfterCashFlow + investmentReturn;

    if (isRetired && financialAsset <= 0 && depletionAge === null) {
      depletionAge = age;
    }

    rows.push({
      year,
      age,
      status: isRetired ? '파이어 후' : '근무 중',
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
      investmentAdded,
      investTax
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


// 수익률 가정이 높을수록 변동성도 큼(자산군 위험-수익 관계). 모든 성공확률 계산이 공유.
export function volForReturn(ratePct) {
  const r = Number(ratePct) || 0;
  return Math.max(0.03, Math.min(0.24, 0.03 + (r - 2) * 0.022));
}

function makeRng(seed) {
  let a = seed >>> 0;
  return () => {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function gaussian(rng) {
  let u = 0, v = 0;
  while (u === 0) u = rng();
  while (v === 0) v = rng();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
}

// 수익률을 평균±변동성으로 추출해 여러 경로를 돌려 목표 나이까지 버틸 확률(%)을 계산.
// 시드 고정 → 같은 조건은 항상 같은 결과(클릭마다 흔들리지 않음).
export function monteCarloSuccess(inputs, { paths = 500, volatility } = {}) {
  const data = normalizeInputs(inputs);
  const mean = toRate(data.annualReturnRate);
  const vol = volatility != null ? volatility : volForReturn(data.annualReturnRate);
  const until = data.simulationUntilAge;
  const seed = (Math.abs(Math.round(
    data.annualReturnRate * 1000 + vol * 100000 + data.financialAsset / 1e5 +
    data.monthlyLivingCost / 1e4 + data.monthlyInvestment / 1e4 + data.targetRetirementAge * 97 +
    data.currentAge * 131 + data.simulationUntilAge * 7 + data.expectedMonthlyPension / 1e4 +
    data.expectedPensionAge * 3 + data.partTimeIncomeAfterRetirement / 1e4
  )) % 2147483629) + 1;
  const rng = makeRng(seed);
  let success = 0;
  for (let p = 0; p < paths; p += 1) {
    const r = simulateRetirement(data, data.targetRetirementAge, { returnFn: () => mean + vol * gaussian(rng) });
    if (!r.depletionAge || r.depletionAge > until) success += 1;
  }
  return Math.round((success / paths) * 100);
}
