import { useEffect, useMemo, useState } from 'react';
import { ArrowLeft, ArrowRight, Clipboard, Link2, RotateCcw, Share2 } from 'lucide-react';
import { buildSimulation, defaultInputs } from '../utils/retirementSimulator.js';
import { buildShareUrl } from '../utils/shareState.js';
import '../firemap.css';

const STORAGE_KEY = 'firemap-inputs-v2';
const BASE_URL = 'https://retire-age-kr.pages.dev/';
const CONTACT_EMAIL = 'retireage.kr@gmail.com';

const questions = [
  {
    key: 'currentAge',
    type: 'age',
    label: '현재 나이',
    title: '지금 몇 살인가요?',
    helper: '현재 나이를 기준으로 퇴사까지 남은 시간을 계산해요.',
    step: 1
  },
  {
    key: 'targetRetirementAge',
    type: 'age',
    label: '퇴사 희망 나이',
    title: '몇 살에 퇴사하고 싶나요?',
    helper: '1살 차이도 결과에 크게 영향을 줘요.',
    step: 1
  },
  {
    key: 'financialAsset',
    type: 'money',
    label: '금융자산',
    title: '지금 금융자산은 얼마인가요?',
    helper: '주식, 예금, 현금처럼 퇴사 후 생활비에 쓸 수 있는 돈 기준이에요.',
    step: 10000000,
    presets: [100000000, 300000000, 500000000, 1000000000]
  },
  {
    key: 'monthlyInvestment',
    type: 'money',
    label: '월 저축액',
    title: '퇴사 전 매달 얼마를 모을까요?',
    helper: '앞으로 매달 투자하거나 저축할 금액을 입력해주세요.',
    step: 100000,
    presets: [500000, 1000000, 2000000, 3000000]
  },
  {
    key: 'monthlyLivingCost',
    type: 'money',
    label: '퇴사 후 월 생활비',
    title: '퇴사 후 한 달 생활비는?',
    helper: '주거비, 식비, 보험료, 취미, 여행비를 포함한 월 생활비예요.',
    step: 100000,
    presets: [2500000, 3500000, 5000000, 7000000]
  }
];

function loadInputs() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) return { ...defaultInputs, ...JSON.parse(saved) };
  } catch {
    return defaultInputs;
  }
  return defaultInputs;
}

function numberValue(value) {
  return Number(String(value ?? '').replace(/[^\d.-]/g, '')) || 0;
}

function formatWon(value) {
  const amount = numberValue(value);
  if (Math.abs(amount) >= 100000000) return `${(amount / 100000000).toFixed(amount % 100000000 === 0 ? 0 : 1)}억`;
  if (Math.abs(amount) >= 10000) return `${Math.round(amount / 10000).toLocaleString('ko-KR')}만`;
  return `${Math.round(amount).toLocaleString('ko-KR')}원`;
}

function formatFullWon(value) {
  const text = formatWon(value);
  return text.endsWith('원') ? text : `${text} 원`;
}

function formatInput(value, type) {
  if (type === 'age') return `${numberValue(value).toLocaleString('ko-KR')}세`;
  return formatWon(value);
}

function getRunwayText(simulation) {
  return simulation.targetResult.depletionAge
    ? `${simulation.targetResult.depletionAge}세`
    : `${simulation.inputs.simulationUntilAge}세 이상`;
}

function scenarioAge(simulation) {
  return simulation.targetResult.depletionAge || simulation.inputs.simulationUntilAge;
}

function compareLabel(base, alternative) {
  const baseAge = scenarioAge(base);
  const altAge = scenarioAge(alternative);
  const diff = Math.max(0, altAge - baseAge);
  if (!base.targetResult.depletionAge && !alternative.targetResult.depletionAge) return '이미 장기 유지';
  if (diff <= 0) return '변화 작음';
  return `${diff}년 개선`;
}

function buildScenario(inputs, patch) {
  return buildSimulation({ ...inputs, ...patch });
}

function makeGraphRows(base, improved) {
  return base.targetResult.rows
    .filter((row, index) => index === 0 || row.age === base.inputs.targetRetirementAge || row.age % 5 === 0 || row.age === base.inputs.simulationUntilAge)
    .slice(0, 14)
    .map((row) => {
      const improvedRow = improved.targetResult.rows.find((item) => item.age === row.age) || row;
      return {
        age: row.age,
        current: Math.max(0, row.financialAsset),
        improved: Math.max(0, improvedRow.financialAsset)
      };
    });
}

function Header({ tag, onReset }) {
  return (
    <header className="fm-topbar">
      <div className="fm-logo">🔥 파이어맵</div>
      <div className="fm-top-actions">
        <span>{tag}</span>
        <button type="button" onClick={onReset} aria-label="초기화"><RotateCcw size={15} /></button>
      </div>
    </header>
  );
}

function HomeScreen({ onStart, onReset }) {
  return (
    <main className="fm-screen">
      <Header tag="2분 계산" onReset={onReset} />
      <section className="fm-hero">
        <p className="fm-eyebrow">퇴사나이 계산기</p>
        <h1>내 돈으로 몇 살까지 버틸 수 있을까?</h1>
        <p>퇴사나이와 FIRE를 앞당기는 방법을 2분 만에 계산해보세요.</p>
        <button className="fm-primary" type="button" onClick={onStart}>시작하기</button>
      </section>
      <section className="fm-card fm-trust-card">
        <span>입력값은 브라우저에만 저장</span>
        <span>투자·세무·법률 자문 아님</span>
      </section>
      <section className="fm-card fm-policy-card">
        <strong>민감한 금액은 공유 전 확인해주세요</strong>
        <p>내 조건 링크를 공유하면 일부 입력값이 링크에 포함될 수 있어요.</p>
      </section>
    </main>
  );
}

function QuestionScreen({ step, inputs, onChange, onPrev, onNext, onReset }) {
  const question = questions[step];
  const value = numberValue(inputs[question.key]);
  const progress = ((step + 1) / questions.length) * 100;
  const isAge = question.type === 'age';

  const changeBy = (amount) => {
    onChange(question.key, Math.max(0, value + amount));
  };

  return (
    <main className="fm-screen">
      <Header tag={`질문 ${step + 1}/${questions.length}`} onReset={onReset} />
      <div className="fm-progress"><i style={{ width: `${progress}%` }} /></div>
      <section className="fm-card fm-question-card">
        <span className="fm-pill">{question.label}</span>
        <h2>{question.title}</h2>
        <p>{question.helper}</p>
        <div className="fm-stepper">
          <button type="button" onClick={() => changeBy(-question.step)}>-</button>
          <input
            inputMode="numeric"
            value={value}
            onChange={(event) => onChange(question.key, event.target.value)}
            aria-label={question.title}
          />
          <button type="button" onClick={() => changeBy(question.step)}>+</button>
        </div>
        <strong className="fm-formatted-value">{formatInput(value, question.type)}</strong>
        {isAge ? (
          <div className="fm-note">나이는 빠른 선택 버튼 없이 1세 단위로만 조절해요.</div>
        ) : (
          <div className="fm-chip-row">
            {question.presets.map((preset) => (
              <button key={preset} type="button" onClick={() => onChange(question.key, preset)}>{formatInput(preset, 'money')}</button>
            ))}
          </div>
        )}
      </section>
      <nav className="fm-bottom-nav">
        <button type="button" onClick={onPrev} disabled={step === 0}><ArrowLeft size={17} /> 이전</button>
        <button type="button" onClick={onNext}>{step === questions.length - 1 ? '결과 보기' : '다음'} <ArrowRight size={17} /></button>
      </nav>
    </main>
  );
}

function ResultHero({ simulation }) {
  const safeAge = simulation.earliestRetirementAge;
  return (
    <section className="fm-card fm-result-hero">
      <p className="fm-eyebrow">내 FIRE 현재 위치</p>
      <h2>{simulation.inputs.targetRetirementAge}세에 퇴사하면<br /><b>{getRunwayText(simulation)}</b>까지 버틸 수 있어요.</h2>
      <p>{safeAge ? `현재 가정으로는 ${safeAge}세 퇴사가 더 안전해 보여요.` : '현재 가정에서는 더 늦은 퇴사가 필요해 보여요.'}</p>
      <div className="fm-score"><span>자산수명 점수</span><strong>{simulation.survivalScore}</strong><small>/100</small></div>
    </section>
  );
}

function ImprovementCards({ inputs, simulation }) {
  const lowerCostValue = Math.max(1200000, inputs.monthlyLivingCost - 1500000);
  const lowerCost = buildScenario(inputs, { monthlyLivingCost: lowerCostValue });
  const earnAfterRetire = buildScenario(inputs, { partTimeIncomeAfterRetirement: inputs.partTimeIncomeAfterRetirement + 1000000 });
  const workMore = buildScenario(inputs, { targetRetirementAge: inputs.targetRetirementAge + 1 });
  const saveMoreBeforeRetire = buildScenario(inputs, { monthlyInvestment: inputs.monthlyInvestment + 1000000 });

  const cards = [
    { tag: '생활비', title: `월 생활비를 ${formatWon(lowerCostValue)}으로 낮추면`, value: getRunwayText(lowerCost), delta: compareLabel(simulation, lowerCost) },
    { tag: '퇴사 후 현금흐름', title: '퇴사 후 월 100만 원 벌면', value: getRunwayText(earnAfterRetire), delta: compareLabel(simulation, earnAfterRetire) },
    { tag: '근무연장', title: '1년 더 근무하면', value: getRunwayText(workMore), delta: compareLabel(simulation, workMore) },
    { tag: '퇴사 전 저축', title: '퇴사 전 월 100만 원 더 모으면', value: getRunwayText(saveMoreBeforeRetire), delta: compareLabel(simulation, saveMoreBeforeRetire) }
  ];

  return (
    <section>
      <div className="fm-section-title"><i>🔥</i><h2>FIRE를 앞당기는 방법</h2></div>
      <div className="fm-grid-2">
        {cards.map((card) => (
          <article className="fm-card fm-mini-card" key={card.title}>
            <span>{card.tag}</span>
            <h3>{card.title}</h3>
            <strong>{card.value}</strong>
            <p>{card.delta}</p>
          </article>
        ))}
      </div>
    </section>
  );
}

function AdSlot() {
  return <div className="fm-ad-slot">광고</div>;
}

function ExperimentScreen({ inputs, onChange, simulation, onReset }) {
  const lowerCost = buildScenario(inputs, { monthlyLivingCost: Math.max(1200000, inputs.monthlyLivingCost - 1500000) });
  const earnMore = buildScenario(inputs, { partTimeIncomeAfterRetirement: inputs.partTimeIncomeAfterRetirement + 1000000 });
  const workMore = buildScenario(inputs, { targetRetirementAge: inputs.targetRetirementAge + 1 });
  const best = [lowerCost, earnMore, workMore].sort((a, b) => scenarioAge(b) - scenarioAge(a))[0];
  const rows = makeGraphRows(simulation, best);
  const maxValue = Math.max(...rows.flatMap((row) => [row.current, row.improved]), 1);
  const width = 360;
  const height = 180;
  const pad = 24;
  const points = (key) => rows.map((row, index) => {
    const x = pad + (index / Math.max(1, rows.length - 1)) * (width - pad * 2);
    const y = 150 - (row[key] / maxValue) * 120;
    return `${x},${Math.max(20, y)}`;
  }).join(' ');

  const adjust = (key, amount) => onChange(key, Math.max(0, numberValue(inputs[key]) + amount));

  return (
    <main className="fm-screen fm-scroll-screen">
      <Header tag="실험" onReset={onReset} />
      <section className="fm-card">
        <p className="fm-eyebrow">조건 바꿔보기</p>
        <h2 className="fm-card-title">숫자를 바꾸면 결과가 바로 달라져요</h2>
        <div className="fm-adjust-list">
          <AdjustItem label="퇴사 나이" value={`${inputs.targetRetirementAge}세`} onMinus={() => adjust('targetRetirementAge', -1)} onPlus={() => adjust('targetRetirementAge', 1)} />
          <AdjustItem label="생활비" value={formatWon(inputs.monthlyLivingCost)} onMinus={() => adjust('monthlyLivingCost', -100000)} onPlus={() => adjust('monthlyLivingCost', 100000)} />
          <AdjustItem label="월 저축액" value={formatWon(inputs.monthlyInvestment)} onMinus={() => adjust('monthlyInvestment', -100000)} onPlus={() => adjust('monthlyInvestment', 100000)} />
          <AdjustItem label="해외 체류" value={`${inputs.overseasMonthsPerYear || 0}개월`} onMinus={() => adjust('overseasMonthsPerYear', -1)} onPlus={() => adjust('overseasMonthsPerYear', 1)} />
        </div>
      </section>
      <section className="fm-card fm-graph-card">
        <p className="fm-eyebrow">연도별 자산 그래프</p>
        <h2 className="fm-card-title">현재 계획과 개선안 비교</h2>
        <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label="자산 그래프">
          <line x1="24" y1="150" x2="340" y2="150" stroke="#f0dcc4" strokeWidth="2" />
          <line x1="24" y1="20" x2="24" y2="150" stroke="#f0dcc4" strokeWidth="2" />
          <polyline points={points('current')} fill="none" stroke="#9ca3af" strokeWidth="5" strokeLinecap="round" strokeLinejoin="round" />
          <polyline points={points('improved')} fill="none" stroke="#ea580c" strokeWidth="5" strokeLinecap="round" strokeLinejoin="round" />
        </svg>
        <div className="fm-legend"><span><i className="current" />현재</span><span><i className="improved" />개선안</span></div>
      </section>
    </main>
  );
}

function AdjustItem({ label, value, onMinus, onPlus }) {
  return (
    <div className="fm-adjust-item">
      <div><span>{label}</span><strong>{value}</strong></div>
      <div className="fm-small-step"><button type="button" onClick={onMinus}>-</button><button type="button" onClick={onPlus}>+</button></div>
    </div>
  );
}

function CurationScreen({ inputs, onReset }) {
  const lowerCostValue = Math.max(1200000, inputs.monthlyLivingCost - 1500000);
  return (
    <main className="fm-screen fm-scroll-screen">
      <Header tag="큐레이션" onReset={onReset} />
      <section className="fm-card fm-city-card">
        <span className="fm-pill">국내 저비용 도시</span>
        <h3>전주·원주·강릉으로 생활비를 낮추면?</h3>
        <p>월 생활비 {formatWon(inputs.monthlyLivingCost)}을 {formatWon(lowerCostValue)} 수준으로 낮추는 시나리오를 비교합니다.</p>
        <small>최신 공식 자료가 확인된 항목만 보여드려요.</small>
      </section>
      <section className="fm-card fm-city-card">
        <span className="fm-pill">해외 저비용 생활</span>
        <h3>치앙마이에서 연 3개월 살아보면?</h3>
        <p>최근 환율과 예상 생활비를 기준으로 FIRE 필요금액이 얼마나 줄어드는지 계산합니다.</p>
        <small>3개월 이상 체류 시 건강보험료 조정 가능성이 있을 수 있어요. 실제 적용 여부는 개인 상황에 따라 달라질 수 있습니다.</small>
      </section>
      <section className="fm-card fm-city-card">
        <span className="fm-pill">현실감 진단</span>
        <h3>내 생활비는 상위 몇 %일까?</h3>
        <p>가구원수별 소비지출 자료가 확인된 경우, 내 FIRE 생활비가 어느 정도 수준인지 비교합니다.</p>
        <small>자료 기준일과 출처를 함께 안내해요.</small>
      </section>
    </main>
  );
}

function ShareScreen({ inputs, simulation, onReset }) {
  const [message, setMessage] = useState('');
  const shareUrl = buildShareUrl(inputs);
  const resultText = [
    '파이어맵 계산 결과',
    `${inputs.targetRetirementAge}세 퇴사 → ${getRunwayText(simulation)}까지`,
    '퇴사 후 월 100만 원 벌기, 1년 더 근무하기, 생활비 줄이기 효과도 비교해봤어요.',
    '',
    BASE_URL
  ].join('\n');

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
    <main className="fm-screen fm-scroll-screen">
      <Header tag="공유" onReset={onReset} />
      <section className="fm-card">
        <p className="fm-eyebrow">공유</p>
        <h2 className="fm-card-title">결과카드 또는 기본 링크 공유</h2>
        <div className="fm-share-preview">
          <strong>{inputs.targetRetirementAge}세 퇴사 → {getRunwayText(simulation)}까지</strong>
          <p>퇴사 후 월 100만 원 벌기, 1년 더 근무하기, 생활비 줄이기 효과도 비교해봤어요.</p>
        </div>
        <button className="fm-primary" type="button" onClick={() => copy(resultText, '결과카드 문구 복사됨')}><Share2 size={18} /> 결과카드 문구 복사</button>
        <button className="fm-secondary" type="button" onClick={() => copy(BASE_URL, '앱 기본 링크 복사됨')}><Link2 size={18} /> 앱 기본 링크 복사</button>
        <button className="fm-secondary" type="button" onClick={() => copy(shareUrl, '내 조건 링크 복사됨')}><Clipboard size={18} /> 내 조건 링크 복사</button>
        {message && <div className="fm-toast">{message}</div>}
      </section>
      <section className="fm-card fm-policy-card">
        <span className="fm-pill">운영 안내</span>
        <h3>개인정보·면책·문의</h3>
        <p>입력값은 서버로 전송하지 않고 이 브라우저에 저장됩니다. 본 서비스는 투자·세무·법률 자문이 아닌 참고용 계산입니다.</p>
        <small>피드백·협업 문의: <b>{CONTACT_EMAIL}</b></small>
      </section>
    </main>
  );
}

function ResultScreen({ inputs, simulation, onReset, onNavigate }) {
  return (
    <main className="fm-screen fm-scroll-screen">
      <Header tag="결과" onReset={onReset} />
      <ResultHero simulation={simulation} />
      <AdSlot />
      <ImprovementCards inputs={inputs} simulation={simulation} />
      <div className="fm-result-actions">
        <button type="button" onClick={() => onNavigate('experiment')}>조건 바꿔보기</button>
        <button type="button" onClick={() => onNavigate('curation')}>도시 시나리오</button>
        <button type="button" onClick={() => onNavigate('share')}>공유하기</button>
      </div>
    </main>
  );
}

export default function FireMapMVP() {
  const [inputs, setInputs] = useState(loadInputs);
  const [screen, setScreen] = useState('home');
  const [step, setStep] = useState(0);
  const simulation = useMemo(() => buildSimulation(inputs), [inputs]);

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(inputs));
    } catch {
      // ignore local storage failures
    }
  }, [inputs]);

  const onChange = (key, value) => {
    setInputs((current) => ({ ...current, [key]: numberValue(value) }));
  };

  const reset = () => {
    setInputs(defaultInputs);
    setStep(0);
    setScreen('home');
    try { localStorage.removeItem(STORAGE_KEY); } catch { /* ignore */ }
  };

  const nextQuestion = () => {
    if (step >= questions.length - 1) {
      setScreen('result');
      window.scrollTo({ top: 0, behavior: 'smooth' });
      return;
    }
    setStep((current) => current + 1);
  };

  if (screen === 'home') return <HomeScreen onStart={() => setScreen('question')} onReset={reset} />;
  if (screen === 'question') {
    return (
      <QuestionScreen
        step={step}
        inputs={inputs}
        onChange={onChange}
        onPrev={() => step === 0 ? setScreen('home') : setStep((current) => current - 1)}
        onNext={nextQuestion}
        onReset={reset}
      />
    );
  }
  if (screen === 'experiment') return <ExperimentScreen inputs={inputs} onChange={onChange} simulation={simulation} onReset={reset} />;
  if (screen === 'curation') return <CurationScreen inputs={inputs} onReset={reset} />;
  if (screen === 'share') return <ShareScreen inputs={inputs} simulation={simulation} onReset={reset} />;
  return <ResultScreen inputs={inputs} simulation={simulation} onReset={reset} onNavigate={setScreen} />;
}
