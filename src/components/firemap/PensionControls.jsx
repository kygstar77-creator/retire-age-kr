import { cleanNumber, formatWon } from '../../firemap-v2/formatters.js';

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

export default function PensionControls({ inputs, onChange }) {
  const age = cleanNumber(inputs.expectedPensionAge || 65);
  const monthly = cleanNumber(inputs.expectedMonthlyPension || 0);
  return (
    <section className="fm-card fm-text-card fm-pension-card">
      <p className="fm-kicker">국민연금</p>
      <h2>국민연금 조건도 같이 바꿔보세요</h2>
      <p>선택한 시작 나이부터 매월 예상 연금만큼 생활비에서 차감해 계산해요.</p>
      <div className="fm-adjust">
        <span>연금 시작 나이</span>
        <strong>{age}세</strong>
        <button type="button" onClick={() => onChange('expectedPensionAge', clamp(age - 1, 55, 75))}>-</button>
        <button type="button" onClick={() => onChange('expectedPensionAge', clamp(age + 1, 55, 75))}>+</button>
      </div>
      <div className="fm-adjust">
        <span>예상 월 연금</span>
        <strong>{formatWon(monthly)}</strong>
        <button type="button" onClick={() => onChange('expectedMonthlyPension', Math.max(0, monthly - 100000))}>-</button>
        <button type="button" onClick={() => onChange('expectedMonthlyPension', monthly + 100000)}>+</button>
      </div>
    </section>
  );
}
