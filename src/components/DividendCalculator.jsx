import { useMemo, useState } from 'react';
import { calculateInvestmentTaxes, defaultTaxInputs } from '../utils/taxCalculator.js';
import { formatCompactMoney } from '../utils/formatters.js';

const fields = [
  ['annualDividendIncome', '연간 배당금', '세전 기준', '원', true],
  ['dividendWithholdingRate', '배당 기본 세율', '기본값 15.4%', '%', false],
  ['financialIncomeThreshold', '금융소득 확인 기준', '기본값 2,000만 원', '원', true],
  ['additionalDividendTaxRate', '초과분 추가 추정세율', '민감도 확인용', '%', false],
  ['foreignStockGain', '해외주식 연간 양도차익', '차익 기준', '원', true],
  ['foreignStockBasicDeduction', '해외주식 기본공제', '기본값 250만 원', '원', true],
  ['foreignStockTaxRate', '해외주식 양도세율', '기본값 22%', '%', false],
  ['targetMonthlyDividendAfterTax', '목표 월 세후 배당금', '월 현금흐름 목표', '원', true],
  ['expectedDividendYield', '예상 배당률', '연 배당률', '%', false],
  ['dividendReinvestmentRate', '배당 재투자 비율', '재투자할 비율', '%', false]
];

export default function DividendCalculator() {
  const [values, setValues] = useState(defaultTaxInputs);
  const result = useMemo(() => calculateInvestmentTaxes(values), [values]);

  const update = (name, value, money) => {
    setValues((current) => ({
      ...current,
      [name]: money ? value.replace(/[^\d-]/g, '') : value
    }));
  };

  return (
    <section className="panel dividend-calculator">
      <div className="section-heading compact-heading">
        <div>
          <p className="eyebrow">Dividend</p>
          <h2>배당금·해외주식 세금 계산기</h2>
        </div>
      </div>
      <p className="tax-intro">
        배당금, 해외주식 양도차익, 목표 월 배당금을 입력해 세후 현금흐름과 필요 원금을 대략 확인합니다.
      </p>

      <div className="tax-grid">
        <div className="tax-inputs">
          {fields.map(([name, label, help, suffix, money]) => (
            <label className="field" key={name}>
              <span>{label}</span>
              <b>{help}</b>
              <div className="input-wrap">
                <input
                  type={money ? 'text' : 'number'}
                  inputMode={money ? 'numeric' : undefined}
                  value={money ? formatInputNumber(values[name]) : values[name]}
                  onChange={(event) => update(name, event.target.value, money)}
                />
                <small>{suffix}</small>
              </div>
              {money && <em>{formatCompactMoney(values[name])}</em>}
            </label>
          ))}
        </div>

        <div className="tax-results">
          <ResultCard title="연 세후 배당금" main={formatCompactMoney(result.dividendTax.afterTaxDividend)} sub={`월 ${formatCompactMoney(result.dividendTax.monthlyAfterTaxDividend)}`} />
          <ResultCard title="배당 세금 추정" main={formatCompactMoney(result.dividendTax.totalTax)} sub={`실효 ${formatPercent(result.dividendTax.effectiveTaxRate)}`} />
          <ResultCard title="해외주식 양도세 추정" main={formatCompactMoney(result.foreignStockTax.tax)} sub={`세후차익 ${formatCompactMoney(result.foreignStockTax.afterTaxGain)}`} />
          <ResultCard title="필요 배당 원금" main={formatCompactMoney(result.requiredAsset.requiredAsset)} sub={`순수령 배당률 ${formatPercent(result.requiredAsset.netYieldRate)}`} />
        </div>
      </div>

      <div className="tax-notice">
        <strong>참고용 계산</strong>
        <p>세율, 공제, 종합과세, 계좌 종류, 환율, 손익통산에 따라 실제 금액은 달라질 수 있습니다.</p>
      </div>
    </section>
  );
}

function ResultCard({ title, main, sub }) {
  return (
    <article className="tax-result-card">
      <span>{title}</span>
      <strong>{main}</strong>
      <small>{sub}</small>
    </article>
  );
}

function formatInputNumber(value) {
  const raw = String(value ?? '').replace(/[^\d-]/g, '');
  if (!raw || raw === '-') return raw;
  const sign = raw.startsWith('-') ? '-' : '';
  const digits = raw.replace('-', '');
  return `${sign}${Number(digits).toLocaleString('ko-KR')}`;
}

function formatPercent(value) {
  return `${Number(value || 0).toLocaleString('ko-KR', { maximumFractionDigits: 1 })}%`;
}
