import { useEffect, useMemo, useState } from 'react';
import Home from './firemap/Home.jsx';
import Question from './firemap/Question.jsx';
import Result from './firemap/Result.jsx';
import Experiment from './firemap/Experiment.jsx';
import Curation from './firemap/Curation.jsx';
import Share from './firemap/Share.jsx';
import Header from './firemap/Header.jsx';
import { buildSimulation, defaultInputs } from '../utils/retirementSimulator.js';
import { STORAGE_KEY, questions } from '../firemap-v2/data.js';
import { cleanNumber } from '../firemap-v2/formatters.js';
import '../firemap.css';
import '../firemap-overrides.css';

const SCREENS = ['home', 'question', 'result', 'experiment', 'curation', 'share', 'community'];

function CommunityPreview({ onBack }) {
  const rows = [
    ['후기', '생활비를 낮추니 결과가 달라졌어요'],
    ['질문', '퇴사 후 월 현금흐름은 어떻게 잡나요?'],
    ['도시', '해외 3개월 살기 체크리스트']
  ];
  return (
    <main className="fm-screen fm-scroll">
      <Header tag="커뮤니티" onBack={onBack} />
      <section className="fm-card fm-text-card fm-community-hero">
        <p className="fm-kicker">소통 공간 미리보기</p>
        <h2>나와 비슷한 FIRE 고민을 같이 비교해요</h2>
        <p>지금은 화면 구조만 검증합니다. 이후 Supabase 기반으로 후기, 질문, 도시 팁, 결과 공유 피드를 붙일 수 있어요.</p>
        <div className="fm-community-stats"><span>후기 <b>128</b></span><span>질문 <b>43</b></span><span>도시 팁 <b>27</b></span></div>
      </section>
      <section className="fm-card fm-community-list">
        <h2>커뮤니티 미리보기</h2>
        {rows.map(([tag, title]) => <article key={title} className="fm-community-post"><em>{tag}</em><strong>{title}</strong><p>실제 글 작성과 댓글은 다음 단계에서 연결합니다.</p></article>)}
      </section>
    </main>
  );
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

function readScreenFromHash() {
  const screen = window.location.hash.replace('#', '');
  return SCREENS.includes(screen) ? screen : 'home';
}

export default function FireMapMVP() {
  const [inputs, setInputs] = useState(loadInputs);
  const [screen, setScreenState] = useState(readScreenFromHash);
  const [step, setStep] = useState(0);
  const simulation = useMemo(() => buildSimulation(inputs), [inputs]);

  useEffect(() => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(inputs)); } catch { /* ignore */ } }, [inputs]);

  useEffect(() => {
    const syncFromHash = () => setScreenState(readScreenFromHash());
    window.addEventListener('hashchange', syncFromHash);
    if (!window.location.hash) window.history.replaceState(null, '', '#home');
    return () => window.removeEventListener('hashchange', syncFromHash);
  }, []);

  const setScreen = (nextScreen) => {
    setScreenState(nextScreen);
    if (window.location.hash !== `#${nextScreen}`) window.history.pushState(null, '', `#${nextScreen}`);
  };
  const onChange = (key, value) => setInputs((current) => ({ ...current, [key]: cleanNumber(value) }));
  const next = () => step >= questions.length - 1 ? setScreen('result') : setStep((current) => current + 1);
  const prevQuestion = () => step === 0 ? setScreen('home') : setStep((current) => current - 1);
  const backToResult = () => setScreen('result');

  if (screen === 'home') return <Home onStart={() => setScreen('question')} />;
  if (screen === 'question') return <Question step={step} inputs={inputs} onChange={onChange} onPrev={prevQuestion} onNext={next} />;
  if (screen === 'experiment') return <Experiment inputs={inputs} onChange={onChange} simulation={simulation} onBack={backToResult} />;
  if (screen === 'curation') return <Curation inputs={inputs} simulation={simulation} onBack={backToResult} />;
  if (screen === 'share') return <Share inputs={inputs} simulation={simulation} onBack={backToResult} />;
  if (screen === 'community') return <CommunityPreview onBack={backToResult} />;
  return <Result inputs={inputs} simulation={simulation} onMove={setScreen} />;
}
