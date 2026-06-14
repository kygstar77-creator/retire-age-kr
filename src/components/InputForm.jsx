import { ChevronDown, RotateCcw } from 'lucide-react';
import { useState } from 'react';
import { formatCompactMoney } from '../utils/formatters.js';

const fields = [
  { group: 'basic', section: '기본', name: 'currentAge', label: '지금 내 나이', help: '만 나이 기준으로 입력하세요.', suffix: '세' },
  { group: 'basic', section: '기본', name: 'targetRetirementAge', label: '파이어하고 싶은 나이', help: '이 나이에 회사를 그만둔다고 가정합니다.', suffix: '세' },
  { group: 'basic', section: '기본', name: 'startYear', label: '계산 시작 연도', help: '올해 기준이면 그대로 두면 됩니다.', suffix: '년' },
  { group: 'basic', section: '자산', name: 'financialAsset', label: '바로 쓸 수 있는 투자·현금 자산', help: '예금, 주식, ETF, 펀드, 연금저축처럼 금융자산만 넣으세요.', suffix: '원', money: true },
  { group: 'basic', section: '자산', name: 'realEstateValue', label: '내 집·부동산 예상 가치', help: '실거주 집도 순자산 계산에는 포함하지만 생활비 인출 재원은 아닙니다.', suffix: '원', money: true },
  { group: 'basic', section: '자산', name: 'debt', label: '아직 남은 대출금', help: '주택담보대출, 신용대출 등 갚아야 할 총액입니다.', suffix: '원', money: true },
  { group: 'basic', section: '현금흐름', name: 'monthlyInvestment', label: '파이어 전 매달 모을 돈', help: '월급에서 생활비를 쓰고 남겨 투자할 수 있는 금액입니다.', suffix: '원', money: true },
  { group: 'basic', section: '현금흐름', name: 'monthlyLivingCost', label: '파이어 후 매달 쓸 생활비', help: '주거비, 식비, 보험료, 취미비까지 포함한 월 지출입니다. 매년 물가만큼 늘어나는 것으로 계산합니다.', suffix: '원', money: true },
  { group: 'basic', section: '가정', name: 'annualReturnRate', label: '투자 수익률', help: '금융자산이 매년 평균 몇 % 불어난다고 볼지입니다.', suffix: '%' },
  { group: 'basic', section: '가정', name: 'inflationRate', label: '물가상승률', help: '이 비율만큼 생활비·국민연금·건보료·해외 체류비가 매년 늘어납니다. (부업 소득은 제외)', suffix: '%' },
  { group: 'basic', section: '가정', name: 'simulationUntilAge', label: '몇 살까지 버티는지 볼까요?', help: '보통 90세 기준으로 확인합니다.', suffix: '세' },
  { group: 'advanced', section: '연금·추가소득', name: 'partTimeIncomeAfterRetirement', label: '파이어 후 매달 벌 수 있는 돈', help: '파트타임, 프리랜서, 임대소득 등 현재 돈 가치로 입력하세요. 물가 미반영(고정 수입으로 계산).', suffix: '원', money: true },
  { group: 'advanced', section: '연금·추가소득', name: 'expectedPensionAge', label: '국민연금 받기 시작하는 나이', help: '예상 수령 시작 나이를 넣으세요.', suffix: '세' },
  { group: 'advanced', section: '연금·추가소득', name: 'expectedMonthlyPension', label: '국민연금 월 예상 수령액', help: '현재 돈 가치로 입력하세요. 물가상승률을 반영해 계산합니다.', suffix: '원', money: true },
  { group: 'advanced', section: '건강보험료', name: 'healthInsuranceEnabled', label: '건보료 반영', help: '파이어 후 예상 건강보험료를 비용에 반영합니다.', toggle: true },
  { group: 'advanced', section: '건강보험료', name: 'monthlyHealthInsurance', label: '예상 월 건강보험료', help: '지역가입자, 피부양자 여부에 따라 실제 금액은 달라질 수 있습니다. 매년 물가만큼 증가하는 것으로 계산합니다.', suffix: '원', money: true },
  { group: 'advanced', section: '건강보험료', name: 'overseasInsurancePauseEnabled', label: '해외 장기체류 건보료 조정 반영', help: '3개월 이상 연속 국외 체류 가능성이 있는 경우만 참고용으로 켜세요.', toggle: true },
  { group: 'advanced', section: '해외 체류', name: 'overseasStayEnabled', label: '해외 체류 시나리오 반영', help: '치앙마이 등 저비용 도시에서 몇 달 사는 경우의 생활비를 반영합니다.', toggle: true },
  { group: 'advanced', section: '해외 체류', name: 'overseasMonthsPerYear', label: '연간 해외 체류 개월', help: '1년에 해외에서 지내는 개월 수입니다.', suffix: '개월' },
  { group: 'advanced', section: '해외 체류', name: 'overseasContinuousDays', label: '1회 연속 체류일', help: '건보료 조정 가능성 판단용 참고값입니다. 확정 판단이 아닙니다.', suffix: '일' },
  { group: 'advanced', section: '해외 체류', name: 'overseasMonthlyCostLocal', label: '현지 월 생활비', help: '예: 치앙마이 50,000 THB처럼 현지 통화 기준으로 입력하세요.', suffix: '현지화', money: true },
  { group: 'advanced', section: '해외 체류', name: 'overseasExchangeRate', label: '적용 환율', help: '1 현지화가 몇 원인지 입력합니다. 예: THB 40원.', suffix: '원' },
  { group: 'advanced', section: '해외 체류', name: 'overseasAnnualExtraCost', label: '항공권·보험·비자 등 연 부대비', help: '해외 체류 때문에 추가로 드는 연간 비용입니다.', suffix: '원', money: true },
  { group: 'advanced', section: '해외 체류', name: 'overseasApplyYears', label: '해외 체류 적용 기간', help: '파이어 후 몇 년 동안 이 생활을 반복할지 입력하세요.', suffix: '년' }
];

export default function InputForm({ values, onChange, onReset }) {
  const [open, setOpen] = useState(true);
  const [advancedOpen, setAdvancedOpen] = useState(false);
  const [step, setStep] = useState(0);
  const visibleFields = advancedOpen ? fields : fields.filter((field) => field.group === 'basic');
  const groupedFields = groupFields(visibleFields);
  const currentStep = groupedFields[Math.min(step, groupedFields.length - 1)];

  const handleInput = (field, value) => {
    const nextValue = field.money ? value.replace(/[^\d-]/g, '') : value;
    onChange(field.name, nextValue);
  };

  const handleToggle = (field) => {
    const current = Number(values[field.name] || 0) === 1;
    onChange(field.name, current ? 0 : 1);
  };

  const handleAdvancedToggle = () => {
    setAdvancedOpen((current) => !current);
    setStep(0);
  };

  return (
    <section className={`panel input-panel ${open ? 'input-open' : ''}`} id="input-area">
      <div className="section-heading">
        <div>
          <p className="eyebrow">입력</p>
          <h2>나의 파이어 조건</h2>
        </div>
        <div className="input-actions">
          <button className="icon-button mobile-toggle" type="button" onClick={() => setOpen((current) => !current)}>
            <ChevronDown size={18} />
            <span>{open ? '입력 닫기' : '입력 수정'}</span>
          </button>
          <button className="icon-button reset-button" type="button" onClick={onReset} title="초기화">
            <RotateCcw size={18} />
            <span>초기화</span>
          </button>
        </div>
      </div>

      <button className={`advanced-toggle ${advancedOpen ? 'active' : ''}`} type="button" onClick={handleAdvancedToggle}>
        <span>{advancedOpen ? '고급 설정 접기' : '고급 설정 펼치기'}</span>
        <small>국민연금 · 추가소득 · 건보료 · 해외체류 · 환율</small>
      </button>

      <div className="mobile-stepper">
        <div>
          <span>{Math.min(step + 1, groupedFields.length)}</span>
          <small>/ {groupedFields.length}</small>
        </div>
        <strong>{currentStep?.[0]}</strong>
      </div>

      <div className="input-grid">
        {groupedFields.map(([section, sectionFields], index) => (
          <div className={`input-section ${index === step ? 'active-section' : ''}`} key={section}>
            <h3>{section}</h3>
            {sectionFields.map((field) => (
              <label className={`field ${field.toggle ? 'toggle-field' : ''}`} key={field.name}>
                <span>{field.label}</span>
                <b>{field.help}</b>
                {field.toggle ? (
                  <button
                    className={`toggle-button ${Number(values[field.name] || 0) === 1 ? 'on' : ''}`}
                    type="button"
                    onClick={() => handleToggle(field)}
                    aria-pressed={Number(values[field.name] || 0) === 1}
                  >
                    <strong>{Number(values[field.name] || 0) === 1 ? 'ON' : 'OFF'}</strong>
                    <small>{Number(values[field.name] || 0) === 1 ? '반영 중' : '미반영'}</small>
                  </button>
                ) : (
                  <>
                    <div className="input-wrap">
                      <input
                        type={field.money ? 'text' : 'number'}
                        inputMode={field.money ? 'numeric' : undefined}
                        value={field.money ? formatInputNumber(values[field.name]) : values[field.name]}
                        onChange={(event) => handleInput(field, event.target.value)}
                      />
                      <small>{field.suffix}</small>
                    </div>
                    {field.money && <em>{formatCompactMoney(values[field.name])}</em>}
                  </>
                )}
              </label>
            ))}
          </div>
        ))}
      </div>

      <p className="input-policy-note">
        건강보험료, 해외 체류, 환율은 참고용 추정입니다. 실제 부과액·체류 조건·결제 환율은 공식 기준과 개인 상황에 따라 달라질 수 있습니다.
      </p>

      <div className="mobile-step-actions">
        <button type="button" disabled={step === 0} onClick={() => setStep((current) => Math.max(0, current - 1))}>
          이전
        </button>
        <button
          type="button"
          onClick={() => {
            if (step < groupedFields.length - 1) {
              setStep((current) => current + 1);
            } else {
              setOpen(false);
              window.scrollTo({ top: 0, behavior: 'smooth' });
            }
          }}
        >
          {step < groupedFields.length - 1 ? '다음' : '결과 보기'}
        </button>
      </div>
    </section>
  );
}

function groupFields(items) {
  return Object.entries(
    items.reduce((groups, item) => {
      groups[item.section] = [...(groups[item.section] || []), item];
      return groups;
    }, {})
  );
}

function formatInputNumber(value) {
  const raw = String(value ?? '').replace(/[^\d-]/g, '');
  if (!raw || raw === '-') return raw;
  const sign = raw.startsWith('-') ? '-' : '';
  const digits = raw.replace('-', '');
  return `${sign}${Number(digits).toLocaleString('ko-KR')}`;
}
