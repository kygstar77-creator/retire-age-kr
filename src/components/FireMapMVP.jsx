import { useEffect, useMemo, useRef, useState } from 'react';
import { pushState } from '../utils/firemapStateApi.js';
import Home from './firemap/Home.jsx';
import AccountCard from './firemap/AccountCard.jsx';
import Question from './firemap/Question.jsx';
import Result from './firemap/Result.jsx';
import Experiment from './firemap/Experiment.jsx';
import MenuAll from './firemap/MenuAll.jsx';
import Community from './firemap/Community.jsx';
import Wall from './firemap/Wall.jsx';
import BottomTabs from './firemap/BottomTabs.jsx';
import Header from './firemap/Header.jsx';
import DependentCheck from './firemap/DependentCheck.jsx';
import FireTypeTest from './firemap/FireTypeTest.jsx';
import { ForeignStockTaxCard, DividendCard, PensionEarlyClaimCard } from './firemap/TaxPensionModules.jsx';
import Leaderboard from './firemap/Leaderboard.jsx';
import CityExplorer from './firemap/CityExplorer.jsx';
import DividendLifeCalc from './firemap/DividendLifeCalc.jsx';
import News from './firemap/News.jsx';
import Settings from './firemap/Settings.jsx';
import { buildSimulation, defaultInputs, inputsIsReal } from '../utils/retirementSimulator.js';
import { STORAGE_KEY, questions } from '../firemap-v2/data.js';
import { cleanNumber } from '../firemap-v2/formatters.js';
import { screens, resolveScreen } from '../firemap-v2/screens.js';
import { getLatestRank } from '../firemap-v2/rankHistory.js';
import { maybeClaimOnLoad, claimDevice, syncAfterAuth, pullInputsIfNewer } from '../utils/firemapStateApi.js';
import { handleKakaoRedirect } from '../utils/kakaoAuth.js';
import { handleNaverRedirect } from '../utils/naverAuth.js';
import { toolPageByPath } from '../firemap-v2/toolPages.js';
import { track } from '../firemap-v2/dailyData.js';
import { logEvent } from '../utils/live.js';
import { decodeInputsFromHash } from '../utils/shareState.js';
import { applyTheme } from '../utils/prefs.js';
import { Toaster, toast } from '../ui/index.js';

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
  // 검색용 경로(/dividend 등)로 들어오면 그 도구 화면. functions/_middleware.js가 같은 표를 쓴다.
  const tool = toolPageByPath(window.location.pathname);
  if (tool && !window.location.hash) return tool.screen;
  // 해시가 없으면: 계산해 본 적이 있으면 결과로, 처음이면 랜딩으로.
  if (!window.location.hash) {
    try { if (getLatestRank()) return 'result'; } catch { /* ignore */ }
    return 'home';
  }
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

  useEffect(() => { applyTheme(); }, []);
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
  useEffect(() => { try { const q = new URLSearchParams(window.location.search || ''); if (q.get('from') === 'push') logEvent('push_open', {}); } catch { /* ignore */ } }, []);
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
    // 검색용 경로로 들어왔으면 크롤러용 본문(#sSeo)을 지우고 주소를 앱 해시로 바꾼다 — 사람 눈엔 앱 그대로.
    const tool = toolPageByPath(window.location.pathname);
    try { const seo = document.getElementById('sSeo'); if (seo) seo.remove(); } catch { /* ignore */ }
    if (tool && !window.location.hash) window.history.replaceState(null, '', `/${screens[tool.screen].hash}`);
    else if (!window.location.hash) window.history.replaceState(null, '', '#home');
    (async () => {
      // 카페 게시용 네이버 로그인에서 돌아온 경우 — 토큰을 받아 두고 인증 카드를 다시 연다.
      const nv = await handleNaverRedirect();
      if (nv && nv.ok) {
        try { sessionStorage.setItem('fm_open_cert', '1'); } catch { /* ignore */ }
        window.location.reload();
        return;
      }
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
    window.addEventListener('appinstalled', onInstalled);
    return () => { window.removeEventListener('hashchange', sync); window.removeEventListener('popstate', sync); window.removeEventListener('appinstalled', onInstalled); };
  }, []);

  const setScreen = (next) => {
    const id = resolveScreen(next);
    setScreenState(id);
    const hash = screens[id].hash;
    if (window.location.hash !== hash) window.history.pushState(null, '', hash);
  };
  const onChange = (key, value) => setInputs((c) => ({ ...c, [key]: cleanNumber(value) }));
  const applyPatch = (patch) => Object.entries(patch).forEach(([k, v]) => onChange(k, v));
  // 결과의 레버처럼 '한 번 누르면 내 입력이 바로 바뀌는' 경로에는 되돌리기를 함께 준다.
  // 도구(건보·세금·연금)는 자체 '해제' 토글이 있어 그대로 둔다.
  const applyPatchWithUndo = (patch, message = '적용했어요. 위 숫자가 바뀌었어요') => {
    const before = {};
    Object.keys(patch || {}).forEach((k) => { before[k] = inputs[k]; });
    applyPatch(patch);
    toast.good(message, { ms: 5200, action: { label: '되돌리기', onClick: () => applyPatch(before) } });
  };
  // 도시/해외체류 적용은 '미리보기 샌드박스'(experiment)로만 — 사용자가 명시적으로 저장하기 전엔 기존 저장 입력을 건드리지 않음.
  const previewPatch = (patch) => { const clean = {}; Object.entries(patch || {}).forEach(([k, v]) => { clean[k] = cleanNumber(v); }); setExpBase(inputs); setExpDraft({ ...inputs, ...clean }); setScreen('experiment'); };
  const previewCity = (krw) => previewPatch({ monthlyLivingCost: krw });
  const next = () => step >= questions.length - 1 ? setScreen('result') : setStep((c) => c + 1);
  const prevQuestion = () => step === 0 ? setScreen('home') : setStep((c) => c - 1);
  const backOf = (id) => () => {
    const ref = referrerRef.current[id];
    delete referrerRef.current[id];
    skipRecordRef.current = true;
    setScreen(ref || screens[id]?.back || 'menu');
  };

  const tool = (id, node) => (
    <main className="fm-screen fm-scroll fm-has-tabbar ds-screen-gap">
      <Header tag={screens[id].title} onBack={backOf(id)} />
      {node}
    </main>
  );

  // 화면 테이블 — screens.js의 키 = 여기 키. if/else 21개 → 표 1개.
  const VIEWS = {
    home: () => <Home onStart={(age) => { if (typeof age === 'number' && age > 0) { onChange('currentAge', age); setStep(1); } else { setStep(0); } setScreen('question'); }} onMove={setScreen} onChange={onChange} simulation={simulation} />,
    question: () => <Question step={step} inputs={inputs} onChange={onChange} onPrev={prevQuestion} onNext={next} />,
    result: () => <Result inputs={inputs} simulation={simulation} rankingSimulation={rankingSimulation} onMove={setScreen} onChange={onChange} />,
    experiment: () => <Experiment inputs={inputs} onChange={onChange} simulation={simulation} onBack={backOf('experiment')} onMove={setScreen} draft={expDraft} setDraft={setExpDraft} base={expBase} setBase={setExpBase} />,
    ranking: () => <Leaderboard simulation={simulation} rankingSimulation={rankingSimulation} onMove={setScreen} />,
    menu: () => <MenuAll onMove={setScreen} />,
    settings: () => <Settings simulation={simulation} onMove={setScreen} onBack={backOf('settings')} />,
    account: () => tool('account', <AccountCard />),
    cities: () => <CityExplorer inputs={inputs} simulation={simulation} onChange={onChange} onMove={setScreen} onPreviewCity={previewCity} onPreviewPatch={previewPatch} onBack={backOf('cities')} />,
    firetype: () => <FireTypeTest simulation={simulation} onChange={onChange} onMove={setScreen} onPreviewCity={previewCity} onBack={backOf('firetype')} />,
    dependent: () => tool('dependent', <DependentCheck inputs={inputs} simulation={simulation} onApply={applyPatch} />),
    foreignTax: () => tool('foreignTax', <><ForeignStockTaxCard inputs={inputs} onApply={applyPatch} /><DividendCard inputs={inputs} onApply={applyPatch} /></>),
    dividend: () => <DividendLifeCalc inputs={inputs} onChange={onChange} onMove={setScreen} onBack={backOf('dividend')} />,
    pension: () => tool('pension', <PensionEarlyClaimCard inputs={inputs} onApply={applyPatch} />),
    news: () => <News onBack={backOf('news')} />,
    wall: () => <Community onBack={backOf('wall')} onMove={setScreen} simulation={simulation} />
  };
  const render = VIEWS[screen] || VIEWS.home;

  return (
    <>
      {render()}
      {screens[screen]?.tab && <BottomTabs current={screen} onMove={setScreen} />}
      <Wall visible={screen === 'result'} />
      <Toaster />
    </>
  );
}
