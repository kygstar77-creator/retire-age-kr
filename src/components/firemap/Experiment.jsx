import { useMemo, useState } from 'react';
import Header from './Header.jsx';
import { investmentScenarios } from '../../firemap-v2/data.js';
import { cleanNumber, formatEok, formatWon } from '../../firemap-v2/formatters.js';
import { buildChartRows, buildScenario, runwayText, scenarioEndAge } from '../../firemap-v2/scenarios.js';

function Adjust({ label, value, minus, plus }) {
  return <div className="fm-adjust"><span>{label}</span><strong>{value}</strong><button type="button" onClick={minus}>-</button><button type="button" onClick={plus}>+</button></div>;
}

function nearestByX(chart, x) {
  return chart.reduce((nearest, row) => Math.abs(row.x - x) < Math.abs(nearest.x - x) ? row : nearest, chart[0]);
}

function AdvancedScenarioCard({ title, description, simulation, baseSimulation, onApply, applyLabel, metrics }) {
  const years = scenarioEndAge(simulation) - scenarioEndAge(baseSimulation);
  const delta = years > 0 ? `${years}년 개선` : years < 0 ? `${Math.abs(years)}년 단축` : '변화 작음';
  return (
    <article className="fm-advanced-card">
      <div>
        <strong>{title}</strong>
        <p>{description}</p>
      </div>
      <div className="fm-advanced-metrics">
        <span>자산수명 <b>{runwayText(simulation)}</b></span>
        <span>현재 대비 <b>{delta}</b></span>
        {metrics.map(([label, value]) => <span key={label}>{label} <b>{value}</b></span>)}
      </div>
      <button type="button" onClick={onApply}>{applyLabel}</button>
    </article>
  );
}

export default function Experiment({ inputs, onChange, simulation, onBack }) {
  const [selectedAge, setSelectedAge] = useState(null);
  const reducedMonthlyLivingCost = Math.max(1200000, inputs.monthlyLivingCost - 1500000);
  const lowerCost = useMemo(() => buildScenario(inputs, { monthlyLivingCost: reducedMonthlyLivingCost }), [inputs, reducedMonthlyLivingCost]);
  const sp500Baseline = useMemo(() => buildScenario(inputs, { annualReturnRate: 8 }), [inputs]);
  const healthInsuranceScenario = useMemo(() => buildScenario(inputs, { healthInsuranceEnabled: 1, monthlyHealthInsurance: 230000 }), [inputs]);
  const chiangMaiScenario = useMemo(() => buildScenario(inputs, { overseasStayEnabled: 1, overseasMonthsPerYear: 3, overseasContinuousDays: 95, overseasMonthlyCostLocal: 65000, overseasExchangeRate: 40, overseasAnnualExtraCost: 1500000, overseasApplyYears: 10 }), [inputs]);
  const chiangMaiInsuranceScenario = useMemo(() => buildScenario(inputs, { overseasStayEnabled: 1, overseasInsurancePauseEnabled: 1, healthInsuranceEnabled: 1, monthlyHealthInsurance: 230000, overseasMonthsPerYear: 3, overseasContinuousDays: 95, overseasMonthlyCostLocal: 65000, overseasExchangeRate: 40, overseasAnnualExtraCost: 1500000, overseasApplyYears: 10 }), [inputs]);
  const dividendTaxScenario = useMemo(() => buildScenario(inputs, { partTimeIncomeAfterRetirement: inputs.partTimeIncomeAfterRetirement + 1000000 }), [inputs]);
  const endAgeGap = scenarioEndAge(simulation) - scenarioEndAge(sp500Baseline);
  const gapText = endAgeGap > 0 ? `S&P500형보다 ${endAgeGap}년 길게` : endAgeGap < 0 ? `S&P500형보다 ${Math.abs(endAgeGap)}년 짧게` : 'S&P500형과 비슷하게';
  const { chart, max } = buildChartRows(simulation, lowerCost, inputs);
  const points = (key) => chart.map((row) => `${row.x},${Math.max(32, key === 'improved' ? row.improvedY : row.currentY)}`).join(' ');
  const adjust = (key, amount) => onChange(key, Math.max(0, cleanNumber(inputs[key]) + amount));
  const applyPatch = (patch) => Object.entries(patch).forEach(([key, value]) => onChange(key, value));
  const last = chart.at(-1);
  const selectedPoint = chart.find((row) => row.age === selectedAge) || last;
  const activeScenario = investmentScenarios.find((scenario) => scenario.annualReturnRate === inputs.annualReturnRate);
  const selectFromPointer = (event) => {
    if (!chart.length) return;
    const svg = event.currentTarget;
    const rect = svg.getBoundingClientRect();
    const x = ((event.clientX - rect.left) / rect.width) * 360;
    setSelectedAge(nearestByX(chart, x).age);
  };

  return (
    <main className="fm-screen fm-scroll">
      <Header tag="실험" onBack={onBack} />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">조건 바꿔보기</p><h2>숫자를 바꾸면 결과가 바로 달라져요</h2>
        <Adjust label="퇴사 나이" value={`${inputs.targetRetirementAge}세`} minus={() => adjust('targetRetirementAge', -1)} plus={() => adjust('targetRetirementAge', 1)} />
        <Adjust label="생활비" value={formatWon(inputs.monthlyLivingCost)} minus={() => adjust('monthlyLivingCost', -100000)} plus={() => adjust('monthlyLivingCost', 100000)} />
        <Adjust label="월 저축액" value={formatWon(inputs.monthlyInvestment)} minus={() => adjust('monthlyInvestment', -100000)} plus={() => adjust('monthlyInvestment', 100000)} />
      </section>
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">투자 수익률 가정</p><h2>투자 성향별로 다시 계산해보기</h2>
        <p>현재 적용 수익률은 연 {inputs.annualReturnRate}%예요. {activeScenario ? activeScenario.copy : '직접 입력한 수익률 가정으로 계산 중이에요.'}</p>
        <div className="fm-chart-summary"><span>선택한 가정 <b>{runwayText(simulation)}</b></span><span>기본 S&P500형 대비 <b>{gapText}</b></span></div>
        <div className="fm-chips fm-return-rail" aria-label="투자 수익률 가정 선택">
          {investmentScenarios.map((scenario) => <button type="button" key={scenario.key} className={scenario.annualReturnRate === inputs.annualReturnRate ? 'is-active' : ''} onClick={() => onChange('annualReturnRate', scenario.annualReturnRate)}>{scenario.label} · 연 {scenario.annualReturnRate}%</button>)}
        </div>
        <small>수익률은 보장값이 아니라 장기 가정이에요. 실제 결과는 시장 상황과 보유 상품에 따라 달라질 수 있어요.</small>
      </section>
      <section className="fm-card fm-text-card fm-advanced-section">
        <p className="fm-kicker">MVP 이후 고급 실험</p><h2>건보료·해외체류·현금흐름까지 같이 보기</h2>
        <p>아직 자문이나 확정값이 아니라, 다음 고도화 단계의 의사결정 시나리오예요. 적용 버튼을 누르면 현재 계산 조건에 바로 반영됩니다.</p>
        <AdvancedScenarioCard
          title="지역가입 건보료 월 23만 원 반영"
          description="퇴사 후 고정비가 늘어나는 보수적 시나리오입니다. 실제 보험료는 소득·재산·제도에 따라 달라져요."
          simulation={healthInsuranceScenario}
          baseSimulation={simulation}
          applyLabel="건보료 반영"
          onApply={() => applyPatch({ healthInsuranceEnabled: 1, monthlyHealthInsurance: 230000 })}
          metrics={[["첫해 건보료", formatWon(healthInsuranceScenario.firstYearHealthInsurance)]]}
        />
        <AdvancedScenarioCard
          title="치앙마이 3개월 살기"
          description="연 3개월 해외 저비용 생활을 적용해 생활비를 낮추는 시나리오입니다. 환율은 1바트 40원으로 둡니다."
          simulation={chiangMaiScenario}
          baseSimulation={simulation}
          applyLabel="해외체류 반영"
          onApply={() => applyPatch({ overseasStayEnabled: 1, overseasMonthsPerYear: 3, overseasContinuousDays: 95, overseasMonthlyCostLocal: 65000, overseasExchangeRate: 40, overseasAnnualExtraCost: 1500000, overseasApplyYears: 10 })}
          metrics={[["첫해 절감", formatWon(chiangMaiScenario.firstYearOverseasSavings)]]}
        />
        <AdvancedScenarioCard
          title="해외 3개월 + 건보료 일시정지"
          description="해외 장기체류로 생활비와 건보료 변화를 함께 보는 공격적 시나리오입니다. 실제 면제 조건은 제도 확인이 필요합니다."
          simulation={chiangMaiInsuranceScenario}
          baseSimulation={simulation}
          applyLabel="복합 시나리오 반영"
          onApply={() => applyPatch({ overseasStayEnabled: 1, overseasInsurancePauseEnabled: 1, healthInsuranceEnabled: 1, monthlyHealthInsurance: 230000, overseasMonthsPerYear: 3, overseasContinuousDays: 95, overseasMonthlyCostLocal: 65000, overseasExchangeRate: 40, overseasAnnualExtraCost: 1500000, overseasApplyYears: 10 })}
          metrics={[["첫해 절감", formatWon(chiangMaiInsuranceScenario.firstYearOverseasSavings)], ["첫해 건보료", formatWon(chiangMaiInsuranceScenario.firstYearHealthInsurance)]]}
        />
        <AdvancedScenarioCard
          title="퇴사 후 월 100만 원 현금흐름"
          description="배당·파트타임·콘텐츠 수익처럼 매달 들어오는 돈이 자산수명에 주는 영향을 봅니다. 세금은 다음 단계에서 분리합니다."
          simulation={dividendTaxScenario}
          baseSimulation={simulation}
          applyLabel="현금흐름 반영"
          onApply={() => onChange('partTimeIncomeAfterRetirement', inputs.partTimeIncomeAfterRetirement + 1000000)}
          metrics={[["월 현금흐름", formatWon(1000000)]]}
        />
      </section>
      <section className="fm-card fm-graph">
        <p className="fm-kicker">내 미래 자산 차트</p><h2>손가락으로 차트를 눌러 나이별 자산을 보세요</h2>
        <div className="fm-chart-summary"><span>현재 계획 <b>{runwayText(simulation)}</b></span><span>생활비 절감안 <b>{runwayText(lowerCost)}</b></span></div>
        <svg className="fm-touch-chart" viewBox="0 0 360 210" role="img" aria-label="나이별 자산 그래프" onPointerDown={selectFromPointer} onPointerMove={(event) => { if (event.buttons === 1 || event.pointerType === 'touch') selectFromPointer(event); }}>
          <line x1="34" y1="152" x2="324" y2="152" /><line x1="34" y1="44" x2="34" y2="152" />
          <text x="34" y="34" className="axis">{formatEok(max)}</text><text x="34" y="174" className="axis">{chart[0]?.age}세</text><text x="292" y="174" className="axis">{last?.age}세</text>
          <polyline points={points('current')} className="current" /><polyline points={points('improved')} className="improved" />
          {selectedPoint && <><line className="fm-crosshair" x1={selectedPoint.x} y1="38" x2={selectedPoint.x} y2="158" /><circle cx={selectedPoint.x} cy={Math.max(32, selectedPoint.currentY)} r="5" className="dot current-dot" /><circle cx={selectedPoint.x} cy={Math.max(32, selectedPoint.improvedY)} r="6" className="dot" /></>}
          <rect className="fm-chart-hitbox" x="28" y="32" width="304" height="130" rx="16" />
        </svg>
        {selectedPoint && <div className="fm-selected-point"><strong>{selectedPoint.age}세 예상 자산</strong><div><span>현재 계획 <b>{formatEok(selectedPoint.current)}</b></span><span>절감안 <b>{formatEok(selectedPoint.improved)}</b></span></div></div>}
        <p className="fm-chart-note">점 맞히기 방식이 아니라 차트 아무 곳이나 누르면 가장 가까운 나이를 보여줘요. 회색은 현재 계획, 주황색은 월 생활비를 줄인 가정입니다. 현재 절감안 기준 생활비는 {formatWon(reducedMonthlyLivingCost)}입니다.</p>
      </section>
    </main>
  );
}
