import Header from './Header.jsx';
import { returnAssumptions } from '../../firemap-v2/data.js';
import { formatWon } from '../../firemap-v2/formatters.js';
import { buildScenario, fireStatus, runwayText, scenarioEndAge } from '../../firemap-v2/scenarios.js';
import { screens, NEXT_ACTION_META } from '../../firemap-v2/screens.js';

function ResultHero({ simulation }) {
  const targetAge = `${simulation.inputs.targetRetirementAge}세`;
  const runway = runwayText(simulation);
  const safeCopy = simulation.earliestRetirementAge
    ? `현재 가정으로는 ${simulation.earliestRetirementAge}세 퇴사가 더 안전해 보여요.`
    : '현재 가정에서는 더 늦은 퇴사가 필요해 보여요.';

  return (
    <section className="fm-card fm-result fm-result-v3">
      <p>내 FIRE 현재 위치</p>
      <h2>{targetAge}에 퇴사하면<br /><b>{runway}</b>까지 버틸 수 있어요.</h2>
      <div className="fm-result-chips">
        <span>은퇴 나이 <b>{targetAge}</b></span>
        <span>경제적 자유 시점 <b>{runway}</b></span>
      </div>
      <p className="fm-result-copy">{safeCopy}</p>
      <div className="fm-result-assumptions">
        <span>{returnAssumptions.label}</span>
        <span>국민연금 {simulation.inputs.expectedPensionAge}세부터 월 {formatWon(simulation.inputs.expectedMonthlyPension)} 반영</span>
      </div>
      <div className="fm-score-box">
        <div>
          <small>FIRE 진단</small>
          <b className="fm-score-status">{fireStatus(simulation.survivalScore)}</b>
        </div>
        <div>
          <small>점수</small>
          <b className="fm-score-number"><em>{simulation.survivalScore}</em>/100</b>
        </div>
        <div className="fm-score-meter" aria-label={`FIRE 점수 ${simulation.survivalScore}점`}>
          <i style={{ width: `${Math.max(8, simulation.survivalScore)}%` }} />
        </div>
        <p>높을수록 퇴사 후 자산 여유가 커요.</p>
      </div>
    </section>
  );
}

function compareText(base, next) {
  const diff = scenarioEndAge(next) - scenarioEndAge(base);
  if (diff > 0) return `현재보다 ${diff}년 개선`;
  if (diff === 0) return '현재와 비슷함';
  return `${Math.abs(diff)}년 악화`;
}

function TopLevers({ inputs, simulation }) {
  const baseCost = Number(inputs.monthlyLivingCost || 0);
  const lowerCostValue = Math.max(1000000, baseCost >= 2500000 ? baseCost - 1000000 : Math.round(baseCost * 0.8 / 100000) * 100000);
  const candidates = [
    ['생활비', `생활비 ${formatWon(lowerCostValue)}`, buildScenario(inputs, { monthlyLivingCost: lowerCostValue })],
    ['현금흐름', '퇴사 후 월 100만', buildScenario(inputs, { partTimeIncomeAfterRetirement: inputs.partTimeIncomeAfterRetirement + 1000000 })],
    ['퇴사시점', '1년 더 근무', buildScenario(inputs, { targetRetirementAge: inputs.targetRetirementAge + 1 })],
    ['저축액', '월 100만 더 저축', buildScenario(inputs, { monthlyInvestment: inputs.monthlyInvestment + 1000000 })]
  ];
  const baseAge = scenarioEndAge(simulation);
  const topTwo = candidates
    .map((item) => [...item, scenarioEndAge(item[2]) - baseAge])
    .sort((a, b) => b[3] - a[3])
    .slice(0, 2);

  return (
    <section>
      <h2 className="fm-section-title">지금 가장 효과 큰 두 가지</h2>
      <div className="fm-improve-grid fm-improve-grid-two">
        {topTwo.map(([tag, title, scenario]) => (
          <article className="fm-improve-card" key={title}>
            <em>{tag}</em>
            <strong>{runwayText(scenario)}</strong>
            <h3>{title}</h3>
            <p>{compareText(simulation, scenario)}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

function NextActions({ onMove }) {
  const actions = screens.result.next || [];
  return (
    <section className="fm-next-actions" aria-label="다음 행동">
      <h2 className="fm-section-title">다음으로 해볼 것</h2>
      <div className="fm-next-grid">
        {actions.map((id) => {
          const meta = NEXT_ACTION_META[id];
          if (!meta) return null;
          return (
            <button type="button" key={id} className={`fm-next-card${meta.primary ? ' fm-next-primary' : ''}`} onClick={() => onMove(id)}>
              <em>{meta.tag}</em><strong>{meta.title}</strong><span>{meta.desc}</span>
            </button>
          );
        })}
      </div>
    </section>
  );
}

export default function Result({ inputs, simulation, onMove, onEditFinalQuestion }) {
  return (
    <main className="fm-screen fm-scroll">
      <Header />
      <ResultHero simulation={simulation} />
      <TopLevers inputs={inputs} simulation={simulation} />
      <NextActions onMove={onMove} />
      <div className="fm-ad">광고</div>
    </main>
  );
}
