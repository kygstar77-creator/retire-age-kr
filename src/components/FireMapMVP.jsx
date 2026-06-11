import { useEffect, useMemo, useState } from 'react';
import Home from './firemap/Home.jsx';
import Question from './firemap/Question.jsx';
import Result from './firemap/Result.jsx';
import Experiment from './firemap/Experiment.jsx';
import City from './firemap/City.jsx';
import Share from './firemap/Share.jsx';
import Community from './firemap/Community.jsx';
import Tools from './firemap/Tools.jsx';
import BottomTabs from './firemap/BottomTabs.jsx';
import Header from './firemap/Header.jsx';
import DependentCheck from './firemap/DependentCheck.jsx';
import { ForeignStockTaxCard, DividendCard, PensionEarlyClaimCard } from './firemap/TaxPensionModules.jsx';
import FloatingFeedback from './firemap/FloatingFeedback.jsx';
import Leaderboard from './firemap/Leaderboard.jsx';
import Consent from './firemap/Consent.jsx';
import { buildSimulation, defaultInputs } from '../utils/retirementSimulator.js';
import { STORAGE_KEY, questions } from '../firemap-v2/data.js';
import { cleanNumber } from '../firemap-v2/formatters.js';
import { screens, resolveScreen } from '../firemap-v2/screens.js';
import { decodeInputsFromHash } from '../utils/shareState.js';
import '../firemap-v3-tokens.css';
import '../firemap.css';
import '../firemap-overrides.css';
import '../firemap-polish.css';
import '../firemap-result-density.css';
import '../firemap-deploy-polish.css';
import '../firemap-release-fixes.css';
import '../firemap-v3-feedback.css';
import '../firemap-v3-hotfix.css';
import '../firemap-v3-ia.css';

function getSharedInputs() {
  try {
    const shared = decodeInputsFromHash(window.location.hash) || decodeInputsFromHash(window.location.search);
    if (shared && Object.keys(shared).length) return shared;
  } catch { /* ignore */ }
  return null;
}

function loadInputs() {
  const shared = getSharedInputs();
  if (shared) return { ...defaultInputs, ...shared };
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) return { ...defaultInputs, ...JSON.parse(saved) };
  } catch { return defaultInputs; }
  return defaultInputs;
}

function readScreenFromHash() {
  if (getSharedInputs() && !Object.values(screens).some((s) => s.hash === window.location.hash)) return 'result';
  return resolveScreen(window.location.hash);
}

export default function FireMapMVP() {
  const [inputs, setInputs] = useState(loadInputs);
  const [screen, setScreenState] = useState(readScreenFromHash);
  const [step, setStep] = useState(0);
  const simulation = useMemo(() => buildSimulation(inputs), [inputs]);

  useEffect(() => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(inputs)); } catch { /* ignore */ } }, [inputs]);

  useEffect(() => {
    const sync = () => setScreenState(readScreenFromHash());
    window.addEventListener('hashchange', sync);
    window.addEventListener('popstate', sync);
    if (!window.location.hash) window.history.replaceState(null, '', '#home');
    return () => { window.removeEventListener('hashchange', sync); window.removeEventListener('popstate', sync); };
  }, []);

  const setScreen = (next) => {
    const id = resolveScreen(next);
    setScreenState(id);
    const hash = screens[id].hash;
    if (window.location.hash !== hash) window.history.pushState(null, '', hash);
  };
  const onChange = (key, value) => setInputs((c) => ({ ...c, [key]: cleanNumber(value) }));
  const applyPatch = (patch) => Object.entries(patch).forEach(([k, v]) => onChange(k, v));
  const next = () => step >= questions.length - 1 ? setScreen('result') : setStep((c) => c + 1);
  const prevQuestion = () => step === 0 ? setScreen('home') : setStep((c) => c - 1);
  const goFinalQuestion = () => { setStep(Math.max(0, questions.length - 1)); setScreen('question'); };
  const backOf = (id) => () => setScreen(screens[id]?.back || 'tools');

  const tool = (id, node) => (
    <main className="fm-screen fm-scroll">
      <Header tag={screens[id].title} onBack={backOf(id)} />
      {node}
    </main>
  );

  const wrap = (node) => (
    <>
      {node}
      {screens[screen]?.tab && <BottomTabs current={screen} onMove={setScreen} />}
      <FloatingFeedback />
      <Consent />
    </>
  );

  let view;
  if (screen === 'home') view = <Home onStart={() => setScreen('question')} />;
  else if (screen === 'question') view = <Question step={step} inputs={inputs} onChange={onChange} onPrev={prevQuestion} onNext={next} />;
  else if (screen === 'tools') view = <Tools onMove={setScreen} />;
  else if (screen === 'experiment') view = <Experiment inputs={inputs} onChange={onChange} simulation={simulation} onBack={backOf('experiment')} />;
  else if (screen === 'city') view = <City inputs={inputs} onChange={onChange} simulation={simulation} onBack={backOf('city')} />;
  else if (screen === 'share') view = <Share inputs={inputs} simulation={simulation} onBack={backOf('share')} />;
  else if (screen === 'community') view = <Community onBack={backOf('community')} />;
  else if (screen === 'ranking') view = <Leaderboard simulation={simulation} onBack={backOf('ranking')} onMove={setScreen} />;
  else if (screen === 'dependent') view = tool('dependent', <DependentCheck onApply={applyPatch} />);
  else if (screen === 'foreignTax') view = tool('foreignTax', <ForeignStockTaxCard />);
  else if (screen === 'dividend') view = tool('dividend', <DividendCard />);
  else if (screen === 'pension') view = tool('pension', <PensionEarlyClaimCard inputs={inputs} onApply={applyPatch} />);
  else view = <Result inputs={inputs} simulation={simulation} onMove={setScreen} onEditFinalQuestion={goFinalQuestion} />;

  return wrap(view);
}
