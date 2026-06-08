import { useState } from 'react';
import { cleanNumber, formatValue, formatWon } from '../../firemap-v2/formatters.js';

const ranges = {
  currentAge: [20, 70],
  targetRetirementAge: [30, 80],
  financialAsset: [0, 5000000000],
  monthlyInvestment: [0, 20000000],
  monthlyLivingCost: [500000, 20000000],
  annualReturnRate: [0, 30],
  expectedPensionAge: [55, 75],
  expectedMonthlyPension: [0, 5000000],
  improvedCost: [500000, 20000000],
  partTimeIncomeAfterRetirement: [0, 10000000]
};

function display(key, value, type = 'money') {
  if (key === 'annualReturnRate') return `${value}%`;
  if (key === 'expectedPensionAge' || key === 'targetRetirementAge' || key === 'currentAge') return `${value}세`;
  if (key === 'improvedCost') return formatWon(value);
  return formatValue(value, type, key);
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, cleanNumber(value)));
}

export default function RangeControl({ label, value, onChange, step = 1, type = 'money', inputKey }) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState('');
  const numeric = cleanNumber(value);
  const [min, max] = ranges[inputKey] || [0, Math.max(numeric * 2, step * 10)];
  const clamped = clamp(numeric, min, max);
  const percent = max > min ? ((clamped - min) / (max - min)) * 100 : 0;
  const minText = display(inputKey, min, type);
  const maxText = display(inputKey, max, type);

  const openDirectEdit = () => {
    setDraft(String(clamped));
    setEditing(true);
  };

  const confirmDirectEdit = () => {
    onChange(clamp(draft, min, max));
    setEditing(false);
  };

  return (
    <>
      <div className="fm-range-control">
        <div className="fm-range-head">
          <span>{label}</span>
          <button type="button" className="fm-range-value" onClick={openDirectEdit} aria-label={`${label} 직접 입력`}>
            {display(inputKey, clamped, type)}
          </button>
        </div>
        <input
          aria-label={label}
          type="range"
          min={min}
          max={max}
          step={step}
          value={clamped}
          onChange={(event) => onChange(cleanNumber(event.target.value))}
          style={{ '--value': `${percent}%` }}
        />
        <div className="fm-range-scale"><span>{minText}</span><span>{maxText}</span></div>
      </div>
      {editing && (
        <div className="fm-input-overlay" role="dialog" aria-modal="true" aria-label={`${label} 직접 입력`}>
          <div className="fm-input-sheet">
            <em>{label}</em>
            <h2>숫자로 직접 입력</h2>
            <p>슬라이더가 불편하면 숫자만 입력해도 돼요. 범위를 넘으면 자동으로 맞춰요.</p>
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
