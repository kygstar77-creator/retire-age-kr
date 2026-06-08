import Header from './Header.jsx';
import { formatWon } from '../../firemap-v2/formatters.js';
import { buildScenario, runwayText, scenarioEndAge } from '../../firemap-v2/scenarios.js';

function AdvancedScenarioCard({ title, description, simulation, baseSimulation, onApply, applyLabel, metrics }) {
  const years = scenarioEndAge(simulation) - scenarioEndAge(baseSimulation);
  const delta = years > 0 ? `${years}년 개선` : years < 0 ? `${Math.abs(years)}년 단축` : '변화 작음';
  return (
    <article className="fm-advanced-card">
      <div>
        <strong>{title}</strong>
        <p>{description}</p>
      </div>
      <div className="fm-advanced-metrics">
        <span>자산수명 <b>{runwayText(simulation)}</b></span>
        <span>현재 대비 <b>{delta}</b></span>
        {metrics.map(([label, value]) => <span key={label}>{label} <b>{value}</b></span>)}
      </div>
      <button type="button" onClick={onApply}>{applyLabel}</button>
    </article>
  );
}

export default function Advanced({ inputs, onChange, simulation, onBack }) {
  const healthInsuranceScenario = buildScenario(inputs, { healthInsuranceEnabled: 1, monthlyHealthInsurance: 230000 });
  const chiangMaiScenario = buildScenario(inputs, { overseasStayEnabled: 1, overseasMonthsPerYear: 3, overseasContinuousDays: 95, overseasMonthlyCostLocal: 65000, overseasExchangeRate: 40, overseasAnnualExtraCost: 1500000, overseasApplyYears: 10 });
  const chiangMaiInsuranceScenario = buildScenario(inputs, { overseasStayEnabled: 1, overseasInsurancePauseEnabled: 1, healthInsuranceEnabled: 1, monthlyHealthInsurance: 230000, overseasMonthsPerYear: 3, overseasContinuousDays: 95, overseasMonthlyCostLocal: 65000, overseasExchangeRate: 40, overseasAnnualExtraCost: 1500000, overseasApplyYears: 10 });
  const cashflowScenario = buildScenario(inputs, { partTimeIncomeAfterRetirement: inputs.partTimeIncomeAfterRetirement + 1000000 });
  const applyPatch = (patch) => Object.entries(patch).forEach(([key, value]) => onChange(key, value));

  return (
    <main className="fm-screen fm-scroll">
      <Header tag="고급 실험" onBack={onBack} />
      <section className="fm-card fm-text-card fm-advanced-section">
        <p className="fm-kicker">고급 실험</p>
        <h2>복잡한 가정은 따로 비교해요</h2>
        <p>건보료, 해외 체류, 퇴사 후 현금흐름처럼 해석이 필요한 조건은 기본 실험과 분리했습니다. 모든 값은 참고 시나리오입니다.</p>
      </section>
      <section className="fm-card fm-text-card fm-advanced-section">
        <p className="fm-kicker">고정비</p>
        <h2>퇴사 후 고정비 반영</h2>
        <AdvancedScenarioCard
          title="지역가입 건보료 월 23만 원 반영"
          description="퇴사 후 고정비가 늘어나는 보수적 시나리오입니다. 실제 보험료는 소득·재산·제도에 따라 달라져요."
          simulation={healthInsuranceScenario}
          baseSimulation={simulation}
          applyLabel="건보료 반영"
          onApply={() => applyPatch({ healthInsuranceEnabled: 1, monthlyHealthInsurance: 230000 })}
          metrics={[["첫해 건보료", formatWon(healthInsuranceScenario.firstYearHealthInsurance)]]}
        />
      </section>
      <section className="fm-card fm-text-card fm-advanced-section">
        <p className="fm-kicker">해외 체류</p>
        <h2>생활비를 낮추는 시나리오</h2>
        <AdvancedScenarioCard
          title="치앙마이 3개월 살기"
          description="연 3개월 해외 저비용 생활을 적용해 생활비를 낮추는 시나리오입니다. 환율은 1바트 40원으로 둡니다."
          simulation={chiangMaiScenario}
          baseSimulation={simulation}
          applyLabel="해외체류 반영"
          onApply={() => applyPatch({ overseasStayEnabled: 1, overseasMonthsPerYear: 3, overseasContinuousDays: 95, overseasMonthlyCostLocal: 65000, overseasExchangeRate: 40, overseasAnnualExtraCost: 1500000, overseasApplyYears: 10 })}
          metrics={[["첫해 절감", formatWon(chiangMaiScenario.firstYearOverseasSavings)]]}
        />
        <AdvancedScenarioCard
          title="해외 3개월 + 건보료 일시정지"
          description="해외 장기체류로 생활비와 건보료 변화를 함께 보는 공격적 시나리오입니다. 실제 면제 조건은 제도 확인이 필요합니다."
          simulation={chiangMaiInsuranceScenario}
          baseSimulation={simulation}
          applyLabel="복합 시나리오 반영"
          onApply={() => applyPatch({ overseasStayEnabled: 1, overseasInsurancePauseEnabled: 1, healthInsuranceEnabled: 1, monthlyHealthInsurance: 230000, overseasMonthsPerYear: 3, overseasContinuousDays: 95, overseasMonthlyCostLocal: 65000, overseasExchangeRate: 40, overseasAnnualExtraCost: 1500000, overseasApplyYears: 10 })}
          metrics={[["첫해 절감", formatWon(chiangMaiInsuranceScenario.firstYearOverseasSavings)], ["첫해 건보료", formatWon(chiangMaiInsuranceScenario.firstYearHealthInsurance)]]}
        />
      </section>
      <section className="fm-card fm-text-card fm-advanced-section">
        <p className="fm-kicker">현금흐름</p>
        <h2>퇴사 후 월수입 실험</h2>
        <AdvancedScenarioCard
          title="퇴사 후 월 100만 원 현금흐름"
          description="배당·파트타임·콘텐츠 수익처럼 매달 들어오는 돈이 자산수명에 주는 영향을 봅니다. 세금은 다음 단계에서 분리합니다."
          simulation={cashflowScenario}
          baseSimulation={simulation}
          applyLabel="현금흐름 반영"
          onApply={() => onChange('partTimeIncomeAfterRetirement', inputs.partTimeIncomeAfterRetirement + 1000000)}
          metrics={[["월 현금흐름", formatWon(1000000)]]}
        />
      </section>
    </main>
  );
}
