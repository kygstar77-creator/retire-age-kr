import { useState } from 'react';

const KEY = 'fm_daily';
const todayStr = () => new Date().toISOString().slice(0, 10);
const yesterdayStr = () => new Date(Date.now() - 86400000).toISOString().slice(0, 10);
const load = () => { try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch { return null; } };
const save = (o) => { try { localStorage.setItem(KEY, JSON.stringify(o)); } catch { /* ignore */ } };
const won = (n) => `${Math.round(n).toLocaleString('ko-KR')}원`;
const big = (n) => {
  if (n >= 100000000) { const v = n / 100000000; return `${v % 1 === 0 ? v : v.toFixed(1)}억`; }
  if (n >= 10000) return `${Math.round(n / 10000).toLocaleString('ko-KR')}만`;
  return `${Math.round(n).toLocaleString('ko-KR')}원`;
};

// 적립 = 내 본 저축(월 저축액과 동기). 매일 체크인으로 연속일·목표까지 게이지가 차오름.
// 퇴사 나이는 계산 결과 그대로(이중계산·절약 중복 없음).
export default function DepositCard({ simulation, onMove }) {
  const inp = (simulation && simulation.inputs) || {};
  const target = (simulation && simulation.requiredFireAssetByFourPercent) || 0;
  const currentAsset = inp.financialAsset || 0;
  const fireAge = (simulation && simulation.earliestRetirementAge) || inp.targetRetirementAge || null;
  const monthlyInvest = inp.monthlyInvestment || 0;
  const defaultDaily = monthlyInvest > 0 ? Math.max(1000, Math.round(monthlyInvest / 30 / 1000) * 1000) : 10000;

  const [cfg, setCfg] = useState(load);
  const [amount, setAmount] = useState((cfg && cfg.amount) || defaultDaily);

  const start = () => { const o = { amount, total: 0, streak: 0, days: 0, lastDate: null }; save(o); setCfg(o); };
  const reset = () => { try { localStorage.removeItem(KEY); } catch { /* ignore */ } setCfg(null); };

  if (!cfg) {
    return (
      <section className="fm-card fm-dc fm-dep">
        <p className="fm-kicker">매일 적립 챌린지 💰</p>
        <h2>하루 한 번 모으고, 목표에 한 칸씩</h2>
        <p className="fm-dc-sub">하루 적립액은 계산기에 넣은 월 저축액 기준이에요(별도 추가가 아니라 ‘내 저축’ 그 자체). 매일 ‘오늘 적립’을 누르면 연속일이 쌓이고 목표 자산까지 게이지가 차올라요.</p>
        <div className="fm-dc-set">
          <div className="fm-dc-amt">하루 <b>{won(amount)}</b></div>
          <input type="range" min="1000" max="100000" step="1000" value={amount} onChange={(e) => setAmount(Number(e.target.value))} />
        </div>
        <button type="button" className="fm-dc-start" onClick={start}>이 금액으로 시작하기 ▶</button>
        <p className="fm-dc-note">퇴사 나이는 계산 결과 그대로예요. 적립은 그 목표까지 매일 채워가는 습관 트래커예요.</p>
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

  const saved = currentAsset + (cfg.total || 0);
  const hasGoal = target > 0;
  const pct = hasGoal ? Math.max(0, Math.min(100, (saved / target) * 100)) : 0;
  const reached = hasGoal && saved >= target;

  return (
    <section className="fm-card fm-dc fm-dep live">
      <div className="fm-dc-top">
        <p className="fm-kicker">매일 적립 💰 {dispStreak}일 연속{dispStreak >= 3 ? ' 🔥' : ''}</p>
        <button type="button" className="fm-inline-link" onClick={reset}>설정</button>
      </div>

      {hasGoal ? (
        <>
          <div className="fm-dep-goalrow">
            <span>목표 {big(target)}까지</span>
            <b>{reached ? '달성! 🎉' : `${pct.toFixed(pct < 10 ? 1 : 0)}%`}</b>
          </div>
          <div className="fm-dep-gauge"><i style={{ width: `${pct}%` }} /></div>
          <p className="fm-dep-mini">{fireAge ? <>이 속도면 예상 퇴사 <b>{fireAge}세</b> · </> : null}누적 적립 {won(cfg.total || 0)} · {cfg.days || 0}일</p>
        </>
      ) : (
        <p className="fm-dep-mini">누적 적립 {won(cfg.total || 0)} · {cfg.days || 0}일 적립 · <button type="button" className="fm-inline-link" onClick={() => onMove && onMove('result')}>퇴사 나이 계산</button>하면 목표 게이지가 생겨요</p>
      )}

      {checkedToday
        ? <button type="button" className="fm-dep-done" disabled>오늘 적립 완료 ✅ · 내일 또 만나요</button>
        : <button type="button" className="fm-dep-check" onClick={checkIn}>오늘 적립 +{won(cfg.amount)} ✅</button>}
      <p className="fm-dc-foot">
        {checkedToday
          ? `오늘 한 칸 채웠어요 · 내일도 적립하면 ${dispStreak + 1}일 연속!`
          : (broken ? '며칠 쉬었네요 — 오늘 다시 시작해요!' : '오늘 적립을 눌러 목표에 한 걸음 더 다가가세요.')}
      </p>
    </section>
  );
}
