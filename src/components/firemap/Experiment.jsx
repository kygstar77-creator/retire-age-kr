import { useMemo, useState } from 'react';
import Header from './Header.jsx';
import PensionControls from './PensionControls.jsx';
import RangeControl from './RangeControl.jsx';
import AssetCompareChart from './AssetCompareChart.jsx';
import { investmentScenarios } from '../../firemap-v2/data.js';
import { sourceLine } from '../../firemap-v2/dataSources.js';
import { buildChartRows, buildScenario, runwayText, scenarioEndAge } from '../../firemap-v2/scenarios.js';

export default function Experiment({ inputs, onChange, simulation, onBack }) {
  const [improvedCost, setImprovedCost] = useState(Math.max(1500000, Math.min(3000000, inputs.monthlyLivingCost - 1000000)));
  const lowerCost = useMemo(() => buildScenario(inputs, { monthlyLivingCost: improvedCost }), [inputs, improvedCost]);
  const sp500Baseline = useMemo(() => buildScenario(inputs, { annualReturnRate: 8 }), [inputs]);
  const endAgeGap = scenarioEndAge(simulation) - scenarioEndAge(sp500Baseline);
  const gapText = endAgeGap > 0 ? `S&P500형보다 ${endAgeGap}년 길게` : endAgeGap < 0 ? `S&P500형보다 ${Math.abs(endAgeGap)}년 짧게` : 'S&P500형과 비슷하게';
  const { chart } = buildChartRows(simulation, lowerCost, inputs);
  const ages = useMemo(() => chart.map((row) => row.age), [chart]);
  const currentSeries = useMemo(() => chart.map((row) => Math.max(0, row.current)), [chart]);
  const improvedSeries = useMemo(() => chart.map((row) => Math.max(0, row.improved)), [chart]);
  const activeScenario = investmentScenarios.find((scenario) => scenario.annualReturnRate === inputs.annualReturnRate);

  return (
    <main className="fm-screen fm-scroll">
      <Header tag="비교" onBack={onBack} />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">조건 바꿔보기</p><h2>손가락으로 밀어서 바로 바꿔보세요</h2>
        <p>현재 자산·나이부터 퇴사 나이·생활비·저축·부업·수익률까지 한 화면에서 자유롭게 바꿔보세요.</p>
        <RangeControl label="현재 나이" value={inputs.currentAge} inputKey="currentAge" type="age" step={1} onChange={(next) => onChange('currentAge', next)} />
        <RangeControl label="퇴사 나이" value={inputs.targetRetirementAge} inputKey="targetRetirementAge" type="age" step={1} onChange={(next) => onChange('targetRetirementAge', next)} />
        <RangeControl label="현재 금융자산" value={inputs.financialAsset} inputKey="financialAsset" type="money" step={1000000} onChange={(next) => onChange('financialAsset', next)} />
        <RangeControl label="월 저축액" value={inputs.monthlyInvestment} inputKey="monthlyInvestment" type="money" step={100000} onChange={(next) => onChange('monthlyInvestment', next)} />
        <RangeControl label="퇴사 후 월 생활비" value={inputs.monthlyLivingCost} inputKey="monthlyLivingCost" type="money" step={100000} onChange={(next) => onChange('monthlyLivingCost', next)} />
        <RangeControl label="퇴사 후 부업 소득" value={inputs.partTimeIncomeAfterRetirement} inputKey="partTimeIncomeAfterRetirement" type="money" step={100000} onChange={(next) => onChange('partTimeIncomeAfterRetirement', next)} />
        <RangeControl label="연 수익률" value={inputs.annualReturnRate} inputKey="annualReturnRate" type="percent" step={1} onChange={(next) => onChange('annualReturnRate', next)} />
        <RangeControl label="절감안 생활비" value={improvedCost} inputKey="improvedCost" type="money" step={100000} onChange={setImprovedCost} />
      </section>
      <PensionControls inputs={inputs} onChange={onChange} />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">수익률 가정</p><h2>투자 성향별로 다시 계산해보기</h2>
        <p>현재 적용 수익률은 연 {inputs.annualReturnRate}%예요. {activeScenario ? activeScenario.copy : '직접 입력한 수익률 가정으로 계산 중이에요.'}</p>
        <div className="fm-chart-summary"><span>선택한 가정 <b>{runwayText(simulation)}</b></span><span>S&P500형 대비 <b>{gapText}</b></span></div>
        <div className="fm-chips fm-return-rail" aria-label="투자 수익률 가정 선택">
          {investmentScenarios.map((scenario) => <button type="button" key={scenario.key} className={scenario.annualReturnRate === inputs.annualReturnRate ? 'is-active' : ''} onClick={() => onChange('annualReturnRate', scenario.annualReturnRate)}>{scenario.label} · 연 {scenario.annualReturnRate}%</button>)}
        </div>
        <small>과거 수익률은 보장값이 아닌 장기 통계 가정이에요. 특정 종목 추천이 아닙니다. {sourceLine('returnPresets')}</small>
      </section>
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">수익률 벤치마크</p><h2>예적금 대비 어디에 두느냐의 차이</h2>
        <p>아래는 자산을 어디에 두느냐의 장기 수익률 가정이에요. 가정을 높일수록 위 차트에서 자산수명·FIRE 시점이 당겨져요. 특정 상품 추천이 아니라 일반 지수 가정입니다.</p>
        <div className="fm-bench">
          {investmentScenarios.map((sc) => (
            <div className="fm-bench-row" key={sc.key}>
              <b>{sc.label}</b><span>연 {sc.annualReturnRate}%</span><em>{sc.copy}</em>
            </div>
          ))}
        </div>
        <small>예적금형(보수)부터 지수형(공격)까지 폭을 비교해 보세요. {sourceLine('returnPresets')}</small>
      </section>
      <section className="fm-card fm-graph">
        <p className="fm-kicker">내 미래 자산 차트</p><h2>나이별 자산 흐름을 비교해보세요</h2>
        <div className="fm-chart-legend">
          <span><i className="fm-dot fm-dot-current" />현재 계획 · {runwayText(simulation)}</span>
          <span><i className="fm-dot fm-dot-improved" />절감안 · {runwayText(lowerCost)}</span>
        </div>
        <AssetCompareChart ages={ages} current={currentSeries} improved={improvedSeries} />
        <p className="fm-chart-note">차트를 누르면 그 나이의 세후 자산이 표시돼요. 회색 점선은 현재 계획, 파란 영역은 절감안 기준입니다.</p>
      </section>
      <nav className="fm-bottom-nav">
        <button type="button" onClick={onBack}>취소</button>
        <button type="button" onClick={onBack}>결과 보기</button>
      </nav>
    </main>
  );
}
