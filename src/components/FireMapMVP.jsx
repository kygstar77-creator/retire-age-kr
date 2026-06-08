import { useEffect, useMemo, useState } from 'react';
import { buildSimulation, defaultInputs } from '../utils/retirementSimulator.js';
import { buildShareUrl } from '../utils/shareState.js';
import { BASE_URL, CONTACT_EMAIL, STORAGE_KEY, domesticCities, investmentScenarios, overseasCities, questions } from '../firemap-v2/data.js';
import { cleanNumber, formatEok, formatValue, formatWon } from '../firemap-v2/formatters.js';
import { buildChartRows, buildScenario, deltaText, fireStatus, runwayText, scenarioEndAge } from '../firemap-v2/scenarios.js';
import '../firemap.css';
import '../firemap-overrides.css';

function loadInputs() {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) return { ...defaultInputs, ...JSON.parse(saved) };
  } catch {
    return defaultInputs;
  }
  return defaultInputs;
}

function Header({ tag, onReset, onBack, hideReset = false }) {
  const resetSafely = () => {
    if (window.confirm('입력값을 초기화하고 처음으로 돌아갈까요?')) onReset();
  };
  return (
    <header className="fm-topbar">
      <div className="fm-logo">🔥 파이어맵</div>
      <div className="fm-actions">
        <span>{tag}</span>
        {onBack && <button type="button" onClick={onBack}>결과로</button>}
        {!hideReset && <button type="button" onClick={resetSafely}>초기화</button>}
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
        <h1>내 돈은 몇 살까지 버틸까?</h1>
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
          <button type="button" className="fm-value-box" onClick={directEdit}>{formatValue(value, question.type, question.key)}</button>
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
      <div><small>FIRE 진단</small><strong>{fireStatus(simulation.survivalScore)}</strong><small>{simulation.survivalScore}/100</small></div>
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
  const [selectedAge, setSelectedAge] = useState(null);
  const reducedMonthlyLivingCost = Math.max(1200000, inputs.monthlyLivingCost - 1500000);
  const lowerCost = buildScenario(inputs, { monthlyLivingCost: reducedMonthlyLivingCost });
  const sp500Baseline = buildScenario(inputs, { annualReturnRate: 8 });
  const endAgeGap = scenarioEndAge(simulation) - scenarioEndAge(sp500Baseline);
  const gapText = endAgeGap > 0 ? `S&P500형보다 ${endAgeGap}년 길게` : endAgeGap < 0 ? `S&P500형보다 ${Math.abs(endAgeGap)}년 짧게` : 'S&P500형과 비슷하게';
  const { chart, max } = buildChartRows(simulation, lowerCost, inputs);
  const points = (key) => chart.map((row) => `${row.x},${Math.max(32, key === 'improved' ? row.improvedY : row.currentY)}`).join(' ');
  const adjust = (key, amount) => onChange(key, Math.max(0, cleanNumber(inputs[key]) + amount));
  const last = chart.at(-1);
  const selectedPoint = chart.find((row) => row.age === selectedAge) || last;
  const activeScenario = investmentScenarios.find((scenario) => scenario.annualReturnRate === inputs.annualReturnRate);
  return (
    <main className="fm-screen fm-scroll">
      <Header tag="실험" onReset={onReset} onBack={onBack} hideReset />
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">조건 바꿔보기</p><h2>숫자를 바꾸면 결과가 바로 달라져요</h2>
        <Adjust label="퇴사 나이" value={`${inputs.targetRetirementAge}세`} minus={() => adjust('targetRetirementAge', -1)} plus={() => adjust('targetRetirementAge', 1)} />
        <Adjust label="생활비" value={formatWon(inputs.monthlyLivingCost)} minus={() => adjust('monthlyLivingCost', -100000)} plus={() => adjust('monthlyLivingCost', 100000)} />
        <Adjust label="월 저축액" value={formatWon(inputs.monthlyInvestment)} minus={() => adjust('monthlyInvestment', -100000)} plus={() => adjust('monthlyInvestment', 100000)} />
      </section>
      <section className="fm-card fm-text-card">
        <p className="fm-kicker">투자 수익률 가정</p><h2>투자 성향별로 다시 계산해보기</h2>
        <p>현재 적용 수익률은 연 {inputs.annualReturnRate}%예요. {activeScenario ? activeScenario.copy : '직접 입력한 수익률 가정으로 계산 중이에요.'}</p>
        <div className="fm-chart-summary"><span>선택한 가정 <b>{runwayText(simulation)}</b></span><span>기본 S&P500형 대비 <b>{gapText}</b></span></div>
        <div className="fm-chips">
          {investmentScenarios.map((scenario) => <button type="button" key={scenario.key} onClick={() => onChange('annualReturnRate', scenario.annualReturnRate)}>{scenario.label} · 연 {scenario.annualReturnRate}%</button>)}
        </div>
        <small>수익률은 보장값이 아니라 장기 가정이에요. 실제 투자 결과는 시장 상황과 보유 상품에 따라 달라질 수 있어요.</small>
      </section>
      <section className="fm-card fm-graph">
        <p className="fm-kicker">내 미래 자산 차트</p><h2>현재 계획과 생활비 절감안 비교</h2>
        <div className="fm-chart-summary"><span>현재 계획 <b>{runwayText(simulation)}</b></span><span>생활비 절감안 <b>{runwayText(lowerCost)}</b></span></div>
        <svg viewBox="0 0 360 210" role="img" aria-label="나이별 자산 그래프">
          <line x1="34" y1="152" x2="324" y2="152" /><line x1="34" y1="44" x2="34" y2="152" />
          <text x="34" y="34" className="axis">{formatEok(max)}</text><text x="34" y="174" className="axis">{chart[0]?.age}세</text><text x="292" y="174" className="axis">{last?.age}세</text>
          <polyline points={points('current')} className="current" /><polyline points={points('improved')} className="improved" />
          {chart.map((row) => <circle key={row.age} cx={row.x} cy={Math.max(32, row.improvedY)} r={selectedPoint?.age === row.age ? '6' : '4'} className="dot" role="button" tabIndex="0" aria-label={`${row.age}세 자산 보기`} onClick={() => setSelectedAge(row.age)} onKeyDown={(event) => { if (event.key === 'Enter' || event.key === ' ') setSelectedAge(row.age); }} />)}
        </svg>
        {selectedPoint && <div className="fm-chart-summary"><span>{selectedPoint.age}세 현재 계획 <b>{formatEok(selectedPoint.current)}</b></span><span>{selectedPoint.age}세 절감안 <b>{formatEok(selectedPoint.improved)}</b></span></div>}
        <p className="fm-chart-note">그래프의 점을 누르면 해당 나이의 자산을 볼 수 있어요. 회색은 현재 입력값 그대로의 계획이에요. 주황색은 현재 생활비에서 월 150만 원을 줄인 가정이라, 위에서 생활비를 바꾸면 함께 다시 계산돼요. 현재 절감안 기준 생활비는 {formatWon(reducedMonthlyLivingCost)}입니다.</p>
      </section>
    </main>
  );
}

function Adjust({ label, value, minus, plus }) {
  return <div className="fm-adjust"><span>{label}</span><strong>{value}</strong><button type="button" onClick={minus}>-</button><button type="button" onClick={plus}>+</button></div>;
}

function Curation({ inputs, simulation, onReset, onBack }) {
  return (
    <main className="fm-screen fm-scroll">
      <Header tag="큐레이션" onReset={onReset} onBack={onBack} hideReset />
      <section className="fm-card fm-text-card"><p className="fm-kicker">도시 시나리오</p><h2>사는 곳을 바꾸면 FIRE가 얼마나 가까워질까?</h2><p>도시별 예상 생활비를 내 조건에 바로 대입해, 자산 수명이 얼마나 달라지는지 보여줍니다.</p></section>
      <ScenarioList title="국내 저비용 도시" inputs={inputs} baseSimulation={simulation} scenarios={domesticCities} />
      <ScenarioList title="해외 저비용 생활" inputs={inputs} baseSimulation={simulation} scenarios={overseasCities} />
      <Info tag="현실감 진단" title="생활비를 낮추는 건 수익률을 올리는 것만큼 강력해요" text="같은 자산이라도 매달 나가는 돈이 줄면 필요한 은퇴자금이 작아지고, 자산이 버티는 시간이 길어집니다." note="다음 단계에서는 환율, 비자, 건보료, 체류 개월을 함께 반영할 예정이에요." />
    </main>
  );
}

function ScenarioList({ title, inputs, baseSimulation, scenarios }) {
  return (
    <section className="fm-card fm-city-list"><h2>{title}</h2>
      {scenarios.map(([name, cost, copy]) => {
        const saving = Math.max(0, inputs.monthlyLivingCost - cost);
        const citySimulation = buildScenario(inputs, { monthlyLivingCost: cost });
        return <article className="fm-city-row" key={name}><div><strong>{name}</strong><p>{copy}</p><p>이 생활비로 계산하면 <b>{runwayText(citySimulation)}</b>까지 버틸 수 있어요. {deltaText(baseSimulation, citySimulation)}.</p></div><span>예상 월 {formatWon(cost)}<br /><b>{saving ? `현재 대비 ${formatWon(saving)} 절감` : '현재와 비슷함'}</b></span></article>;
      })}
      <small>도시별 금액은 1인 생활비 참고 시나리오이며 실제 주거비, 의료비, 환율, 비자 조건에 따라 달라질 수 있어요.</small>
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
      <Header tag="공유" onReset={onReset} onBack={onBack} hideReset />
      <section className="fm-card fm-text-card"><p className="fm-kicker">공유</p><h2>내 FIRE 결과 공유하기</h2><p>이미지로 저장하거나 링크로 공유할 수 있어요.</p><div className="fm-share-preview"><strong>{inputs.targetRetirementAge}세 퇴사 → {runwayText(simulation)}까지</strong><p>퇴사 후 월 100만 원 벌기, 1년 더 근무하기, 생활비 줄이기 효과도 비교해봤어요.</p></div><button className="fm-primary" type="button" onClick={shareImage}>결과 이미지 공유하기</button><button className="fm-secondary" type="button" onClick={() => copy(shareText, '결과 문구 복사됨')}>결과 문구 복사</button><button className="fm-secondary" type="button" onClick={() => copy(BASE_URL, '앱 기본 링크 복사됨')}>앱 기본 링크 복사</button><button className="fm-secondary" type="button" onClick={() => copy(shareUrl, '내 조건 링크 복사됨')}>내 조건 링크 복사</button>{message && <div className="fm-toast">{message}</div>}</section>
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
  if (screen === 'curation') return <Curation inputs={inputs} simulation={simulation} onReset={reset} onBack={backToResult} />;
  if (screen === 'share') return <Share inputs={inputs} simulation={simulation} onReset={reset} onBack={backToResult} />;
  return <Result inputs={inputs} simulation={simulation} onReset={reset} onMove={setScreen} />;
}
