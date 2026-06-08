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

export default function RangeControl({ label, value, onChange, step = 1, type = 'money', inputKey }) {
  const numeric = cleanNumber(value);
  const [min, max] = ranges[inputKey] || [0, Math.max(numeric * 2, step * 10)];
  const clamped = Math.max(min, Math.min(max, numeric));
  const percent = max > min ? ((clamped - min) / (max - min)) * 100 : 0;
  const minText = display(inputKey, min, type);
  const maxText = display(inputKey, max, type);

  return (
    <div className="fm-range-control">
      <div className="fm-range-head">
        <span>{label}</span>
        <strong>{display(inputKey, clamped, type)}</strong>
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
  );
}
