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

export default function Experiment({ inputs, onChange, simulation, onBack }) {
  const [selectedAge, setSelectedAge] = useState(null);
  const [improvedCost, setImprovedCost] = useState(Math.max(1200000, inputs.monthlyLivingCost - 1500000));
  const lowerCost = useMemo(() => buildScenario(inputs, { monthlyLivingCost: improvedCost }), [inputs, improvedCost]);
  const sp500Baseline = useMemo(() => buildScenario(inputs, { annualReturnRate: 8 }), [inputs]);
  const endAgeGap = scenarioEndAge(simulation) - scenarioEndAge(sp500Baseline);
  const gapText = endAgeGap > 0 ? `S&P500형보다 ${endAgeGap}년 길게` : endAgeGap < 0 ? `S&P500형보다 ${Math.abs(endAgeGap)}년 짧게` : 'S&P500형과 비슷하게';
  const { chart, max } = buildChartRows(simulation, lowerCost, inputs);
  const points = (key) => chart.map((row) => `${row.x},${Math.max(32, key === 'improved' ? row.improvedY : row.currentY)}`).join(' ');
  const adjust = (key, amount) => onChange(key, Math.max(0, cleanNumber(inputs[key]) + amount));
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
        <p>이 화면에서는 퇴사 나이, 생활비, 월 저축액, 수익률처럼 기본 숫자만 조정해요.</p>
        <Adjust label="퇴사 나이" value={`${inputs.targetRetirementAge}세`} minus={() => adjust('targetRetirementAge', -1)} plus={() => adjust('targetRetirementAge', 1)} />
        <Adjust label="생활비" value={formatWon(inputs.monthlyLivingCost)} minus={() => adjust('monthlyLivingCost', -100000)} plus={() => adjust('monthlyLivingCost', 100000)} />
        <Adjust label="월 저축액" value={formatWon(inputs.monthlyInvestment)} minus={() => adjust('monthlyInvestment', -100000)} plus={() => adjust('monthlyInvestment', 100000)} />
        <Adjust label="연 수익률" value={`${inputs.annualReturnRate}%`} minus={() => adjust('annualReturnRate', -1)} plus={() => adjust('annualReturnRate', 1)} />
        <Adjust label="절감안 생활비" value={formatWon(improvedCost)} minus={() => setImprovedCost((value) => Math.max(1200000, value - 100000))} plus={() => setImprovedCost((value) => value + 100000)} />
      </section>
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">투자 수익률 가정</p><h2>투자 성향별로 다시 계산해보기</h2>
        <p>현재 적용 수익률은 연 {inputs.annualReturnRate}%예요. {activeScenario ? activeScenario.copy : '직접 입력한 수익률 가정으로 계산 중이에요.'}</p>
        <div className="fm-chart-summary"><span>선택한 가정 <b>{runwayText(simulation)}</b></span><span>기본 S&P500형 대비 <b>{gapText}</b></span></div>
        <div className="fm-chips fm-return-rail" aria-label="투자 수익률 가정 선택">
          {investmentScenarios.map((scenario) => <button type="button" key={scenario.key} className={scenario.annualReturnRate === inputs.annualReturnRate ? 'is-active' : ''} onClick={() => onChange('annualReturnRate', scenario.annualReturnRate)}>{scenario.label} · 연 {scenario.annualReturnRate}%</button>)}
        </div>
        <small>수익률은 보장값이 아니라 장기 가정이에요. 직접 조절하거나 프리셋을 눌러 비교할 수 있어요.</small>
      </section>
      <section className="fm-card fm-graph">
        <p className="fm-kicker">내 미래 자산 차트</p><h2>손가락으로 차트를 눌러 나이별 자산을 보세요</h2>
        <div className="fm-chart-summary"><span>현재 계획 <b>{runwayText(simulation)}</b></span><span>생활비 절감안 <b>{runwayText(lowerCost)}</b></span></div>
        <svg className="fm-touch-chart" viewBox="0 0 360 210" role="img" aria-label="나이별 자산 그래프" onPointerDown={selectFromPointer} onPointerMove={(event) => { if (event.buttons === 1 || event.pointerType === 'touch') selectFromPointer(event); }}>
          <line x1="34" y1="152" x2="324" y2="152" /><line x1="34" y1="44" x2="34" y2="152" />
          <text x="34" y="34" className="axis">Y축 {formatEok(max)}</text><text x="34" y="174" className="axis">X축 {chart[0]?.age}세</text><text x="292" y="174" className="axis">{last?.age}세</text>
          <polyline points={points('current')} className="current" /><polyline points={points('improved')} className="improved" />
          {selectedPoint && <><line className="fm-crosshair" x1={selectedPoint.x} y1="38" x2={selectedPoint.x} y2="158" /><circle cx={selectedPoint.x} cy={Math.max(32, selectedPoint.currentY)} r="5" className="dot current-dot" /><circle cx={selectedPoint.x} cy={Math.max(32, selectedPoint.improvedY)} r="6" className="dot" /></>}
          <rect className="fm-chart-hitbox" x="28" y="32" width="304" height="130" rx="16" />
        </svg>
        {selectedPoint && <div className="fm-selected-point"><strong>{selectedPoint.age}세 예상 자산</strong><div><span>현재 계획 <b>{formatEok(selectedPoint.current)}</b></span><span>절감안 <b>{formatEok(selectedPoint.improved)}</b></span></div></div>}
        <p className="fm-chart-note">차트는 1살 단위 데이터를 사용해요. 회색은 현재 계획, 주황색은 절감안 생활비 {formatWon(improvedCost)} 기준입니다.</p>
      </section>
    </main>
  );
}
