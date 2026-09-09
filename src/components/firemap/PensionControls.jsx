// 국민연금 조건 — 받기 시작 나이·정상 월 연금. 조기수령 도구(PensionEarlyClaimCard)와 같은 값을 써요.
import { Card, SectionHead, RangeField } from '../../ui/index.js';
import { cleanNumber, formatWon } from '../../firemap-v2/formatters.js';
import { earlyClaim } from '../../firemap-v2/pension.js';

const eok = (n) => formatWon(Math.round(n || 0));

export default function PensionControls({ inputs, onChange }) {
  const normalAge = cleanNumber(inputs.expectedPensionAge || 65);
  const monthly = cleanNumber(inputs.expectedMonthlyPension || 0);
  const claim = cleanNumber(inputs.pensionClaimAge) > 0 ? cleanNumber(inputs.pensionClaimAge) : normalAge;
  const eff = earlyClaim(monthly, normalAge, claim);
  const hint = claim < normalAge
    ? <>조기수령 <b className="num">{claim}세</b> · <b className="num">{eff.reductionPct}%</b> 줄어 월 <b className="num">{eok(eff.monthly)}</b>로 계산해요</>
    : claim > normalAge
      ? <><b className="num">{claim}세</b>부터 받아요 · 늦게 받는 가산은 아직 안 넣어요</>
      : <>정상 수령 <b className="num">{normalAge}세</b> 기준이에요 · 당기면 자동으로 줄어요</>;
  return (
    <Card>
      <SectionHead size="sm" kicker="국민연금" title="국민연금 조건도 같이 바꿔요" desc="정상보다 일찍 받으면 1년에 6%씩 평생 줄어요" />
      <RangeField label="받기 시작 나이" value={claim} min={Math.max(55, normalAge - 5)} max={Math.min(75, normalAge + 5)} step={1} format={(v) => `${Math.round(v)}세`} onChange={(next) => onChange('pensionClaimAge', Math.round(next) === normalAge ? 0 : Math.round(next))} />
      <RangeField label="정상 월 연금" value={monthly} min={0} max={5000000} step={100000} money format={eok} chips={[100000, 500000, 1000000]} onChange={(next) => onChange('expectedMonthlyPension', next)} />
      <p className="ds-caption ds-mt-2 ds-mb-0">{hint}</p>
    </Card>
  );
}
