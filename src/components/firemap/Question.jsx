// 질문 5 — F1 가드: 자산·저축·생활비가 0이면 '다음' 비활성 + '예시로 채우기'(30대 중앙값). 초기화 칩 제거.
import { useState } from 'react';
import { TopBar, ProgressBar, Card, SectionHead, RangeField, Fold, Button, Chip, Chips } from '../../ui/index.js';
import { questions } from '../../firemap-v2/data.js';
import { cleanNumber, formatValue, formatWon } from '../../firemap-v2/formatters.js';

const RANGES = { currentAge: [20, 70], targetRetirementAge: [30, 80], financialAsset: [0, 2000000000], monthlyInvestment: [0, 20000000], monthlyLivingCost: [500000, 20000000], realEstateValue: [0, 3000000000], debt: [0, 1000000000] };
const CHIPS = { financialAsset: [10000000, 100000000, 1000000000], monthlyInvestment: [100000, 500000, 1000000], monthlyLivingCost: [100000, 500000, 1000000], realEstateValue: [100000000, 500000000], debt: [10000000, 100000000] };
const EXAMPLE = { financialAsset: 150000000, monthlyInvestment: 1500000, monthlyLivingCost: 2500000 };
const REQUIRED = new Set(['financialAsset', 'monthlyInvestment', 'monthlyLivingCost']);

export default function Question({ step, inputs, onChange, onPrev, onNext }) {
  const q = questions[step];
  const value = cleanNumber(inputs[q.key]);
  const isAge = q.type === 'age';
  const isFinal = step === questions.length - 1;
  const isAsset = q.key === 'financialAsset';
  const [min, max] = RANGES[q.key] || [0, 100];
  const fmt = (v) => (isAge ? `${v}세` : formatValue(v, 'money', q.key));
  const blocked = REQUIRED.has(q.key) && value <= 0;
  const reVal = cleanNumber(inputs.realEstateValue); const debtVal = cleanNumber(inputs.debt);
  const [showExtra, setShowExtra] = useState(reVal > 0 || debtVal > 0);

  return (
    <main className="fm-screen fm-question-screen ds-screen-gap">
      <TopBar title={`질문 ${step + 1}/${questions.length}`} onBack={onPrev} />
      <ProgressBar value={step + 1} max={questions.length} thin />
      <Card padding="lg">
        <SectionHead kicker={q.label} title={q.title} desc={q.helper} />
        <RangeField label={q.label} value={value} min={min} max={max} step={isAge ? 1 : undefined} money={!isAge} format={fmt} chips={CHIPS[q.key] || []} required={REQUIRED.has(q.key)} onChange={(v) => onChange(q.key, v)} hint={isAge ? '1세 단위로 조절해요' : `${q.unit}로 조절해요 · 값을 탭하면 직접 입력`} />
        {blocked && (
          <Chips className="ds-mt-2">
            <Chip onClick={() => onChange(q.key, EXAMPLE[q.key])}>✨ 예시로 채우기 · {formatWon(EXAMPLE[q.key])}</Chip>
          </Chips>
        )}
        {isAsset && (
          <Fold title="부동산·부채 (선택)" hint="순자산·또래 비교에만 반영 · 파이어 나이엔 영향 없음" defaultOpen={showExtra} onOpen={() => setShowExtra(true)} className="ds-mt-3">
            <RangeField label="부동산" value={reVal} min={0} max={RANGES.realEstateValue[1]} money format={(v) => formatWon(v)} chips={CHIPS.realEstateValue} onChange={(v) => onChange('realEstateValue', v)} />
            <RangeField label="부채" value={debtVal} min={0} max={RANGES.debt[1]} money format={(v) => formatWon(v)} chips={CHIPS.debt} onChange={(v) => onChange('debt', v)} />
          </Fold>
        )}
      </Card>
      <div className="ds-bottomcta ds-bottomcta--fixed">
        <Button variant="secondary" size="lg" onClick={onPrev}>이전</Button>
        <Button variant="primary" size="lg" disabled={blocked} onClick={onNext}>{isFinal ? '결과 보기' : '다음'}</Button>
      </div>
    </main>
  );
}
