import { useEffect, useMemo, useState } from 'react';
import { buildSimulation, defaultInputs } from '../utils/retirementSimulator.js';
import { buildShareUrl } from '../utils/shareState.js';
import '../firemap.css';

const STORAGE_KEY = 'firemap-inputs-v2';
const CONTACT_EMAIL = 'retireage.kr@gmail.com';
const BASE_URL = 'https://retire-age-kr.pages.dev/';

const questions = [
  { key: 'currentAge', type: 'age', label: '현재 나이', title: '지금 몇 살인가요?', helper: '현재 나이를 기준으로 퇴사까지 남은 시간을 계산해요.', step: 1 },
  { key: 'targetRetirementAge', type: 'age', label: '퇴사 희망 나이', title: '몇 살에 퇴사하고 싶나요?', helper: '1살 차이도 결과에 크게 영향을 줘요.', step: 1 },
  { key: 'financialAsset', type: 'money', label: '금융자산', title: '지금 금융자산은 얼마인가요?', helper: '주식, 예금, 현금처럼 퇴사 후 생활비에 쓸 수 있는 돈 기준이에요.', step: 10000000, presets: [100000000, 300000000, 500000000, 1000000000] },
  { key: 'monthlyInvestment', type: 'money', label: '월 저축액', title: '퇴사 전 매달 얼마를 모을까요?', helper: '앞으로 매달 투자하거나 저축할 금액을 입력해주세요.', step: 100000, presets: [500000, 1000000, 2000000, 3000000] },
  { key: 'monthlyLivingCost', type: 'money', label: '퇴사 후 월 생활비', title: '퇴사 후 한 달 생활비는?', helper: '주거비, 식비, 보험료, 취미, 여행비를 포함한 월 생활비예요.', step: 100000, presets: [2500000, 3500000, 5000000, 7000000] }
];

function cleanNumber(value) {
  return Number(String(value ?? '').replace(/[^\d.-]/g, '')) || 0;
}

function loadInputs() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) return { ...defaultInputs, ...JSON.parse(saved) };
  } catch {
    return defaultInputs;
  }
  return defaultInputs;
}

function formatWon(value) {
  const amount = cleanNumber(value);
  if (Math.abs(amount) >= 100000000) {
    const eok = amount / 100000000;
    return `${Number.isInteger(eok) ? eok.toFixed(0) : eok.toFixed(1)}억`;
  }
  if (Math.abs(amount) >= 10000) return `${Math.round(amount / 10000).toLocaleString('ko-KR')}만`;
  return `${Math.round(amount).toLocaleString('ko-KR')}원`;
}

function formatValue(value, type) {
  return type === 'age' ? `${cleanNumber(value)}세` : formatWon(value);
}

function runwayText(simulation) {
  return simulation.targetResult.depletionAge
    ? `${simulation.targetResult.depletionAge}세`
    : `${simulation.inputs.simulationUntilAge}세 이상`;
}

function scenarioEndAge(simulation) {
  return simulation.targetResult.depletionAge || simulation.inputs.simulationUntilAge;
}

function buildScenario(inputs, patch) {
  return buildSimulation({ ...inputs, ...patch });
}

function deltaText(base, next) {
  const baseAge = scenarioEndAge(base);
  const nextAge = scenarioEndAge(next);
  const diff = Math.max(0, nextAge - baseAge);
  if (!base.targetResult.depletionAge && !next.targetResult.depletionAge) return '이미 장기 유지';
  return diff > 0 ? `${diff}년 개선` : '변화 작음';
}

function Header({ tag, onReset }) {
  return (
    <header className="fm-topbar">
      <div className="fm-logo">🔥 파이어맵</div>
      <div className="fm-actions"><span>{tag}</span><button type="button" onClick={onReset}>초기화</button></div>
    </header>
  );
}

function Home({ onStart, onReset }) {
  return (
    <main className="fm-screen">
      <Header tag="2분 계산" onReset={onReset} />
      <section className="fm-hero">
        <p>퇴사나이 계산기</p>
        <h1>내 돈으로 몇 살까지 버틸 수 있을까?</h1>
        <span>퇴사나이와 FIRE를 앞당기는 방법을 2분 만에 계산해보세요.</span>
        <button type="button" onClick={onStart}>시작하기</button>
      </section>
      <section className="fm-card fm-two">
        <strong>입력값은 브라우저에만 저장</strong>
        <strong>투자·세무·법률 자문 아님</strong>
      </section>
      <section className="fm-card fm-text-card">
        <b>민감한 금액은 공유 전 확인해주세요</b>
        <p>내 조건 링크를 공유하면 일부 입력값이 링크에 포함될 수 있어요.</p>
      </section>
    </main>
  );
}

function Question({ step, inputs, onChange, onPrev, onNext, onReset }) {
  const question = questions[step];
  const value = cleanNumber(inputs[question.key]);
  const isAge = question.type === 'age';
  const progress = `${((step + 1) / questions.length) * 100}%`;
  const changeBy = (amount) => onChange(question.key, Math.max(0, value + amount));

  return (
    <main className="fm-screen">
      <Header tag={`질문 ${step + 1}/${questions.length}`} onReset={onReset} />
      <div className="fm-progress"><i style={{ width: progress }} /></div>
      <section className="fm-card fm-question">
        <em>{question.label}</em>
        <h2>{question.title}</h2>
        <p>{question.helper}</p>
        <div className="fm-stepper">
          <button type="button" onClick={() => changeBy(-question.step)}>-</button>
          <input inputMode="numeric" value={value} aria-label={question.title} onChange={(event) => onChange(question.key, event.target.value)} />
          <button type="button" onClick={() => changeBy(question.step)}>+</button>
        </div>
        <strong>{formatValue(value, question.type)}</strong>
        {isAge ? <small>나이는 빠른 선택 버튼 없이 1세 단위로만 조절해요.</small> : (
          <div className="fm-chips">
            {question.presets.map((preset) => <button type="button" key={preset} onClick={() => onChange(question.key, preset)}>{formatWon(preset)}</button>)}
          </div>
        )}
      </section>
      <nav className="fm-bottom-nav">
        <button type="button" onClick={onPrev}>이전</button>
        <button type="button" onClick={onNext}>{step === questions.length - 1 ? '결과 보기' : '다음'}</button>
      </nav>
    </main>
  );
}

function ResultHero({ simulation }) {
  return (
    <section className="fm-card fm-result">
      <p>내 FIRE 현재 위치</p>
      <h2>{simulation.inputs.targetRetirementAge}세에 퇴사하면<br /><b>{runwayText(simulation)}</b>까지 버틸 수 있어요.</h2>
      <span>{simulation.earliestRetirementAge ? `현재 가정으로는 ${simulation.earliestRetirementAge}세 퇴사가 더 안전해 보여요.` : '현재 가정에서는 더 늦은 퇴사가 필요해 보여요.'}</span>
      <div><small>자산수명 점수</small><strong>{simulation.survivalScore}</strong><small>/100</small></div>
    </section>
  );
}

function ImprovementCards({ inputs, simulation }) {
  const lowerCostValue = Math.max(1200000, inputs.monthlyLivingCost - 1500000);
  const lowerCost = buildScenario(inputs, { monthlyLivingCost: lowerCostValue });
  const earnAfterRetire = buildScenario(inputs, { partTimeIncomeAfterRetirement: inputs.partTimeIncomeAfterRetirement + 1000000 });
  const workMore = buildScenario(inputs, { targetRetirementAge: inputs.targetRetirementAge + 1 });
  const saveMore = buildScenario(inputs, { monthlyInvestment: inputs.monthlyInvestment + 1000000 });
  const cards = [
    ['생활비', `월 생활비를 ${formatWon(lowerCostValue)}으로 낮추면`, lowerCost],
    ['퇴사 후 현금흐름', '퇴사 후 월 100만 원 벌면', earnAfterRetire],
    ['근무연장', '1년 더 근무하면', workMore],
    ['퇴사 전 저축', '퇴사 전 월 100만 원 더 모으면', saveMore]
  ];

  return (
    <section>
      <h2 className="fm-section-title">🔥 FIRE를 앞당기는 방법</h2>
      <div className="fm-card-grid">
        {cards.map(([tag, title, scenario]) => (
          <article className="fm-card fm-mini" key={title}>
            <em>{tag}</em>
            <h3>{title}</h3>
            <strong>{runwayText(scenario)}</strong>
            <p>{deltaText(simulation, scenario)}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

function Result({ inputs, simulation, onReset, onMove }) {
  return (
    <main className="fm-screen fm-scroll">
      <Header tag="결과" onReset={onReset} />
      <ResultHero simulation={simulation} />
      <div className="fm-ad">광고</div>
      <ImprovementCards inputs={inputs} simulation={simulation} />
      <div className="fm-menu">
        <button type="button" onClick={() => onMove('experiment')}>조건 바꿔보기</button>
        <button type="button" onClick={() => onMove('curation')}>도시 시나리오</button>
        <button type="button" onClick={() => onMove('share')}>공유하기</button>
      </div>
    </main>
  );
}

function Experiment({ inputs, onChange, simulation, onReset }) {
  const lowerCost = buildScenario(inputs, { monthlyLivingCost: Math.max(1200000, inputs.monthlyLivingCost - 1500000) });
  const rows = simulation.targetResult.rows.filter((row, index) => index === 0 || row.age % 5 === 0 || row.age === inputs.targetRetirementAge).slice(0, 12);
  const improvedRows = lowerCost.targetResult.rows;
  const max = Math.max(...rows.map((row) => Math.max(row.financialAsset, improvedRows.find((item) => item.age === row.age)?.financialAsset || 0)), 1);
  const points = (key) => rows.map((row, index) => {
    const matched = improvedRows.find((item) => item.age === row.age) || row;
    const value = key === 'improved' ? matched.financialAsset : row.financialAsset;
    const x = 24 + (index / Math.max(1, rows.length - 1)) * 312;
    const y = 150 - (Math.max(0, value) / max) * 120;
    return `${x},${Math.max(20, y)}`;
  }).join(' ');
  const adjust = (key, amount) => onChange(key, Math.max(0, cleanNumber(inputs[key]) + amount));

  return (
    <main className="fm-screen fm-scroll">
      <Header tag="실험" onReset={onReset} />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">조건 바꿔보기</p>
        <h2>숫자를 바꾸면 결과가 바로 달라져요</h2>
        <Adjust label="퇴사 나이" value={`${inputs.targetRetirementAge}세`} minus={() => adjust('targetRetirementAge', -1)} plus={() => adjust('targetRetirementAge', 1)} />
        <Adjust label="생활비" value={formatWon(inputs.monthlyLivingCost)} minus={() => adjust('monthlyLivingCost', -100000)} plus={() => adjust('monthlyLivingCost', 100000)} />
        <Adjust label="월 저축액" value={formatWon(inputs.monthlyInvestment)} minus={() => adjust('monthlyInvestment', -100000)} plus={() => adjust('monthlyInvestment', 100000)} />
      </section>
      <section className="fm-card fm-graph">
        <p className="fm-kicker">연도별 자산 그래프</p>
        <h2>현재 계획과 개선안 비교</h2>
        <svg viewBox="0 0 360 180" role="img" aria-label="자산 그래프">
          <line x1="24" y1="150" x2="340" y2="150" />
          <polyline points={points('current')} className="current" />
          <polyline points={points('improved')} className="improved" />
        </svg>
      </section>
    </main>
  );
}

function Adjust({ label, value, minus, plus }) {
  return <div className="fm-adjust"><span>{label}</span><strong>{value}</strong><button type="button" onClick={minus}>-</button><button type="button" onClick={plus}>+</button></div>;
}

function Curation({ inputs, onReset }) {
  const lower = Math.max(1200000, inputs.monthlyLivingCost - 1500000);
  return (
    <main className="fm-screen fm-scroll">
      <Header tag="큐레이션" onReset={onReset} />
      <Info tag="국내 저비용 도시" title="전주·원주·강릉으로 생활비를 낮추면?" text={`월 생활비 ${formatWon(inputs.monthlyLivingCost)}을 ${formatWon(lower)} 수준으로 낮추는 시나리오를 비교합니다.`} note="최신 공식 자료가 확인된 항목만 보여드려요." />
      <Info tag="해외 저비용 생활" title="치앙마이에서 연 3개월 살아보면?" text="최근 환율과 예상 생활비를 기준으로 FIRE 필요금액이 얼마나 줄어드는지 계산합니다." note="3개월 이상 체류 시 건강보험료 조정 가능성이 있을 수 있어요. 실제 적용 여부는 개인 상황에 따라 달라질 수 있습니다." />
      <Info tag="현실감 진단" title="내 생활비는 상위 몇 %일까?" text="가구원수별 소비지출 자료가 확인된 경우, 내 FIRE 생활비가 어느 정도 수준인지 비교합니다." note="자료 기준일과 출처를 함께 안내해요." />
    </main>
  );
}

function Info({ tag, title, text, note }) {
  return <section className="fm-card fm-info"><em>{tag}</em><h2>{title}</h2><p>{text}</p><small>{note}</small></section>;
}

function Share({ inputs, simulation, onReset }) {
  const [message, setMessage] = useState('');
  const shareUrl = buildShareUrl(inputs);
  const shareText = `파이어맵 계산 결과\n${inputs.targetRetirementAge}세 퇴사 → ${runwayText(simulation)}까지\n퇴사 후 월 100만 원 벌기, 1년 더 근무하기, 생활비 줄이기 효과도 비교해봤어요.\n\n${BASE_URL}`;
  const copy = async (text, label) => {
    try {
      await navigator.clipboard.writeText(text);
      setMessage(label);
      window.setTimeout(() => setMessage(''), 1800);
    } catch {
      setMessage('복사 권한이 막혀 있어요. 직접 복사해주세요.');
    }
  };

  return (
    <main className="fm-screen fm-scroll">
      <Header tag="공유" onReset={onReset} />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">공유</p>
        <h2>결과카드 또는 기본 링크 공유</h2>
        <div className="fm-share-preview"><strong>{inputs.targetRetirementAge}세 퇴사 → {runwayText(simulation)}까지</strong><p>퇴사 후 월 100만 원 벌기, 1년 더 근무하기, 생활비 줄이기 효과도 비교해봤어요.</p></div>
        <button className="fm-primary" type="button" onClick={() => copy(shareText, '결과카드 문구 복사됨')}>결과카드 문구 복사</button>
        <button className="fm-secondary" type="button" onClick={() => copy(BASE_URL, '앱 기본 링크 복사됨')}>앱 기본 링크 복사</button>
        <button className="fm-secondary" type="button" onClick={() => copy(shareUrl, '내 조건 링크 복사됨')}>내 조건 링크 복사</button>
        {message && <div className="fm-toast">{message}</div>}
      </section>
      <section className="fm-card fm-info">
        <em>운영 안내</em><h2>개인정보·면책·문의</h2>
        <p>입력값은 서버로 전송하지 않고 이 브라우저에 저장됩니다. 본 서비스는 투자·세무·법률 자문이 아닌 참고용 계산입니다.</p>
        <small>피드백·협업 문의: <b>{CONTACT_EMAIL}</b></small>
      </section>
    </main>
  );
}

export default function FireMapMVP() {
  const [inputs, setInputs] = useState(loadInputs);
  const [screen, setScreen] = useState('home');
  const [step, setStep] = useState(0);
  const simulation = useMemo(() => buildSimulation(inputs), [inputs]);

  useEffect(() => {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(inputs)); } catch { /* ignore */ }
  }, [inputs]);

  const onChange = (key, value) => setInputs((current) => ({ ...current, [key]: cleanNumber(value) }));
  const reset = () => { setInputs(defaultInputs); setStep(0); setScreen('home'); try { localStorage.removeItem(STORAGE_KEY); } catch { /* ignore */ } };
  const next = () => step >= questions.length - 1 ? setScreen('result') : setStep((current) => current + 1);

  if (screen === 'home') return <Home onStart={() => setScreen('question')} onReset={reset} />;
  if (screen === 'question') return <Question step={step} inputs={inputs} onChange={onChange} onPrev={() => step === 0 ? setScreen('home') : setStep((current) => current - 1)} onNext={next} onReset={reset} />;
  if (screen === 'experiment') return <Experiment inputs={inputs} onChange={onChange} simulation={simulation} onReset={reset} />;
  if (screen === 'curation') return <Curation inputs={inputs} onReset={reset} />;
  if (screen === 'share') return <Share inputs={inputs} simulation={simulation} onReset={reset} />;
  return <Result inputs={inputs} simulation={simulation} onReset={reset} onMove={setScreen} />;
}
