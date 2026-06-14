import { useState } from 'react';
import { calculateInvestmentTaxes } from '../../utils/taxCalculator.js';
import { earlyClaim } from '../../firemap-v2/pension.js';
import { formatWon } from '../../firemap-v2/formatters.js';

function Stepper({ label, unit, value, set, step }) {
  return (
    <label className="fm-dc-field">
      <span>{label}</span>
      <span className="fm-dc-input">
        <button type="button" onClick={() => set(Math.max(0, value - step))} aria-label="감소">−</button>
        <input inputMode="numeric" value={value} onChange={(e) => set(Math.max(0, Number(e.target.value.replace(/[^0-9]/g, '')) || 0))} />
        <button type="button" onClick={() => set(value + step)} aria-label="증가">+</button>
        <em>{unit}</em>
      </span>
    </label>
  );
}

export function ForeignStockTaxCard({ inputs, onApply }) {
  const [gainManwon, setGain] = useState(5000);
  const { foreignStockTax: t } = calculateInvestmentTaxes({ foreignStockGain: gainManwon * 10000 });
  return (
    <section className="fm-card fm-text-card fm-advanced-section">
      <p className="fm-kicker">해외주식 양도세</p>
      <h2>분할 매도 시 세금</h2>
      <Stepper label="연 매도차익(손익통산)" unit="만원" value={gainManwon} set={setGain} step={500} />
      <div className="fm-dc-result ok">
        <small>250만원 기본공제 후 22%, 과표 3억 초과분 27.5%</small>
        <ul>
          <li>과세표준 {formatWon(t.taxableGain)}</li>
          <li>양도소득세 약 {formatWon(t.tax)} (실효 {t.effectiveTaxRate.toFixed(1)}%)</li>
          <li>세후 실현액 {formatWon(t.afterTaxGain)}</li>
        </ul>
      </div>
      <small>과거·가정 기반 참고 계산이며 특정 종목 추천이 아닙니다.</small>
      {onApply && (Number(inputs?.investType) === 1
        ? <button type="button" className="fm-dc-apply on" onClick={() => onApply({ investType: 0 })}>✓ 결과에 반영됨 (해외 양도세) · 해제</button>
        : <button type="button" className="fm-dc-apply" onClick={() => onApply({ investType: 1 })}>이 세금(해외 양도세)을 결과에 반영하기</button>)}
      {onApply && <small className="fm-dc-applynote">투자 유형은 하나만 반영돼요 — 국내(면제)·해외 양도세·배당세 중 택1.</small>}
    </section>
  );
}

export function DividendCard({ inputs, onApply }) {
  const [annualManwon, setAnnual] = useState(1500);
  const annual = annualManwon * 10000;
  const { dividendTax: d } = calculateInvestmentTaxes({ annualDividendIncome: annual });
  const over2000 = annualManwon > 2000;
  const over1000 = annualManwon > 1000;
  return (
    <section className="fm-card fm-text-card fm-advanced-section">
      <p className="fm-kicker">배당 소득</p>
      <h2>배당 생활 시 세금·건보료 경고</h2>
      <Stepper label="연 배당소득" unit="만원" value={annualManwon} set={setAnnual} step={100} />
      <div className={`fm-dc-result ${over2000 || over1000 ? 'no' : 'ok'}`}>
        <ul>
          <li>원천징수 15.4% 후 월 배당 약 {formatWon(d.monthlyAfterTaxDividend)}</li>
          {over1000 && <li>금융소득 1,000만원 초과 → 지역가입 시 건보료 부과소득 합산</li>}
          {over2000 && <li>금융소득 2,000만원 초과 → 금융소득종합과세 대상(누진 가산 가능)</li>}
          {!over1000 && <li>현재 구간은 건보료·종합과세 경고선 아래예요</li>}
        </ul>
      </div>
      <small>참고용 계산이며 개별 투자 자문이 아닙니다.</small>
      {onApply && (Number(inputs?.investType) === 2
        ? <button type="button" className="fm-dc-apply on" onClick={() => onApply({ investType: 0 })}>✓ 결과에 반영됨 (배당세) · 해제</button>
        : <button type="button" className="fm-dc-apply" onClick={() => onApply({ investType: 2 })}>이 세금(배당세 15.4%)을 결과에 반영하기</button>)}
      {onApply && <small className="fm-dc-applynote">투자 유형은 하나만 반영돼요 — 국내(면제)·해외 양도세·배당세 중 택1.</small>}
    </section>
  );
}

export function PensionEarlyClaimCard({ inputs, onApply }) {
  const normalAge = inputs.expectedPensionAge || 65;
  const normalMonthly = inputs.expectedMonthlyPension || 0;
  const [claimAge, setClaimAge] = useState(normalAge);
  const r = earlyClaim(normalMonthly, normalAge, claimAge);
  return (
    <section className="fm-card fm-text-card fm-advanced-section">
      <p className="fm-kicker">국민연금</p>
      <h2>조기수령 득실</h2>
      <p>정상 {normalAge}세·월 {formatWon(normalMonthly)} 기준. 당겨 받으면 연 6%씩(최대 5년·30%) 감액돼 평생 유지돼요.</p>
      <Stepper label="수령 시작 나이" unit="세" value={claimAge} set={setClaimAge} step={1} />
      <div className="fm-dc-result ok">
        <ul>
          <li>{r.yearsEarly}년 조기 → {r.reductionPct}% 감액</li>
          <li>예상 월 수령액 {formatWon(r.monthly)}</li>
        </ul>
      </div>
      {normalMonthly > 0 && (
        <button type="button" className="fm-dc-apply" onClick={() => onApply({ expectedPensionAge: claimAge, expectedMonthlyPension: r.monthly })}>
          조기수령 가정 반영하기
        </button>
      )}
    </section>
  );
}
