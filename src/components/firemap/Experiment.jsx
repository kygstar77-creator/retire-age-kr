// 바꿔보기 — 미리보기 샌드박스. 숫자 하나(StatHero) + 핵심 3개 + 접힘 5. 저장 전엔 내 결과·등수에 반영 안 됨.
import { useEffect, useMemo, useState } from 'react';
import { TopBar, StatHero, Card, SectionHead, RangeField, Fold, Chips, Chip, Badge, BottomCTA, Button, toast } from '../../ui/index.js';
import PensionControls from './PensionControls.jsx';
import AssetGrowthChart from './AssetGrowthChart.jsx';
import { investmentScenarios } from '../../firemap-v2/data.js';
import { sourceLine } from '../../firemap-v2/dataSources.js';
import { buildScenario, runwayText, buildGrowthSeries } from '../../firemap-v2/scenarios.js';
import { formatWon, cleanNumber } from '../../firemap-v2/formatters.js';
import '../../ui/screens/experiment.css';

const R = {
  currentAge: [20, 70], targetRetirementAge: [30, 80], financialAsset: [0, 2000000000], realEstateValue: [0, 3000000000], debt: [0, 1000000000],
  monthlyInvestment: [0, 20000000], monthlyLivingCost: [500000, 20000000], annualReturnRate: [0, 30], salaryGrowthRate: [0, 15], inflationRate: [0, 10],
  partTimeIncomeAfterRetirement: [0, 10000000], monthlyRentalIncome: [0, 10000000]
};
const C = {
  financialAsset: [10000000, 100000000, 1000000000], realEstateValue: [100000000, 500000000, 1000000000], debt: [10000000, 100000000],
  monthlyInvestment: [100000, 500000, 1000000], monthlyLivingCost: [100000, 500000, 1000000], partTimeIncomeAfterRetirement: [100000, 500000, 1000000], monthlyRentalIncome: [100000, 500000, 1000000]
};
const eok = (n) => formatWon(Math.round(n || 0));
const ageFmt = (v) => `${v}세`;
const pctFmt = (v) => `${v}%`;
const cx = (...a) => a.filter(Boolean).join(' ');

export default function Experiment({ inputs, onChange, onBack, onMove, draft: draftProp, setDraft: setDraftProp, base: baseProp, setBase: setBaseProp }) {
  // 바꿔보기는 '미리보기 샌드박스'. draft를 부모가 보관하면 그걸 써서 세금 도구 등 다른 화면을 다녀와도 유지되고, 없으면 로컬로 동작.
  const [localDraft, setLocalDraft] = useState(inputs);
  const draft = draftProp ?? localDraft;
  const setDraft = setDraftProp ?? setLocalDraft;
  const editDraft = (key, value) => setDraft((c) => ({ ...(c ?? inputs), [key]: cleanNumber(value) }));
  const [saved, setSaved] = useState(false);

  const simulation = useMemo(() => buildScenario(draft, {}), [draft]);
  const yearsToRetire = Math.max(1, draft.targetRetirementAge - draft.currentAge);
  const savingYearsValue = draft.savingYears > 0 ? Math.min(draft.savingYears, yearsToRetire) : yearsToRetire;
  const growth = useMemo(() => buildGrowthSeries(simulation), [simulation]);
  const retIdx = useMemo(() => growth.ages.indexOf(draft.targetRetirementAge), [growth, draft.targetRetirementAge]);
  const principalAtRet = retIdx >= 0 ? growth.principal[retIdx] : (growth.principal.at(-1) || 0);
  const gainsAtRet = retIdx >= 0 ? growth.gains[retIdx] : (growth.gains.at(-1) || 0);
  const activeScenario = investmentScenarios.find((scenario) => scenario.annualReturnRate === draft.annualReturnRate);
  const reVal = cleanNumber(draft.realEstateValue);
  const debtVal = cleanNumber(draft.debt);
  const rentVal = cleanNumber(draft.monthlyRentalIncome);
  const netWorth = simulation.netWorth;
  const hasAssetExtra = reVal > 0 || debtVal > 0 || rentVal > 0;
  const earliest = simulation.earliestRetirementAge;
  const need = Math.round(simulation.requiredFireAssetByFourPercent || 0);

  const PREVIEW_ONLY = ['investType', 'dividendYield'];
  // 샌드박스 슬라이더가 직접 바꾸는 핵심 값들. 이 값들이 (질문 재입력 등으로) 실제로 바뀐 경우에만 샌드박스를 새로 시드.
  // 세금·연금 도구가 '반영'으로 건드리는 값(investType·dividendIncomeMonthly·pensionClaimAge 등)은 여기 없으므로,
  // 도구를 다녀오거나 거기서 세금을 반영해도 바꿔보기 작업이 날아가지 않는다.
  const SANDBOX_KEYS = ['currentAge', 'targetRetirementAge', 'financialAsset', 'monthlyInvestment', 'monthlyLivingCost', 'savingYears', 'salaryGrowthRate', 'partTimeIncomeAfterRetirement', 'inflationRate', 'annualReturnRate'];
  const dirty = useMemo(() => Object.keys(draft).some((k) => !PREVIEW_ONLY.includes(k) && cleanNumber(draft[k]) !== cleanNumber(inputs[k])), [draft, inputs]);
  const commit = () => {
    Object.entries(draft).forEach(([k, v]) => { if (!PREVIEW_ONLY.includes(k)) onChange(k, v); });
    setSaved(true); setTimeout(() => setSaved(false), 2400);
    toast.good('내 결과에 반영했어요');
  };
  const reset = () => { setDraft({ ...inputs }); setBaseProp?.({ ...inputs }); setSaved(false); };

  // 다른 화면(세금 도구 등)을 다녀와도 샌드박스 유지.
  // 판정 기준은 draft가 아니라 base(시드 시점 inputs 스냅샷): 사용자의 draft 편집은 base를 안 바꾸므로 안 날아가고,
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

  const money = (key, label, hint) => (
    <RangeField label={label} value={cleanNumber(draft[key])} min={R[key][0]} max={R[key][1]} money format={eok} chips={C[key] || []} hint={hint} onChange={(v) => editDraft(key, v)} />
  );
  const heroSub = !earliest
    ? '아직 파이어 나이가 안 나와요 · 생활비를 낮춰보세요'
    : dirty ? '저장 전엔 미리보기예요 · 내 결과엔 아직 반영 안 됐어요'
      : saved ? '내 결과와 등수에 반영됐어요' : '아래 값을 밀면 위 숫자가 바로 바뀌어요';

  return (
    <main className={cx('fm-screen fm-scroll fm-has-tabbar ds-screen-gap', dirty && 'ds-has-fixedcta')}>
      <TopBar title="바꿔보기" onBack={onBack} actions={saved ? <Badge tone="good">저장됨</Badge> : null} />

      <StatHero
        tone="dark" size="title" className="sc-exp-hero"
        label={dirty ? '바꾸면 이렇게 돼요' : '지금 조건이면'}
        value={earliest ? `${earliest}` : '아직'} unit={earliest ? '세' : ''}
        sub={heroSub}
        tiles={[
          { label: '필요 자산', value: eok(need) },
          { label: '자산 수명', value: runwayText(simulation) },
          { label: '파이어 때 자산', value: simulation.retirementFinancialAsset ? eok(simulation.retirementFinancialAsset) : '—' }
        ]}
      />

      <Card>
        <SectionHead size="sm" kicker="핵심 3개" title="이 셋이 파이어 나이를 정해요" desc="값을 탭하면 직접 입력할 수 있어요" />
        {money('monthlyInvestment', '월 저축액')}
        {money('monthlyLivingCost', '파이어 후 월 생활비')}
        {money('partTimeIncomeAfterRetirement', '파이어 후 부업 소득', '물가와 상관없이 고정 수입으로 계산해요')}
      </Card>

      <Fold icon="🎂" title="나이·자산" hint={`${draft.currentAge}세 → ${draft.targetRetirementAge}세 · 지금 ${eok(draft.financialAsset)}`}>
        <RangeField label="현재 나이" value={cleanNumber(draft.currentAge)} min={R.currentAge[0]} max={R.currentAge[1]} step={1} format={ageFmt} onChange={(v) => editDraft('currentAge', v)} />
        <RangeField label="파이어 나이" value={cleanNumber(draft.targetRetirementAge)} min={R.targetRetirementAge[0]} max={R.targetRetirementAge[1]} step={1} format={ageFmt} onChange={(v) => editDraft('targetRetirementAge', v)} />
        {money('financialAsset', '현재 금융자산', '주식·예금·현금처럼 파이어 후 생활비로 쓸 수 있는 돈이에요')}
      </Fold>

      <Fold icon="⚙️" title="고급 가정" hint={`저축 ${savingYearsValue}년 · 연봉 ${draft.salaryGrowthRate}% · 물가 ${draft.inflationRate}% · 수익 ${draft.annualReturnRate}%`}>
        <RangeField label="저축 기간" value={savingYearsValue} min={1} max={yearsToRetire} step={1} format={(v) => `${v}년`} hint={`기본은 파이어까지 ${yearsToRetire}년 매달 저축이에요 · 줄이면 이후엔 모은 돈을 굴리기만 해요`} onChange={(v) => editDraft('savingYears', v >= yearsToRetire ? 0 : v)} />
        <RangeField label="연봉 상승률" value={cleanNumber(draft.salaryGrowthRate)} min={R.salaryGrowthRate[0]} max={R.salaryGrowthRate[1]} step={1} format={pctFmt} hint="저축액도 매년 이만큼 늘어요" onChange={(v) => editDraft('salaryGrowthRate', v)} />
        <RangeField label="물가 상승률" value={cleanNumber(draft.inflationRate)} min={R.inflationRate[0]} max={R.inflationRate[1]} step={1} format={pctFmt} hint="생활비·연금·건보료·임대수익이 매년 이만큼 올라요" onChange={(v) => editDraft('inflationRate', v)} />
        <RangeField label="연 수익률" value={cleanNumber(draft.annualReturnRate)} min={R.annualReturnRate[0]} max={R.annualReturnRate[1]} step={1} format={pctFmt} onChange={(v) => editDraft('annualReturnRate', v)} />
        <Chips className="ds-mt-2">
          {investmentScenarios.map((sc) => (
            <Chip key={sc.key} on={sc.annualReturnRate === draft.annualReturnRate} onClick={() => editDraft('annualReturnRate', sc.annualReturnRate)}>{sc.label} {sc.annualReturnRate}%</Chip>
          ))}
        </Chips>
        <p className="ds-caption ds-mt-2">{activeScenario ? activeScenario.copy : '직접 넣은 수익률로 계산해요'} · 과거 평균일 뿐 미래를 보장하지 않아요 · {sourceLine('returnPresets')}</p>
        <Button variant="ghost" size="sm" className="ds-mt-2" onClick={() => (onMove ? onMove('foreignTax') : (window.location.hash = '#foreignTax'))}>양도·배당세는 세금 도구에서 →</Button>
      </Fold>

      <Fold icon="🏠" title="부동산·부채·임대수익" hint={hasAssetExtra ? `순자산 ${eok(netWorth)}` : '순자산·또래 비교에만 반영'} defaultOpen={hasAssetExtra}>
        {money('realEstateValue', '부동산')}
        {money('debt', '부채')}
        <p className="ds-caption">순자산 <b className="num">{eok(netWorth)}</b> · 부동산과 부채는 순자산·또래 비교에만 반영돼요</p>
        {money('monthlyRentalIncome', '파이어 후 월 임대수익', '세후 기준이에요 · 생활비를 메워 파이어 나이를 앞당겨요')}
      </Fold>

      <Fold icon="🏛️" title="국민연금" hint="받는 나이 · 월 수령액">
        <PensionControls inputs={draft} onChange={editDraft} />
      </Fold>

      <Fold icon="📈" title="자산 흐름" hint={`넣은 돈 ${eok(principalAtRet)} · 불어난 돈 ${eok(gainsAtRet)}`}>
        <AssetGrowthChart ages={growth.ages} principal={growth.principal} gains={growth.gains} retirementAge={draft.targetRetirementAge} depletionAge={simulation.targetResult.depletionAge} />
        <p className="ds-caption ds-mt-2">파이어 <b className="num">{draft.targetRetirementAge}세</b> 기준 · 넣은 돈 <b className="num">{eok(principalAtRet)}</b> · 불어난 돈 <b className="num">{eok(gainsAtRet)}</b> · 파이어 후엔 쓰면서 줄어요</p>
      </Fold>

      <p className="ds-caption ds-textcenter">참고용 계산이에요 · 투자 자문이 아니에요</p>

      {dirty && <BottomCTA fixed className="sc-exp-cta" secondary={{ label: '되돌리기', onClick: reset }} primary={{ label: '이 조건을 내 결과로 저장', onClick: commit }} />}
    </main>
  );
}
