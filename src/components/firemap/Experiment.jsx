import { useMemo, useState } from 'react';
import Header from './Header.jsx';
import ResultSimTabs from './ResultSimTabs.jsx';
import PensionControls from './PensionControls.jsx';
import RangeControl from './RangeControl.jsx';
import AssetCompareChart from './AssetCompareChart.jsx';
import AssetGrowthChart from './AssetGrowthChart.jsx';
import { investmentScenarios } from '../../firemap-v2/data.js';
import { sourceLine } from '../../firemap-v2/dataSources.js';
import { buildChartRows, buildScenario, runwayText, buildGrowthSeries } from '../../firemap-v2/scenarios.js';
import { formatWon, cleanNumber } from '../../firemap-v2/formatters.js';

export default function Experiment({ inputs, onChange, onBack }) {
  // 바꿔보기는 '미리보기 샌드박스'. 로컬 draft에서만 굴리고, [저장]을 눌러야만
  // 실제 inputs(=결과 화면·리더보드 등수·localStorage)에 반영된다. (실험값이 등수를 오염시키지 않도록)
  const [draft, setDraft] = useState(inputs);
  const editDraft = (key, value) => setDraft((c) => ({ ...c, [key]: cleanNumber(value) }));
  const [improvedCost, setImprovedCost] = useState(Math.max(1500000, Math.min(3000000, inputs.monthlyLivingCost - 1000000)));
  const [chartMode, setChartMode] = useState('compare');
  const [saved, setSaved] = useState(false);

  const simulation = useMemo(() => buildScenario(draft, {}), [draft]);
  const lowerCost = useMemo(() => buildScenario(draft, { monthlyLivingCost: improvedCost }), [draft, improvedCost]);
  const yearsToRetire = Math.max(1, draft.targetRetirementAge - draft.currentAge);
  const savingYearsValue = draft.savingYears > 0 ? Math.min(draft.savingYears, yearsToRetire) : yearsToRetire;
  const impacts = useMemo(() => investmentScenarios.map((sc) => {
    const s = buildScenario(draft, { annualReturnRate: sc.annualReturnRate });
    return { ...sc, runway: runwayText(s) };
  }), [draft]);
  const { chart } = buildChartRows(simulation, lowerCost, draft);
  const ages = useMemo(() => chart.map((row) => row.age), [chart]);
  const currentSeries = useMemo(() => chart.map((row) => Math.max(0, row.current)), [chart]);
  const improvedSeries = useMemo(() => chart.map((row) => Math.max(0, row.improved)), [chart]);
  const growth = useMemo(() => buildGrowthSeries(simulation), [simulation]);
  const retIdx = useMemo(() => growth.ages.indexOf(draft.targetRetirementAge), [growth, draft.targetRetirementAge]);
  const principalAtRet = retIdx >= 0 ? growth.principal[retIdx] : (growth.principal.at(-1) || 0);
  const gainsAtRet = retIdx >= 0 ? growth.gains[retIdx] : (growth.gains.at(-1) || 0);
  const activeScenario = investmentScenarios.find((scenario) => scenario.annualReturnRate === draft.annualReturnRate);
  const investType = Number(draft.investType || 0);
  const grossDivAtRetire = Math.round((simulation.retirementFinancialAsset || draft.financialAsset || 0) * ((draft.dividendYield || 0) / 100));

  const dirty = useMemo(() => Object.keys(draft).some((k) => cleanNumber(draft[k]) !== cleanNumber(inputs[k])), [draft, inputs]);
  const commit = () => { Object.entries(draft).forEach(([k, v]) => onChange(k, v)); setSaved(true); setTimeout(() => setSaved(false), 2400); };
  const reset = () => { setDraft(inputs); setSaved(false); };

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar">
      <Header tag="바꿔보기" onBack={onBack} />
      <ResultSimTabs current="sim" />
      <section className="fm-card fm-sim-live">
        <p className="fm-sim-live-kicker">{dirty ? '바꾼 조건 미리보기' : '지금 조건이면'}</p>
        <div className="fm-sim-live-row">
          <div><small>퇴사 가능</small><b>{simulation.earliestRetirementAge ? `${simulation.earliestRetirementAge}세` : '아직'}</b></div>
          <div><small>자산 수명</small><b>{runwayText(simulation)}</b></div>
        </div>
        {dirty ? (
          <div className="fm-sim-actions">
            <span className="fm-sim-actions-note">여기서 바꾼 값은 <b>미리보기</b>예요 · 저장 전엔 내 결과·등수에 반영되지 않아요</span>
            <div className="fm-sim-actions-btns">
              <button type="button" className="fm-sim-reset" onClick={reset}>되돌리기</button>
              <button type="button" className="fm-sim-save" onClick={commit}>이 조건을 내 결과로 저장</button>
            </div>
          </div>
        ) : (
          <p className="fm-sim-live-note">{saved ? '✓ 내 결과·등수에 반영됐어요' : '아래 수치를 밀면 위 숫자가 바로 바뀌어요 (미리보기)'}</p>
        )}
      </section>
      <section className="fm-card fm-graph">
        <p className="fm-kicker">내 미래 자산 차트</p><h2>나이별 자산 흐름을 비교해보세요</h2>
        <div className="fm-chips fm-chart-mode" role="tablist" aria-label="차트 보기 전환">
          <button type="button" className={chartMode === 'compare' ? 'is-active' : ''} onClick={() => setChartMode('compare')}>현재 vs 절감안</button>
          <button type="button" className={chartMode === 'growth' ? 'is-active' : ''} onClick={() => setChartMode('growth')}>원금 vs 불어난 돈</button>
        </div>
        {chartMode === 'compare' ? (
          <>
            <div className="fm-chart-legend">
              <span><i className="fm-dot fm-dot-current" />현재 계획 · {runwayText(simulation)}</span>
              <span><i className="fm-dot fm-dot-improved" />절감안 · {runwayText(lowerCost)}</span>
            </div>
            <AssetCompareChart ages={ages} current={currentSeries} improved={improvedSeries} depletionAge={simulation.targetResult.depletionAge} improvedDepletionAge={lowerCost.targetResult.depletionAge} retirementAge={draft.targetRetirementAge} />
            <p className="fm-chart-note">차트를 누르면 그 나이의 세후 자산이 표시돼요. 회색 점선은 현재 계획, 파란 영역은 절감안 기준입니다.</p>
          </>
        ) : (
          <>
            <div className="fm-chart-legend">
              <span><i className="fm-dot fm-dot-principal" />내가 넣은 돈 · {formatWon(principalAtRet)}</span>
              <span><i className="fm-dot fm-dot-gains" />불어난 돈 · {formatWon(gainsAtRet)}</span>
            </div>
            <AssetGrowthChart ages={growth.ages} principal={growth.principal} gains={growth.gains} retirementAge={draft.targetRetirementAge} depletionAge={simulation.targetResult.depletionAge} />
            <p className="fm-chart-note">퇴사({draft.targetRetirementAge}세) 시점 기준 · 파란색은 내가 직접 넣은 돈, 주황색은 투자로 불어난 돈이에요. 퇴사 후엔 쓰면서 줄어들어요.</p>
          </>
        )}
      </section>
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">조건 바꿔보기</p><h2>손가락으로 밀어서 바로 바꿔보세요</h2>
        <p>현재 자산·나이부터 퇴사 나이·생활비·저축·부업·수익률까지 한 화면에서 자유롭게 바꿔보세요.</p>
        <RangeControl label="현재 나이" value={draft.currentAge} inputKey="currentAge" type="age" step={1} onChange={(next) => editDraft('currentAge', next)} />
        <RangeControl label="퇴사 나이" value={draft.targetRetirementAge} inputKey="targetRetirementAge" type="age" step={1} onChange={(next) => editDraft('targetRetirementAge', next)} />
        <RangeControl label="현재 금융자산" value={draft.financialAsset} inputKey="financialAsset" type="money" step={10000000} onChange={(next) => editDraft('financialAsset', next)} />
        <RangeControl label="월 저축액" value={draft.monthlyInvestment} inputKey="monthlyInvestment" type="money" step={100000} onChange={(next) => editDraft('monthlyInvestment', next)} />
        <RangeControl label="앞으로 저축하는 기간" value={savingYearsValue} inputKey="savingYears" type="years" step={1} maxOverride={yearsToRetire} onChange={(next) => editDraft('savingYears', next >= yearsToRetire ? 0 : next)} />
        <p className="fm-range-note">기본은 퇴사까지({yearsToRetire}년) 매달 저축이에요. 줄이면 그만큼만 저축하고, 이후엔 모은 돈을 굴리기만 해요(코스트 파이어).</p>
        <RangeControl label="연봉 상승률(저축도 매년 증가)" value={draft.salaryGrowthRate} inputKey="salaryGrowthRate" type="percent" step={1} onChange={(next) => editDraft('salaryGrowthRate', next)} />
        <RangeControl label="퇴사 후 월 생활비" value={draft.monthlyLivingCost} inputKey="monthlyLivingCost" type="money" step={100000} onChange={(next) => editDraft('monthlyLivingCost', next)} />
        <RangeControl label="퇴사 후 부업 소득" value={draft.partTimeIncomeAfterRetirement} inputKey="partTimeIncomeAfterRetirement" type="money" step={100000} onChange={(next) => editDraft('partTimeIncomeAfterRetirement', next)} />
        <p className="fm-range-note">부업 소득은 물가에 연동되지 않아요 — 생활비·연금과 달리 매년 오르지 않는 고정 수입으로 계산해요.</p>
        <RangeControl label="연 수익률" value={draft.annualReturnRate} inputKey="annualReturnRate" type="percent" step={1} onChange={(next) => editDraft('annualReturnRate', next)} />
        <RangeControl label="물가 상승률(생활비 매년 증가)" value={draft.inflationRate} inputKey="inflationRate" type="percent" step={1} onChange={(next) => editDraft('inflationRate', next)} />
        <p className="fm-range-note">이 비율만큼 <strong>생활비·국민연금·건보료·해외 체류비</strong>가 매년 올라요. (부업 소득만 제외)</p>
        <RangeControl label="절감안 생활비" value={improvedCost} inputKey="improvedCost" type="money" step={100000} onChange={setImprovedCost} />
      </section>
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">투자 유형 · 세금</p><h2>어디에 투자하느냐로 세금이 달라져요</h2>
        <div className="fm-chips fm-invest-chips" aria-label="투자 유형 선택">
          <button type="button" className={investType === 0 ? 'is-active' : ''} onClick={() => editDraft('investType', 0)}>국내주식 · 양도세 면제</button>
          <button type="button" className={investType === 1 ? 'is-active' : ''} onClick={() => editDraft('investType', 1)}>해외주식 · 양도세 22%</button>
          <button type="button" className={investType === 2 ? 'is-active' : ''} onClick={() => editDraft('investType', 2)}>배당 생활 · 배당세 15.4%</button>
        </div>
        {investType === 2 && <RangeControl label="배당수익률" value={draft.dividendYield} inputKey="dividendYield" type="percent" step={1} onChange={(next) => editDraft('dividendYield', next)} />}
        {investType === 2 && Number(draft.dividendYield || 0) >= Number(draft.annualReturnRate || 0) && <p className="fm-range-note fm-tax-warn">⚠️ 배당수익률이 연 수익률보다 크면 원금이 줄어요.</p>}
        {investType === 2 && grossDivAtRetire > 20000000 && <p className="fm-range-note">⚠️ 퇴사 시 연 배당 약 {formatWon(grossDivAtRetire)} · 금융소득 2,000만 초과 → 종합과세·건보료 부담↑ (도구 탭에서 정밀 확인)</p>}
        <div className="fm-tax-explain">
          <p className="fm-tax-explain-title">ℹ️ 선택한 유형의 세금</p>
          {investType === 0 && <p className="fm-tax-explain-line">국내주식은 양도세가 <b>면제</b>예요(대주주 제외). 팔아서 생활비를 써도 투자 세금 부담이 없어요.</p>}
          {investType === 1 && <p className="fm-tax-explain-line">해외주식은 퇴사 후 <b>매년 쓰는 만큼 팔 때 그 차익</b>에 <b>22%</b>(매년 250만 공제). 한 번에 매도가 아니에요.</p>}
          {investType === 2 && <p className="fm-tax-explain-line">배당으로 생활하면 받는 배당마다 <b>15.4%</b> 원천징수돼요. (금융소득 2,000만 초과 시 종합과세↑)</p>}
          <p className="fm-tax-explain-sub">종합과세 누진·ISA/연금 절세는 개인 상황별이라 결과엔 반영하지 않아요.</p>
          <div className="fm-tax-links">
            <a href="/guide/dividend-tax-thresholds.html" target="_blank" rel="noopener">배당 세금 경계선 →</a>
            <a href="/guide/isa-pension-accounts.html" target="_blank" rel="noopener">ISA·연금 절세 →</a>
          </div>
        </div>
      </section>
      <PensionControls inputs={draft} onChange={editDraft} />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">수익률 가정</p><h2>어디에 두느냐에 따라 이렇게 달라져요</h2>
        <p>현재 적용 수익률은 연 {draft.annualReturnRate}%예요. {activeScenario ? activeScenario.copy : '직접 입력한 수익률 가정으로 계산 중이에요.'} 아래에서 가정을 바꾸면 자산수명이 함께 바뀝니다.</p>
        <div className="fm-chips fm-return-rail" aria-label="투자 수익률 가정 선택">
          {investmentScenarios.map((scenario) => <button type="button" key={scenario.key} className={scenario.annualReturnRate === draft.annualReturnRate ? 'is-active' : ''} onClick={() => editDraft('annualReturnRate', scenario.annualReturnRate)}>{scenario.label} · 연 {scenario.annualReturnRate}%</button>)}
        </div>
        <div className="fm-bench">
          {impacts.map((sc) => (
            <div className={`fm-bench-row2${sc.annualReturnRate === draft.annualReturnRate ? ' is-active' : ''}`} key={sc.key}>
              <div className="fm-bench-head"><b>{sc.label}</b><span>연 {sc.annualReturnRate}%</span></div>
              <div className="fm-bench-metrics"><span>이 가정이면 자산수명 <b>{sc.runway}</b>까지</span></div>
              <em>{sc.copy}</em>
            </div>
          ))}
        </div>
        <small>예적금부터 공격적 투자까지, 같은 자산도 어디에 두느냐로 자산수명이 달라져요. 가정이 높을수록 기대수익도, 변동성(위험)도 커집니다. 과거 통계 기반 가정이며 특정 상품 추천이 아니에요. {sourceLine('returnPresets')}</small>
      </section>
    </main>
  );
}
