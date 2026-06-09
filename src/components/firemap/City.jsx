import Header from './Header.jsx';
import { domesticCities, overseasCities } from '../../firemap-v2/data.js';
import { formatWon } from '../../firemap-v2/formatters.js';
import { buildScenario, deltaText, runwayText } from '../../firemap-v2/scenarios.js';
import { sourceLine } from '../../firemap-v2/dataSources.js';

function Info({ tag, title, text, note }) {
  return <section className="fm-card fm-info"><em>{tag}</em><h2>{title}</h2><p>{text}</p><small>{note}</small></section>;
}

function ScenarioList({ title, inputs, baseSimulation, scenarios }) {
  return (
    <section className="fm-card fm-city-list"><h2>{title}</h2>
      {scenarios.map(([name, cost, copy]) => {
        const saving = Math.max(0, inputs.monthlyLivingCost - cost);
        const citySimulation = buildScenario(inputs, { monthlyLivingCost: cost });
        return <article className="fm-city-row" key={name}><div><strong>{name}</strong><p>{copy}</p><p>이 생활비로 계산하면 <b>{runwayText(citySimulation)}</b>까지 버틸 수 있어요. {deltaText(baseSimulation, citySimulation)}.</p></div><span>예상 월 {formatWon(cost)}<br /><b>{saving ? `현재 대비 ${formatWon(saving)} 절감` : '현재와 비슷함'}</b></span></article>;
      })}
      <small>도시별 금액은 1인 생활비 참고 시나리오이며 실제 주거비, 의료비, 환율, 비자 조건에 따라 달라질 수 있어요. {sourceLine('cityCost')}</small>
    </section>
  );
}

export default function City({ inputs, simulation, onBack }) {
  return (
    <main className="fm-screen fm-scroll">
      <Header onBack={onBack} />
      <section className="fm-card fm-text-card"><p className="fm-kicker">도시 시나리오</p><h2>사는 곳을 바꾸면 FIRE가 얼마나 가까워질까?</h2><p>도시별 예상 생활비를 내 조건에 바로 대입해, 자산 수명이 얼마나 달라지는지 보여줍니다.</p></section>
      <ScenarioList title="국내 저비용 도시" inputs={inputs} baseSimulation={simulation} scenarios={domesticCities} />
      <ScenarioList title="해외 저비용 생활" inputs={inputs} baseSimulation={simulation} scenarios={overseasCities} />
      <Info tag="현실감 진단" title="생활비를 낮추는 건 수익률을 올리는 것만큼 강력해요" text="같은 자산이라도 매달 나가는 돈이 줄면 필요한 은퇴자금이 작아지고, 자산이 버티는 시간이 길어집니다." note="다음 단계에서는 환율, 비자, 건보료, 체류 개월을 함께 반영할 예정이에요." />
    </main>
  );
}
