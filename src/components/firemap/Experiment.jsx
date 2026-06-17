import { useEffect, useMemo, useState } from 'react';
import Header from './Header.jsx';
import ResultSimTabs from './ResultSimTabs.jsx';
import PensionControls from './PensionControls.jsx';
import RangeControl from './RangeControl.jsx';
import AssetGrowthChart from './AssetGrowthChart.jsx';
import { investmentScenarios } from '../../firemap-v2/data.js';
import { sourceLine } from '../../firemap-v2/dataSources.js';
import { buildScenario, runwayText, buildGrowthSeries } from '../../firemap-v2/scenarios.js';
import { formatWon, cleanNumber } from '../../firemap-v2/formatters.js';

export default function Experiment({ inputs, onChange, onBack, onMove, draft: draftProp, setDraft: setDraftProp, base: baseProp, setBase: setBaseProp }) {
  // 바꿔보기는 '미리보기 샘드박스'. draft를 부모가 보관하면 그걸 써서 세금 도구 등 다른 화면을 다녀와도 유지되고, 없으면 로컬로 동작.
  const [localDraft, setLocalDraft] = useState(inputs);
  const draft = draftProp ?? localDraft;
  const setDraft = setDraftProp ?? setLocalDraft;
  const editDraft = (key, value) => setDraft((c) => ({ ...(c ?? inputs), [key]: cleanNumber(value) }));
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [showTax, setShowTax] = useState(false);
  const [showPension, setShowPension] = useState(false);
  const [showReturns, setShowReturns] = useState(false);
  const [showAssets, setShowAssets] = useState(false);
  const [saved, setSaved] = useState(false);

  const simulation = useMemo(() => buildScenario(draft, {}), [draft]);
  const yearsToRetire = Math.max(1, draft.targetRetirementAge - draft.currentAge);
  const savingYearsValue = draft.savingYears > 0 ? Math.min(draft.savingYears, yearsToRetire) : yearsToRetire;
  const impacts = useMemo(() => investmentScenarios.map((sc) => {
    const s = buildScenario(draft, { annualReturnRate: sc.annualReturnRate });
    return { ...sc, runway: runwayText(s) };
  }), [draft]);
  const growth = useMemo(() => buildGrowthSeries(simulation), [simulation]);
  const retIdx = useMemo(() => growth.ages.indexOf(draft.targetRetirementAge), [growth, draft.targetRetirementAge]);
  const principalAtRet = retIdx >= 0 ? growth.principal[retIdx] : (growth.principal.at(-1) || 0);
  const gainsAtRet = retIdx >= 0 ? growth.gains[retIdx] : (growth.gains.at(-1) || 0);
  const activeScenario = investmentScenarios.find((scenario) => scenario.annualReturnRate === draft.annualReturnRate);
  const investType = Number(draft.investType || 0);
  const grossDivAtRetire = Math.round((simulation.retirementFinancialAsset || draft.financialAsset || 0) * ((draft.dividendYield || 0) / 100));
  const reVal = cleanNumber(draft.realEstateValue);
  const debtVal = cleanNumber(draft.debt);
  const rentVal = cleanNumber(draft.monthlyRentalIncome);
  const netWorth = simulation.netWorth;
  const hasAssetExtra = reVal > 0 || debtVal > 0 || rentVal > 0;

  const PREVIEW_ONLY = ['investType', 'dividendYield'];
  // 샘드박스 슬라이더가 직접 바꾸는 핵심 값들. 이 값들이 (질문 재입력 등으로) 실제로 바뀐 경우에만 샘드박스를 새로 시드.
  // 세금·연금 도구가 '반영'으로 건드리는 값(investType·dividendIncomeMonthly·pensionClaimAge 등)은 여기 없으므로,
  // 도구를 다녀오거나 거기서 세금을 반영해도 바꿔보기 작업이 날아가지 않는다.
  const SANDBOX_KEYS = ['currentAge', 'targetRetirementAge', 'financialAsset', 'monthlyInvestment', 'monthlyLivingCost', 'savingYears', 'salaryGrowthRate', 'partTimeIncomeAfterRetirement', 'inflationRate', 'annualReturnRate'];
  const dirty = useMemo(() => Object.keys(draft).some((k) => !PREVIEW_ONLY.includes(k) && cleanNumber(draft[k]) !== cleanNumber(inputs[k])), [draft, inputs]);
  const commit = () => { Object.entries(draft).forEach(([k, v]) => { if (!PREVIEW_ONLY.includes(k)) onChange(k, v); }); setSaved(true); setTimeout(() => setSaved(false), 2400); };
  const reset = () => { setDraft({ ...inputs }); setBaseProp?.({ ...inputs }); setSaved(false); };

  // 하단 액션 독이 떠 있는 동안 본문 여백 확보 + 피드백 FAB를 독 위로 올림.
  useEffect(() => {
    document.body.classList.toggle('fm-exp-dock', dirty);
    return () => document.body.classList.remove('fm-exp-dock');
  }, [dirty]);

  // 다른 화면(세금 도구 등)을 다녀와도 샘드박스 유지.
  // 판정 기준은 draft가 아니라 base(시드 시점 inputs 스넹샷): 사용자의 draft 편집은 base를 안 바꾸므로 안 날아가고,
  // 질문 재입력 등으로 '핵심 입력값(inputs)' 자체가 바뀐 경우에만 새로 시드한다.
  useEffect(() => {
    if (draftProp == null || baseProp == null) {
      setDraftProp?.({ ...inputs });
      setBaseProp?.({ ...inputs });
      return;
    }
    const inputsChanged = SANDBOX_KEYS.some((k) => cleanNumber(inputs[k]) !== cleanNumber(baseProp[k]));
    if (inputsChanged) {
      setDraftProp({ ...inputs });
      setBaseProp({ ...inputs });
    }
  }, [inputs]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar">
      <Header tag="바꿔보기" onBack={onBack} />
      <ResultSimTabs current="sim" />
      <section className="fm-card fm-sim-live">
        <p className="fm-sim-live-kicker">{dirty ? '바꿜 조건 미리보기' : '지금 조건이면'}</p>
        <div className="fm-sim-live-row">
          <div><small>파이어 가능</small><b>{simulation.earliestRetirementAge ? `${simulation.earliestRetirementAge}세` : '아직'}</b></div>
          <div><small>자산 수명</small><b>{runwayText(simulation)}</b></div>
        </div>
        <p className="fm-sim-live-note">{dirty ? '바꿜 값은 미리보기예요 · 아래 버튼으로 저장 ↓' : (saved ? '✓ 내 결과·등수에 반영됐어요' : '아래 수치를 밀면 위 숫자가 바로 바뀌어요 (미리보기)')}</p>
      </section>
      <section className="fm-card fm-graph">
        <p className="fm-kicker">내 미래 자산 차트</p><h2>내가 넣은 돈, 이렇게 불어나요</h2>
        <div className="fm-chart-legend">
          <span><i className="fm-dot fm-dot-principal" />내가 넣은 돈 · {formatWon(principalAtRet)}</span>
          <span><i className="fm-dot fm-dot-gains" />불어난 돈 · {formatWon(gainsAtRet)}</span>
        </div>
        <AssetGrowthChart ages={growth.ages} principal={growth.principal} gains={growth.gains} retirementAge={draft.targetRetirementAge} depletionAge={simulation.targetResult.depletionAge} />
        <p className="fm-chart-note">파이어({draft.targetRetirementAge}세) 시점 기준 · 파란색은 내가 직접 넣은 돈, 주황색은 투자로 불어난 돈이에요. 파이어 후엔 쓰면서 줄어들어요.</p>
      </section>
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">조건 바꿔보기</p><h2>손가락으로 밀어서 바로 바꿔보세요</h2>
        <p>핵심 수치를 밀면 위 결과가 즉시 바뀌어요. 더 자세한 가정은 ‘고급 설정’에서.</p>
        <RangeControl label="현재 나이" value={draft.currentAge} inputKey="currentAge" type="age" step={1} onChange={(next) => editDraft('currentAge', next)} />
        <RangeControl label="파이어 나이" value={draft.targetRetirementAge} inputKey="targetRetirementAge" type="age" step={1} onChange={(next) => editDraft('targetRetirementAge', next)} />
        <RangeControl label="현재 금융자산" value={draft.financialAsset} inputKey="financialAsset" type="money" step={10000000} onChange={(next) => editDraft('financialAsset', next)} />
        <RangeControl label="월 저축액" value={draft.monthlyInvestment} inputKey="monthlyInvestment" type="money" step={100000} onChange={(next) => editDraft('monthlyInvestment', next)} />
        <RangeControl label="파이어 후 월 생활비" value={draft.monthlyLivingCost} inputKey="monthlyLivingCost" type="money" step={100000} onChange={(next) => editDraft('monthlyLivingCost', next)} />
        <button type="button" className="fm-advanced-toggle" onClick={() => setShowAdvanced((v) => !v)} aria-expanded={showAdvanced}>
          고급 설정 (저축 기간 · 연봉 상승 · 부업 · 물가) {showAdvanced ? '▴' : '▾'}
        </button>
        {showAdvanced && (
          <div className="fm-advanced">
            <RangeControl label="앞으로 저축하는 기간" value={savingYearsValue} inputKey="savingYears" type="years" step={1} maxOverride={yearsToRetire} onChange={(next) => editDraft('savingYears', next >= yearsToRetire ? 0 : next)} />
            <p className="fm-range-note">기본은 파이어까지({yearsToRetire}년) 매달 저축이에요. 줄이면 그만큼만 저축하고, 이후엔 모은 돈을 굴리기만 해요(코스트 파이어).</p>
            <RangeControl label="연봉 상승률(저축도 매년 증가)" value={draft.salaryGrowthRate} inputKey="salaryGrowthRate" type="percent" step={1} onChange={(next) => editDraft('salaryGrowthRate', next)} />
            <RangeControl label="파이어 후 부업 소득" value={draft.partTimeIncomeAfterRetirement} inputKey="partTimeIncomeAfterRetirement" type="money" step={100000} onChange={(next) => editDraft('partTimeIncomeAfterRetirement', next)} />
            <p className="fm-range-note">부업 소득은 물가에 연동되지 않아요 — 매년 오르지 않는 고정 수입으로 계산해요. ‘파이어 후 현금흐름’ 도구의 ‘배당 인출 소득’은 이와 <b>별도 칸</b>으로 합산되며 설정한 성장률만큼 매년 늘어요.</p>
            <RangeControl label="물가 상승률(생활비 매년 증가)" value={draft.inflationRate} inputKey="inflationRate" type="percent" step={1} onChange={(next) => editDraft('inflationRate', next)} />
            <p className="fm-range-note">이 비율만큼 <strong>생활비·국민연금·건보료·해외 체류비·임대수익</strong>이 매년 올라요. (부업 소득만 제외)</p>
          </div>
        )}
        <button type="button" className="fm-advanced-toggle" onClick={() => setShowAssets((v) => !v)} aria-expanded={showAssets}>
          부동산·부채·임대수익 {(showAssets || hasAssetExtra) ? '▴' : '▾'}
        </button>
        {(showAssets || hasAssetExtra) && (
          <div className="fm-advanced">
            <RangeControl label="부동산" value={reVal} inputKey="realEstateValue" type="money" step={1000000} onChange={(next) => editDraft('realEstateValue', next)} />
            <RangeControl label="부채" value={debtVal} inputKey="debt" type="money" step={1000000} onChange={(next) => editDraft('debt', next)} />
            <p className="fm-sim-networth" style={{ margin: '8px 0 0', padding: '10px 12px', borderRadius: '10px', background: 'rgba(30,40,89,0.06)', fontSize: '13px', color: '#1e2859', fontWeight: 700 }}>
              순자산 {formatWon(netWorth)} <span style={{ fontWeight: 500, color: 'var(--fm-muted, #6b6f76)' }}>(금융자산 + 부동산 − 부채)</span>
            </p>
            <p className="fm-range-note">부동산 <b>가치</b>와 부채는 <b>순자산·또래 비교</b>에만 반영돼요. 살고 있는 집은 매달 생활비를 못 만들어서 파이어 가능 나이엔 영향이 없어요.</p>
            <RangeControl label="파이어 후 월 임대수익" value={rentVal} inputKey="monthlyRentalIncome" type="money" step={100000} onChange={(next) => editDraft('monthlyRentalIncome', next)} />
            <p className="fm-range-note">월세·전세 등에서 <b>매달 들어오는 임대수익</b>이에요(세후 기준). 이 돈은 생활비를 직접 메워주므로 <b>파이어 가능 나이를 앞당겨요</b> — 위 ‘파이어 가능’ 숫자가 바뀝니다. 임대료는 물가 따라 매년 오른다고 가정해요.</p>
          </div>
        )}
      </section>
      <button type="button" className="fm-section-toggle" onClick={() => (onMove ? onMove('foreignTax') : (window.location.hash = '#foreignTax'))}>투자 세금(양도·배당)은 ‘세금 도구’에서 <small>결과·등수는 공정성 위해 세전 기준</small><i>›</i></button>
      <button type="button" className="fm-section-toggle" onClick={() => setShowPension((v) => !v)} aria-expanded={showPension}>국민연금 설정 <small>받는 나이·월 수령액</small><i>{showPension ? '▴' : '▾'}</i></button>
      {showPension && <PensionControls inputs={draft} onChange={editDraft} />}
      <button type="button" className="fm-section-toggle" onClick={() => setShowReturns((v) => !v)} aria-expanded={showReturns}>수익률 가정 비교 <small>예적금~공격투자</small><i>{showReturns ? '▴' : '▾'}</i></button>
      {showReturns && (
      <section className="fm-card fm-text-card">
        <p>현재 적용 수익률은 연 {draft.annualReturnRate}%예요. {activeScenario ? activeScenario.copy : '직접 입력한 수익률 가정으로 계산 중이에요.'} 아래에서 가정을 바꾸면 자산수명이 함께 바뀝니다.</p>
        <RangeControl label="연 수익률" value={draft.annualReturnRate} inputKey="annualReturnRate" type="percent" step={1} onChange={(next) => editDraft('annualReturnRate', next)} />
        <div className="fm-bench">
          {impacts.map((sc) => (
            <button type="button" className={`fm-bench-row2${sc.annualReturnRate === draft.annualReturnRate ? ' is-active' : ''}`} key={sc.key} onClick={() => editDraft('annualReturnRate', sc.annualReturnRate)}>
              <b>{sc.label}</b><span>연 {sc.annualReturnRate}%</span><em>자산수명 {sc.runway}</em>
            </button>
          ))}
        </div>
        <small>흔히 인용되는 장기 명목 평균 기준이에요(세전·물가 별도). 가정이 높을수록 기대수익도 변동성(위험)도 커지고, 과거 평균일 뿐 미래를 보장하지 않아요. 특정 상품 추천이 아닙니다. {sourceLine('returnPresets')}</small>
      </section>
      )}
      {dirty && (
        <div className="fm-sim-dock" role="region" aria-label="바꿔보기 저장">
          <span className="fm-sim-dock-note">저장 전엔 <b>미리보기</b>예요 · 내 결과·등수 미반영</span>
          <div className="fm-sim-dock-btns">
            <button type="button" className="fm-sim-reset" onClick={reset}>되돌리기</button>
            <button type="button" className="fm-sim-save" onClick={commit}>이 조건을 내 결과로 저장</button>
          </div>
        </div>
      )}
    </main>
  );
}
