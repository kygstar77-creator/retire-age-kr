const encodedPrefix = 's=';
const publicUrl = 'https://retire-age-kr.pages.dev/';

export function encodeInputsToHash(inputs) {
  try {
    const json = JSON.stringify(inputs);
    return `${encodedPrefix}${encodeURIComponent(btoa(unescape(encodeURIComponent(json))))}`;
  } catch {
    return '';
  }
}

export function decodeInputsFromHash(hash) {
  try {
    const cleanHash = hash.replace(/^#/, '');
    if (!cleanHash.startsWith(encodedPrefix)) return null;
    const encoded = cleanHash.slice(encodedPrefix.length);
    const json = decodeURIComponent(escape(atob(decodeURIComponent(encoded))));
    return JSON.parse(json);
  } catch {
    return null;
  }
}

export function buildShareUrl() {
  return publicUrl;
}

export function buildScenarioShareUrl(inputs) {
  const url = new URL(publicUrl);
  url.hash = encodeInputsToHash(inputs);
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
    '내 자산으로 몇 살에 퇴사할 수 있을지 계산해보기'
  ].join('\n');
}
