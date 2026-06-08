import { useEffect, useMemo, useState } from 'react';
import { buildSimulation, defaultInputs } from '../utils/retirementSimulator.js';
import { buildShareUrl } from '../utils/shareState.js';
import '../firemap.css';
import '../firemap-overrides.css';

const STORAGE_KEY = 'firemap-inputs-v2';
const CONTACT_EMAIL = 'retireage.kr@gmail.com';
const BASE_URL = 'https://retire-age-kr.pages.dev/';

const questions = [
  { key: 'currentAge', type: 'age', label: '현재 나이', title: '지금 몇 살인가요?', helper: '현재 나이를 기준으로 퇴사까지 남은 시간을 계산해요.', step: 1 },
  { key: 'targetRetirementAge', type: 'age', label: '퇴사 희망 나이', title: '몇 살에 퇴사하고 싶나요?', helper: '1살 차이도 결과에 크게 영향을 줘요.', step: 1 },
  { key: 'financialAsset', type: 'money', label: '금융자산', title: '지금 금융자산은 얼마인가요?', helper: '주식, 예금, 현금처럼 퇴사 후 생활비에 쓸 수 있는 돈 기준이에요.', step: 1000000, presets: [100000000, 300000000, 500000000, 1000000000], unit: '100만 원 단위' },
  { key: 'monthlyInvestment', type: 'money', label: '월 저축액', title: '퇴사 전 매달 얼마를 모을까요?', helper: '앞으로 매달 투자하거나 저축할 금액을 입력해주세요.', step: 100000, presets: [500000, 1000000, 2000000, 3000000], unit: '10만 원 단위' },
  { key: 'monthlyLivingCost', type: 'money', label: '퇴사 후 월 생활비', title: '퇴사 후 한 달 생활비는?', helper: '주거비, 식비, 보험료, 취미, 여행비를 포함한 월 생활비예요.', step: 100000, presets: [2500000, 3500000, 5000000, 7000000], unit: '10만 원 단위' }
];

const domesticCities = [
  ['전주', 3500000, '주거비와 생활비를 낮추면서 도시 인프라를 유지하는 국내형 시나리오'],
  ['원주', 3300000, '수도권 접근성과 낮은 주거비를 함께 보는 반퇴형 시나리오'],
  ['강릉', 3700000, '해안 생활 선호자를 위한 생활비 절감·삶의 만족도 균형 시나리오']
];

const overseasCities = [
  ['치앙마이', 2600000, '연 3개월 체류 기준. 생활비 절감과 건보료 조정 가능성을 함께 확인'],
  ['다낭', 2800000, '따뜻한 기후와 낮은 체류비를 반영한 단기 해외살이 시나리오'],
  ['쿠알라룸푸르', 3200000, '도시 인프라와 영어 생활권을 고려한 해외 FIRE 후보지']
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

function formatEok(value) {
  return `${(Math.max(0, cleanNumber(value)) / 100000000).toFixed(1)}억`;
}

function formatValue(value, type) {
  return type === 'age' ? `${cleanNumber(value)}세` : formatWon(value);
}

function runwayText(simulation) {
  return simulation.targetResult.depletionAge ? `${simulation.targetResult.depletionAge}세` : `${simulation.inputs.simulationUntilAge}세 이상`;
}

function scenarioEndAge(simulation) {
  return simulation.targetResult.depletionAge || simulation.inputs.simulationUntilAge;
}

function buildScenario(inputs, patch) {
  return buildSimulation({ ...inputs, ...patch });
}

function deltaText(base, next) {
  const diff = Math.max(0, scenarioEndAge(next) - scenarioEndAge(base));
  if (!base.targetResult.depletionAge && !next.targetResult.depletionAge) return '이미 장기 유지';
  return diff > 0 ? `${diff}년 개선` : '변화 작음';
}

function Header({ tag, onReset, onBack }) {
  const resetSafely = () => {
    if (window.confirm('입력값을 초기화하고 처음으로 돌아갈까요?')) onReset();
  };
  return (
    <header className="fm-topbar">
      <div className="fm-logo">🔥 파이어맵</div>
      <div className="fm-actions">
        <span>{tag}</span>
        {onBack && <button type="button" onClick={onBack}>결과로</button>}
        <button type="button" onClick={resetSafely}>초기화</button>
      </div>
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
  const directEdit = () => {
    const typed = window.prompt(`${question.title}\n숫자만 입력해주세요.`, String(value));
    if (typed !== null) onChange(question.key, typed);
  };

  return (
    <main className="fm-screen">
      <Header tag={`질문 ${step + 1}/${questions.length}`} onReset={onReset} />
      <div className="fm-progress"><i style={{ width: progress }} /></div>
      <section className="fm-card fm-question">
        <em>{question.label}</em>
        <h2>{question.title}</h2>
        <p>{question.helper}</p>
        <div className="fm-stepper fm-stepper-display">
          <button type="button" onClick={() => changeBy(-question.step)}>-</button>
          <button type="button" className="fm-value-box" onClick={directEdit}>{formatValue(value, question.type)}</button>
          <button type="button" onClick={() => changeBy(question.step)}>+</button>
        </div>
        {isAge ? <small>나이는 빠른 선택 버튼 없이 1세 단위로만 조절해요.</small> : (
          <>
            <small>{question.unit}로 조절돼요. 가운데 금액을 누르면 직접 입력할 수 있어요.</small>
            <div className="fm-chips">
              {question.presets.map((preset) => <button type="button" key={preset} onClick={() => onChange(question.key, preset)}>{formatWon(preset)}</button>)}
            </div>
          </>
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
            <em>{tag}</em><h3>{title}</h3><strong>{runwayText(scenario)}</strong><p>{deltaText(simulation, scenario)}</p>
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

function Experiment({ inputs, onChange, simulation, onReset, onBack }) {
  const lowerCost = buildScenario(inputs, { monthlyLivingCost: Math.max(1200000, inputs.monthlyLivingCost - 1500000) });
  const rows = simulation.targetResult.rows.filter((row, index) => index === 0 || row.age % 5 === 0 || row.age === inputs.targetRetirementAge || row.age === inputs.simulationUntilAge).slice(0, 12);
  const improvedRows = lowerCost.targetResult.rows;
  const max = Math.max(...rows.map((row) => Math.max(row.financialAsset, improvedRows.find((item) => item.age === row.age)?.financialAsset || 0)), 1);
  const chart = rows.map((row, index) => {
    const matched = improvedRows.find((item) => item.age === row.age) || row;
    const x = 34 + (index / Math.max(1, rows.length - 1)) * 286;
    return { age: row.age, x, current: row.financialAsset, improved: matched.financialAsset, currentY: 152 - (Math.max(0, row.financialAsset) / max) * 108, improvedY: 152 - (Math.max(0, matched.financialAsset) / max) * 108 };
  });
  const points = (key) => chart.map((row) => `${row.x},${Math.max(32, key === 'improved' ? row.improvedY : row.currentY)}`).join(' ');
  const adjust = (key, amount) => onChange(key, Math.max(0, cleanNumber(inputs[key]) + amount));
  const last = chart.at(-1);
  return (
    <main className="fm-screen fm-scroll">
      <Header tag="실험" onReset={onReset} onBack={onBack} />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">조건 바꿔보기</p><h2>숫자를 바꾸면 결과가 바로 달라져요</h2>
        <Adjust label="퇴사 나이" value={`${inputs.targetRetirementAge}세`} minus={() => adjust('targetRetirementAge', -1)} plus={() => adjust('targetRetirementAge', 1)} />
        <Adjust label="생활비" value={formatWon(inputs.monthlyLivingCost)} minus={() => adjust('monthlyLivingCost', -100000)} plus={() => adjust('monthlyLivingCost', 100000)} />
        <Adjust label="월 저축액" value={formatWon(inputs.monthlyInvestment)} minus={() => adjust('monthlyInvestment', -100000)} plus={() => adjust('monthlyInvestment', 100000)} />
      </section>
      <section className="fm-card fm-graph">
        <p className="fm-kicker">연도별 자산 그래프</p><h2>현재 계획과 생활비 절감안 비교</h2>
        <svg viewBox="0 0 360 210" role="img" aria-label="나이별 자산 그래프">
          <line x1="34" y1="152" x2="324" y2="152" /><line x1="34" y1="44" x2="34" y2="152" />
          <text x="34" y="34" className="axis">{formatEok(max)}</text><text x="34" y="174" className="axis">{chart[0]?.age}세</text><text x="292" y="174" className="axis">{last?.age}세</text>
          <polyline points={points('current')} className="current" /><polyline points={points('improved')} className="improved" />
          {chart.map((row) => <circle key={row.age} cx={row.x} cy={Math.max(32, row.improvedY)} r="4" className="dot" />)}
        </svg>
        <div className="fm-chart-summary"><span>현재 마지막 자산 <b>{formatEok(last?.current)}</b></span><span>개선안 마지막 자산 <b>{formatEok(last?.improved)}</b></span></div>
        <p className="fm-chart-note">점은 5년 단위 시점입니다. 다음 단계에서 점을 눌러 해당 나이의 자산을 보는 기능을 추가할 수 있어요.</p>
      </section>
    </main>
  );
}

function Adjust({ label, value, minus, plus }) {
  return <div className="fm-adjust"><span>{label}</span><strong>{value}</strong><button type="button" onClick={minus}>-</button><button type="button" onClick={plus}>+</button></div>;
}

function Curation({ inputs, onReset, onBack }) {
  return (
    <main className="fm-screen fm-scroll">
      <Header tag="큐레이션" onReset={onReset} onBack={onBack} />
      <section className="fm-card fm-text-card"><p className="fm-kicker">도시 시나리오</p><h2>사는 곳을 바꾸면 FIRE가 얼마나 가까워질까?</h2><p>생활비를 낮추는 국내·해외 후보지를 내 월 생활비와 비교합니다.</p></section>
      <ScenarioList title="국내 저비용 도시" currentCost={inputs.monthlyLivingCost} scenarios={domesticCities} />
      <ScenarioList title="해외 저비용 생활" currentCost={inputs.monthlyLivingCost} scenarios={overseasCities} />
      <Info tag="현실감 진단" title="내 생활비는 상위 몇 %일까?" text="가구원수별 소비지출 자료가 확인된 경우, 내 FIRE 생활비가 어느 정도 수준인지 비교합니다." note="자료 기준일과 출처를 함께 안내해요." />
    </main>
  );
}

function ScenarioList({ title, currentCost, scenarios }) {
  return (
    <section className="fm-card fm-city-list"><h2>{title}</h2>
      {scenarios.map(([name, cost, copy]) => {
        const saving = Math.max(0, currentCost - cost);
        return <article className="fm-city-row" key={name}><div><strong>{name}</strong><p>{copy}</p></div><span>월 {formatWon(cost)}<br /><b>{saving ? `${formatWon(saving)} 절감` : '비슷함'}</b></span></article>;
      })}
      <small>도시별 값은 참고용이며 실제 주거비, 의료비, 환율, 비자 조건에 따라 달라질 수 있어요.</small>
    </section>
  );
}

function Info({ tag, title, text, note }) {
  return <section className="fm-card fm-info"><em>{tag}</em><h2>{title}</h2><p>{text}</p><small>{note}</small></section>;
}

function roundRect(ctx, x, y, width, height, radius) {
  ctx.beginPath(); ctx.moveTo(x + radius, y); ctx.arcTo(x + width, y, x + width, y + height, radius); ctx.arcTo(x + width, y + height, x, y + height, radius); ctx.arcTo(x, y + height, x, y, radius); ctx.arcTo(x, y, x + width, y, radius); ctx.closePath();
}

async function makeShareImage(inputs, simulation) {
  const canvas = document.createElement('canvas'); canvas.width = 1200; canvas.height = 630;
  const ctx = canvas.getContext('2d'); ctx.fillStyle = '#fff7ed'; ctx.fillRect(0, 0, 1200, 630);
  const gradient = ctx.createLinearGradient(0, 0, 1200, 630); gradient.addColorStop(0, '#1f2937'); gradient.addColorStop(0.55, '#ea580c'); gradient.addColorStop(1, '#fb923c');
  ctx.fillStyle = gradient; roundRect(ctx, 70, 70, 1060, 490, 42); ctx.fill();
  ctx.fillStyle = '#fed7aa'; ctx.font = 'bold 42px sans-serif'; ctx.fillText('🔥 파이어맵 계산 결과', 120, 155);
  ctx.fillStyle = '#ffffff'; ctx.font = 'bold 78px sans-serif'; ctx.fillText(`${inputs.targetRetirementAge}세 퇴사`, 120, 275); ctx.fillText(`${runwayText(simulation)}까지`, 120, 370);
  ctx.fillStyle = '#fff7ed'; ctx.font = 'bold 34px sans-serif'; ctx.fillText('생활비 줄이기 · 퇴사 후 월 100만 원 · 1년 더 근무 효과 비교', 120, 450);
  ctx.fillStyle = '#fed7aa'; ctx.font = 'bold 30px sans-serif'; ctx.fillText('retire-age-kr.pages.dev', 120, 510);
  return new Promise((resolve) => canvas.toBlob(resolve, 'image/png', 0.95));
}

function Share({ inputs, simulation, onReset, onBack }) {
  const [message, setMessage] = useState('');
  const shareUrl = buildShareUrl(inputs);
  const shareText = `파이어맵 계산 결과\n${inputs.targetRetirementAge}세 퇴사 → ${runwayText(simulation)}까지\n퇴사 후 월 100만 원 벌기, 1년 더 근무하기, 생활비 줄이기 효과도 비교해봤어요.\n\n${BASE_URL}`;
  const copy = async (text, label) => { try { await navigator.clipboard.writeText(text); setMessage(label); setTimeout(() => setMessage(''), 1800); } catch { setMessage('복사 권한이 막혀 있어요. 직접 복사해주세요.'); } };
  const shareImage = async () => {
    const blob = await makeShareImage(inputs, simulation); const file = new File([blob], 'firemap-result.png', { type: 'image/png' });
    if (navigator.canShare?.({ files: [file] })) { await navigator.share({ files: [file], title: '파이어맵 계산 결과', text: '내 FIRE 결과 카드' }); setMessage('이미지 카드 공유창을 열었어요'); }
    else { const url = URL.createObjectURL(blob); window.open(url, '_blank'); setMessage('이미지 카드를 새 창으로 열었어요. 길게 눌러 저장하세요.'); }
  };
  return (
    <main className="fm-screen fm-scroll">
      <Header tag="공유" onReset={onReset} onBack={onBack} />
      <section className="fm-card fm-text-card"><p className="fm-kicker">공유</p><h2>결과카드 이미지 또는 링크 공유</h2><div className="fm-share-preview"><strong>{inputs.targetRetirementAge}세 퇴사 → {runwayText(simulation)}까지</strong><p>퇴사 후 월 100만 원 벌기, 1년 더 근무하기, 생활비 줄이기 효과도 비교해봤어요.</p></div><button className="fm-primary" type="button" onClick={shareImage}>이미지 카드 만들기/공유</button><button className="fm-secondary" type="button" onClick={() => copy(shareText, '결과 문구 복사됨')}>결과 문구 복사</button><button className="fm-secondary" type="button" onClick={() => copy(BASE_URL, '앱 기본 링크 복사됨')}>앱 기본 링크 복사</button><button className="fm-secondary" type="button" onClick={() => copy(shareUrl, '내 조건 링크 복사됨')}>내 조건 링크 복사</button>{message && <div className="fm-toast">{message}</div>}</section>
      <section className="fm-card fm-info"><em>운영 안내</em><h2>개인정보·면책·문의</h2><p>입력값은 서버로 전송하지 않고 이 브라우저에 저장됩니다. 본 서비스는 투자·세무·법률 자문이 아닌 참고용 계산입니다.</p><small>피드백·협업 문의: <b>{CONTACT_EMAIL}</b></small></section>
    </main>
  );
}

export default function FireMapMVP() {
  const [inputs, setInputs] = useState(loadInputs);
  const [screen, setScreen] = useState('home');
  const [step, setStep] = useState(0);
  const simulation = useMemo(() => buildSimulation(inputs), [inputs]);
  useEffect(() => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(inputs)); } catch { /* ignore */ } }, [inputs]);
  const onChange = (key, value) => setInputs((current) => ({ ...current, [key]: cleanNumber(value) }));
  const reset = () => { setInputs(defaultInputs); setStep(0); setScreen('home'); try { localStorage.removeItem(STORAGE_KEY); } catch { /* ignore */ } };
  const next = () => step >= questions.length - 1 ? setScreen('result') : setStep((current) => current + 1);
  const backToResult = () => setScreen('result');
  if (screen === 'home') return <Home onStart={() => setScreen('question')} onReset={reset} />;
  if (screen === 'question') return <Question step={step} inputs={inputs} onChange={onChange} onPrev={() => step === 0 ? setScreen('home') : setStep((current) => current - 1)} onNext={next} onReset={reset} />;
  if (screen === 'experiment') return <Experiment inputs={inputs} onChange={onChange} simulation={simulation} onReset={reset} onBack={backToResult} />;
  if (screen === 'curation') return <Curation inputs={inputs} onReset={reset} onBack={backToResult} />;
  if (screen === 'share') return <Share inputs={inputs} simulation={simulation} onReset={reset} onBack={backToResult} />;
  return <Result inputs={inputs} simulation={simulation} onReset={reset} onMove={setScreen} />;
}
