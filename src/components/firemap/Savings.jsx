import { useEffect, useState } from 'react';
import Header from './Header.jsx';
import { CHALLENGES, QUOTES, QUICK, dayIdx, todayStr, yesterdayStr, wonStr, readJSON, fmtAdvance, dailyNeedOf, addSave, removeEntry, setTotal, track } from '../../firemap-v2/dailyData.js';

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

export default function Savings({ simulation, onMove }) {
  const ch = CHALLENGES[dayIdx() % CHALLENGES.length];
  const quote = QUOTES[dayIdx() % QUOTES.length];
  const [sv, setSv] = useState(() => readJSON('fm_save'));
  const [st, setSt] = useState(() => readJSON('fm_challenge'));
  const dailyNeed = dailyNeedOf(simulation);

  useEffect(() => {
    try {
      const inp = simulation.inputs;
      const fireAge = simulation.earliestRetirementAge || inp.targetRetirementAge;
      localStorage.setItem('fm_plan', JSON.stringify({ dailyNeed, fireAge, currentAge: inp.currentAge, ok: dailyNeed == null }));
    } catch { /* ignore */ }
  }, [simulation, dailyNeed]);
  useEffect(() => { track('save_tab_view'); }, []);

  const todaySaved = sv && sv.lastDate === todayStr() ? (sv.today || 0) : 0;
  const totalSaved = sv ? (sv.total || 0) : 0;
  const daysCount = sv ? (sv.days || 0) : 0;
  const streak = st ? st.count : 0;
  const doneToday = st && st.lastDate === todayStr();
  const advSec = (amount) => (dailyNeed ? (amount / dailyNeed) * 86400 : 0);
  const todayAdv = fmtAdvance(advSec(todaySaved));
  const totalAdv = fmtAdvance(advSec(totalSaved));
  const todayEntries = sv && sv.lastDate === todayStr() && Array.isArray(sv.entries) ? sv.entries : [];

  const log = (amount, label) => { setSv(addSave(amount, label)); track('save_log', { value: amount, item: label || '직접입력' }); };
  const editTotal = () => { const v = window.prompt('누적 절약액을 수정할까요? (원)', String(totalSaved)); if (v == null) return; setSv(setTotal(String(v).replace(/[^0-9]/g, ''))); };
  const custom = () => {
    const v = window.prompt('오늘 얼마를 아꼈나요? (원)');
    const n = Number(String(v || '').replace(/[^0-9]/g, ''));
    if (n > 0) log(n, '직접 입력');
  };
  const completeCh = () => {
    if (doneToday) return;
    const consec = st && st.lastDate === yesterdayStr() ? st.count + 1 : 1;
    const next = { count: consec, lastDate: todayStr() };
    try { localStorage.setItem('fm_challenge', JSON.stringify(next)); } catch { /* ignore */ }
    setSt(next);
    if (ch.s > 0) setSv(addSave(ch.s, '오늘의 미션'));
    track('save_mission_done');
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
                <button type="button" className="fm-entry-del" aria-label="삭제" onClick={() => setSv(removeEntry(e.id))}>✕</button>
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
      </section>

      <section className="fm-card fm-daily-mission">
        <p className="fm-daily-quote">오늘의 미션 · {ch.t}{ch.s > 0 ? ` (≈${wonStr(ch.s)})` : ''}</p>
        <button type="button" className={`fm-daily-btn full${doneToday ? ' done' : ''}`} onClick={completeCh} disabled={doneToday}>
          {doneToday ? '오늘 미션 완료 ✓' : '미션 완료하고 적립'}
        </button>
      </section>
    </main>
  );
}
