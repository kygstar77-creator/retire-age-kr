import { useState } from 'react';
import { assessDependentEligibility, estimateLocalPremium, estimateBaristaPremium } from '../../firemap-v2/healthInsurance.js';
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
  const [mode, setMode] = useState('local'); // 'local' 지역가입자 | 'barista' 바리스타 파이어(직장가입자)
  const [wage, setWage] = useState(100);      // 월 파트타임 급여(보수월액, 만원)

  const r = assessDependentEligibility({ otherIncomeManwon: other, financialIncomeManwon: fin, propertyTaxBaseEok: prop, hasBusinessIncome: biz, hasRentalIncome: rental });
  const est = estimateLocalPremium({ chargeableIncomeManwon: r.combinedIncome, propertyTaxBaseEok: prop });
  const bar = estimateBaristaPremium({ wageMonthlyManwon: wage, otherIncomeManwon: other, financialIncomeManwon: fin });
  const saving = est.monthly - bar.monthly; // 지역 대비 바리스타 절감(원/월)
  const applyMonthly = mode === 'barista' ? bar.monthly : est.monthly;

  return (
    <section className="fm-card fm-text-card fm-advanced-section">
      <p className="fm-kicker">파이어 후 건보료</p>
      <h2>파이어 후 건보료, 얼마 낼까?</h2>
      <p>파이어 후 피부양자로 남을 수 있는지 + 지역가입자가 되면 <b>월 건보료가 얼마</b>인지 추정해요. 바리스타 파이어(파트타임으로 직장가입자 유지)와도 비교돼요. (참고용 근사 · 공단 확인 필요)</p>

      <div className="fm-dc-mode" style={{ display: 'flex', gap: 8, margin: '4px 0 12px' }}>
        <button type="button" onClick={() => setMode('local')} className={mode === 'local' ? 'on' : ''} style={{ flex: 1, padding: '10px 8px', borderRadius: 12, border: mode === 'local' ? '1.5px solid #2563eb' : '1px solid #e5e7eb', background: mode === 'local' ? '#eff6ff' : '#fff', fontWeight: 700, fontSize: 13, color: mode === 'local' ? '#1d4ed8' : '#6b7280', cursor: 'pointer' }}>완전 은퇴 (지역가입자)</button>
        <button type="button" onClick={() => setMode('barista')} className={mode === 'barista' ? 'on' : ''} style={{ flex: 1, padding: '10px 8px', borderRadius: 12, border: mode === 'barista' ? '1.5px solid #ff5a00' : '1px solid #e5e7eb', background: mode === 'barista' ? '#fff4ec' : '#fff', fontWeight: 700, fontSize: 13, color: mode === 'barista' ? '#c2410c' : '#6b7280', cursor: 'pointer' }}>☕ 바리스타 파이어 (직장가입자)</button>
      </div>

      <div className="fm-dc-fields">
        {mode === 'barista' && <NumField label="월 파트타임 급여(보수월액)" unit="만원" value={wage} set={setWage} step={10} />}
        <NumField label="금융 외 보수외소득(임대·연금·사업, 연)" unit="만원" value={other} set={setOther} step={100} />
        <NumField label="금융소득(이자+배당, 연)" unit="만원" value={fin} set={setFin} step={100} />
        {mode === 'local' && <NumField label="재산세 과세표준" unit="억" value={prop} set={setProp} step={1} />}
        {mode === 'local' && (
          <div className="fm-dc-toggles">
            <button type="button" className={biz ? 'on' : ''} onClick={() => setBiz(!biz)}>사업자+소득</button>
            <button type="button" className={rental ? 'on' : ''} onClick={() => setRental(!rental)}>주택임대소득</button>
          </div>
        )}
      </div>

      {mode === 'local' ? (
        <>
          <div className={`fm-dc-result ${r.eligible ? 'ok' : 'no'}`}>
            <strong>{r.eligible ? '피부양자 자격 유지 가능' : '피부양자 자격 박탈 가능'}</strong>
            <small>합산소득 {r.combinedIncome.toLocaleString()}만원 기준</small>
            <ul>{r.reasons.map((t) => <li key={t}>{t}</li>)}</ul>
          </div>
          <div className="fm-dc-prem">
            <div className="fm-dc-prem-row"><span>지역가입자가 되면 예상 월 건보료</span><b>약 {formatWon(est.monthly)}</b></div>
            <small>소득보험료 약 {formatWon(est.incomeMonthly)} + 재산보험료 약 {formatWon(est.propMonthly)} · 장기요양 포함 · 2026 요율(7.19%)·점수단가 211.5원·재산 1억 공제 근사. 정확한 금액은 공단 확인.</small>
            {r.eligible && <p className="fm-dc-prem-note">지금은 피부양자라 0원이지만, 위 소득·재산을 넘으면 이 금액을 내게 돼요.</p>}
          </div>
        </>
      ) : (
        <>
          <div className="fm-dc-prem" style={{ background: '#fff4ec', borderColor: '#ffd9c2' }}>
            <div className="fm-dc-prem-row"><span>바리스타 파이어 시 예상 월 건보료</span><b>약 {formatWon(bar.monthly)}</b></div>
            <small>
              보수월액보험료 약 {formatWon(bar.wagePremium)}(급여 {formatWon(wage * 10000)} × 7.19% × 50% 근로자부담)
              {bar.overThreshold
                ? ` + 소득월액보험료 약 ${formatWon(bar.incomePremium)}(합산 보수외소득 ${bar.combinedOther.toLocaleString()}만원 중 2,000만원 초과분)`
                : ' · 보수외소득 2,000만원 이하 → 추가 없음'} · 장기요양 포함 · 2026 요율.
            </small>
            <p className="fm-dc-prem-note">
              ☕ 직장가입자라 <b>재산은 건보료에 안 잡혀요.</b> 이자·배당은 연 1,000만원까지는 건보료에 안 잡히고, 합산 보수외소득(금융소득+임대·연금·사업)이 <b>2,000만원 넘는 부분부터</b> 소득월액보험료가 추가돼요.
            </p>
          </div>
          <div className="fm-dc-prem" style={{ marginTop: 8 }}>
            <div className="fm-dc-prem-row"><span>완전 은퇴(지역가입자) 시</span><b>약 {formatWon(est.monthly)}</b></div>
            {saving > 0
              ? <p className="fm-dc-prem-note" style={{ color: '#c2410c', fontWeight: 700 }}>→ 바리스타 파이어 시 월 약 {formatWon(saving)} 절감 (자산 기반 지역 건보료 회피)</p>
              : <p className="fm-dc-prem-note">→ 이 조건에선 지역가입자가 더 유리할 수 있어요(급여·소득에 따라 달라짐).</p>}
          </div>
        </>
      )}

      {Number(inputs?.healthInsuranceEnabled) > 0
        ? <button type="button" className="fm-dc-apply on" onClick={() => onApply({ healthInsuranceEnabled: 0, monthlyHealthInsurance: 0 })}>✓ 건보료가 결과에 반영됨 (월 {formatWon(Number(inputs?.monthlyHealthInsurance) || 0)}) · 해제</button>
        : <button type="button" className="fm-dc-apply" onClick={() => onApply({ healthInsuranceEnabled: 1, monthlyHealthInsurance: applyMonthly })}>이 건보료(월 {formatWon(applyMonthly)})를 내 파이어 계산에 반영하기</button>}

      <p className="fm-dc-foot" style={{ fontSize: 11, color: '#9aa3bf', marginTop: 10, lineHeight: 1.5 }}>추정치예요(2026년 요율 기준). 분리과세 이자·배당 등 일부 예외는 단순화했어요. 정확한 금액은 국민건강보험공단에서 확인하세요. 투자·세무 조언이 아닙니다. · 출처: 국민건강보험공단·보건복지부 2026 요율</p>
    </section>
  );
}
