import { useState } from 'react';
import { cleanNumber, formatValue, formatWon } from '../../firemap-v2/formatters.js';

const ranges = {
  currentAge: [20, 70],
  targetRetirementAge: [30, 80],
  financialAsset: [0, 5000000000],
  monthlyInvestment: [0, 20000000],
  monthlyLivingCost: [500000, 20000000],
  annualReturnRate: [0, 30],
  salaryGrowthRate: [0, 15],
  expectedPensionAge: [55, 75],
  expectedMonthlyPension: [0, 5000000],
  improvedCost: [500000, 20000000],
  partTimeIncomeAfterRetirement: [0, 10000000]
};

// 돈 필드별 빠른 가산 칩 (타이핑 최소화, 상한 없음)
const chipSets = {
  financialAsset: [10000000, 100000000, 1000000000],
  monthlyInvestment: [100000, 500000, 1000000],
  monthlyLivingCost: [100000, 500000, 1000000],
  improvedCost: [100000, 500000, 1000000],
  expectedMonthlyPension: [100000, 500000, 1000000],
  partTimeIncomeAfterRetirement: [100000, 500000, 1000000]
};

function display(key, value, type = 'money') {
  if (key === 'annualReturnRate' || key === 'salaryGrowthRate') return `${value}%`;
  if (key === 'expectedPensionAge' || key === 'targetRetirementAge' || key === 'currentAge') return `${value}세`;
  if (key === 'improvedCost') return formatWon(value);
  return formatValue(value, type, key);
}

function chipLabel(amount) {
  if (amount >= 100000000) return `+${amount / 100000000}억`;
  return `+${amount / 10000}만`;
}

export default function RangeControl({ label, value, onChange, step = 1, type = 'money', inputKey }) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState('');
  const numeric = cleanNumber(value);
  const [min, max] = ranges[inputKey] || [0, Math.max(numeric * 2, step * 10)];
  const isMoney = type === 'money';
  const upperClamp = isMoney ? Infinity : max; // 돈은 직접 입력 시 상한 제거
  const stored = Math.max(min, Math.min(upperClamp, numeric)); // 표시용 실제 값(돈은 상한 없음)
  const sliderValue = Math.max(min, Math.min(max, numeric)); // 슬라이더 썸 위치(범위 내)
  const percent = max > min ? ((sliderValue - min) / (max - min)) * 100 : 0;
  const overMax = isMoney && numeric > max;
  const chips = chipSets[inputKey] || [];

  const openDirectEdit = () => { setDraft(String(Math.round(stored))); setEditing(true); };
  const confirmDirectEdit = () => {
    onChange(Math.max(min, Math.min(upperClamp, cleanNumber(draft))));
    setEditing(false);
  };
  const addChip = (amount) => onChange(Math.max(min, Math.min(upperClamp, numeric + amount)));

  return (
    <>
      <div className="fm-range-control">
        <div className="fm-range-head">
          <span>{label}</span>
          <button type="button" className="fm-range-value" onClick={openDirectEdit} aria-label={`${label} 직접 입력`}>
            {display(inputKey, stored, type)}
            <small className="fm-range-edit-hint">탭해서 입력</small>
          </button>
        </div>
        <input
          aria-label={label}
          type="range"
          min={min}
          max={max}
          step={step}
          value={sliderValue}
          onChange={(event) => onChange(cleanNumber(event.target.value))}
          style={{ '--value': `${percent}%` }}
        />
        <div className="fm-range-scale">
          <span>{display(inputKey, min, type)}</span>
          <span>{overMax ? '직접 입력 값' : display(inputKey, max, type)}</span>
        </div>
        {chips.length > 0 && (
          <div className="fm-range-chips" aria-label={`${label} 빠른 입력`}>
            {chips.map((amount) => (
              <button type="button" key={amount} onClick={() => addChip(amount)}>{chipLabel(amount)}</button>
            ))}
            <button type="button" className="fm-chip-reset" onClick={() => onChange(min)}>초기화</button>
          </div>
        )}
      </div>
      {editing && (
        <div className="fm-input-overlay" role="dialog" aria-modal="true" aria-label={`${label} 직접 입력`}>
          <div className="fm-input-sheet">
            <em>{label}</em>
            <h2>숫자로 직접 입력</h2>
            <p>{isMoney ? '슬라이더 최댓값보다 큰 금액도 입력할 수 있어요.' : '슬라이더가 불편하면 숫자만 입력해도 돼요.'}</p>
            <input
              autoFocus
              inputMode="numeric"
              pattern="[0-9]*"
              value={draft}
              onChange={(event) => setDraft(event.target.value.replace(/[^0-9]/g, ''))}
              onKeyDown={(event) => {
                if (event.key === 'Enter') confirmDirectEdit();
                if (event.key === 'Escape') setEditing(false);
              }}
            />
            <div className="fm-input-actions">
              <button type="button" onClick={() => setEditing(false)}>취소</button>
              <button type="button" onClick={confirmDirectEdit}>확인</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
