import { ChevronDown, RotateCcw } from 'lucide-react';
import { useState } from 'react';
import { Button, Input } from 'antd';
import { formatCompactMoney } from '../utils/formatters.js';

const fields = [
  { section: '기본', name: 'currentAge', label: '지금 내 나이', help: '만 나이 기준으로 입력하세요.', suffix: '세' },
  { section: '기본', name: 'targetRetirementAge', label: '퇴사하고 싶은 나이', help: '이 나이에 회사를 그만둔다고 가정합니다.', suffix: '세' },
  { section: '기본', name: 'startYear', label: '계산 시작 연도', help: '올해 기준이면 그대로 두면 됩니다.', suffix: '년' },
  { section: '자산', name: 'financialAsset', label: '바로 쓸 수 있는 투자·현금 자산', help: '예금, 주식, ETF, 펀드, 연금저축처럼 금융자산만 넣으세요.', suffix: '원', money: true },
  { section: '자산', name: 'realEstateValue', label: '내 집·부동산 예상 가치', help: '실거주 집도 순자산 계산에는 포함하지만 생활비 인출 재원은 아닙니다.', suffix: '원', money: true },
  { section: '자산', name: 'debt', label: '아직 남은 대출금', help: '주택담보대출, 신용대출 등 갚아야 할 총액입니다.', suffix: '원', money: true },
  { section: '현금흐름', name: 'monthlyInvestment', label: '퇴사 전 매달 모을 돈', help: '월급에서 생활비를 쓰고 남겨 투자할 수 있는 금액입니다.', suffix: '원', money: true },
  { section: '현금흐름', name: 'monthlyLivingCost', label: '퇴사 후 매달 쓸 생활비', help: '주거비, 식비, 보험료, 취미비까지 포함한 월 지출입니다.', suffix: '원', money: true },
  { section: '현금흐름', name: 'partTimeIncomeAfterRetirement', label: '퇴사 후 매달 벌 수 있는 돈', help: '현재 돈 가치로 입력하세요. 앱이 물가상승률을 반영해 계산합니다.', suffix: '원', money: true },
  { section: '연금', name: 'expectedPensionAge', label: '국민연금 받기 시작하는 나이', help: '예상 수령 시작 나이를 넣으세요.', suffix: '세' },
  { section: '연금', name: 'expectedMonthlyPension', label: '국민연금 월 예상 수령액', help: '현재 돈 가치로 입력하세요. 65세 이후에는 물가상승률을 반영해 계산합니다.', suffix: '원', money: true },
  { section: '가정', name: 'annualReturnRate', label: '투자 수익률', help: '금융자산이 매년 평균 몇 % 불어난다고 볼지입니다.', suffix: '%' },
  { section: '가정', name: 'inflationRate', label: '물가상승률', help: '생활비가 매년 몇 %씩 늘어난다고 볼지입니다.', suffix: '%' },
  { section: '가정', name: 'simulationUntilAge', label: '몇 살까지 버티는지 볼까요?', help: '보통 90세 기준으로 확인합니다.', suffix: '세' }
];

export default function InputForm({ values, onChange, onReset }) {
  const [open, setOpen] = useState(true);
  const [step, setStep] = useState(0);
  const groupedFields = groupFields(fields);
  const currentStep = groupedFields[step];

  const handleInput = (field, value) => {
    const nextValue = field.money ? value.replace(/[^\d-]/g, '') : value;
    onChange(field.name, nextValue);
  };

  return (
    <section className={`panel input-panel ${open ? 'input-open' : ''}`} id="input-area">
      <div className="section-heading">
        <div>
          <p className="eyebrow">입력</p>
          <h2>나의 퇴사 조건</h2>
        </div>
        <div className="input-actions">
          <Button
            className="mobile-toggle"
            icon={<ChevronDown size={18} />}
            onClick={() => setOpen((current) => !current)}
          >
            {open ? '입력 닫기' : '입력 수정'}
          </Button>
          <Button icon={<RotateCcw size={18} />} onClick={onReset} title="초기화">
            초기화
          </Button>
        </div>
      </div>

      <div className="mobile-stepper">
        <div>
          <span>{step + 1}</span>
          <small>/ {groupedFields.length}</small>
        </div>
        <strong>{currentStep?.[0]}</strong>
      </div>

      <div className="input-grid">
        {groupedFields.map(([section, sectionFields], index) => (
          <div className={`input-section ${index === step ? 'active-section' : ''}`} key={section}>
            <h3>{section}</h3>
            {sectionFields.map((field) => (
              <label className="field" key={field.name}>
                <span>{field.label}</span>
                <b>{field.help}</b>
                <Input
                  size="large"
                  type={field.money ? 'text' : 'number'}
                  inputMode={field.money ? 'numeric' : undefined}
                  addonAfter={field.suffix}
                  value={field.money ? formatInputNumber(values[field.name]) : values[field.name]}
                  onChange={(event) => handleInput(field, event.target.value)}
                />
                {field.money && <em>{formatCompactMoney(values[field.name])}</em>}
              </label>
            ))}
          </div>
        ))}
      </div>

      <div className="mobile-step-actions">
        <Button disabled={step === 0} onClick={() => setStep((current) => Math.max(0, current - 1))}>
          이전
        </Button>
        <Button
          type="primary"
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
        </Button>
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
