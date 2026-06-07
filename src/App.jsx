import { useEffect, useMemo, useState } from 'react';
import InputForm from './components/InputForm.jsx';
import DecisionDashboard from './components/DecisionDashboard.jsx';
import GrowthPanel from './components/GrowthPanel.jsx';
import InsightReport from './components/InsightReport.jsx';
import DividendCalculator from './components/DividendCalculator.jsx';
import ScenarioComparison from './components/ScenarioComparison.jsx';
import SummaryCards from './components/SummaryCards.jsx';
import YearlyTable from './components/YearlyTable.jsx';
import { buildSimulation, defaultInputs, normalizeInputs } from './utils/retirementSimulator.js';
import { buildShareUrl, decodeInputsFromHash } from './utils/shareState.js';
import './tabs.css';

const storageKey = 'toesanai-inputs-v1';

const tabs = [
  { id: 'calculator', label: '계산기', description: '핵심 입력과 결과' },
  { id: 'analysis', label: '분석', description: '민감도와 상세표' },
  { id: 'share', label: '공유', description: '링크와 피드백' }
];

function loadInitialInputs() {
  try {
    const shared = decodeInputsFromHash(window.location.hash);
    if (shared) return { ...defaultInputs, ...shared };
    const saved = localStorage.getItem(storageKey);
    return saved ? { ...defaultInputs, ...JSON.parse(saved) } : defaultInputs;
  } catch {
    return defaultInputs;
  }
}

function formatWon(value) {
  const amount = Number(value || 0);
  if (Math.abs(amount) >= 100000000) return `${(amount / 100000000).toFixed(1)}억 원`;
  if (Math.abs(amount) >= 10000) return `${Math.round(amount / 10000).toLocaleString()}만 원`;
  return `${Math.round(amount).toLocaleString()}원`;
}

function buildShareSummary(inputs, simulation) {
  const depletionText = simulation.targetResult.depletionAge
    ? `${simulation.targetResult.depletionAge}세`
    : `${inputs.simulationUntilAge}세 이상`;

  return [
    '내 퇴사나이 계산 결과',
    '',
    `목표 퇴사 나이: ${inputs.targetRetirementAge}세`,
    `퇴사 후 월 생활비: ${formatWon(inputs.monthlyLivingCost)}`,
    `퇴사 시 예상 금융자산: ${formatWon(simulation.retirementFinancialAsset)}`,
    `예상 자산 유지 나이: ${depletionText}`,
    `기대 연수익률: ${inputs.annualReturnRate}%`,
    `퇴사 첫해 건보료 반영액: ${formatWon(simulation.firstYearHealthInsurance)}`,
    `퇴사 첫해 해외체류 절감액: ${formatWon(simulation.firstYearOverseasSavings)}`,
    '',
    '계산해보기:',
    buildShareUrl(inputs),
    '',
    '※ 이 결과는 입력값 기반 참고용 시뮬레이션이며 투자·세무·법률 자문이 아닙니다.'
  ].join('\n');
}

function PolicySections() {
  return (
    <>
      <section className="disclaimer">
        <strong>참고용 시뮬레이션</strong>
        <p>
          퇴사나이는 입력값과 가정에 따른 계산 결과를 제공하며, 투자 권유나 재무 자문이 아닙니다.
          실제 의사결정 전에는 세금, 건강보험, 주거비, 가족 상황, 시장 변동성을 함께 검토하세요.
        </p>
      </section>
      <section className="disclaimer security-note">
        <strong>개인정보 보호</strong>
        <p>
          입력한 자산 정보는 서버로 전송하지 않고 이 브라우저에만 저장됩니다. 공용 PC에서는 사용 후 초기화를 눌러주세요.
        </p>
      </section>
      <section className="legal-panel" id="legal">
        <div className="section-heading">
          <div>
            <p className="eyebrow">운영 안내</p>
            <h2>개인정보·이용약관·면책 고지</h2>
          </div>
        </div>
        <div className="legal-grid">
          <article>
            <h3>개인정보처리방침 요약</h3>
            <p>
              퇴사나이는 서버, 로그인, 데이터베이스를 사용하지 않습니다. 사용자가 입력한 자산 정보는
              브라우저 localStorage에만 저장되며, 운영자에게 전송되지 않습니다.
            </p>
          </article>
          <article>
            <h3>이용약관 요약</h3>
            <p>
              본 서비스는 사용자가 입력한 가정에 따라 계산 결과를 제공하는 참고용 도구입니다.
              사용자는 본인의 판단과 책임으로 결과를 활용해야 합니다.
            </p>
          </article>
          <article>
            <h3>재무 자문 아님</h3>
            <p>
              퇴사나이는 투자 권유, 금융상품 추천, 세무·법률·재무 자문을 제공하지 않습니다.
              실제 퇴사나 투자 결정 전에는 전문가 상담과 공식 자료 확인이 필요합니다.
            </p>
          </article>
        </div>
      </section>
    </>
  );
}

function AdjustmentSummary({ simulation }) {
  const inputs = simulation.inputs;
  const baselineDepletion = simulation.baselineForAdjustments?.depletionAge;
  const adjustedDepletion = simulation.targetResult.depletionAge;
  const baselineText = baselineDepletion ? `${baselineDepletion}세` : `${inputs.simulationUntilAge}세 이상`;
  const adjustedText = adjustedDepletion ? `${adjustedDepletion}세` : `${inputs.simulationUntilAge}세 이상`;
  const healthOn = inputs.healthInsuranceEnabled === 1;
  const overseasOn = inputs.overseasStayEnabled === 1;

  return (
    <section className="panel adjustment-summary">
      <div className="section-heading compact-heading">
        <div>
          <p className="eyebrow">고급 설정 반영</p>
          <h2>건보료·해외체류 효과</h2>
        </div>
      </div>
      <div className="adjustment-grid">
        <article>
          <span>퇴사 첫해 건보료</span>
          <strong>{healthOn ? formatWon(simulation.firstYearHealthInsurance) : '미반영'}</strong>
          <small>사용자 입력 기준</small>
        </article>
        <article>
          <span>퇴사 첫해 해외체류 절감</span>
          <strong>{overseasOn ? formatWon(simulation.firstYearOverseasSavings) : '미반영'}</strong>
          <small>환율·부대비 포함</small>
        </article>
        <article>
          <span>기본 대비 자산 유지</span>
          <strong>{baselineText} → {adjustedText}</strong>
          <small>고급 설정 전후 비교</small>
        </article>
      </div>
      <p>
        건강보험료와 해외 체류는 실제 공단 기준, 체류일수, 환율, 비자, 보험료에 따라 달라질 수 있습니다.
        이 영역은 의사결정 전 대략적인 민감도를 보는 참고용입니다.
      </p>
    </section>
  );
}

function CalculatorTab({ inputs, normalizedInputs, simulation, onChange, onReset, onMoveToAnalysis }) {
  return (
    <div className="tab-layout calculator-layout">
      <InputForm values={inputs} onChange={onChange} onReset={onReset} />
      <div className="results">
        <DecisionDashboard simulation={simulation} />
        <AdjustmentSummary simulation={simulation} />
        <GrowthPanel inputs={normalizedInputs} simulation={simulation} />
        <SummaryCards simulation={simulation} />
        <button className="wide-secondary-button" type="button" onClick={onMoveToAnalysis}>
          자세히 분석 보기
        </button>
      </div>
    </div>
  );
}

function AnalysisTab({ simulation }) {
  return (
    <div className="results tab-single-column">
      <section className="panel analysis-intro">
        <div className="section-heading compact-heading">
          <div>
            <p className="eyebrow">Analysis</p>
            <h2>결과를 바꾸는 핵심 변수</h2>
          </div>
        </div>
        <p>
          현재는 근무 연장 시나리오와 연도별 상세표를 제공합니다. 고급 설정을 켜면 건강보험료,
          해외 체류, 환율 가정이 자산수명에 함께 반영됩니다.
        </p>
        <div className="analysis-roadmap">
          <article><strong>기본</strong><span>수익률·생활비·퇴사나이</span></article>
          <article><strong>고급</strong><span>건보료·해외체류 수동 입력</span></article>
          <article><strong>추후</strong><span>환율 자동 업데이트</span></article>
        </div>
      </section>
      <DividendCalculator />
      <AdjustmentSummary simulation={simulation} />
      <InsightReport simulation={simulation} />
      <ScenarioComparison simulation={simulation} />
      <YearlyTable rows={simulation.targetResult.rows} />
    </div>
  );
}

function ShareTab({ normalizedInputs, simulation }) {
  const [message, setMessage] = useState('');
  const shareUrl = useMemo(() => buildShareUrl(normalizedInputs), [normalizedInputs]);
  const shareSummary = useMemo(() => buildShareSummary(normalizedInputs, simulation), [normalizedInputs, simulation]);

  const copyText = async (text, successMessage) => {
    try {
      await navigator.clipboard.writeText(text);
      setMessage(successMessage);
    } catch {
      setMessage('복사 권한이 막혀 있어요. 아래 요약을 직접 복사해주세요.');
    }
  };

  return (
    <div className="results tab-single-column share-tab">
      <section className="panel share-panel">
        <div className="section-heading compact-heading">
          <div>
            <p className="eyebrow">Share</p>
            <h2>결과를 저장하거나 공유하기</h2>
          </div>
        </div>
        <p>
          공유 기능은 개인정보를 최소화하는 방향으로 유지합니다. 이름, 이메일, 계좌 정보는 받지 않고,
          링크에는 계산에 필요한 숫자만 담습니다.
        </p>
        <div className="share-actions">
          <button type="button" onClick={() => copyText(shareSummary, '결과 요약을 복사했어요.')}>
            결과 요약 복사
          </button>
          <button type="button" onClick={() => copyText(shareUrl, '계산 링크를 복사했어요.')}>
            계산 링크 복사
          </button>
        </div>
        {message && <p className="copy-message" role="status">{message}</p>}
        <label className="share-preview">
          <span>공유 요약 미리보기</span>
          <textarea readOnly value={shareSummary} />
        </label>
      </section>

      <section className="panel share-panel soft-panel">
        <div className="section-heading compact-heading">
          <div>
            <p className="eyebrow">Community Ready</p>
            <h2>커뮤니티는 작게 연결</h2>
          </div>
        </div>
        <p>
          초기에는 자체 게시판, 로그인, 이메일 수집 없이 결과 요약을 복사해 외부 채널에서 피드백 받는 구조가 안전합니다.
        </p>
        <div className="privacy-checklist">
          <span>이름 수집 없음</span>
          <span>이메일 수집 없음</span>
          <span>민감정보 최소화</span>
          <span>참고용 고지 유지</span>
        </div>
      </section>
    </div>
  );
}

export default function App() {
  const [inputs, setInputs] = useState(loadInitialInputs);
  const [activeTab, setActiveTab] = useState('calculator');
  const normalizedInputs = useMemo(() => normalizeInputs(inputs), [inputs]);
  const simulation = useMemo(() => buildSimulation(normalizedInputs), [normalizedInputs]);

  useEffect(() => {
    localStorage.setItem(storageKey, JSON.stringify(normalizedInputs));
  }, [normalizedInputs]);

  const handleChange = (name, value) => {
    setInputs((current) => ({ ...current, [name]: value }));
  };

  const handleReset = () => {
    setInputs(defaultInputs);
    localStorage.removeItem(storageKey);
  };

  return (
    <main className="app-shell">
      <section className="hero">
        <div>
          <p className="brand">퇴사나이</p>
          <h1>내 자산으로 몇 살에 퇴사할 수 있을까?</h1>
          <p>
            생활비, 국민연금, 반퇴 소득, 건보료, 해외 체류까지 단계적으로 반영하는 한국형 FIRE 시뮬레이터입니다.
          </p>
        </div>
        <div className="hero-metric">
          <span>목표 퇴사</span>
          <strong>{normalizedInputs.targetRetirementAge}세</strong>
        </div>
      </section>

      <nav className="tab-nav" aria-label="퇴사나이 주요 기능">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            type="button"
            className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
            aria-pressed={activeTab === tab.id}
          >
            <strong>{tab.label}</strong>
            <span>{tab.description}</span>
          </button>
        ))}
      </nav>

      {activeTab === 'calculator' && (
        <CalculatorTab
          inputs={inputs}
          normalizedInputs={normalizedInputs}
          simulation={simulation}
          onChange={handleChange}
          onReset={handleReset}
          onMoveToAnalysis={() => setActiveTab('analysis')}
        />
      )}

      {activeTab === 'analysis' && <AnalysisTab simulation={simulation} />}
      {activeTab === 'share' && <ShareTab normalizedInputs={normalizedInputs} simulation={simulation} />}

      <div className="common-policy-sections">
        <PolicySections />
      </div>

      <nav className="mobile-bottom-bar">
        <button type="button" onClick={() => setActiveTab('calculator')}>계산기로 이동</button>
        <button type="button" onClick={() => navigator.clipboard.writeText(buildShareUrl(normalizedInputs))}>링크 복사</button>
      </nav>
    </main>
  );
}
