import { useState, useEffect } from 'react';
import { fmtAdvance, dailyNeedOf } from '../../firemap-v2/dailyData.js';
import { pushState, pullKey } from '../../utils/firemapStateApi.js';

const KEY = 'fm_daily';
const todayStr = () => new Date().toISOString().slice(0, 10);
const monthStr = () => new Date().toISOString().slice(0, 7);
const yesterdayStr = () => new Date(Date.now() - 86400000).toISOString().slice(0, 10);
const load = () => { try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch { return null; } };
const save = (o) => { try { localStorage.setItem(KEY, JSON.stringify(o)); } catch { /* ignore */ } };
const won = (n) => `${Math.round(n).toLocaleString('ko-KR')}원`;

// 적립 = 내 본 저축. 매월 '계획(월 저축액)'까지는 이미 퇴사 나이에 반영 → 앞당김 0.
// 계획을 '초과'한 만큼만 추가 자산으로 보고 퇴사를 앞당김(이중계산 없음).
export default function DepositCard({ simulation, onMove }) {
  const inp = (simulation && simulation.inputs) || {};
  const fireAge = (simulation && simulation.earliestRetirementAge) || inp.targetRetirementAge || null;
  const monthlyPlan = inp.monthlyInvestment || 0;
  const dailyNeed = dailyNeedOf(simulation);
  const defaultDaily = monthlyPlan > 0 ? Math.max(1000, Math.round(monthlyPlan / 30 / 1000) * 1000) : 10000;

  const [cfg, setCfg] = useState(load);
  const [amount, setAmount] = useState((cfg && cfg.amount) || defaultDaily);
  const [editing, setEditing] = useState(false);

  useEffect(() => {
    let alive = true;
    pullKey('fm_daily').then((v) => { if (alive && v) { try { localStorage.setItem('fm_daily', JSON.stringify(v)); } catch { /* ignore */ } setCfg(v); if (v.amount) setAmount(v.amount); } });
    return () => { alive = false; };
  }, []);

  const start = () => { const o = { amount, total: 0, streak: 0, days: 0, lastDate: null, monthKey: null, monthTotal: 0, surplusTotal: 0 }; save(o); setCfg(o); };
  const reset = () => { if (!window.confirm('적립 기록을 초기화할까요? 누적·연속일이 사라져요.')) return; try { localStorage.removeItem(KEY); } catch { /* ignore */ } setCfg(null); setEditing(false); };
  const openEdit = () => { setAmount((cfg && cfg.amount) || defaultDaily); setEditing((e) => !e); };
  const saveAmount = () => { const next = { ...cfg, amount }; save(next); setCfg(next); pushState('fm_daily', next); setEditing(false); };

  if (!cfg) {
    return (
      <section className="fm-card fm-dep">
        <p className="fm-kicker">매일 적립 챌린지 💰</p>
        <h2>하루 한 번 모으고, 계획을 넘기면 퇴사 당기기</h2>
        <p className="fm-dc-sub">하루 적립액은 계산기에 넣은 월 저축액 기준이에요(슬라이더로 자유롭게 조절). 매일 ‘오늘 적립’을 누르면 이번 달 계획 바가 차오르고, <b>월 저축액을 초과해 더 모은 만큼만</b> 퇴사가 앞당겨져요.</p>
        <div className="fm-dc-set">
          <div className="fm-dc-amt">하루 <b>{won(amount)}</b></div>
          <input type="range" min="1000" max="100000" step="1000" value={amount} onChange={(e) => setAmount(Number(e.target.value))} />
        </div>
        <button type="button" className="fm-dc-start" onClick={start}>이 금액으로 시작하기 ▶</button>
        <p className="fm-dc-note">퇴사 나이는 계산 결과 그대로예요. 계획보다 더 모은 ‘초과분’만 추가로 당깁니다.</p>
      </section>
    );
  }

  const today = todayStr();
  const m = monthStr();
  const checkedToday = cfg.lastDate === today;
  const broken = cfg.lastDate && cfg.lastDate !== today && cfg.lastDate !== yesterdayStr();
  const dispStreak = broken && !checkedToday ? 0 : (cfg.streak || 0);
  const monthTotal = cfg.monthKey === m ? (cfg.monthTotal || 0) : 0;
  const surplus = cfg.surplusTotal || 0;
  const planPct = monthlyPlan > 0 ? Math.max(0, Math.min(100, (monthTotal / monthlyPlan) * 100)) : 0;
  const advLabel = dailyNeed && surplus > 0 ? (fmtAdvance((surplus / dailyNeed) * 86400) || null) : null;

  const checkIn = () => {
    if (cfg.lastDate === today) return;
    const cont = cfg.lastDate === yesterdayStr();
    const base = cfg.monthKey === m ? (cfg.monthTotal || 0) : 0;
    const after = base + cfg.amount;
    const surplusGain = Math.max(0, after - Math.max(base, monthlyPlan)); // 계획 초과한 부분만
    const next = {
      ...cfg,
      total: (cfg.total || 0) + cfg.amount,
      days: (cfg.days || 0) + 1,
      streak: cont ? (cfg.streak || 0) + 1 : 1,
      lastDate: today,
      monthKey: m,
      monthTotal: after,
      surplusTotal: (cfg.surplusTotal || 0) + surplusGain
    };
    save(next); setCfg(next); pushState('fm_daily', next);
  };

  return (
    <section className="fm-card fm-dep live">
      <div className="fm-dc-top">
        <p className="fm-kicker">매일 적립 💰 {dispStreak}일 연속{dispStreak >= 3 ? ' 🔥' : ''}</p>
        <button type="button" className="fm-inline-link" onClick={openEdit}>{editing ? '닫기' : `하루 ${won(cfg.amount)} · 변경`}</button>
      </div>

      {editing ? (
        <div className="fm-dep-edit">
          <div className="fm-dc-amt">하루 <b>{won(amount)}</b></div>
          <input type="range" min="1000" max="100000" step="1000" value={amount} onChange={(e) => setAmount(Number(e.target.value))} />
          <div className="fm-dep-edit-row">
            <button type="button" className="fm-dep-edit-reset" onClick={reset}>기록 초기화</button>
            <button type="button" className="fm-dep-edit-save" onClick={saveAmount} disabled={amount === cfg.amount}>저장</button>
          </div>
          <p className="fm-dc-note">누적·연속일은 그대로 두고 하루 적립액만 바꿔요(다음 적립부터 적용).</p>
        </div>
      ) : (
        <>
          {monthlyPlan > 0 ? (
            <>
              <div className="fm-dep-goalrow">
                <span>이번 달 적립 계획</span>
                <b>{Math.round(planPct)}%</b>
              </div>
              <div className="fm-dep-gauge"><i style={{ width: `${planPct}%` }} /></div>
              <p className="fm-dep-mini">
                이번 달 {won(monthTotal)} / 계획 {won(monthlyPlan)}
                {advLabel ? <> · 계획 초과로 퇴사 <b>{advLabel}</b> 앞당김 ⏩</> : null}
                {fireAge ? ` · 예상 퇴사 ${fireAge}세` : ''}
              </p>
            </>
          ) : (
            <p className="fm-dep-mini">누적 적립 {won(cfg.total || 0)} · {cfg.days || 0}일 · <button type="button" className="fm-inline-link" onClick={() => onMove && onMove('result')}>퇴사 나이 계산</button>하면 계획 대비 진행이 보여요</p>
          )}

          {checkedToday
            ? <button type="button" className="fm-dep-done" disabled>오늘 적립 완료 ✅ · 내일 또 만나요</button>
            : <button type="button" className="fm-dep-check" onClick={checkIn}>오늘 적립 +{won(cfg.amount)} ✅</button>}
          <p className="fm-dc-foot">
            {checkedToday
              ? `오늘 채웠어요 · 내일도 적립하면 ${dispStreak + 1}일 연속!`
              : (broken ? '며칠 쉬었네요 — 오늘 다시 시작해요!' : '오늘 적립을 눌러 이번 달 계획을 채워가세요.')}
          </p>
        </>
      )}
    </section>
  );
}
