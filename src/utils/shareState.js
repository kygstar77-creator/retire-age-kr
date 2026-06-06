const encodedPrefix = 's=';

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

export function buildShareUrl(inputs) {
  const url = new URL(window.location.href);
  url.hash = encodeInputsToHash(inputs);
  return url.toString();
}

export function buildShareText(simulation) {
  const { inputs, survivalScore, earliestRetirementAge, safeWithdrawalRate, fireGap, targetResult } = simulation;
  const survivesTargetAge = !targetResult.depletionAge || targetResult.depletionAge > inputs.simulationUntilAge;
  const verdict = survivesTargetAge ? `${inputs.simulationUntilAge}세까지 고갈 없음` : `${targetResult.depletionAge}세 고갈 예상`;
  const gapText = fireGap <= 0
    ? `${(Math.abs(fireGap) / 100000000).toLocaleString('ko-KR', { maximumFractionDigits: 1 })}억 여유`
    : `${(fireGap / 100000000).toLocaleString('ko-KR', { maximumFractionDigits: 1 })}억 낮음`;

  return [
    `퇴사나이 결과`,
    `${inputs.targetRetirementAge}세 퇴사 판정: ${verdict}`,
    `자산수명 점수: ${survivalScore}/100`,
    `가장 빠른 퇴사 가능 나이: ${earliestRetirementAge ? `${earliestRetirementAge}세` : '없음'}`,
    `첫해 인출률: ${safeWithdrawalRate.toLocaleString('ko-KR', { maximumFractionDigits: 1 })}%`,
    `4% 룰 참고 차이: ${gapText}`
  ].join('\n');
}
