import { useState, useEffect } from 'react';
import { fmtAdvance, dailyNeedOf, wonStr } from '../../firemap-v2/dailyData.js';

const KEY = 'fm_daily';
const load = () => { try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch { return null; } };
const save = (o) => { try { localStorage.setItem(KEY, JSON.stringify(o)); } catch { /* ignore */ } };
const saveTotalNow = () => { try { const o = JSON.parse(localStorage.getItem('fm_save') || 'null'); return (o && o.total) || 0; } catch { return 0; } };

// 하루 저축액을 정하면, 매 순간 퇴사가 앞당겨지는 걸 실시간으로 보여주는 라이브 시계.
export default function DailyClock({ simulation }) {
  const dailyNeed = dailyNeedOf(simulation);
  const inp = simulation.inputs;
  const fireAge = simulation.earliestRetirementAge || inp.targetRetirementAge;
  const [cfg, setCfg] = useState(load);
  const [amount, setAmount] = useState((cfg && cfg.amount) || 10000);
  const [now, setNow] = useState(Date.now());

  useEffect(() => {
    if (!cfg) return undefined;
    const t = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(t);
  }, [cfg]);

  if (dailyNeed == null) {
    return (
      <section className="fm-card fm-dc done">
        <p className="fm-kicker">퇴사 라이브 시계 ⏱</p>
        <p>이미 목표 자산을 넘었어요. 매일 더 모으는 돈은 은퇴 후 여유로 그대로 쌓여요. 🎉</p>
      </section>
    );
  }

  const start = () => { const o = { amount, start: Date.now() }; save(o); setCfg(o); };
  const reset = () => { try { localStorage.removeItem(KEY); } catch { /* ignore */ } setCfg(null); };

  if (!cfg) {
    return (
      <section className="fm-card fm-dc">
        <p className="fm-kicker">퇴사 라이브 시계 ⏱</p>
        <h2>하루 얼마씩 모으면 퇴사가 다가올까?</h2>
        <p className="fm-dc-sub">매일 정한 금액을 모은다고 가정하면, 퇴사가 지금 이 순간에도 앞당겨지는 걸 실시간으로 보여드려요. 절약 탭에서 아낀 돈도 자동으로 합산돼요. 내일 다시 오면 더 당겨져 있어요.</p>
        <div className="fm-dc-set">
          <div className="fm-dc-amt">하루 <b>{wonStr(amount)}</b></div>
          <input type="range" min="1000" max="100000" step="1000" value={amount} onChange={(e) => setAmount(Number(e.target.value))} />
        </div>
        <button type="button" className="fm-dc-start" onClick={start}>이 금액으로 시작하기 ▶</button>
        <p className="fm-dc-note">실제 투자 권유가 아니라 동기부여용 가정이에요. 언제든 금액을 바꾸거나 끌 수 있어요.</p>
      </section>
    );
  }

  const elapsedSec = Math.max(0, (now - cfg.start) / 1000);
  const days = Math.floor(elapsedSec / 86400);
  const accruedDaily = cfg.amount * (elapsedSec / 86400);
  const saveTotal = saveTotalNow();
  const accrued = accruedDaily + saveTotal;
  const advLabel = fmtAdvance((accrued / dailyNeed) * 86400) || '0초';
  const todayAccrued = cfg.amount * ((elapsedSec % 86400) / 86400);
  const todayAdv = fmtAdvance((todayAccrued / dailyNeed) * 86400) || '0초';

  return (
    <section className="fm-card fm-dc live">
      <div className="fm-dc-top">
        <p className="fm-kicker">퇴사 라이브 시계 ⏱ {days + 1}일째</p>
        <button type="button" className="fm-inline-link" onClick={reset}>설정</button>
      </div>
      <div className="fm-dc-big">
        <small>하루저축 {wonStr(accruedDaily)}{saveTotal > 0 ? ` + 절약 ${wonStr(saveTotal)}` : ''} · 합계 {wonStr(accrued)}</small>
        <b>퇴사 {advLabel} 앞당김</b>
        <span className="fm-dc-tick">⏱ 지금도 다가오는 중…</span>
      </div>
      <p className="fm-dc-foot">오늘 저축분으로만 +{todayAdv} · 절약 탭에서 더 아끼면 그만큼 추가로 당겨져요. 예상 퇴사 {fireAge}세 기준.</p>
    </section>
  );
}
