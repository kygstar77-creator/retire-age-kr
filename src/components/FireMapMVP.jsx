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
  // 화면 진입 출처 기억: 도구에서 '이전'을 들어온 화면(예: 바꿔보기)으로 되돌리기 위함.
  const referrerRef = useRef({});
  const screenRef = useRef(screen);
  const skipRecordRef = useRef(false);
  // 바꿔보기(experiment) 샌드박스 draft를 부모가 보관 → 세금 도구 등 다른 화면을 다녀와도 유지.
  const [expDraft, setExpDraft] = useState(null);
  // 개인 결과는 도구에서 반영한 투자유형(해외 양도세·배당세)·건보료를 반영.
  const simulation = useMemo(() => buildSimulation(inputs), [inputs]);
  // 등수·점수 제출은 세전(investType=0)으로 모두에게 공정하게 비교 (양도·배당세 선택과 무관).
  const rankingSimulation = useMemo(() => buildSimulation({ ...inputs, investType: 0 }), [inputs]);

  useEffect(() => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(inputs)); } catch { /* ignore */ } try { pushState('firemap-inputs-v3', inputs); } catch { /* ignore */ } }, [inputs]);
  useEffect(() => { try { window.scrollTo(0, 0); } catch { /* ignore */ } }, [screen, step]);
  useEffect(() => { if (screen === 'question') { try { if (sessionStorage.getItem('fm_recalc')) { sessionStorage.removeItem('fm_recalc'); setStep(0); } } catch { /* ignore */ } } }, [screen]);

  // 화면이 바뀔 때마다 '어디서 왔는지' 기록(뒤로가기 제외) → 도구의 '이전'이 올바른 화면으로 복귀.
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
  const backOf = (id) => () => {
    const ref = referrerRef.current[id];
    delete referrerRef.current[id];
    skipRecordRef.current = true; // 이번 이동은 '뒤로'이므로 referrer 기록 안 함(핑퐁 방지)
    setScreen(ref || screens[id]?.back || 'tools');
  };

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
  if (screen === 'home') view = <Home onStart={(age) => { if (typeof age === 'number' && age > 0) { onChange('currentAge', age); setStep(1); } else { setStep(0); } setScreen('question'); }} onMove={setScreen} onChange={onChange} simulation={simulation} />;
  else if (screen === 'question') view = <Question step={step} inputs={inputs} onChange={onChange} onPrev={prevQuestion} onNext={next} />;
  else if (screen === 'tools') view = <Tools onMove={setScreen} />;
  else if (screen === 'experiment') view = <Experiment inputs={inputs} onChange={onChange} simulation={simulation} onBack={backOf('experiment')} onMove={setScreen} draft={expDraft} setDraft={setExpDraft} />;
  else if (screen === 'city') view = <City inputs={inputs} onChange={onChange} simulation={simulation} onBack={backOf('city')} />;
  else if (screen === 'share') view = <Share inputs={inputs} simulation={simulation} onBack={backOf('share')} />;
  else if (screen === 'community') view = <Community onBack={backOf('community')} onMove={setScreen} />;
  else if (screen === 'ranking') view = <Leaderboard simulation={simulation} rankingSimulation={rankingSimulation} onBack={backOf('ranking')} onMove={setScreen} />;
  else if (screen === 'cities') view = <CityExplorer inputs={inputs} simulation={simulation} onChange={onChange} onMove={setScreen} onBack={backOf('cities')} />;
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
