// 해외 체류 모듈 — City.jsx(도달 불가 화면)에서 분리. 지역 탐색(CityExplorer) 해외 탭에서만 쓴다.
// 적용은 미리보기 샌드박스(experiment)로만 — 저장 입력을 직접 바꾸지 않는다(즉시 저장 버그 수정).
import { useState } from 'react';
import { formatWon } from '../../firemap-v2/formatters.js';
import { buildScenario, deltaText, runwayText } from '../../firemap-v2/scenarios.js';
import { getFx } from '../../firemap-v2/market.js';
import { Card, SectionHead, Button, Chip, Chips, Notice } from '../../ui/index.js';

function Stepper({ label, unit, value, set, step, min = 0, max = Infinity }) {
  return (
    <div className="ds-range" style={{ padding: '8px 0' }}>
      <div className="ds-range__head">
        <span className="ds-range__label">{label}</span>
        <span className="ds-row">
          <button type="button" className="ds-iconbtn ds-iconbtn--sm" aria-label="감소" onClick={() => set(Math.max(min, value - step))}>−</button>
          <input className="ds-input num" style={{ width: 96, textAlign: 'center', padding: '6px 4px' }} inputMode="numeric" value={value} onChange={(e) => set(Math.min(max, Math.max(min, Number(e.target.value.replace(/[^0-9]/g, '')) || 0)))} aria-label={label} />
          <button type="button" className="ds-iconbtn ds-iconbtn--sm" aria-label="증가" onClick={() => set(Math.min(max, value + step))}>+</button>
          <span className="ds-caption">{unit}</span>
        </span>
      </div>
    </div>
  );
}

export function OverseasStayModule({ inputs, simulation, onPreviewPatch }) {
  const [months, setMonths] = useState(3);
  const [localCost, setLocalCost] = useState(65000);
  const [fx, setFx] = useState(() => getFx('THB'));
  const [pause, setPause] = useState(true);
  const patch = { overseasStayEnabled: 1, overseasMonthsPerYear: months, overseasContinuousDays: months >= 3 ? 95 : 0, overseasMonthlyCostLocal: localCost, overseasExchangeRate: fx, overseasInsurancePauseEnabled: pause ? 1 : 0, overseasApplyYears: 10 };
  const scenario = buildScenario(inputs, patch);
  return (
    <Card>
      <SectionHead size="sm" kicker="해외 체류" title="체류 조건을 바꿔 자산수명 보기" desc="연 체류 개월·현지 생활비·환율을 조절해요. 90일 이상 연속 체류면 건보료 정지 가정을 켤 수 있어요." />
      <Stepper label="연 체류 개월" unit="개월" value={months} set={setMonths} step={1} min={0} max={12} />
      <Stepper label="현지 월 생활비" unit="현지통화" value={localCost} set={setLocalCost} step={5000} />
      <Stepper label="환율(현지통화당 원)" unit="원" value={fx} set={setFx} step={1} />
      <Chips className="ds-mt-2"><Chip on={pause} onClick={() => setPause(!pause)}>건보료 정지 가정</Chip></Chips>
      <Notice tone="good" className="ds-mt-3">이 조건이면 <b>{runwayText(scenario)}</b>까지 — {deltaText(simulation, scenario)} · 첫해 절감 약 {formatWon(scenario.firstYearOverseasSavings)}</Notice>
      <Button variant="tint" size="md" full className="ds-mt-3" onClick={() => onPreviewPatch && onPreviewPatch(patch)}>이 조건 미리보기(바꿔보기)</Button>
      <p className="ds-caption ds-mt-2" style={{ marginBottom: 0 }}>참고용 시나리오예요. 실제 비자·건보료 면제 요건은 제도 확인이 필요해요.</p>
    </Card>
  );
}
