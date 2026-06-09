import { useState } from 'react';
import { assessDependentEligibility } from '../../firemap-v2/healthInsurance.js';

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

export default function DependentCheck({ onApply }) {
  const [other, setOther] = useState(0);
  const [fin, setFin] = useState(0);
  const [prop, setProp] = useState(3);
  const [biz, setBiz] = useState(false);
  const [rental, setRental] = useState(false);
  const r = assessDependentEligibility({ otherIncomeManwon: other, financialIncomeManwon: fin, propertyTaxBaseEok: prop, hasBusinessIncome: biz, hasRentalIncome: rental });

  return (
    <section className="fm-card fm-text-card fm-advanced-section">
      <p className="fm-kicker">건강보험</p>
      <h2>피부양자 자격 판정</h2>
      <p>퇴사 후 자녀 등의 건강보험 피부양자로 남을 수 있는지 조건으로 판정해요. 참고용이며 실제는 공단 확인이 필요해요.</p>
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
      {!r.eligible && (
        <button type="button" className="fm-dc-apply" onClick={() => onApply({ healthInsuranceEnabled: 1, monthlyHealthInsurance: 230000 })}>
          지역가입 건보료(월 23만 가정) 반영하기
        </button>
      )}
    </section>
  );
}
