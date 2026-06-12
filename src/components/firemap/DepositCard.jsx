import { useState } from 'react';
import { fmtAdvance } from '../../firemap-v2/dailyData.js';

const KEY = 'fm_daily';
const todayStr = () => new Date().toISOString().slice(0, 10);
const yesterdayStr = () => new Date(Date.now() - 86400000).toISOString().slice(0, 10);
const load = () => { try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch { return null; } };
const save = (o) => { try { localStorage.setItem(KEY, JSON.stringify(o)); } catch { /* ignore */ } };
const wonStr = (n) => `${Math.round(n).toLocaleString('ko-KR')}원`;
const readPlan = () => { try { return JSON.parse(localStorage.getItem('fm_plan') || 'null'); } catch { return null; } };
const saveBonus = () => { try { const o = JSON.parse(localStorage.getItem('fm_save') || 'null'); return (o && o.total) || 0; } catch { return 0; } };

// 매일 '오늘 적립'을 눌러 누적·연속일을 쌓는 습관형 카드. 퇴사 나이 계산 결과(fm_plan)가 있으면 앞당김도 표시.
export default function DepositCard({ onMove }) {
  const [cfg, setCfg] = useState(load);
  const [amount, setAmount] = useState((cfg && cfg.amount) || 10000);
  const plan = readPlan();
  const dailyNeed = plan && typeof plan.dailyNeed === 'number' ? plan.dailyNeed : null;
  const goalReached = !!(plan && plan.ok === true);

  const start = () => { const o = { amount, total: 0, streak: 0, days: 0, lastDate: null }; save(o); setCfg(o); };
  const reset = () => { try { localStorage.removeItem(KEY); } catch { /* ignore */ } setCfg(null); };

  if (!cfg) {
    return (
      <section className="fm-card fm-dc fm-dep">
        <p className="fm-kicker">매일 적립 챌린지 💰</p>
        <h2>하루 얼마씩 모아 퇴사 앞당기기</h2>
        <p className="fm-dc-sub">계산기에 입력한 월 저축액과는 별개로, 평소보다 ‘더’ 모으는 추가 적립이에요. 매일 ‘오늘 적립’만 누르면 누적·연속일이 쌓이고 퇴사가 그만큼 앞당겨져요.</p>
        <div className="fm-dc-set">
          <div className="fm-dc-amt">하루 <b>{wonStr(amount)}</b></div>
          <input type="range" min="1000" max="100000" step="1000" value={amount} onChange={(e) => setAmount(Number(e.target.value))} />
        </div>
        <button type="button" className="fm-dc-start" onClick={start}>이 금액으로 시작하기 ▶</button>
        <p className="fm-dc-note">실제 투자 권유가 아니라 습관 만들기용이에요. 언제든 끄거나 금액을 바꿀 수 있어요.</p>
      </section>
    );
  }

  const today = todayStr();
  const checkedToday = cfg.lastDate === today;
  const broken = cfg.lastDate && cfg.lastDate !== today && cfg.lastDate !== yesterdayStr();
  const dispStreak = broken && !checkedToday ? 0 : (cfg.streak || 0);

  const checkIn = () => {
    if (cfg.lastDate === today) return;
    const cont = cfg.lastDate === yesterdayStr();
    const next = { ...cfg, total: (cfg.total || 0) + cfg.amount, days: (cfg.days || 0) + 1, streak: cont ? (cfg.streak || 0) + 1 : 1, lastDate: today };
    save(next); setCfg(next);
  };

  const bonus = saveBonus();
  const combined = (cfg.total || 0) + bonus;
  const advLabel = dailyNeed ? (fmtAdvance((combined / dailyNeed) * 86400) || '0초') : null;

  return (
    <section className="fm-card fm-dc fm-dep live">
      <div className="fm-dc-top">
        <p className="fm-kicker">매일 적립 💰 {dispStreak}일 연속{dispStreak >= 3 ? ' 🔥' : ''}</p>
        <button type="button" className="fm-inline-link" onClick={reset}>설정</button>
      </div>
      <div className="fm-dc-big">
        <small>누적 적립 {wonStr(cfg.total || 0)}{bonus > 0 ? ` + 절약 ${wonStr(bonus)}` : ''} · {cfg.days || 0}일 적립</small>
        <small className="fm-dep-hint">월 저축액과 별개의 추가분 기준</small>
        {advLabel
          ? <b>퇴사 {advLabel} 앞당김</b>
          : goalReached
            ? <b>이미 목표 달성! 💰</b>
            : <b>{wonStr(combined)} 모음</b>}
      </div>
      {checkedToday
        ? <button type="button" className="fm-dep-done" disabled>오늘 적립 완료 ✅ · 내일 또 만나요</button>
        : <button type="button" className="fm-dep-check" onClick={checkIn}>오늘 적립 +{wonStr(cfg.amount)} ✅</button>}
      <p className="fm-dc-foot">
        {checkedToday ? `내일도 적립하면 ${dispStreak + 1}일 연속!` : (broken ? '며칠 쉬었네요 — 오늘 다시 시작해요!' : '오늘 적립을 눌러 연속일을 이어가세요.')}
        {!dailyNeed && !goalReached && <> · <button type="button" className="fm-inline-link" onClick={() => onMove && onMove('result')}>퇴사 나이 계산</button>하면 며칠 앞당겨지는지 보여요</>}
      </p>
    </section>
  );
}
