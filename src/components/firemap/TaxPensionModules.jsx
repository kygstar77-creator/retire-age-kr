// 세금·연금 도구 3개 — 결론(StatHero md) 위, 입력(RangeField) 아래, 반영 버튼 하나. TopBar는 FireMapMVP 도구 래퍼가 그려요.
import { useState } from 'react';
import { Card, SectionHead, RangeField, StatHero, Button, Notice, toast } from '../../ui/index.js';
import { calculateInvestmentTaxes } from '../../utils/taxCalculator.js';
import { earlyClaim } from '../../firemap-v2/pension.js';
import { formatWon } from '../../firemap-v2/formatters.js';

const eok = (n) => formatWon(Math.round(n || 0));

export function ForeignStockTaxCard({ inputs, onApply }) {
  const [gain, setGain] = useState(50000000);
  const { foreignStockTax: t } = calculateInvestmentTaxes({ foreignStockGain: gain });
  const cur = Number(inputs?.investType) || 0;
  const hasCG = cur === 1 || cur === 3;
  const hasDiv = cur === 2 || cur === 3;
  const next = hasCG ? (hasDiv ? 2 : 0) : (hasDiv ? 3 : 1);
  return (
    <>
      <StatHero
        tone="light" size="md"
        label="해외주식 양도세 · 1년에"
        value={eok(t.tax)}
        sub={<>세후 <b className="num">{eok(t.afterTaxGain)}</b> 남아요 · 실효 <b className="num">{Math.round(t.effectiveTaxRate)}%</b></>}
        tiles={[
          { label: '매도 차익', value: eok(t.gain) },
          { label: '과세표준', value: eok(t.taxableGain) },
          { label: '실효세율', value: `${Math.round(t.effectiveTaxRate)}%` }
        ]}
      />
      <Card>
        <SectionHead size="sm" kicker="해외주식 양도세" title="1년에 얼마나 팔아요?" desc="250만원 공제 후 22% · 3억 넘는 부분은 27.5%" />
        <RangeField label="연 매도 차익" value={gain} min={0} max={300000000} step={1000000} money format={eok} chips={[10000000, 50000000, 100000000]} onChange={setGain} hint="손실과 이익을 합친 금액이에요" />
        {onApply && (hasCG
          ? <Button variant="secondary" size="md" full className="ds-mt-2" onClick={() => { onApply({ investType: next }); toast('해외 양도세 반영을 해제했어요'); }}>✓ 반영 중 · 해외 양도세 · 해제</Button>
          : <Button variant="primary" size="md" full className="ds-mt-2" onClick={() => { onApply({ investType: next }); toast.good('해외 양도세를 반영했어요'); }}>해외 양도세 반영</Button>)}
        {onApply && <p className="ds-caption ds-mt-2 ds-mb-0">배당세와 같이 켤 수 있어요 · 참고용 계산이에요 · 투자 자문이 아니에요</p>}
      </Card>
    </>
  );
}

export function DividendCard({ inputs, onApply }) {
  const [annual, setAnnual] = useState(15000000);
  const { dividendTax: d } = calculateInvestmentTaxes({ annualDividendIncome: annual });
  const over2000 = annual > 20000000;
  const over1000 = annual > 10000000;
  const cur = Number(inputs?.investType) || 0;
  const hasCG = cur === 1 || cur === 3;
  const hasDiv = cur === 2 || cur === 3;
  const next = hasDiv ? (hasCG ? 1 : 0) : (hasCG ? 3 : 2);
  return (
    <>
      <StatHero
        tone="light" size="md"
        label="세후 월 배당"
        value={eok(d.monthlyAfterTaxDividend)}
        sub={over2000 ? '2,000만원을 넘어 종합과세 대상이에요' : over1000 ? '1,000만원을 넘어 건보료에 잡혀요' : '건보료·종합과세 경고선 아래예요'}
        tiles={[
          { label: '연 배당 · 세전', value: eok(d.grossDividend) },
          { label: '원천징수 15.4%', value: eok(d.withholdingTax) },
          { label: '연 배당 · 세후', value: eok(d.afterTaxDividend) }
        ]}
      />
      <Card>
        <SectionHead size="sm" kicker="배당 소득" title="1년에 배당을 얼마 받아요?" desc="이자와 배당을 합친 금융소득 기준이에요" />
        <RangeField label="연 배당소득" value={annual} min={0} max={50000000} step={1000000} money format={eok} chips={[1000000, 5000000, 10000000]} onChange={setAnnual} />
        {over2000 && <Notice tone="warn" icon="⚠️" className="ds-mt-2">연 배당 <b className="num">{eok(annual)}</b> · 2,000만원을 넘으면 종합과세 대상이에요</Notice>}
        {!over2000 && over1000 && <Notice tone="warn" icon="🩺" className="ds-mt-2">연 배당 <b className="num">{eok(annual)}</b> · 1,000만원을 넘으면 건보료에 잡혀요</Notice>}
        {onApply && (hasDiv
          ? <Button variant="secondary" size="md" full className="ds-mt-2" onClick={() => { onApply({ investType: next }); toast('배당세 반영을 해제했어요'); }}>✓ 반영 중 · 배당세 · 해제</Button>
          : <Button variant="primary" size="md" full className="ds-mt-2" onClick={() => { onApply({ investType: next, dividendIncomeMonthly: 0 }); toast.good('배당세를 반영했어요'); }}>배당세 15.4% 반영</Button>)}
        {onApply && <p className="ds-caption ds-mt-2 ds-mb-0">양도세와 같이 켤 수 있어요 · 배당으로 파이어의 배당 소득과는 한쪽만 켜져요</p>}
        <p className="ds-caption ds-mt-2 ds-mb-0">참고용 계산이에요 · 투자 자문이 아니에요</p>
      </Card>
    </>
  );
}

export function PensionEarlyClaimCard({ inputs, onApply }) {
  const normalAge = Number(inputs.expectedPensionAge) || 65;
  const normalMonthly = Number(inputs.expectedMonthlyPension) || 0;
  const appliedClaim = Number(inputs.pensionClaimAge) || 0;
  const [claimAge, setClaimAge] = useState(appliedClaim > 0 ? appliedClaim : normalAge);
  const r = earlyClaim(normalMonthly, normalAge, claimAge);
  const applied = appliedClaim > 0 ? earlyClaim(normalMonthly, normalAge, appliedClaim) : null;
  return (
    <>
      <StatHero
        tone="light" size="md"
        label={<><b className="num">{claimAge}세</b>부터 받으면 월</>}
        value={eok(r.monthly)}
        sub={r.yearsEarly > 0 ? <><b className="num">{r.yearsEarly}년</b> 일찍 · <b className="num">{r.reductionPct}%</b> 줄어 평생 이어져요</> : <>정상 수령 <b className="num">{normalAge}세</b> 기준이에요</>}
        tiles={[
          { label: '정상 월 연금', value: eok(normalMonthly) },
          { label: '줄어드는 비율', value: `${r.reductionPct}%` },
          { label: '월 차이', value: eok(normalMonthly - r.monthly) }
        ]}
      />
      <Card>
        <SectionHead size="sm" kicker="국민연금" title="몇 살부터 받을까요?" desc="1년 당길 때마다 6%씩 · 최대 5년 30% 줄어요" />
        <RangeField label="받기 시작 나이" value={claimAge} min={Math.max(55, normalAge - 5)} max={normalAge} step={1} format={(v) => `${Math.round(v)}세`} onChange={(v) => setClaimAge(Math.round(v))} />
        {normalMonthly <= 0 && <Notice tone="warn" icon="💬" className="ds-mt-2">정상 월 연금이 0이에요 · 바꿔보기에서 국민연금을 먼저 넣어요</Notice>}
        {normalMonthly > 0 && (applied
          ? <Button variant="secondary" size="md" full className="ds-mt-2" onClick={() => { onApply({ pensionClaimAge: 0 }); toast('정상 수령으로 되돌렸어요'); }}>✓ 반영 중 · {appliedClaim}세 · {applied.reductionPct}% 감액 · 되돌리기</Button>
          : (claimAge < normalAge
            ? <Button variant="primary" size="md" full className="ds-mt-2" onClick={() => { onApply({ pensionClaimAge: claimAge }); toast.good(`${claimAge}세 조기수령을 반영했어요`); }}>{claimAge}세 조기수령 반영</Button>
            : <Button variant="primary" size="md" full className="ds-mt-2" disabled>나이를 {normalAge}세보다 낮추면 반영할 수 있어요</Button>))}
        <p className="ds-caption ds-mt-2 ds-mb-0">정상 나이·월액은 질문이나 바꿔보기에서 정해요 · 여기선 시작 나이만 바꿔요</p>
      </Card>
    </>
  );
}
