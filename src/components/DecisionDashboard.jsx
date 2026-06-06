import { ShieldCheck, TrendingUp, Wallet, Waves } from 'lucide-react';
import { formatEok, formatPercent, statusMeta } from '../utils/formatters.js';

export default function DecisionDashboard({ simulation }) {
  const {
    inputs,
    status,
    survivalScore,
    safeWithdrawalRate,
    requiredFireAssetByFourPercent,
    fireGap,
    bridgeYears,
    runwayYears,
    retirementFinancialAsset,
    targetResult
  } = simulation;
  const meta = statusMeta[status];
  const progress = Math.min(100, Math.max(0, survivalScore));
  const survivesTargetAge = !targetResult.depletionAge || targetResult.depletionAge > inputs.simulationUntilAge;
  const title = survivesTargetAge
    ? `${inputs.targetRetirementAge}세 퇴사 후 ${inputs.simulationUntilAge}세까지 고갈되지 않습니다`
    : `${inputs.targetRetirementAge}세 퇴사 시 ${targetResult.depletionAge}세에 고갈될 수 있습니다`;
  const survivalText = survivesTargetAge ? '통과' : `${runwayYears}년`;
  const referenceGapText = fireGap <= 0 ? `${formatEok(Math.abs(fireGap))} 여유` : `${formatEok(fireGap)} 낮음`;

  return (
    <section className={`decision-panel decision-${status}`}>
      <div className="decision-main">
        <span className={`badge badge-${status}`}>{meta.label}</span>
        <h2>{title}</h2>
        <p>
          퇴사 시점 금융자산은 {formatEok(retirementFinancialAsset)}이고 첫해 예상 인출률은 {formatPercent(safeWithdrawalRate)}입니다.
          판정은 입력한 종료 나이까지 금융자산이 마이너스가 되는지로 계산합니다.
        </p>
        <div className="score-meter" aria-label="자산수명 점수">
          <span style={{ width: `${progress}%` }} />
        </div>
      </div>

      <div className="decision-score">
        <small>자산수명 점수</small>
        <strong>{survivalScore}</strong>
        <span>/ 100</span>
      </div>

      <div className="metric-strip">
        <Metric icon={<TrendingUp size={18} />} label={`${inputs.simulationUntilAge}세까지 자산수명`} value={survivalText} tone={status} />
        <Metric icon={<ShieldCheck size={18} />} label="4% 룰 참고자산" value={formatEok(requiredFireAssetByFourPercent)} />
        <Metric icon={<Wallet size={18} />} label="보수 기준 차이" value={referenceGapText} tone="neutral" />
        <Metric icon={<Waves size={18} />} label="국민연금 전 공백기" value={`${bridgeYears}년`} />
      </div>
    </section>
  );
}

function Metric({ icon, label, value, tone = 'neutral' }) {
  return (
    <article className={`strip-card strip-${tone}`}>
      <span>{icon}</span>
      <div>
        <small>{label}</small>
        <strong>{value}</strong>
      </div>
    </article>
  );
}
