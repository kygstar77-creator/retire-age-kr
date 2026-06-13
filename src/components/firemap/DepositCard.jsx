import { useState, useEffect } from 'react';
import { pushState, pullKey } from '../../utils/firemapStateApi.js';
import { notifySavingsChanged } from '../../utils/savingsEngine.js';

const KEY = 'fm_daily';
const dayKey = (d) => d.toISOString().slice(0, 10);
const todayStr = () => dayKey(new Date());
const monthStr = () => new Date().toISOString().slice(0, 7);
const load = () => { try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch { return null; } };
const save = (o) => { try { localStorage.setItem(KEY, JSON.stringify(o)); } catch { /* ignore */ } };
const won = (n) => `${Math.round(n).toLocaleString('ko-KR')}원`;

// 연속 기록일: 오늘(없으면 어제)부터 거꾸로 기록이 있는 날 수
function streakOf(days) {
  let s = 0;
  let d = new Date();
  if (!(days[todayStr()] > 0)) d = new Date(Date.now() - 86400000);
  for (let i = 0; i < 3660; i += 1) {
    if (days[dayKey(d)] > 0) { s += 1; d = new Date(d.getTime() - 86400000); } else break;
  }
  return s;
}

// 적립 = 매일 '실제로 저축한 금액'을 기록. 월별 실제 저축이 계획(월 저축액)을 넘긴 만큼만 퇴사 앞당김.
export default function DepositCard({ simulation, onMove }) {
  const inp = (simulation && simulation.inputs) || {};
  const monthlyPlan = inp.monthlyInvestment || 0;
  const suggested = monthlyPlan > 0 ? Math.max(1000, Math.round(monthlyPlan / 30 / 1000) * 1000) : 10000;

  const [cfg, setCfg] = useState(() => load() || { days: {} });
  const [editing, setEditing] = useState(false);
  const [inputAmt, setInputAmt] = useState('');
  const [dayChoice, setDayChoice] = useState('today'); // 'today' | 'yesterday'

  useEffect(() => {
    let alive = true;
    pullKey('fm_daily').then((v) => { if (alive && v && v.days) { try { localStorage.setItem('fm_daily', JSON.stringify(v)); } catch { /* ignore */ } setCfg(v); } });
    return () => { alive = false; };
  }, []);

  const days = cfg.days || {};
  const today = todayStr();
  const yest = dayKey(new Date(Date.now() - 86400000));
  const m = monthStr();
  const loggedToday = days[today] != null;
  const selDate = dayChoice === 'yesterday' ? yest : today;
  const loggedSel = days[selDate] != null;

  // 월별 합계 → 이번 달 실제 / 초과분 누적
  const byMonth = {};
  Object.entries(days).forEach(([d, amt]) => { const mk = d.slice(0, 7); byMonth[mk] = (byMonth[mk] || 0) + (Number(amt) || 0); });
  const monthTotal = byMonth[m] || 0;
  const streak = streakOf(days);
  const planPct = monthlyPlan > 0 ? Math.max(0, Math.min(100, (monthTotal / monthlyPlan) * 100)) : 0;

  const openInput = () => { setDayChoice('today'); setInputAmt(String(days[today] || suggested)); setEditing(true); };
  const pickDay = (c) => { setDayChoice(c); const dt = c === 'yesterday' ? yest : today; setInputAmt(days[dt] != null ? String(days[dt]) : (c === 'today' ? String(suggested) : '')); };
  const saveToday = () => {
    const amt = Math.max(0, Math.round(Number(String(inputAmt).replace(/[^0-9]/g, '')) || 0));
    const nextDays = { ...days };
    if (amt > 0) nextDays[selDate] = amt; else delete nextDays[selDate];
    const next = { ...cfg, days: nextDays };
    save(next); setCfg(next); pushState('fm_daily', next); notifySavingsChanged(); setEditing(false);
  };
  const reset = () => { if (!window.confirm('적립 기록을 모두 지울까요? 되돌릴 수 없어요.')) return; const next = { days: {} }; save(next); setCfg(next); pushState('fm_daily', next); notifySavingsChanged(); setEditing(false); };

  return (
    <section className="fm-card fm-dep live">
      <div className="fm-dc-top">
        <p className="fm-kicker">매일 적립 💰 {streak}일 연속{streak >= 3 ? ' 🔥' : ''}</p>
        {Object.keys(days).length > 0 && <button type="button" className="fm-inline-link" onClick={reset}>초기화</button>}
      </div>

      {monthlyPlan > 0 ? (
        <>
          <div className="fm-dep-goalrow">
            <span>이번 달 실제 저축</span>
            <b>{Math.round(planPct)}%</b>
          </div>
          <div className="fm-dep-gauge"><i style={{ width: `${planPct}%` }} /></div>
          <p className="fm-dep-mini">
            이번 달 <b>{won(monthTotal)}</b> / 계획 {won(monthlyPlan)}
            {monthTotal >= monthlyPlan && monthlyPlan > 0 ? <> · 계획 달성! 위 ‘실제 퇴사’에 반영돼요</> : null}
          </p>
        </>
      ) : (
        <p className="fm-dep-mini">이번 달 실제 저축 <b>{won(monthTotal)}</b> · {Object.keys(days).length}일 기록 · <button type="button" className="fm-inline-link" onClick={() => onMove && onMove('result')}>퇴사 나이 계산</button>하면 계획 대비 진행이 보여요</p>
      )}

      {editing ? (
        <div className="fm-dep-edit">
          <div className="fm-dep-daytoggle" role="group" aria-label="기록할 날짜">
            <button type="button" className={dayChoice === 'today' ? 'on' : ''} onClick={() => pickDay('today')}>오늘</button>
            <button type="button" className={dayChoice === 'yesterday' ? 'on' : ''} onClick={() => pickDay('yesterday')}>어제</button>
          </div>
          <label className="fm-dep-inlabel" htmlFor="fm-dep-in">{dayChoice === 'yesterday' ? '어제' : '오늘'} 실제로 저축한 금액 (원)</label>
          <input id="fm-dep-in" inputMode="numeric" className="fm-dep-in" value={inputAmt} onChange={(e) => setInputAmt(e.target.value.replace(/[^0-9]/g, ''))} placeholder={String(suggested)} />
          <div className="fm-dep-edit-row">
            <button type="button" className="fm-dep-edit-reset" onClick={() => setEditing(false)}>취소</button>
            <button type="button" className="fm-dep-edit-save" onClick={saveToday}>저장</button>
          </div>
          <p className="fm-dc-note">매일 실제 저축액을 기록하면 “이번 달 실제 저축”이 쌓여요. 빠뜨렸으면 ‘어제’로 바꿔 소급 입력할 수 있어요.</p>
        </div>
      ) : (
        <>
          {loggedToday
            ? <button type="button" className="fm-dep-check done" onClick={openInput}>오늘 저축 {won(days[today])} 기록됨 · 수정 ✏️</button>
            : <button type="button" className="fm-dep-check" onClick={openInput}>오늘 저축 입력하기 ✍️</button>}
          <p className="fm-dc-foot">
            {loggedToday
              ? `오늘 기록 완료 · 내일도 적으면 ${streak + 1}일 연속!`
              : '오늘 실제로 저축한 금액을 적어보세요. 계획보다 더 모으면 퇴사가 당겨져요.'}
          </p>
        </>
      )}
    </section>
  );
}
