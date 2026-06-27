import { useEffect, useMemo, useRef, useState } from 'react';
import { getLatestRank } from '../firemap-v2/rankHistory.js';
import { pushState } from '../utils/firemapStateApi.js';
import Home from './firemap/Home.jsx';
import AccountCard from './firemap/AccountCard.jsx';
import Question from './firemap/Question.jsx';
import Result from './firemap/Result.jsx';
import Experiment from './firemap/Experiment.jsx';
import City from './firemap/City.jsx';
import Share from './firemap/Share.jsx';
import Community from './firemap/Community.jsx';
import Tools from './firemap/Tools.jsx';
import MenuAll from './firemap/MenuAll.jsx';
import BottomTabs from './firemap/BottomTabs.jsx';
import Header from './firemap/Header.jsx';
import DependentCheck from './firemap/DependentCheck.jsx';
import FireTypeTest from './firemap/FireTypeTest.jsx';
import { ForeignStockTaxCard, DividendCard, PensionEarlyClaimCard } from './firemap/TaxPensionModules.jsx';
import FloatingFeedback from './firemap/FloatingFeedback.jsx';
import Leaderboard from './firemap/Leaderboard.jsx';
import CityExplorer from './firemap/CityExplorer.jsx';
import DividendLifeCalc from './firemap/DividendLifeCalc.jsx';
import Savings from './firemap/Savings.jsx';
import FirePlan from './firemap/FirePlan.jsx';
import FireIndex from './firemap/FireIndex.jsx';
import JourneyStage from './firemap/JourneyStage.jsx';
import Consent from './firemap/Consent.jsx';
import LiveBanner from './firemap/LiveBanner.jsx';
import PullToRefresh from './firemap/PullToRefresh.jsx';
import { buildSimulation, defaultInputs, inputsIsReal } from '../utils/retirementSimulator.js';
import { STORAGE_KEY, questions } from '../firemap-v2/data.js';
import { cleanNumber } from '../firemap-v2/formatters.js';
import { screens, resolveScreen } from '../firemap-v2/screens.js';
import { maybeClaimOnLoad, claimDevice, syncAfterAuth, pullInputsIfNewer } from '../utils/firemapStateApi.js';
import { handleKakaoRedirect } from '../utils/kakaoAuth.js';
import { track } from '../firemap-v2/dailyData.js';
import { logEvent } from '../utils/live.js';
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
  const referrerRef = useRef({});
  const screenRef = useRef(screen);
  const skipRecordRef = useRef(false);
  const inputsMounted = useRef(false);
  const skipStampRef = useRef(false);
  const [expDraft, setExpDraft] = useState(null);
  const [expBase, setExpBase] = useState(null);
  const simulation = useMemo(() => buildSimulation(inputs), [inputs]);
  const rankingSimulation = useMemo(() => buildSimulation({ ...inputs, investType: 0 }), [inputs]);

  useEffect(() => {
    if (!inputsIsReal(inputs)) return;
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(inputs)); } catch { /* ignore */ }
    if (!inputsMounted.current) { inputsMounted.current = true; return; }
    if (skipStampRef.current) { skipStampRef.current = false; return; }
    const ts = Date.now();
    try { localStorage.setItem('fm_inputs_ts', String(ts)); } catch { /* ignore */ }
    try { pushState('firemap-inputs-v3', inputs); pushState('fm_inputs_ts', ts); } catch { /* ignore */ }
  }, [inputs]);
  useEffect(() => { try { window.scrollTo(0, 0); } catch { /* ignore */ } }, [screen, step]);
  useEffect(() => { try { logEvent('screen_view', { screen }); } catch { /* ignore */ } }, [screen]);
  useEffect(() => { try { logEvent('session_start', {}); } catch { /* ignore */ } }, []);
  useEffect(() => {
    try {
      const orig = window.gtag;
      window.gtag = function (cmd, name, params) {
        try { if (cmd === 'event' && name) logEvent(name, params || {}); } catch { /* ignore */ }
        if (typeof orig === 'function') return orig.apply(this, arguments);
        return undefined;
      };
    } catch { /* ignore */ }
  }, []);
  useEffect(() => { if (screen === 'question') { try { if (sessionStorage.getItem('fm_recalc')) { sessionStorage.removeItem('fm_recalc'); setStep(0); } } catch { /* ignore */ } } }, [screen]);

  useEffect(() => {
    const prev = screenRef.current;
    if (prev !== screen) {
      if (!skipRecordRef.current) referrerRef.current[screen] = prev;
      skipRecordRef.current = false;
      screenRef.current = screen;
    }
  }, [screen]);

  useEffect(() => {
    const sync = () => setScreenState(readScreenFromHash());
    window.addEventListener('hashchange', sync);
    window.addEventListener('popstate', sync);
    if (!window.location.hash) window.history.replaceState(null, '', '#home');
    (async () => {
      const r = await handleKakaoRedirect();
      if (r && r.ok) {
        try { await claimDevice(); await syncAfterAuth(); } catch (e) { /* ignore */ }
        window.location.reload();
        return;
      }
      maybeClaimOnLoad();
      try { const sIn = await pullInputsIfNewer(); if (sIn) { skipStampRef.current = true; setInputs((c) => ({ ...c, ...sIn })); } } catch (e) { /* ignore */ }
    })();
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
  // 도시 적용은 '미리보기 샌드박스'(experiment)로만 — 사용자가 명시적으로 저장하기 전엔 기존 저장 입력을 건드리지 않음.
  const previewCity = (krw) => { const c = cleanNumber(krw); setExpBase(inputs); setExpDraft({ ...inputs, monthlyLivingCost: c }); setScreen('experiment'); };
  const next = () => step >= questions.length - 1 ? setScreen('result') : setStep((c) => c + 1);
  const prevQuestion = () => step === 0 ? setScreen('home') : setStep((c) => c - 1);
  const goFinalQuestion = () => { setStep(Math.max(0, questions.length - 1)); setScreen('question'); };
  const backOf = (id) => () => {
    const ref = referrerRef.current[id];
    delete referrerRef.current[id];
    skipRecordRef.current = true;
    setScreen(ref || screens[id]?.back || 'menu');
  };

  const tool = (id, node) => (
    <main className="fm-screen fm-scroll">
      <Header tag={screens[id].title} onBack={backOf(id)} />
      {node}
    </main>
  );

  const wrap = (node) => (
    <>
      <PullToRefresh />
      <LiveBanner />
      {node}
      {screens[screen]?.tab && <BottomTabs current={screen} onMove={setScreen} />}
      <FloatingFeedback />
      <Consent />
    </>
  );

  let view;
  if (screen === 'home') view = <Home onStart={(age) => { if (typeof age === 'number' && age > 0) { onChange('currentAge', age); setStep(1); } else { setStep(0); } setScreen('question'); }} onMove={setScreen} onChange={onChange} simulation={simulation} />;
  else if (screen === 'question') view = <Question step={step} inputs={inputs} onChange={onChange} onPrev={prevQuestion} onNext={next} />;
  else if (screen === 'tools') view = <Tools onMove={setScreen} />;
  else if (screen === 'menu') view = <MenuAll onMove={setScreen} />;
  else if (screen === 'journey') view = <JourneyStage simulation={simulation} onMove={setScreen} onBack={backOf('journey')} />;
  else if (screen === 'index') view = <FireIndex simulation={simulation} onBack={backOf('index')} />;
  else if (screen === 'experiment') view = <Experiment inputs={inputs} onChange={onChange} simulation={simulation} onBack={backOf('experiment')} onMove={setScreen} draft={expDraft} setDraft={setExpDraft} base={expBase} setBase={setExpBase} />;
  else if (screen === 'city') view = <City inputs={inputs} onChange={onChange} simulation={simulation} onBack={backOf('city')} />;
  else if (screen === 'share') view = <Share inputs={inputs} simulation={simulation} onBack={backOf('share')} />;
  else if (screen === 'community') view = <Community onBack={backOf('community')} onMove={setScreen} simulation={simulation} />;
  else if (screen === 'ranking') view = <Leaderboard simulation={simulation} rankingSimulation={rankingSimulation} onBack={backOf('ranking')} onMove={setScreen} />;
  else if (screen === 'cities') view = <CityExplorer inputs={inputs} simulation={simulation} onChange={onChange} onMove={setScreen} onBack={backOf('cities')} />;
  else if (screen === 'firetype') view = <FireTypeTest simulation={simulation} onChange={onChange} onMove={setScreen} onPreviewCity={previewCity} onBack={backOf('firetype')} />;
  else if (screen === 'dependent') view = tool('dependent', <DependentCheck inputs={inputs} onApply={applyPatch} />);
  else if (screen === 'foreignTax') view = tool('foreignTax', <><ForeignStockTaxCard inputs={inputs} onApply={applyPatch} /><DividendCard inputs={inputs} onApply={applyPatch} /></>);
  else if (screen === 'dividend') view = <DividendLifeCalc inputs={inputs} onChange={onChange} onMove={setScreen} onBack={backOf('dividend')} />;
  else if (screen === 'save') view = <Savings simulation={simulation} onMove={setScreen} />;
  else if (screen === 'firePlan') view = <FirePlan simulation={simulation} onMove={setScreen} onChange={onChange} />;
  else if (screen === 'pension') view = tool('pension', <PensionEarlyClaimCard inputs={inputs} onApply={applyPatch} />);
  else if (screen === 'account') view = tool('account', <AccountCard />);
  else view = <Result inputs={inputs} simulation={simulation} rankingSimulation={rankingSimulation} onMove={setScreen} onChange={onChange} onEditFinalQuestion={goFinalQuestion} />;

  return wrap(view);
}
