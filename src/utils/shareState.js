const encodedPrefix = 's=';
const publicUrl = 'https://retire-age-kr.pages.dev/';

const compactKeyMap = {
  age: 'currentAge',
  fire: 'targetRetirementAge',
  year: 'startYear',
  fa: 'financialAsset',
  re: 'realEstateValue',
  debt: 'debt',
  save: 'monthlyInvestment',
  cost: 'monthlyLivingCost',
  r: 'annualReturnRate',
  inf: 'inflationRate',
  pAge: 'expectedPensionAge',
  pen: 'expectedMonthlyPension',
  side: 'partTimeIncomeAfterRetirement',
  until: 'simulationUntilAge',
  hi: 'healthInsuranceEnabled',
  hiCost: 'monthlyHealthInsurance',
  hiPause: 'overseasInsurancePauseEnabled',
  os: 'overseasStayEnabled',
  osMo: 'overseasMonthsPerYear',
  osDays: 'overseasContinuousDays',
  osCost: 'overseasMonthlyCostLocal',
  fx: 'overseasExchangeRate',
  osExtra: 'overseasAnnualExtraCost',
  osYears: 'overseasApplyYears'
};

export function encodeInputsToHash(inputs) {
  try {
    const json = JSON.stringify(inputs);
    return `${encodedPrefix}${encodeURIComponent(btoa(unescape(encodeURIComponent(json))))}`;
  } catch {
    return '';
  }
}

export function decodeInputsFromHash(input) {
  try {
    const value = String(input || '');
    if (value.startsWith('?')) return decodeInputsFromSearch(value);

    if (!value && typeof window !== 'undefined' && window.location?.search) {
      const queryDecoded = decodeInputsFromSearch(window.location.search);
      if (queryDecoded) return queryDecoded;
    }

    const cleanHash = value.replace(/^#/, '');
    if (!cleanHash.startsWith(encodedPrefix)) return null;
    const encoded = cleanHash.slice(encodedPrefix.length);
    const json = decodeURIComponent(escape(atob(decodeURIComponent(encoded))));
    return JSON.parse(json);
  } catch {
    return null;
  }
}

export function buildShareUrl(inputs) {
  if (!inputs) return publicUrl;
  return buildScenarioShareUrl(inputs);
}

export function buildScenarioShareUrl(inputs) {
  const url = new URL(publicUrl);
  const params = new URLSearchParams();

  Object.entries(compactKeyMap).forEach(([shortKey, inputKey]) => {
    const value = inputs[inputKey];
    if (value === undefined || value === null || value === '') return;
    params.set(shortKey, String(value));
  });

  url.search = params.toString();
  return url.toString();
}

export function buildShareText(simulation) {
  const { inputs, survivalScore, earliestRetirementAge, safeWithdrawalRate, targetResult } = simulation;
  const survivesTargetAge = !targetResult.depletionAge || targetResult.depletionAge > inputs.simulationUntilAge;
  const verdict = survivesTargetAge
    ? `${inputs.targetRetirementAge}세 퇴사 시 ${inputs.simulationUntilAge}세까지 고갈 없음`
    : `${inputs.targetRetirementAge}세 퇴사 시 ${targetResult.depletionAge}세 고갈 예상`;

  return [
    '퇴사나이 계산 결과',
    verdict,
    `자산수명 점수: ${survivalScore}/100`,
    `가장 빠른 퇴사 가능 나이: ${earliestRetirementAge ? `${earliestRetirementAge}세` : '없음'}`,
    `퇴사 첫해 인출률: ${safeWithdrawalRate.toLocaleString('ko-KR', { maximumFractionDigits: 1 })}%`,
    '',
    '내 조건으로 몇 살에 퇴사 가능한지 바로 열어보기'
  ].join('\n');
}

function decodeInputsFromSearch(search) {
  const params = new URLSearchParams(search);
  const decoded = {};

  Object.entries(compactKeyMap).forEach(([shortKey, inputKey]) => {
    if (!params.has(shortKey)) return;
    decoded[inputKey] = params.get(shortKey);
  });

  return Object.keys(decoded).length ? decoded : null;
}
