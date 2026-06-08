import Header from './Header.jsx';
import { returnAssumptions } from '../../firemap-v2/data.js';
import { formatWon } from '../../firemap-v2/formatters.js';
import { buildScenario, deltaText, fireStatus, runwayText } from '../../firemap-v2/scenarios.js';

function ResultHero({ simulation }) {
  const targetAge = `${simulation.inputs.targetRetirementAge}세`;
  const runway = runwayText(simulation);
  return (
    <section className="fm-card fm-result fm-result-v3">
      <p>내 FIRE 현재 위치</p>
      <h2>{targetAge}에 퇴사하면<br /><b>{runway}</b>까지 버틸 수 있어요.</h2>
      <div className="fm-result-chips">
        <span>은퇴 나이 <b>{targetAge}</b></span>
        <span>경제적 자유 시점 <b>{runway}</b></span>
      </div>
      <p className="fm-result-copy">{simulation.earliestRetirementAge ? `현재 가정으로는 ${simulation.earliestRetirementAge}세 퇴사가 더 안전해 보여요.` : '현재 가정에서는 더 늦은 퇴사가 필요해 보여요.'}</p>
      <div className="fm-result-assumptions">
        <span>{returnAssumptions.label}</span>
        <span>국민연금 {simulation.inputs.expectedPensionAge}세부터 월 {formatWon(simulation.inputs.expectedMonthlyPension)} 반영</span>
      </div>
      <div className="fm-score-box"><small>FIRE 진단</small><strong>{fireStatus(simulation.survivalScore)}</strong><small>{simulation.survivalScore}/100</small></div>
    </section>
  );
}

function ImprovementCards({ inputs, simulation }) {
  const baseCost = Number(inputs.monthlyLivingCost || 0);
  const lowerCostValue = Math.max(1000000, baseCost >= 2500000 ? baseCost - 1000000 : Math.round(baseCost * 0.8 / 100000) * 100000);
  const lowerCost = buildScenario(inputs, { monthlyLivingCost: lowerCostValue });
  const earnAfterRetire = buildScenario(inputs, { partTimeIncomeAfterRetirement: inputs.partTimeIncomeAfterRetirement + 1000000 });
  const workMore = buildScenario(inputs, { targetRetirementAge: inputs.targetRetirementAge + 1 });
  const saveMore = buildScenario(inputs, { monthlyInvestment: inputs.monthlyInvestment + 1000000 });
  const cards = [
    ['생활비', `월 생활비를 ${formatWon(lowerCostValue)}으로 낮추면`, lowerCost],
    ['퇴사 후 현금흐름', '퇴사 후 월 100만 원 벌면', earnAfterRetire],
    ['근무연장', '1년 더 근무하면', workMore],
    ['퇴사 전 저축', '퇴사 전 월 100만 원 더 모으면', saveMore]
  ];
  return (
    <section>
      <h2 className="fm-section-title">FIRE를 앞당기는 방법</h2>
      <div className="fm-card-grid">
        {cards.map(([tag, title, scenario]) => (
          <article className="fm-card fm-mini" key={title}>
            <em>{tag}</em><h3>{title}</h3><strong>{runwayText(scenario)}</strong><p>{deltaText(simulation, scenario)}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

export default function Result({ inputs, simulation, onMove, onEditFinalQuestion }) {
  return (
    <main className="fm-screen fm-scroll">
      <Header tag="결과" onBack={onEditFinalQuestion} />
      <ResultHero simulation={simulation} />
      <div className="fm-result-top-actions">
        <button type="button" className="fm-primary" onClick={() => onMove('experiment')}>조건 바꿔보기</button>
        <button type="button" className="fm-secondary" onClick={() => onMove('share')}>공유하기</button>
      </div>
      <div className="fm-menu fm-result-menu">
        <button type="button" onClick={() => onMove('curation')}>도시 시나리오<span>도시별 생활비</span></button>
      </div>
      <div className="fm-ad">광고</div>
      <ImprovementCards inputs={inputs} simulation={simulation} />
    </main>
  );
}
