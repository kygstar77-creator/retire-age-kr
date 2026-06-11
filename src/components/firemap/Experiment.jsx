import { useMemo, useState } from 'react';
import Header from './Header.jsx';
import PensionControls from './PensionControls.jsx';
import RangeControl from './RangeControl.jsx';
import AssetCompareChart from './AssetCompareChart.jsx';
import { investmentScenarios } from '../../firemap-v2/data.js';
import { sourceLine } from '../../firemap-v2/dataSources.js';
import { buildChartRows, buildScenario, runwayText } from '../../firemap-v2/scenarios.js';
import { monteCarloSuccess } from '../../utils/retirementSimulator.js';

export default function Experiment({ inputs, onChange, simulation, onBack }) {
  const [improvedCost, setImprovedCost] = useState(Math.max(1500000, Math.min(3000000, inputs.monthlyLivingCost - 1000000)));
  const lowerCost = useMemo(() => buildScenario(inputs, { monthlyLivingCost: improvedCost }), [inputs, improvedCost]);
  const yearsToRetire = Math.max(1, inputs.targetRetirementAge - inputs.currentAge);
  const savingYearsValue = inputs.savingYears > 0 ? Math.min(inputs.savingYears, yearsToRetire) : yearsToRetire;
  const impacts = useMemo(() => investmentScenarios.map((sc) => {
    const s = buildScenario(inputs, { annualReturnRate: sc.annualReturnRate });
    return { ...sc, runway: runwayText(s), success: monteCarloSuccess({ ...inputs, annualReturnRate: sc.annualReturnRate }) };
  }), [inputs]);
  const { chart } = buildChartRows(simulation, lowerCost, inputs);
  const ages = useMemo(() => chart.map((row) => row.age), [chart]);
  const currentSeries = useMemo(() => chart.map((row) => Math.max(0, row.current)), [chart]);
  const improvedSeries = useMemo(() => chart.map((row) => Math.max(0, row.improved)), [chart]);
  const activeScenario = investmentScenarios.find((scenario) => scenario.annualReturnRate === inputs.annualReturnRate);

  return (
    <main className="fm-screen fm-scroll">
      <Header tag="비교" onBack={onBack} />
      <section className="fm-card fm-graph">
        <p className="fm-kicker">내 미래 자산 차트</p><h2>나이별 자산 흐름을 비교해보세요</h2>
        <div className="fm-chart-legend">
          <span><i className="fm-dot fm-dot-current" />현재 계획 · {runwayText(simulation)}</span>
          <span><i className="fm-dot fm-dot-improved" />절감안 · {runwayText(lowerCost)}</span>
        </div>
        <AssetCompareChart ages={ages} current={currentSeries} improved={improvedSeries} depletionAge={simulation.targetResult.depletionAge} improvedDepletionAge={lowerCost.targetResult.depletionAge} retirementAge={inputs.targetRetirementAge} />
        <p className="fm-chart-note">차트를 누르면 그 나이의 세후 자산이 표시돼요. 회색 점선은 현재 계획, 파란 영역은 절감안 기준입니다.</p>
      </section>
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">조건 바꿔보기</p><h2>손가락으로 밀어서 바로 바꿔보세요</h2>
        <p>현재 자산·나이부터 퇴사 나이·생활비·저축·부업·수익률까지 한 화면에서 자유롭게 바꿔보세요.</p>
        <RangeControl label="현재 나이" value={inputs.currentAge} inputKey="currentAge" type="age" step={1} onChange={(next) => onChange('currentAge', next)} />
        <RangeControl label="퇴사 나이" value={inputs.targetRetirementAge} inputKey="targetRetirementAge" type="age" step={1} onChange={(next) => onChange('targetRetirementAge', next)} />
        <RangeControl label="현재 금융자산" value={inputs.financialAsset} inputKey="financialAsset" type="money" step={10000000} onChange={(next) => onChange('financialAsset', next)} />
        <RangeControl label="월 저축액" value={inputs.monthlyInvestment} inputKey="monthlyInvestment" type="money" step={100000} onChange={(next) => onChange('monthlyInvestment', next)} />
        <RangeControl label="앞으로 저축하는 기간" value={savingYearsValue} inputKey="savingYears" type="years" step={1} maxOverride={yearsToRetire} onChange={(next) => onChange('savingYears', next >= yearsToRetire ? 0 : next)} />
        <p className="fm-range-note">기본은 퇴사까지({yearsToRetire}년) 매달 저축이에요. 줄이면 그만큼만 저축하고, 이후엔 모은 돈을 굴리기만 해요(코스트 파이어).</p>
        <RangeControl label="연봉 상승률(저축도 매년 증가)" value={inputs.salaryGrowthRate} inputKey="salaryGrowthRate" type="percent" step={1} onChange={(next) => onChange('salaryGrowthRate', next)} />
        <RangeControl label="퇴사 후 월 생활비" value={inputs.monthlyLivingCost} inputKey="monthlyLivingCost" type="money" step={100000} onChange={(next) => onChange('monthlyLivingCost', next)} />
        <RangeControl label="퇴사 후 부업 소득" value={inputs.partTimeIncomeAfterRetirement} inputKey="partTimeIncomeAfterRetirement" type="money" step={100000} onChange={(next) => onChange('partTimeIncomeAfterRetirement', next)} />
        <RangeControl label="연 수익률" value={inputs.annualReturnRate} inputKey="annualReturnRate" type="percent" step={1} onChange={(next) => onChange('annualReturnRate', next)} />
        <RangeControl label="물가 상승률(생활비 매년 증가)" value={inputs.inflationRate} inputKey="inflationRate" type="percent" step={1} onChange={(next) => onChange('inflationRate', next)} />
        <RangeControl label="절감안 생활비" value={improvedCost} inputKey="improvedCost" type="money" step={100000} onChange={setImprovedCost} />
      </section>
      <PensionControls inputs={inputs} onChange={onChange} />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">수익률 가정</p><h2>어디에 두느냐에 따라 이렇게 달라져요</h2>
        <p>현재 적용 수익률은 연 {inputs.annualReturnRate}%예요. {activeScenario ? activeScenario.copy : '직접 입력한 수익률 가정으로 계산 중이에요.'} 아래에서 가정을 바꾸면 자산수명·성공확률이 함께 바뀝니다.</p>
        <div className="fm-chips fm-return-rail" aria-label="투자 수익률 가정 선택">
          {investmentScenarios.map((scenario) => <button type="button" key={scenario.key} className={scenario.annualReturnRate === inputs.annualReturnRate ? 'is-active' : ''} onClick={() => onChange('annualReturnRate', scenario.annualReturnRate)}>{scenario.label} · 연 {scenario.annualReturnRate}%</button>)}
        </div>
        <div className="fm-bench">
          {impacts.map((sc) => (
            <div className={`fm-bench-row2${sc.annualReturnRate === inputs.annualReturnRate ? ' is-active' : ''}`} key={sc.key}>
              <div className="fm-bench-head"><b>{sc.label}</b><span>연 {sc.annualReturnRate}%</span></div>
              <div className="fm-bench-metrics"><span>자산수명 <b>{sc.runway}</b></span><span>성공확률 <b>{sc.success}%</b></span></div>
              <div className="fm-bench-bar"><i style={{ width: `${sc.success}%` }} /></div>
              <em>{sc.copy}</em>
            </div>
          ))}
        </div>
        <small>예적금부터 공격적 투자까지, 같은 자산도 어디에 두느냐로 자산수명·성공확률이 달라져요. 가정이 높을수록 변동성(위험)도 커집니다. 성공확률은 변동성과 함께 500회 시뮬한 값(결과 화면과 같은 기준)이며 특정 상품 추천이 아니에요. {sourceLine('returnPresets')}</small>
      </section>
      <nav className="fm-bottom-nav">
        <button type="button" onClick={onBack}>취소</button>
        <button type="button" onClick={onBack}>결과 보기</button>
      </nav>
    </main>
  );
}
