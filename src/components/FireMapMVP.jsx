import { useEffect, useMemo, useState } from 'react';
import { getLatestRank } from '../firemap-v2/rankHistory.js';
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
import CityExplorer from './firemap/CityExplorer.jsx';
import DividendLifeCalc from './firemap/DividendLifeCalc.jsx';
import Savings from './firemap/Savings.jsx';
import FirePlan from './firemap/FirePlan.jsx';
import Consent from './firemap/Consent.jsx';
import { buildSimulation, defaultInputs } from '../utils/retirementSimulator.js';
import { STORAGE_KEY, questions } from '../firemap-v2/data.js';
import { cleanNumber } from '../firemap-v2/formatters.js';
import { screens, resolveScreen } from '../firemap-v2/screens.js';
import { maybeClaimOnLoad } from '../utils/firemapStateApi.js';
import { track } from '../firemap-v2/dailyData.js';
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
import '../firemap-status.css';
import '../firemap-premium.css';

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
  // 결과·등수·라벨은 항상 '세전(investType=0)' 기준으로 일관되게. 세금 탐색은 바꿔보기 미리보기에서만.
  const simulation = useMemo(() => buildSimulation({ ...inputs, investType: 0 }), [inputs]);

  useEffect(() => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(inputs)); } catch { /* ignore */ } }, [inputs]);
  useEffect(() => { try { window.scrollTo(0, 0); } catch { /* ignore */ } }, [screen, step]);

  useEffect(() => {
    const sync = () => setScreenState(readScreenFromHash());
    window.addEventListener('hashchange', sync);
    window.addEventListener('popstate', sync);
    if (!window.location.hash) window.history.replaceState(null, '', '#home');
    maybeClaimOnLoad();
    // 홈화면(스탠드얼론) 실행 · 설치 · 재방문 측정
    try {
      const standalone = (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) || window.navigator.standalone === true;
      if (standalone) track('app_standalone_open');
      const FS = 'fm_first_seen';
      const now = Date.now();
      const first = Number(localStorage.getItem(FS) || 0);
      if (!first) { localStorage.setItem(FS, String(now)); }
      else { const days = Math.floor((now - first) / 86400000); if (days >= 1) track('returning_visit', { days }); }
    } catch { /* ignore */ }
    const onInstalled = () => track('app_installed');
    const onPrompt = () => track('install_prompt_available');
    window.addEventListener('appinstalled', onInstalled);
    window.addEventListener('beforeinstallprompt', onPrompt);
    return () => { window.removeEventListener('hashchange', sync); window.removeEventListener('popstate', sync); window.removeEventListener('appinstalled', onInstalled); window.removeEventListener('beforeinstallprompt', onPrompt); };
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
      {screens[screen]?.tab && <BottomTabs current={screen} onMove={(t) => setScreen(t === 'home' && getLatestRank() ? 'result' : t)} />}
      <FloatingFeedback />
      <Consent />
    </>
  );

  let view;
  if (screen === 'home') view = <Home onStart={(age) => { if (typeof age === 'number' && age > 0) { onChange('currentAge', age); setStep(1); } else { setStep(0); } setScreen('question'); }} onMove={setScreen} onChange={onChange} simulation={simulation} />;
  else if (screen === 'question') view = <Question step={step} inputs={inputs} onChange={onChange} onPrev={prevQuestion} onNext={next} />;
  else if (screen === 'tools') view = <Tools onMove={setScreen} />;
  else if (screen === 'experiment') view = <Experiment inputs={inputs} onChange={onChange} simulation={simulation} onBack={backOf('experiment')} />;
  else if (screen === 'city') view = <City inputs={inputs} onChange={onChange} simulation={simulation} onBack={backOf('city')} />;
  else if (screen === 'share') view = <Share inputs={inputs} simulation={simulation} onBack={backOf('share')} />;
  else if (screen === 'community') view = <Community onBack={backOf('community')} />;
  else if (screen === 'ranking') view = <Leaderboard simulation={simulation} onBack={backOf('ranking')} onMove={setScreen} />;
  else if (screen === 'cities') view = <CityExplorer inputs={inputs} simulation={simulation} onChange={onChange} onMove={setScreen} onBack={backOf('cities')} />;
  else if (screen === 'dependent') view = tool('dependent', <DependentCheck onApply={applyPatch} />);
  else if (screen === 'foreignTax') view = tool('foreignTax', <ForeignStockTaxCard />);
  else if (screen === 'dividend') view = <DividendLifeCalc inputs={inputs} onChange={onChange} onMove={setScreen} onBack={backOf('dividend')} />;
  else if (screen === 'save') view = <Savings simulation={simulation} onMove={setScreen} />;
  else if (screen === 'firePlan') view = <FirePlan simulation={simulation} onMove={setScreen} onChange={onChange} />;
  else if (screen === 'pension') view = tool('pension', <PensionEarlyClaimCard inputs={inputs} onApply={applyPatch} />);
  else view = <Result inputs={inputs} simulation={simulation} onMove={setScreen} onChange={onChange} onEditFinalQuestion={goFinalQuestion} />;

  return wrap(view);
}
