import { useEffect, useMemo, useState } from 'react';
import Home from './firemap/Home.jsx';
import Question from './firemap/Question.jsx';
import Result from './firemap/Result.jsx';
import Experiment from './firemap/Experiment.jsx';
import Advanced from './firemap/Advanced.jsx';
import Curation from './firemap/Curation.jsx';
import Share from './firemap/Share.jsx';
import FloatingFeedback from './firemap/FloatingFeedback.jsx';
import { buildSimulation, defaultInputs } from '../utils/retirementSimulator.js';
import { STORAGE_KEY, questions } from '../firemap-v2/data.js';
import { cleanNumber } from '../firemap-v2/formatters.js';
import '../firemap.css';
import '../firemap-overrides.css';
import '../firemap-polish.css';
import '../firemap-result-density.css';
import '../firemap-deploy-polish.css';
import '../firemap-release-fixes.css';
import '../firemap-v3-feedback.css';

const SCREENS = ['home', 'question', 'result', 'experiment', 'advanced', 'curation', 'share'];

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
  const goFinalQuestion = () => { setStep(Math.max(0, questions.length - 1)); setScreen('question'); };
  const wrap = (node) => <>{node}<FloatingFeedback /></>;

  if (screen === 'home') return wrap(<Home onStart={() => setScreen('question')} />);
  if (screen === 'question') return wrap(<Question step={step} inputs={inputs} onChange={onChange} onPrev={prevQuestion} onNext={next} />);
  if (screen === 'experiment') return wrap(<Experiment inputs={inputs} onChange={onChange} simulation={simulation} onBack={backToResult} />);
  if (screen === 'advanced') return wrap(<Advanced inputs={inputs} onChange={onChange} simulation={simulation} onBack={backToResult} />);
  if (screen === 'curation') return wrap(<Curation inputs={inputs} simulation={simulation} onBack={backToResult} />);
  if (screen === 'share') return wrap(<Share inputs={inputs} simulation={simulation} onBack={backToResult} />);
  return wrap(<Result inputs={inputs} simulation={simulation} onMove={setScreen} onEditFinalQuestion={goFinalQuestion} />);
}
