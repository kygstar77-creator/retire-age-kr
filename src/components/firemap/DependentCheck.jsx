import { useState } from 'react';
import { assessDependentEligibility, estimateLocalPremium } from '../../firemap-v2/healthInsurance.js';
import { formatWon } from '../../firemap-v2/formatters.js';

function NumField({ label, unit, value, set, step = 100 }) {
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

export default function DependentCheck({ inputs, onApply }) {
  const [other, setOther] = useState(0);
  const [fin, setFin] = useState(0);
  const [prop, setProp] = useState(3);
  const [biz, setBiz] = useState(false);
  const [rental, setRental] = useState(false);
  const r = assessDependentEligibility({ otherIncomeManwon: other, financialIncomeManwon: fin, propertyTaxBaseEok: prop, hasBusinessIncome: biz, hasRentalIncome: rental });
  const est = estimateLocalPremium({ chargeableIncomeManwon: r.combinedIncome, propertyTaxBaseEok: prop });

  return (
    <section className="fm-card fm-text-card fm-advanced-section">
      <p className="fm-kicker">파이어 후 건보료</p>
      <h2>파이어 후 건보료, 얼마 낼까?</h2>
      <p>파이어 후 피부양자로 남을 수 있는지 + 지역가입자가 되면 <b>월 건보료가 얼마</b>인지 추정해요. 대부분의 계산기가 빠뜨리는 부분이에요. (참고용 근사 · 공단 확인 필요)</p>
      <div className="fm-dc-fields">
        <NumField label="금융 외 합산소득(연)" unit="만원" value={other} set={setOther} step={100} />
        <NumField label="금융소득(이자+배당, 연)" unit="만원" value={fin} set={setFin} step={100} />
        <NumField label="재산세 과세표준" unit="억" value={prop} set={setProp} step={1} />
        <div className="fm-dc-toggles">
          <button type="button" className={biz ? 'on' : ''} onClick={() => setBiz(!biz)}>사업자+소득</button>
          <button type="button" className={rental ? 'on' : ''} onClick={() => setRental(!rental)}>주택임대소득</button>
        </div>
      </div>
      <div className={`fm-dc-result ${r.eligible ? 'ok' : 'no'}`}>
        <strong>{r.eligible ? '피부양자 자격 유지 가능' : '피부양자 자격 박탈 가능'}</strong>
        <small>합산소득 {r.combinedIncome.toLocaleString()}만원 기준</small>
        <ul>{r.reasons.map((t) => <li key={t}>{t}</li>)}</ul>
      </div>
      <div className="fm-dc-prem">
        <div className="fm-dc-prem-row"><span>지역가입자가 되면 예상 월 건보료</span><b>약 {formatWon(est.monthly)}</b></div>
        <small>소득보험료 약 {formatWon(est.incomeMonthly)} + 재산보험료 약 {formatWon(est.propMonthly)} · 장기요양 포함 · 2025 요율(7.09%)·점수단가 208.4원·재산 1억 공제 근사. 정확한 금액은 공단 확인.</small>
        {r.eligible && <p className="fm-dc-prem-note">지금은 피부양자라 0원이지만, 위 소득·재산을 넘으면 이 금액을 내게 돼요.</p>}
      </div>
      {Number(inputs?.healthInsuranceEnabled) > 0
        ? <button type="button" className="fm-dc-apply on" onClick={() => onApply({ healthInsuranceEnabled: 0, monthlyHealthInsurance: 0 })}>✓ 건보료가 결과에 반영됨 (월 {formatWon(Number(inputs?.monthlyHealthInsurance) || 0)}) · 해제</button>
        : <button type="button" className="fm-dc-apply" onClick={() => onApply({ healthInsuranceEnabled: 1, monthlyHealthInsurance: est.monthly })}>이 건보료(월 {formatWon(est.monthly)})를 내 파이어 계산에 반영하기</button>}
    </section>
  );
}
