import { AlertTriangle, CheckCircle2, Clock3, WalletCards } from 'lucide-react';
import { formatAge, formatEok, statusMeta } from '../utils/formatters.js';

export default function SummaryCards({ simulation }) {
  const { inputs, targetResult, earliestRetirementAge, status, retirementFinancialAsset, safeWithdrawalRate } = simulation;
  const survivesTargetAge = !targetResult.depletionAge || targetResult.depletionAge > inputs.simulationUntilAge;
  const verdictText = survivesTargetAge ? `${inputs.simulationUntilAge}세까지 고갈 없음` : `${targetResult.depletionAge}세 고갈 예상`;
  const depletionText = targetResult.depletionAge ? `${targetResult.depletionAge}세` : `${inputs.simulationUntilAge}세 이후`;

  const cards = [
    {
      icon: <Clock3 size={20} />,
      label: '목표 파이어 판정',
      value: verdictText,
      detail: `${inputs.targetRetirementAge}세 파이어 기준`,
      tone: status
    },
    {
      icon: <AlertTriangle size={20} />,
      label: '자산 고갈 나이',
      value: depletionText,
      detail: targetResult.depletionAge ? '금융자산이 0원 이하가 되는 시점' : '시뮬레이션 기간 내 고갈 없음',
      tone: status
    },
    {
      icon: <CheckCircle2 size={20} />,
      label: '가장 빠른 파이어 가능 나이',
      value: formatAge(earliestRetirementAge),
      detail: `${inputs.simulationUntilAge}세까지 금융자산 유지 기준`,
      tone: earliestRetirementAge ? 'stable' : 'risk'
    },
    {
      icon: <WalletCards size={20} />,
      label: '파이어 시점 금융자산',
      value: formatEok(retirementFinancialAsset),
      detail: `첫해 예상 인출률 ${safeWithdrawalRate.toLocaleString('ko-KR', { maximumFractionDigits: 1 })}%`,
      tone: 'neutral'
    }
  ];

  return (
    <section className="summary-grid">
      {cards.map((card) => (
        <article className={`summary-card tone-${card.tone}`} key={card.label}>
          <div className="card-top">
            <span className="card-icon">{card.icon}</span>
            <span className={`badge badge-${card.tone}`}>{statusMeta[card.tone]?.label ?? '정보'}</span>
          </div>
          <p>{card.label}</p>
          <strong>{card.value}</strong>
          <small>{card.detail}</small>
        </article>
      ))}
    </section>
  );
}
