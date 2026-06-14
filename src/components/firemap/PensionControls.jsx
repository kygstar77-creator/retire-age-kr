import { cleanNumber, formatWon } from '../../firemap-v2/formatters.js';
import { earlyClaim } from '../../firemap-v2/pension.js';
import RangeControl from './RangeControl.jsx';

export default function PensionControls({ inputs, onChange }) {
  const normalAge = cleanNumber(inputs.expectedPensionAge || 65);
  const monthly = cleanNumber(inputs.expectedMonthlyPension || 0);
  const claim = cleanNumber(inputs.pensionClaimAge) > 0 ? cleanNumber(inputs.pensionClaimAge) : normalAge;
  const eff = earlyClaim(monthly, normalAge, claim);
  return (
    <section className="fm-card fm-text-card fm-pension-card">
      <p className="fm-kicker">국민연금</p>
      <h2>국민연금 조건도 같이 바꿔보세요</h2>
      <p>받기 시작 나이를 정상보다 일찍 당기면 자동으로 감액해 계산해요. (조기수령 도구와 같은 값)</p>
      <RangeControl label="연금 받기 시작 나이" value={claim} inputKey="pensionClaimAge" type="age" step={1} onChange={(next) => onChange('pensionClaimAge', next === normalAge ? 0 : next)} />
      <RangeControl label="정상 월 연금 (정상 나이 기준)" value={monthly} inputKey="expectedMonthlyPension" type="money" step={100000} onChange={(next) => onChange('expectedMonthlyPension', next)} />
      {claim < normalAge
        ? <p className="fm-range-note">조기수령 {claim}세 → <b>{eff.reductionPct}% 감액</b>돼 실제 월 약 {formatWon(eff.monthly)} 적용 (정상 {normalAge}세 기준).</p>
        : claim > normalAge
          ? <p className="fm-range-note">{claim}세부터 수령 — 월 연금은 동일하게 계산해요 (연기 증액은 미반영).</p>
          : <p className="fm-range-note">정상 수령({normalAge}세) 기준이에요. 시작 나이를 당기면 자동 감액돼요.</p>}
    </section>
  );
}
