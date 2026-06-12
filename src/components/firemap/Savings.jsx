import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { statsRank } from '../../firemap-v2/rank.js';
import { buildScenarioShareUrl } from '../../utils/shareState.js';
import { submitSave, fetchSaveTop, fetchMySaveRank } from '../../utils/firemapSaveApi.js';
import { CHALLENGES, QUOTES, QUICK, dayIdx, todayStr, wonStr, readJSON, fmtAdvance, dailyNeedOf, addSave, removeEntry, setTotal, track } from '../../firemap-v2/dailyData.js';

function FireProgressBar({ simulation, totalSaved, dailyNeed }) {
  const inp = simulation.inputs;
  const fireAge = simulation.earliestRetirementAge || inp.targetRetirementAge;
  if (!dailyNeed) {
    return (
      <div className="fm-fp done">
        <p className="fm-fp-cap">🎉 이미 목표 자산을 넘었어요. 절약한 돈은 은퇴 후 여유로 그대로 쌓여요.</p>
      </div>
    );
  }
  const totalDays = Math.max(1, (fireAge - inp.currentAge) * 365.25);
  const advancedDays = totalSaved / dailyNeed;
  const pct = Math.max(0, Math.min(100, (advancedDays / totalDays) * 100));
  const advLabel = fmtAdvance(advancedDays * 86400) || '0초';
  const effAge = Math.max(inp.currentAge, fireAge - advancedDays / 365.25);
  let yrs = Math.floor(effAge);
  let mos = Math.round((effAge - yrs) * 12);
  if (mos >= 12) { yrs += 1; mos = 0; }
  return (
    <div className="fm-fp">
      <div className="fm-fp-labels"><span>지금 {inp.currentAge}세</span><span>예상 퇴사 {fireAge}세</span></div>
      <div className="fm-fp-track">
        <div className="fm-fp-gain" style={{ width: `${pct}%` }} />
        <div className="fm-fp-flag" style={{ left: `${100 - pct}%` }}>🏁</div>
      </div>
      <p className="fm-fp-cap">{totalSaved > 0 ? <>절약으로 <b>{advLabel}</b> 당겼어요 · </> : null}지금 속도면 퇴사 <b>{yrs}세 {mos}개월</b></p>
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
  const myCid = (() => { try { return localStorage.getItem('fm_cid'); } catch { return null; } })();
  const dailyNeed = dailyNeedOf(simulation);

  useEffect(() => {
    try {
      const inp = simulation.inputs;
      const fireAge = simulation.earliestRetirementAge || inp.targetRetirementAge;
      localStorage.setItem('fm_plan', JSON.stringify({ dailyNeed, fireAge, currentAge: inp.currentAge, ok: dailyNeed == null }));
    } catch { /* ignore */ }
  }, [simulation, dailyNeed]);
  useEffect(() => { track('save_tab_view'); refresh(todaySaved); /* eslint-disable-next-line */ }, []);

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
    const tVal = nextSv.lastDate === todayStr() ? (nextSv.today || 0) : 0;
    const adv = dailyNeed ? (nextSv.total || 0) / dailyNeed : null;
    let nick = '';
    try { nick = localStorage.getItem('fm_nickname') || ''; } catch { /* ignore */ }
    submitSave({ todaySaved: tVal, totalSaved: nextSv.total || 0, advancedDays: adv, streak: nextSv.streak, nickname: nick, ageBand })
      .then(() => refresh(tVal));
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
    } catch { url = 'https://retire-age-kr.pages.dev/'; }
    const text = adLabel ? `절약으로 파이어를 ${adLabel} 앞당겼어요 🔥 나도 해보기` : '아낀 돈으로 파이어 앞당기기 🔥 나도 해보기';
    if (navigator.share) {
      try { await navigator.share({ title: '파이어맵 — 오늘의 절약', text, url }); track('share', { type: 'save' }); track('share_link_copy', { type: 'save' }); return; }
      catch (e) { if (e && e.name === 'AbortError') return; }
    }
    try { await navigator.clipboard.writeText(url); track('share', { type: 'save' }); track('share_link_copy', { type: 'save' }); window.alert('공유 링크를 복사했어요. 단톡방에 붙여넣어 보세요!'); }
    catch { onMove('share'); }
  };

  const log = (amount, label) => { const next = addSave(amount, label); setSv(next); track('save_log', { value: amount, item: label || '직접입력' }); persist(next); };
  const editTotal = () => { const v = window.prompt('누적 절약액을 수정할까요? (원)', String(totalSaved)); if (v == null) return; { const next = setTotal(String(v).replace(/[^0-9]/g, '')); setSv(next); persist(next); } };
  const custom = () => {
    const v = window.prompt('오늘 얼마를 아꼈나요? (원)');
    const n = Number(String(v || '').replace(/[^0-9]/g, ''));
    if (n > 0) log(n, '직접 입력');
  };

  return (
    <main className="fm-screen fm-scroll fm-has-tabbar">
      <Header tag="절약" />
      <p className="fm-daily-wisdom">“{quote}”</p>

      <section className="fm-card fm-save-screen">
        <p className="fm-kicker">오늘의 절약 🔥 {streak}일 연속</p>
        <div className="fm-save-hero">
          <small>오늘 아낀 돈</small>
          <b>{wonStr(todaySaved)}</b>
          {dailyNeed
            ? (todaySaved > 0 && todayAdv && <span className="fm-save-adv">파이어 <b>{todayAdv}</b> 앞당김 ⏩</span>)
            : <span className="fm-save-adv muted">이미 목표 달성 — 아낀 돈은 여유로 쌓여요</span>}
        </div>

        <FireProgressBar simulation={simulation} totalSaved={totalSaved} dailyNeed={dailyNeed} />

        {ch.s > 0 && (
          <button type="button" className="fm-save-rec" onClick={() => log(ch.s, ch.t)}>
            <span>💡 오늘의 추천 · {ch.t}</span><em>+{wonStr(ch.s)}</em>
          </button>
        )}
        <div className="fm-save-chips" aria-label="오늘 아낀 항목 기록">
          {QUICK.map((q) => (
            <button type="button" key={q.label} onClick={() => log(q.won, q.label)}>
              <span>{q.emoji} {q.label}</span><em>+{wonStr(q.won)}</em>
            </button>
          ))}
          <button type="button" className="fm-save-custom" onClick={custom}>✏️ 직접 입력</button>
        </div>

        {todayEntries.length > 0 && (
          <ul className="fm-save-entries" aria-label="오늘 기록">
            {todayEntries.slice().reverse().map((e) => (
              <li key={e.id}>
                <span>{e.label}</span>
                <em>+{wonStr(e.won)}</em>
                <button type="button" className="fm-entry-del" aria-label="삭제" onClick={() => { const next = removeEntry(e.id); setSv(next); persist(next); }}>✕</button>
              </li>
            ))}
          </ul>
        )}

        <div className="fm-save-total">
          누적 절약 <b>{wonStr(totalSaved)}</b>
          {dailyNeed && totalSaved > 0 && totalAdv && <> · 파이어 <b>{totalAdv}</b> 앞당김</>}
          {daysCount > 0 && <> · {daysCount}일째</>}
          {' '}<button type="button" className="fm-inline-link" onClick={editTotal}>수정</button>
        </div>
        <p className="fm-save-link">이 결과는 <button type="button" className="fm-inline-link" onClick={() => onMove('result')}>퇴사 나이 계산</button> 결과와 연동돼요. 누적 기록은 사라지지 않고 계속 쌓여요.</p>
        <button type="button" className="fm-save-share" onClick={shareSave}>🔥 내 절약 성과 공유하기</button>
      </section>

      <section className="fm-card">
        <p className="fm-kicker">오늘의 절약 랭킹 🏆</p>
        <p className="fm-section-sub">오늘 가장 많이 아낀 사람들이에요 · 매일 새로 시작해요</p>
        {rank && <p className="fm-save-myrank">오늘 내 절약 <b>{wonStr(todaySaved)}</b> · {rank.total.toLocaleString()}명 중 <b>{rank.position.toLocaleString()}위</b></p>}
        <div className="fm-nick-row">
          <input id="fm-save-nick" maxLength={16} value={nick} placeholder="닉네임 (예: 파이어왕)" onChange={(e) => setNick(e.target.value)} />
          <button type="button" onClick={saveNick}>{nickSaved ? '등록됨 ✓' : '닉네임 등록'}</button>
        </div>
        <p className="fm-section-sub">닉네임을 넣으면 아래 랭킹에 바로 내 이름으로 올라가요. 익명도 괜찮아요.</p>
        <ol className="fm-lb-list">
          {top === null && <li className="fm-lb-empty">불러오는 중…</li>}
          {top && top.length === 0 && <li className="fm-lb-empty">아직 오늘 기록이 적어요. 첫 주자가 되어보세요!</li>}
          {top && top.map((r, i) => {
            const mine = r.client_id && myCid && r.client_id === myCid;
            return (
              <li key={i} className={`fm-lb-row${i < 3 ? ' top3' : ''}${mine ? ' me' : ''}`}>
                <span className="fm-lb-rank">{medal(i)}</span>
                <span className="fm-lb-who">{r.nickname || '익명'}{mine ? ' (나)' : ''}{r.age_band ? ` · ${r.age_band}대` : ''}</span>
                <span className="fm-lb-score">{wonStr(r.today_saved)}</span>
              </li>
            );
          })}
        </ol>
      </section>
    </main>
  );
}
