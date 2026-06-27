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
const SEC_YEAR = Math.floor(365.25 * SEC_DAY); // 목표 시각 계산용(달력 기준, 윤년 포함)
const TARGET_KEY = 'fm_fire_target';

// 남은 시간(ms) → 년/일/시/분/초. 표시는 1년=365일로 분해해 365일이 되면 다음 해로 올림(‘365일’ 박힘 방지).
function decompose(ms) {
  const totalSec = Math.max(0, Math.floor(ms / 1000));
  const totalDays = Math.floor(totalSec / SEC_DAY);
  const yr = Math.floor(totalDays / 365);
  const days = totalDays - yr * 365; // 0~364
  let r = totalSec - totalDays * SEC_DAY;
  const h = Math.floor(r / 3600); r -= h * 3600;
  const m = Math.floor(r / 60); const s = r - m * 60;
  return { yr, days, h, m, s };
}
const pad = (n) => String(n).padStart(2, '0');
const readTarget = () => { try { return JSON.parse(localStorage.getItem(TARGET_KEY) || 'null'); } catch { return null; } };

export default function FireClock({ simulation }) {
  const [, setTick] = useState(0);
  const targetRef = useRef(null);

  // 파이어 정보: { rem(남은 햇수), fireAge } / 계산 전이면 null
  const fireInfo = () => {
    if (!hasCalculated()) return null;
    const inp = (simulation && simulation.inputs) || {};
    const cur = Number(inp.currentAge) || 0;
    let fireAge;
    try { const p = computeProgress(simulation); fireAge = (p && p.actualAgeYears != null) ? p.actualAgeYears : (simulation.earliestRetirementAge || inp.targetRetirementAge); }
    catch { fireAge = simulation.earliestRetirementAge || inp.targetRetirementAge; }
    if (!fireAge || !cur) return null;
    return { rem: fireAge - cur, fireAge };
  };

  // 목표 시각(파이어 D-day)을 한 번 정해 저장 → 방문/새로고침마다 리셋되지 않고 실제로 줄어듦.
  // 계획(fireAge)이 바뀌면(재계산·저축 반영으로 시점 이동) 목표를 새로 잡음.
  const reanchor = () => {
    const info = fireInfo();
    if (info == null) { targetRef.current = null; return; }
    if (info.rem <= 0) { targetRef.current = 0; return; }
    const stored = readTarget();
    if (stored && Math.abs(Number(stored.fireAge) - info.fireAge) < 0.02 && Number(stored.at) > Date.now()) {
      targetRef.current = Number(stored.at); // 같은 계획이면 기존 목표 유지(카운트다운 진행)
    } else {
      const at = Date.now() + info.rem * SEC_YEAR * 1000;
      targetRef.current = at;
      try { localStorage.setItem(TARGET_KEY, JSON.stringify({ at, fireAge: info.fireAge })); } catch { /* ignore */ }
    }
  };

  useEffect(() => {
    reanchor();
    const t = setInterval(() => setTick((n) => n + 1), 1000);
    const h = () => { reanchor(); setTick((n) => n + 1); };
    window.addEventListener('fm-savings-changed', h);
    return () => { clearInterval(t); window.removeEventListener('fm-savings-changed', h); };
    // eslint-disable-next-line
  }, []);

  const info = fireInfo();
  if (info == null) return null;
  if (info.rem <= 0) {
    return (
      <section className='fm-clock done'>
        <style>{STYLE}</style>
        <p className='fm-clock-cap'>🔥 파이어 카운트다운</p>
        <p className='fm-clock-big'>🎉 지금 파이어 가능!</p>
        <p className='fm-clock-sub'>이미 목표 자산을 넘었어요</p>
      </section>
    );
  }
  if (targetRef.current == null || targetRef.current === 0) reanchor();
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
