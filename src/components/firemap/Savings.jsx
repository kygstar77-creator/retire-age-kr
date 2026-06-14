import { useEffect, useRef, useState } from 'react';
import Header from './Header.jsx';
import { identityIds, accountHandle } from '../../utils/identity.js';
import IdentityLine from './IdentityLine.jsx';
import DepositCard from './DepositCard.jsx';
import { pushState, pullKey } from '../../utils/firemapStateApi.js';
import { statsRank } from '../../firemap-v2/rank.js';
import { funHandle } from '../../firemap-v2/funName.js';
import { buildScenarioShareUrl } from '../../utils/shareState.js';
import { fetchSaveTop, fetchMySaveRank } from '../../utils/firemapSaveApi.js';
import { notifySavingsChanged, reportBoard, hasCalculated, computeProgress } from '../../utils/savingsEngine.js';
import { CHALLENGES, QUOTES, QUICK, dayIdx, todayStr, wonStr, readJSON, fmtAdvance, dailyNeedOf, addSave, removeEntry, setTotal, track } from '../../firemap-v2/dailyData.js';

function FireProgressBar({ simulation, totalSaved, dailyNeed }) {
  if (!hasCalculated()) {
    return (
      <div className="fm-fp">
        <p className="fm-fp-cap">먼저 <b>파이어 계산</b>을 하면, 절약·적립이 파이어를 얼마나 당기는지 시간으로 보여드려요.</p>
      </div>
    );
  }
  const inp = simulation.inputs;
  const fireAge = simulation.earliestRetirementAge || inp.targetRetirementAge;
  if (!dailyNeed) {
    return (
      <div className="fm-fp done">
        <p className="fm-fp-cap">🎉 이미 목표 자산을 넘었어요. 아낀 돈은 파이어 후 여유로 그대로 쌓여요.</p>
      </div>
    );
  }
  const totalDays = Math.max(1, (fireAge - inp.currentAge) * 365.25);
  const advancedDays = totalSaved / dailyNeed;
  const pct = Math.max(0, Math.min(100, (advancedDays / totalDays) * 100));
  return (
    <div className="fm-fp">
      <div className="fm-fp-labels"><span>지금 {inp.currentAge}세</span><span>목표 {fireAge}세</span></div>
      <div className="fm-fp-track">
        <div className="fm-fp-gain" style={{ width: `${pct}%` }} />
        <div className="fm-fp-flag" style={{ left: `${100 - pct}%` }}>🏁</div>
      </div>
      <p className="fm-fp-cap">누적 절약 <b>{wonStr(totalSaved)}</b> · 실제 저축에 반영돼요</p>
    </div>
  );
}

const medal = (i) => (i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : String(i + 1));

export default function Savings({ simulation, onMove }) {
  const ch = CHALLENGES[dayIdx() % CHALLENGES.length];
  const quote = QUOTES[dayIdx() % QUOTES.length];
  const [sv, setSv] = useState(() => readJSON('fm_save'));
  const [nick, setNick] = useState(() => { try { return localStorage.getItem('fm_nickname') || ''; } catch { return ''; } });
  const [nickSaved, setNickSaved] = useState(false);
  const [saveView, setSaveView] = useState('deposit');
  const [tick, setTick] = useState(0);
  const [flash, setFlash] = useState(null);
  const flashRef = useRef(0);
  const [customOpen, setCustomOpen] = useState(false);
  const [customVal, setCustomVal] = useState('');
  const [editTot, setEditTot] = useState(false);
  const [totVal, setTotVal] = useState('');
  const myIds = identityIds();
  const acctHandle = accountHandle();
  const dailyNeed = dailyNeedOf(simulation);

  useEffect(() => { track('save_tab_view'); refresh(todaySaved); pullKey('fm_save').then((v) => { if (v) { try { localStorage.setItem('fm_save', JSON.stringify(v)); } catch { /* ignore */ } setSv(v); } }); /* eslint-disable-next-line */ }, []);

  useEffect(() => {
    const h = () => setTick((n) => n + 1);
    window.addEventListener('fm-savings-changed', h);
    return () => window.removeEventListener('fm-savings-changed', h);
  }, []);
  const prog = (() => { void tick; try { return computeProgress(simulation); } catch { return null; } })();

  const todaySaved = sv && sv.lastDate === todayStr() ? (sv.today || 0) : 0;
  const totalSaved = sv ? (sv.total || 0) : 0;
  const daysCount = sv ? (sv.days || 0) : 0;
  const streak = sv ? (sv.streak || 0) : 0;
  const advSec = (amount) => (dailyNeed ? (amount / dailyNeed) * 86400 : 0);
  const todayAdv = fmtAdvance(advSec(todaySaved));
  const totalAdv = fmtAdvance(advSec(totalSaved));
  const todayEntries = sv && sv.lastDate === todayStr() && Array.isArray(sv.entries) ? sv.entries : [];
  const ageBand = statsRank(simulation).ageBand;
  const [top, setTop] = useState(null);
  const [rank, setRank] = useState(null);
  const refresh = (todayVal) => {
    Promise.all([fetchSaveTop(10), fetchMySaveRank(todayVal)]).then(([t, r]) => { setTop(t); setRank(r); });
  };
  const persist = (nextSv) => {
    notifySavingsChanged();
    pushState('fm_save', nextSv);
    const tVal = nextSv.lastDate === todayStr() ? (nextSv.today || 0) : 0;
    reportBoard(simulation).then(() => refresh(tVal));
  };
  const saveNick = () => {
    const v = nick.trim().slice(0, 16);
    try { localStorage.setItem('fm_nickname', v); } catch { /* ignore */ }
    setNick(v);
    const cur = readJSON('fm_save');
    if (cur) persist(cur); else refresh(todaySaved);
    setNickSaved(true);
    setTimeout(() => setNickSaved(false), 1800);
  };
  const shareSave = async () => {
    const adLabel = fmtAdvance(advSec(totalSaved)) || '';
    let url;
    try {
      const u = new URL(buildScenarioShareUrl(simulation.inputs));
      u.pathname = '/s';
      u.searchParams.set('sd', String(Math.round(totalSaved)));
      if (adLabel) u.searchParams.set('ad', adLabel);
      url = u.toString();
    } catch { url = 'https://firemap.kr/'; }
    const text = adLabel ? `절약으로 파이어를 ${adLabel} 앞당겼어요 🔥 나도 해보기` : '아낀 돈으로 파이어 앞당기기 🔥 나도 해보기';
    if (navigator.share) {
      try { await navigator.share({ title: '파이어맵 — 오늘의 절약', text, url }); track('share', { type: 'save' }); track('share_link_copy', { type: 'save' }); return; }
      catch (e) { if (e && e.name === 'AbortError') return; }
    }
    try { await navigator.clipboard.writeText(url); track('share', { type: 'save' }); track('share_link_copy', { type: 'save' }); window.alert('공유 링크를 복사했어요. 단톡방에 붙여넣어 보세요!'); }
    catch { onMove('share'); }
  };

  const log = (amount, label) => {
    const next = addSave(amount, label); setSv(next);
    track('save_log', { value: amount, item: label || '직접입력' });
    const t = fmtAdvance(advSec(amount));
    if (t) { setFlash(t); window.clearTimeout(flashRef.current); flashRef.current = window.setTimeout(() => setFlash(null), 2600); }
    persist(next);
  };
  const editTotal = () => { setTotVal(String(totalSaved)); setEditTot(true); };
  const submitTotal = () => { const next = setTotal(String(totVal).replace(/[^0-9]/g, '')); setSv(next); persist(next); setEditTot(false); };
  const submitCustom = () => { const n = Number(String(customVal).replace(/[^0-9]/g, '')); if (n > 0) log(n, '직접 입력'); setCustomVal(''); setCustomOpen(false); };

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar">
      <Header tag="저축" />
      <p className="fm-daily-wisdom">“{quote}”</p>
      <div className="fm-rs-tabs" role="tablist" aria-label="적립/절약">
        <button type="button" role="tab" aria-selected={saveView === 'deposit'} className={saveView === 'deposit' ? 'on' : ''} onClick={() => setSaveView('deposit')}>💰 적립</button>
        <button type="button" role="tab" aria-selected={saveView === 'frugal'} className={saveView === 'frugal' ? 'on' : ''} onClick={() => setSaveView('frugal')}>✂️ 절약</button>
      </div>
      {hasCalculated() && prog && prog.planAge != null && (() => {
        const yv = prog.actualAgeYears != null ? prog.actualAgeYears : prog.planAge;
        const yy = Math.floor(yv);
        let rem = (yv - yy) * 365.25;
        const mo = Math.floor(rem / 30.4375); rem -= mo * 30.4375;
        const dd = Math.floor(rem);
        const ageStr = `${yy}세${mo > 0 ? ` ${mo}개월` : ''}${dd > 0 ? ` ${dd}일` : ''}`;
        const fmtMin = (sec) => { let m = Math.floor(sec / 60); const d = Math.floor(m / 1440); m -= d * 1440; const h = Math.floor(m / 60); const mm = m - h * 60; const parts = []; if (d) parts.push(`${d}일`); if (h) parts.push(`${h}시간`); if (mm || !parts.length) parts.push(`${mm}분`); return parts.join(' '); };
        const adv = prog.advanceDays;
        const TH = 1 / 1440;
        const src = (prog.depDev > 0 && prog.saveBonus > 0) ? '절약·초과 적립으로' : prog.depDev > 0 ? '초과 적립으로' : '절약으로';
        return (
          <section className="fm-fireclock" aria-live="polite">
            <p className="fm-fireclock-cap">예상 파이어</p>
            <p className="fm-fireclock-age"><b>{ageStr}</b></p>
            {prog.atGoal
              ? <p className="fm-fireclock-delta">🎉 이미 목표 자산을 넘었어요</p>
              : adv >= TH
                ? <p className="fm-fireclock-delta">⏱️ {src} <b>{fmtMin(adv * 86400)}</b> 앞당겼어요</p>
                : adv <= -TH
                  ? <p className="fm-fireclock-delta behind">적립이 계획보다 부족해 <b>{fmtMin(Math.abs(adv) * 86400)}</b> 밀렸어요</p>
                  : <p className="fm-fireclock-delta neutral">계획대로 가는 중 · 절약하면 앞당겨져요</p>}
          </section>
        );
      })()}
      <p className="fm-save-explain">
        {saveView === 'deposit'
          ? <>💰 <b>적립</b> = 실제로 투자·저축한 돈. <b>파이어 시점에 바로 반영</b>돼요.</>
          : <>✂️ <b>절약</b> = 안 쓴 돈으로 <b>파이어 시간을 사는 것</b>. 천 원 아끼면 그만큼 파이어가 당겨져요.</>}
      </p>
      {saveView === 'deposit' && <DepositCard simulation={simulation} onMove={onMove} />}
      {saveView === 'frugal' && (
      <>
      <section className="fm-card fm-save-screen">
        <p className="fm-kicker">오늘의 절약 🔥 {streak}일 연속</p>
        <div className="fm-save-hero">
          <small>오늘 아낀 돈</small>
          <b>{wonStr(todaySaved)}</b>
          {dailyNeed
            ? (todaySaved > 0 && <span className="fm-save-adv">⏱️ 오늘 파이어 <b>{todayAdv || '몇 초'}</b> 샀어요 · <button type="button" className="fm-inline-link" onClick={() => onMove('home')}>현황 보기</button></span>)
            : <span className="fm-save-adv muted">이미 목표 달성 — 아낀 돈은 여유로 쌓여요</span>}
        </div>

        {flash && <div className="fm-time-flash" role="status">⏱️ 방금 파이어 <b>{flash}</b>를 샀어요!</div>}

        <FireProgressBar simulation={simulation} totalSaved={totalSaved} dailyNeed={dailyNeed} />

        {ch.s > 0 && (
          <button type="button" className="fm-save-rec" onClick={() => log(ch.s, ch.t)}>
            <span>💡 오늘의 추천 · {ch.t}</span><em>+{wonStr(ch.s)}{dailyNeed && fmtAdvance(advSec(ch.s)) ? <i className="fm-chip-time">⏱️{fmtAdvance(advSec(ch.s))}</i> : null}</em>
          </button>
        )}
        <div className="fm-save-chips" aria-label="오늘 아낀 항목 기록">
          {QUICK.map((q) => (
            <button type="button" key={q.label} onClick={() => log(q.won, q.label)}>
              <span>{q.emoji} {q.label}</span><em>+{wonStr(q.won)}{dailyNeed && fmtAdvance(advSec(q.won)) ? <i className="fm-chip-time">⏱️{fmtAdvance(advSec(q.won))}</i> : null}</em>
            </button>
          ))}
          <button type="button" className="fm-save-custom" onClick={() => setCustomOpen((v) => !v)}>✏️ 직접 입력</button>
        </div>
        {customOpen && (
          <div className="fm-save-inline">
            <input inputMode="numeric" className="fm-save-inline-in" value={customVal} onChange={(e) => setCustomVal(e.target.value.replace(/[^0-9]/g, ''))} placeholder="오늘 아낀 금액 (원)" autoFocus />
            <button type="button" className="fm-save-inline-go" onClick={submitCustom}>기록</button>
          </div>
        )}

        {todayEntries.length > 0 && (
          <>
            <ul className="fm-save-entries" aria-label="오늘 기록">
              {todayEntries.slice().reverse().slice(0, 8).map((e) => (
                <li key={e.id}>
                  <span>{e.label}</span>
                  <em>+{wonStr(e.won)}</em>
                  <button type="button" className="fm-entry-del" aria-label="삭제" onClick={() => { const next = removeEntry(e.id); setSv(next); persist(next); }}>✕</button>
                </li>
              ))}
            </ul>
            {todayEntries.length > 8 && <p className="fm-save-entries-more">외 {todayEntries.length - 8}개 더 · 오늘 총 {todayEntries.length}건 (매일 0시 새로 시작)</p>}
          </>
        )}

        <div className="fm-save-total">
          누적 절약 <b>{wonStr(totalSaved)}</b>
          {daysCount > 0 && <> · {daysCount}일째</>}
          {' '}<button type="button" className="fm-inline-link" onClick={editTotal}>수정</button>
        </div>
        {editTot && (
          <div className="fm-save-inline">
            <input inputMode="numeric" className="fm-save-inline-in" value={totVal} onChange={(e) => setTotVal(e.target.value.replace(/[^0-9]/g, ''))} placeholder="누적 절약액 (원)" autoFocus />
            <button type="button" className="fm-save-inline-go" onClick={submitTotal}>저장</button>
            <button type="button" className="fm-save-inline-cancel" onClick={() => setEditTot(false)}>취소</button>
          </div>
        )}
        <p className="fm-save-link">이 결과는 <button type="button" className="fm-inline-link" onClick={() => onMove('result')}>파이어 계산</button> 결과와 연동돼요. 누적 기록은 사라지지 않고 계속 쌓여요.</p>
        <button type="button" className="fm-save-share" onClick={shareSave}>🔥 내 절약 성과 공유하기</button>
      </section>

      <section className="fm-card">
        <p className="fm-kicker">오늘의 절약 랭킹 🏆</p>
        <p className="fm-section-sub">오늘 가장 많이 아낀 사람들이에요 · 매일 새로 시작해요</p>
        {rank && <p className="fm-save-myrank">오늘 내 절약 <b>{wonStr(todaySaved)}</b> · {rank.total.toLocaleString()}명 중 <b>{rank.position.toLocaleString()}위</b></p>}
        <IdentityLine onMove={onMove} />
        <ol className="fm-lb-list">
          {top === null && <li className="fm-lb-empty">불러오는 중…</li>}
          {top && top.length === 0 && <li className="fm-lb-empty">아직 오늘 기록이 적어요. 첫 주자가 되어보세요!</li>}
          {top && top.map((r, i) => {
            const mine = r.client_id && myIds.includes(r.client_id);
            return (
              <li key={i} className={`fm-lb-row${i < 3 ? ' top3' : ''}${mine ? ' me' : ''}`}>
                <span className="fm-lb-rank">{medal(i)}</span>
                <span className="fm-lb-who">{mine && acctHandle ? acctHandle : (r.nickname || funHandle(r.client_id))}{mine ? ' (나)' : ''}{r.age_band ? ` · ${r.age_band}대` : ''}</span>
                <span className="fm-lb-score">{wonStr(r.today_saved)}</span>
              </li>
            );
          })}
        </ol>
      </section>
      </>
      )}
    </main>
  );
}
