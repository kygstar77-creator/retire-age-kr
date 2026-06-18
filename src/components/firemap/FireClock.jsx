import { useEffect, useRef, useState } from 'react';
import { computeProgress, hasCalculated } from '../../utils/savingsEngine.js';

const STYLE = `
.fm-clock{text-align:center;background:linear-gradient(135deg,#10151c,#1b2735);color:#fff;border-radius:18px;padding:16px 14px;margin:0 0 12px}
.fm-clock-cap{font-size:12px;color:#9fb0c2;margin:0 0 6px;font-weight:700}
.fm-clock-big{font-size:22px;font-weight:800;margin:0}
.fm-clock-big b{color:#ff8a3d}
.fm-clock-time{font-variant-numeric:tabular-nums;font-size:30px;font-weight:800;letter-spacing:.02em;margin:4px 0 0}
.fm-clock-sub{font-size:11.5px;color:#8aa0b4;margin:6px 0 0}
.fm-clock.done .fm-clock-big{color:#34d399}
`;

const SEC_DAY = 86400;
const SEC_YEAR = Math.floor(365.25 * SEC_DAY);
function decompose(ms) {
  let totalSec = Math.max(0, Math.floor(ms / 1000));
  const yr = Math.floor(totalSec / SEC_YEAR); totalSec -= yr * SEC_YEAR;
  const days = Math.floor(totalSec / SEC_DAY); totalSec -= days * SEC_DAY;
  const h = Math.floor(totalSec / 3600); totalSec -= h * 3600;
  const m = Math.floor(totalSec / 60); const s = totalSec - m * 60;
  return { yr, days, h, m, s };
}
const pad = (n) => String(n).padStart(2, '0');

export default function FireClock({ simulation }) {
  const [, setTick] = useState(0);
  const targetRef = useRef(null);

  const remYears = () => {
    if (!hasCalculated()) return null;
    const inp = (simulation && simulation.inputs) || {};
    const cur = Number(inp.currentAge) || 0;
    let fireAge;
    try { const p = computeProgress(simulation); fireAge = (p && p.actualAgeYears != null) ? p.actualAgeYears : (simulation.earliestRetirementAge || inp.targetRetirementAge); }
    catch { fireAge = simulation.earliestRetirementAge || inp.targetRetirementAge; }
    if (!fireAge || !cur) return null;
    return fireAge - cur;
  };

  const reanchor = () => {
    const rem = remYears();
    targetRef.current = (rem == null) ? null : Date.now() + Math.max(0, rem) * SEC_YEAR * 1000;
  };

  useEffect(() => {
    reanchor();
    const t = setInterval(() => setTick((n) => n + 1), 1000);
    const h = () => { reanchor(); setTick((n) => n + 1); };
    window.addEventListener('fm-savings-changed', h);
    return () => { clearInterval(t); window.removeEventListener('fm-savings-changed', h); };
    // eslint-disable-next-line
  }, []);

  const rem = remYears();
  if (rem == null) return null;
  if (rem <= 0) {
    return (
      <section className='fm-clock done'>
        <style>{STYLE}</style>
        <p className='fm-clock-cap'>🔥 파이어 카운트다운</p>
        <p className='fm-clock-big'>🎉 지금 파이어 가능!</p>
        <p className='fm-clock-sub'>이미 목표 자산을 넘었어요</p>
      </section>
    );
  }
  if (targetRef.current == null) reanchor();
  const left = (targetRef.current || Date.now()) - Date.now();
  const d = decompose(left);
  return (
    <section className='fm-clock'>
      <style>{STYLE}</style>
      <p className='fm-clock-cap'>🔥 파이어까지 남은 시간</p>
      <p className='fm-clock-big'><b>{d.yr}</b>년 <b>{d.days}</b>일</p>
      <p className='fm-clock-time'>{pad(d.h)}:{pad(d.m)}:{pad(d.s)}</p>
      <p className='fm-clock-sub'>매일 저축하면 시계가 빨라져요</p>
    </section>
  );
}
