import { useEffect, useMemo, useState } from 'react';
import InputForm from './components/InputForm.jsx';
import DecisionDashboard from './components/DecisionDashboard.jsx';
import GrowthPanel from './components/GrowthPanel.jsx';
import InsightReport from './components/InsightReport.jsx';
import ScenarioComparison from './components/ScenarioComparison.jsx';
import SummaryCards from './components/SummaryCards.jsx';
import YearlyTable from './components/YearlyTable.jsx';
import { buildSimulation, defaultInputs, normalizeInputs } from './utils/retirementSimulator.js';
import { buildShareUrl, decodeInputsFromHash } from './utils/shareState.js';

const storageKey = 'toesanai-inputs-v1';

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

export default function App() {
  const [inputs, setInputs] = useState(loadInitialInputs);
  const normalizedInputs = useMemo(() => normalizeInputs(inputs), [inputs]);
  const simulation = useMemo(() => buildSimulation(normalizedInputs), [normalizedInputs]);

  useEffect(() => {
    localStorage.setItem(storageKey, JSON.stringify(normalizedInputs));
  }, [normalizedInputs]);

  const handleChange = (name, value) => {
    setInputs((current) => ({
      ...current,
      [name]: value
    }));
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
            금융자산, 생활비, 국민연금, 반퇴 소득을 넣고 퇴사 가능 나이와 자산 고갈 시점을 바로 확인하세요.
          </p>
        </div>
        <div className="hero-metric">
          <span>목표 퇴사</span>
          <strong>{normalizedInputs.targetRetirementAge}세</strong>
        </div>
      </section>

      <div className="layout">
        <InputForm values={inputs} onChange={handleChange} onReset={handleReset} />
        <div className="results">
          <DecisionDashboard simulation={simulation} />
          <GrowthPanel inputs={normalizedInputs} simulation={simulation} />
          <SummaryCards simulation={simulation} />
          <InsightReport simulation={simulation} />
          <ScenarioComparison simulation={simulation} />
          <YearlyTable rows={simulation.targetResult.rows} />
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
        </div>
      </div>
      <nav className="mobile-bottom-bar">
        <a href="#input-area">입력으로 이동</a>
        <button type="button" onClick={() => navigator.clipboard.writeText(buildShareUrl(normalizedInputs))}>
          링크 복사
        </button>
      </nav>
    </main>
  );
}
