import { useEffect, useState } from 'react';
import { computeProgress, ageLabel, gapLabel, hasCalculated } from '../../utils/savingsEngine.js';

const won = (n) => `${Math.round(n).toLocaleString('ko-KR')}원`;

// 헤드라인: 계획 파이어(기준선) vs 실제 파이어(실제 저축 반영) + 격차. 앞당김=초록, 밀림=앰버.
export default function FireStatus({ simulation, onMove }) {
  const [, setTick] = useState(0);
  useEffect(() => {
    const fn = () => setTick((t) => t + 1);
    window.addEventListener('fm-savings-changed', fn);
    window.addEventListener('focus', fn);
    return () => { window.removeEventListener('fm-savings-changed', fn); window.removeEventListener('focus', fn); };
  }, []);

  if (!hasCalculated()) return null;
  const p = computeProgress(simulation);
  const inp = simulation.inputs;
  const cur = Number(inp.currentAge) || 0;
  const canRetire = !!(simulation && simulation.earliestRetirementAge);

  if (!canRetire) {
    return (
      <section className="fm-card fm-status even">
        <p className="fm-kicker">내 파이어 현황</p>
        <p className="fm-status-note">지금 조건만으론 파이어가 어려워요. 저축·절약을 쌓거나 <button type="button" className="fm-inline-link" onClick={() => onMove && onMove('result')}>조건을 바꿔</button> 보면 ‘실제 파이어’가 잡혀요.</p>
      </section>
    );
  }

  if (p.atGoal) {
    return (
      <section className="fm-card fm-status done">
        <p className="fm-kicker">내 파이어 현황</p>
        <p className="fm-status-done">🎉 이미 목표 자산을 넘었어요. 적립·절약으로 모은 돈은 파이어 후 여유로 그대로 쌓여요.</p>
      </section>
    );
  }

  const planAge = p.planAge;
  const actAge = p.actualAgeYears != null ? p.actualAgeYears : planAge;
  const dir = p.direction; // ahead | behind | even
  const gap = gapLabel(p.advanceDays);
  const src = (p.depDev > 0 && p.saveBonus > 0) ? '절약·초과 적립으로' : p.depDev > 0 ? '초과 적립으로' : '절약으로';

  const end = Math.max(planAge, actAge) + 0.0001;
  const span = Math.max(1, end - cur);
  const planPct = Math.max(0, Math.min(100, ((planAge - cur) / span) * 100));
  const actPct = Math.max(0, Math.min(100, ((actAge - cur) / span) * 100));
  const fillPct = Math.min(planPct, actPct);

  return (
    <section className={`fm-card fm-status ${dir}`}>
      <p className="fm-kicker">내 파이어 현황</p>

      <div className="fm-status-ages">
        <div className="fm-status-age plan">
          <small>계획 파이어</small>
          <b>{ageLabel(planAge)}</b>
        </div>
        <div className={`fm-status-age actual ${dir}`}>
          <small>실제 파이어</small>
          <b>{ageLabel(actAge)}</b>
        </div>
      </div>

      <div className={`fm-status-gap ${dir}`}>
        {dir === 'ahead' && <span>⏩ {src} <b>{gap} 앞당김</b></span>}
        {dir === 'behind' && <span>🐢 적립이 계획보다 부족해 <b>{gap} 밀림</b></span>}
        {dir === 'even' && <span>계획대로 가는 중 — 절약하면 앞당겨져요</span>}
      </div>

      <div className="fm-status-track">
        <div className="fm-status-fill" style={{ width: `${fillPct}%` }} />
        <span className="fm-status-flag act" style={{ left: `${actPct}%` }} aria-hidden="true">🏁</span>
        <span className="fm-status-flag plan" style={{ left: `${planPct}%` }} aria-hidden="true">🏁</span>
      </div>
      <div className="fm-status-axis">
        <span>지금 {cur}세</span>
        <span>{dir === 'behind' ? '계획 · 실제' : dir === 'ahead' ? '실제 · 계획' : '계획'}</span>
      </div>

      <div className="fm-status-feed">
        <button type="button" className="fm-status-chip" onClick={() => onMove && onMove('save')}>
          <small>이번 달 적립</small>
          <b>{won(p.monthDeposit)}{p.monthlyPlan > 0 ? <em> / {won(p.monthlyPlan)}</em> : null}</b>
        </button>
        <button type="button" className="fm-status-chip" onClick={() => onMove && onMove('save')}>
          <small>누적 절약</small>
          <b>{won(p.saveBonus)}</b>
        </button>
      </div>
      <p className="fm-status-note">적립·절약이 ‘실제 저축’으로 합쳐져 실제 파이어 나이에 반영돼요. 같은 돈은 한 번만 기록하세요.</p>
      <button type="button" className="fm-inline-link fm-plan-link" onClick={() => onMove && onMove('firePlan')}>📊 내 파이어 플랜 자세히 보기 →</button>
    </section>
  );
}
