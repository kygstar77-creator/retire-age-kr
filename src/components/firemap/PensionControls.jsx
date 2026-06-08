import { cleanNumber } from '../../firemap-v2/formatters.js';
import RangeControl from './RangeControl.jsx';

export default function PensionControls({ inputs, onChange }) {
  const age = cleanNumber(inputs.expectedPensionAge || 65);
  const monthly = cleanNumber(inputs.expectedMonthlyPension || 0);
  return (
    <section className="fm-card fm-text-card fm-pension-card">
      <p className="fm-kicker">국민연금</p>
      <h2>국민연금 조건도 같이 바꿔보세요</h2>
      <p>선택한 시작 나이부터 매월 예상 연금만큼 생활비에서 차감해 계산해요.</p>
      <RangeControl label="연금 시작 나이" value={age} inputKey="expectedPensionAge" type="age" step={1} onChange={(next) => onChange('expectedPensionAge', next)} />
      <RangeControl label="예상 월 연금" value={monthly} inputKey="expectedMonthlyPension" type="money" step={100000} onChange={(next) => onChange('expectedMonthlyPension', next)} />
    </section>
  );
}
