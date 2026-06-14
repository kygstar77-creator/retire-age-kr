import { FileText } from 'lucide-react';
import { formatAge, formatEok, formatPercent, statusMeta } from '../utils/formatters.js';

export default function InsightReport({ simulation }) {
  const {
    inputs,
    targetResult,
    earliestRetirementAge,
    status,
    gainedYears,
    extraAssetFromOneMoreYear,
    safeWithdrawalRate,
    fireGap,
    bridgeYears,
    retirementFinancialAsset
  } = simulation;
  const survivesTargetAge = !targetResult.depletionAge || targetResult.depletionAge > inputs.simulationUntilAge;
  const isPensionGapRisk = targetResult.depletionAge && targetResult.depletionAge < inputs.expectedPensionAge;
  const oneMoreYearMessage = gainedYears > 0
    ? `1년 더 근무하면 자산수명이 약 ${gainedYears}년 늘어납니다.`
    : `1년 더 근무해도 고갈 나이는 같지만, ${inputs.simulationUntilAge}세 잔여 금융자산은 약 ${formatEok(extraAssetFromOneMoreYear)} 늘어납니다.`;
  const fourPercentMessage = fireGap > 0
    ? `4% 룰만 단독으로 보면 파이어 시점 금융자산이 참고 기준보다 약 ${formatEok(fireGap)} 낮습니다. 다만 이 앱의 파이어 판정은 4% 룰이 아니라 입력한 수익률, 물가, 국민연금, 종료 나이를 모두 반영한 자산 고갈 여부입니다.`
    : `4% 룰 기준으로도 파이어 시점 금융자산이 약 ${formatEok(Math.abs(fireGap))} 더 많습니다.`;
  const pensionGapMessage = bridgeYears > 0
    ? isPensionGapRisk
      ? `국민연금을 받기 전 ${bridgeYears}년 동안 생활비를 금융자산으로 버텨야 하는데, 이 기간 전에 자산이 먼저 고갈될 수 있습니다.`
      : `국민연금을 받기 전 ${bridgeYears}년은 월급과 연금이 모두 없는 공백기입니다. 현재 입력값에서는 이 구간을 통과합니다.`
    : '파이어 시점이 국민연금 수령 이후라 연금 전 공백기는 거의 없습니다.';

  const messages = [
    survivesTargetAge
      ? `사용자가 입력한 종료 나이인 ${inputs.simulationUntilAge}세까지 금융자산이 고갈되지 않습니다. 이 기준에서는 ${inputs.targetRetirementAge}세 파이어가 가능합니다.`
      : `${inputs.targetRetirementAge}세에 파이어하면 ${targetResult.depletionAge}세에 금융자산이 고갈될 수 있어 입력한 ${inputs.simulationUntilAge}세까지 버티기 어렵습니다.`,
    `목표 파이어 첫해 예상 인출률은 ${formatPercent(safeWithdrawalRate)}이고, 파이어 시점 금융자산은 약 ${formatEok(retirementFinancialAsset)}입니다.`,
    pensionGapMessage,
    oneMoreYearMessage,
    fourPercentMessage,
    '국민연금과 파이어 후 소득은 현재 돈 가치로 입력한 금액에 물가상승률을 반영해 계산합니다.',
    earliestRetirementAge
      ? `${inputs.simulationUntilAge}세까지 고갈되지 않는 가장 빠른 파이어 가능 나이는 ${formatAge(earliestRetirementAge)}입니다.`
      : '현재 가정에서는 70세까지 근무해도 목표 종료 나이까지 금융자산 유지가 어렵습니다.'
  ];

  return (
    <section className={`panel insight insight-${status}`}>
      <div className="section-heading">
        <div>
          <p className="eyebrow">AI 리포트</p>
          <h2>파이어나이 해석</h2>
        </div>
        <span className={`badge badge-${status}`}>{statusMeta[status].label}</span>
      </div>
      <div className="insight-title">
        <FileText size={22} />
        <strong>{survivesTargetAge ? '입력한 나이까지는 자산수명이 충분합니다' : statusMeta[status].summary}</strong>
      </div>
      <ul>
        {messages.map((message) => (
          <li key={message}>{message}</li>
        ))}
      </ul>
    </section>
  );
}
