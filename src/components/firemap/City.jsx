import { useState } from 'react';
import Header from './Header.jsx';
import { domesticCities, overseasCities } from '../../firemap-v2/data.js';
import { formatWon } from '../../firemap-v2/formatters.js';
import { buildScenario, deltaText, runwayText } from '../../firemap-v2/scenarios.js';
import { sourceLine } from '../../firemap-v2/dataSources.js';
import { getFx } from '../../firemap-v2/market.js';

function ScenarioList({ title, inputs, baseSimulation, scenarios }) {
  return (
    <section className="fm-card fm-city-list"><h2>{title}</h2>
      {scenarios.map(([name, cost, copy, info]) => {
        const saving = Math.max(0, inputs.monthlyLivingCost - cost);
        const citySimulation = buildScenario(inputs, { monthlyLivingCost: cost });
        return (
          <article className="fm-city-row" key={name}>
            <div>
              <strong>{name}</strong><p>{copy}</p>
              {info && <p className="fm-city-info">{info}</p>}
              <p>이 생활비로 계산하면 <b>{runwayText(citySimulation)}</b>까지 버틸 수 있어요. {deltaText(baseSimulation, citySimulation)}.</p>
            </div>
            <span>예상 월 {formatWon(cost)}<br /><b>{saving ? `현재 대비 ${formatWon(saving)} 절감` : '현재와 비슷함'}</b></span>
          </article>
        );
      })}
      <small>도시별 금액은 1인 생활비 참고 시나리오이며 실제 주거비, 의료비, 환율, 비자 조건에 따라 달라질 수 있어요. {sourceLine('cityCost')}</small>
    </section>
  );
}

function Stepper({ label, unit, value, set, step, min = 0, max = Infinity }) {
  return (
    <label className="fm-dc-field">
      <span>{label}</span>
      <span className="fm-dc-input">
        <button type="button" onClick={() => set(Math.max(min, value - step))} aria-label="감소">−</button>
        <input inputMode="numeric" value={value} onChange={(e) => set(Math.min(max, Math.max(min, Number(e.target.value.replace(/[^0-9]/g, '')) || 0)))} />
        <button type="button" onClick={() => set(Math.min(max, value + step))} aria-label="증가">+</button>
        <em>{unit}</em>
      </span>
    </label>
  );
}

function OverseasStayModule({ inputs, simulation, onChange }) {
  const [months, setMonths] = useState(3);
  const [localCost, setLocalCost] = useState(65000);
  const [fx, setFx] = useState(() => getFx('THB'));
  const [pause, setPause] = useState(true);
  const patch = {
    overseasStayEnabled: 1,
    overseasMonthsPerYear: months,
    overseasContinuousDays: months >= 3 ? 95 : 0,
    overseasMonthlyCostLocal: localCost,
    overseasExchangeRate: fx,
    overseasInsurancePauseEnabled: pause ? 1 : 0,
    overseasApplyYears: 10
  };
  const scenario = buildScenario(inputs, patch);
  const apply = () => Object.entries(patch).forEach(([k, v]) => onChange(k, v));

  return (
    <section className="fm-card fm-text-card fm-advanced-section">
      <p className="fm-kicker">해외 체류 (직접 조절)</p>
      <h2>체류 조건을 바꿔 자산수명 보기</h2>
      <p>연 체류 개월·현지 생활비·환율을 조절해 자산수명이 어떻게 달라지는지 직접 비교해요. 90일 이상 연속 체류 시 건보료 정지 가정을 켤 수 있어요.</p>
      <div className="fm-dc-fields">
        <Stepper label="연 체류 개월" unit="개월" value={months} set={setMonths} step={1} min={0} max={12} />
        <Stepper label="현지 월 생활비" unit="현지통화" value={localCost} set={setLocalCost} step={5000} />
        <Stepper label="환율(현지통화당 원)" unit="원" value={fx} set={setFx} step={1} />
        <div className="fm-dc-toggles">
          <button type="button" className={pause ? 'on' : ''} onClick={() => setPause(!pause)}>건보료 정지 가정</button>
        </div>
      </div>
      <div className="fm-dc-result ok">
        <ul>
          <li>이 조건이면 <b>{runwayText(scenario)}</b>까지 — {deltaText(simulation, scenario)}</li>
          <li>첫해 생활비 절감 약 {formatWon(scenario.firstYearOverseasSavings)}</li>
        </ul>
      </div>
      <button type="button" className="fm-dc-apply" onClick={apply}>이 해외체류 조건 반영하기</button>
      <small>참고용 시나리오예요. 실제 비자·건보료 면제 요건은 제도 확인이 필요해요.</small>
    </section>
  );
}

export default function City({ inputs, simulation, onBack, onChange }) {
  return (
    <main className="fm-screen fm-scroll">
      <Header onBack={onBack} />
      <section className="fm-card fm-text-card"><p className="fm-kicker">도시 비교 · 해외 체류</p><h2>도시·체류 조건을 바꾸면 자산이 얼마나 더 버틸까?</h2><p>국내 저비용 도시부터 해외 체류(연 체류 개월·환율·건보료 정지)까지, 내 조건에 바로 대입해 자산수명 변화를 비교해요. 세계 지도로 고르려면 「해외 파이어 도시」를 쓰세요.</p></section>
      <ScenarioList title="국내 저비용 도시" inputs={inputs} baseSimulation={simulation} scenarios={domesticCities} />
      <ScenarioList title="해외 저비용 생활" inputs={inputs} baseSimulation={simulation} scenarios={overseasCities} />
      {onChange && <OverseasStayModule inputs={inputs} simulation={simulation} onChange={onChange} />}
    </main>
  );
}
