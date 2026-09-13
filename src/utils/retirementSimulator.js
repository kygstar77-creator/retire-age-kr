import { earlyClaim, pensionStartAgeForBirthYear, clampClaimAge } from '../firemap-v2/pension.js';

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
  monthlyRentalIncome: 0, // 은퇴 후 월 임대수익(세후) — 물가 따라 매년 인상. 부동산을 안 팔고 월세로 버티는 현실 반영(파이어 나이에 영향).
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
  dividendYield: 4,
  dividendIncomeMonthly: 0, // 배당 '인출 소득'(세후 월) — 부업소득과 분리. 배당세 모드와 상호배타.
  dividendIncomeGrowth: 0,  // 배당 인출 소득의 매년 성장률(%)
  pensionClaimAge: 0        // 국민연금 조기수령 나이(0=정상). 정상연금은 baseline로 보존.
};

const toRate = (value) => Number(value || 0) / 100;
const yearly = (monthly) => Number(monthly || 0) * 12;
const enabled = (value) => Number(value || 0) === 1;
const clamp = (value, min, max) => Math.max(min, Math.min(max, Number(value || 0)));

// 입력값이 '실제 사용자 데이터'인지(기본값과 다른지) 판버.
// 동기화에서 미편집 기본값이 다른 기기 데이터를 덮어쓰는 것을 막는 데 사용.
export function inputsIsReal(v) {
  if (!v || typeof v !== 'object') return false;
  const keys = new Set([...Object.keys(defaultInputs), ...Object.keys(v)]);
  for (const k of keys) {
    if (JSON.stringify(v[k]) !== JSON.stringify(defaultInputs[k])) return true;
  }
  return false;
}

export function simulateRetirement(inputs, retirementAge = Number(inputs.targetRetirementAge), opts = {}) {
  const data = normalizeInputs(inputs);
  const annualReturn = toRate(data.annualReturnRate);
  const inflation = toRate(data.inflationRate);
  const savingYears = data.savingYears > 0 ? data.savingYears : Infinity; // 0 = 파이어할 때까지 저축
  let financialAsset = data.financialAsset;
  let costBasis = data.financialAsset; // 양도세 차익 추정용(취득원가 누적)
  const investType = Math.round(data.investType) || 0; // 0 국내(면제) · 1 해외 양도세２２% · 2 배당１５.４% · 3 둘 다
  const dividendYield = toRate(data.dividendYield);
  const DIV_TAX = 0.154; const CG_EXEMPT = 2500000;
  // 해외주식 양도세 — 250만원 공제 후 22% 단일(양도세 20% + 지방세 2%). 구간 없음.
  // 3억 초과 27.5%는 국내 상장주식 대주주 세율이라 해외주식엔 해당 없다(국세청·증권사 안내).
  const capitalGainTax = (gain) => Math.max(0, gain - CG_EXEMPT) * 0.22;
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
    // 해외에 나가 있으면 건보료도 그만큼 덜 낸다 — 절감액에 같이 넣어야 '첫해 절감'이 실제와 맞는다.
    const healthInsuranceFull = (isRetired && enabled(data.healthInsuranceEnabled))
      ? data.monthlyHealthInsurance * 12 * inflationFactor : 0;
    const insuranceSaved = Math.max(0, healthInsuranceFull - healthInsuranceExpense);
    const livingCost = adjustedLivingCost + healthInsuranceExpense;
    // 부업소득은 물가 미반영(명목 고정): 생활비·월급과 달리 자동 인상 주체가 없으므로 입력한 금액 그대로 본다.
    const partTimeIncome = isRetired ? yearly(data.partTimeIncomeAfterRetirement) : 0;
    const pensionIncome = isRetired && age >= data.expectedPensionAge
      ? yearly(data.expectedMonthlyPension) * inflationFactor
      : 0;
    // 배당 인출소득은 쓰지 않는다 — 연 수익률(총수익률)에 배당이 이미 들어 있어 두 번 세어진다.
    const dividendIncome = 0;
    // 임대수익: 생활비처럼 물가 따라 매년 인상(임대료는 장기적으로 물가에 연동). 부동산을 안 팔고 월세로 버티는 현실 반영.
    const rentalIncome = isRetired ? yearly(data.monthlyRentalIncome) * inflationFactor : 0;
    const withdrawal = isRetired ? Math.max(0, livingCost - partTimeIncome - pensionIncome - dividendIncome - rentalIncome) : 0;
    const salaryGrowth = toRate(data.salaryGrowthRate);
    const stillSaving = !isRetired && yearsFromStart >= 1 && yearsFromStart <= savingYears;
    const investmentAdded = stillSaving ? yearly(data.monthlyInvestment) * Math.pow(1 + salaryGrowth, yearsFromStart) : 0;
    if (investmentAdded > 0) costBasis += investmentAdded;
    // 투자 유형별 세금(파이어 후): 국내=0 · 해외=인출차익 22%(250만 공제) · 배당=배당세 15.4%
    let investTax = 0;
    // 배당세는 파이어 전에도 매년 떼인다(재투자해도 원천징수). 양도세는 팔 때만이라 파이어 후에만.
    if (financialAsset > 0 && (investType === 2 || investType === 3)) {
      investTax += financialAsset * dividendYield * DIV_TAX;
    }
    if (isRetired && financialAsset > 0) {
      if (investType === 1 || investType === 3) { // 해외주식 양도세: 매도 차익분 22%(250만 공제)
        const gainRatio = Math.max(0, (financialAsset - costBasis) / financialAsset);
        const gain = withdrawal * gainRatio;
        investTax += capitalGainTax(gain);
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
      overseasSavings: (overseasAdjustment?.annualSavings ?? 0) + insuranceSaved,
      partTimeIncome,
      pensionIncome,
      rentalIncome,
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

// 필요 자산 — 지금 그만둬도 자산이 마르지 않는 최소 금액(오늘 돈).
// 파이어 나이를 찾는 것과 같은 시뮬레이션을 쓴다. 그래서 지금 자산이 이 금액에 닿는 순간
// 파이어 가능 나이가 현재 나이가 되고 달성률도 100%가 된다. 4% 룰과 답이 갈리지 않는다.
export function findRequiredAssetNow(inputs) {
  const data = normalizeInputs(inputs);
  const cur = data.currentAge;
  const fits = (v) => findEarliestRetirementAge({ ...data, financialAsset: v }) === cur;
  let lo = 0;
  let hi = 5000000000;
  if (!fits(hi)) return null;
  for (let i = 0; i < 26; i += 1) {
    const mid = (lo + hi) / 2;
    if (fits(mid)) hi = mid; else lo = mid;
  }
  return Math.ceil(hi);
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
  // 필요 자산 — 파이어 첫해 순인출액의 25배. 화면은 오늘 자산과 나란히 보므로 오늘 화폐로 돌려준다.
  // (미래 명목값이 필요하면 requiredFireAssetNominal)
  const yearsToTarget = Math.max(0, data.targetRetirementAge - data.currentAge);
  const inflationToTarget = Math.pow(1 + toRate(data.inflationRate), yearsToTarget);
  const requiredFireAssetNominal = firstRetirementExpense / 0.04;
  const requiredFireAssetByFourPercent = requiredFireAssetNominal / inflationToTarget;

  // 화면 히어로는 '가장 이른 파이어 나이'를 띄운다. 그 나이 기준 금액을 같은 잣대(오늘 화폐)로 같이 내준다.
  // 이게 없으면 필요 자산(오늘 돈)과 파이어 때 자산(미래 명목)을 나란히 두게 돼 서로 비교가 안 된다.
  // 화면에 나가는 금액은 전부 오늘 돈으로 바꾼다. 그래프·표·카드가 같은 줄을 읽게 하려는 것.
  const toToday = (rows) => rows.map((row) => {
    const f = Math.pow(1 + toRate(data.inflationRate), Math.max(0, row.age - data.currentAge));
    return { ...row, financialAssetToday: Math.max(0, row.financialAsset) / f, investmentAddedToday: (row.investmentAdded || 0) / f };
  });
  let atEarliest = null;
  if (earliestRetirementAge) {
    const er = simulateRetirement(data, earliestRetirementAge);
    const erRow = er.rows.find((row) => row.age === earliestRetirementAge);
    const f = Math.pow(1 + toRate(data.inflationRate), Math.max(0, earliestRetirementAge - data.currentAge));
    atEarliest = {
      age: earliestRetirementAge,
      assetToday: (erRow?.financialAsset ?? 0) / f,
      requiredToday: ((erRow?.withdrawal ?? 0) / 0.04) / f,
      depletionAge: er.depletionAge,
      rows: toToday(er.rows)
    };
  }
  // 목표 나이 때 자산은 그때 통장에 찍힐 금액(명목)이다. 화면은 오늘 돈으로 보여주므로 같이 내준다.
  const retirementFinancialAssetToday = retirementFinancialAsset / inflationToTarget;
  const requiredAssetNow = findRequiredAssetNow(data);
  // 결과·바꿔보기·인증 카드가 읽는 한 벌. 가능 나이가 없으면(70세까지 안 되면) 목표 나이 흐름을 보여준다.
  // 금액은 그때 통장에 찍힐 금액(명목). 오늘 돈으로 바꾸면 18년 모은 돈이 줄어든 것처럼 보인다.
  const earliestRows = atEarliest ? atEarliest.rows : toToday(targetResult.rows);
  const fireAge = atEarliest ? earliestRetirementAge : data.targetRetirementAge;
  const fireRow = earliestRows.find((row) => row.age === fireAge);
  const displayResult = {
    retirementAge: fireAge,
    depletionAge: atEarliest ? atEarliest.depletionAge : targetResult.depletionAge,
    rows: earliestRows,
    fireAsset: Math.max(0, fireRow?.financialAsset ?? 0),
    fireAssetToday: atEarliest ? atEarliest.assetToday : retirementFinancialAssetToday
  };
  const fireGap = requiredFireAssetNominal - retirementFinancialAsset;
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
    firstYearRentalIncome: retirementRow?.rentalIncome ?? 0,
    pensionStartWithdrawal: pensionStartRow?.withdrawal ?? null,
    retirementFinancialAsset,
    finalFinancialAsset: finalRow?.financialAsset ?? targetResult.finalFinancialAsset,
    safeWithdrawalRate,
    retirementFinancialAssetToday,
    requiredAssetNow,
    requiredFireAssetByFourPercent,
    requiredFireAssetNominal,
    atEarliest,
    displayResult,
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
  const data = Object.fromEntries(
    Object.entries(merged).map(([key, value]) => [key, Number(String(value ?? '').replace(/[^\d.-]/g, '')) || 0])
  );
  // 목표 나이가 현재 나이보다 앞이면 목표 행이 없어 필요 자산이 0원으로 나온다. 현재 나이로 맞춘다.
  if (data.targetRetirementAge < data.currentAge) data.targetRetirementAge = data.currentAge;
  // 노령연금 개시 나이는 출생연도로 법에 정해져 있다. 화면에서 고칠 수 있는 값이 아니므로 여기서 정한다.
  // 이렇게 막지 않으면 공유 링크의 pen 값이 그대로 들어와 40세 개시 같은 값도 통했다.
  const birthYear = data.startYear - data.currentAge;
  data.expectedPensionAge = pensionStartAgeForBirthYear(birthYear);
  data.pensionClaimAge = clampClaimAge(data.pensionClaimAge, data.expectedPensionAge);
  // 국민연금 조기수령: 정상연금(baseline)은 그대로, 조기수령 나이가 이르면 '실효 연금'만 감액(누적 감액 방지)
  if (data.pensionClaimAge > 0 && data.pensionClaimAge !== data.expectedPensionAge) {
    const ec = earlyClaim(data.expectedMonthlyPension, data.expectedPensionAge, data.pensionClaimAge);
    data.expectedMonthlyPension = ec.monthly; // 조기=감액(연 6%), 연기=증액(연 7.2%)
    data.expectedPensionAge = data.pensionClaimAge;
  }
  return data;
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
