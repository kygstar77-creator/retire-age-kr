// DS-26 Countdown — 파이어까지 남은 시간(년·일 + 시:분:초). 글자 크기는 토큰(--ds-fs-*)만 쓴다.
// 개편 1~2주차에 빠졌으나 조사 7번(디데이·카운트다운 수요 검증: TheDayBefore·倒数日)에 따라 되살린다.
// 목표 시각은 한 번 정해 저장해 두므로 새로고침해도 리셋되지 않고 실제로 줄어든다. 파이어 나이가 바뀌면 다시 잡는다.
import { useEffect, useRef, useState } from 'react';

const SEC_DAY = 86400;
const SEC_YEAR = Math.floor(365.25 * SEC_DAY);
const TARGET_KEY = 'fm_fire_target';
const pad = (n) => String(n).padStart(2, '0');

function decompose(ms) {
  const totalSec = Math.max(0, Math.floor(ms / 1000));
  const totalDays = Math.floor(totalSec / SEC_DAY);
  const yr = Math.floor(totalDays / 365);
  const days = totalDays - yr * 365;
  let r = totalSec - totalDays * SEC_DAY;
  const h = Math.floor(r / 3600); r -= h * 3600;
  const m = Math.floor(r / 60); const s = r - m * 60;
  return { yr, days, h, m, s };
}
const readTarget = () => { try { return JSON.parse(localStorage.getItem(TARGET_KEY) || 'null'); } catch { return null; } };

export function Countdown({ simulation }) {
  const [, setTick] = useState(0);
  const targetRef = useRef(null);
  const cur = Number(simulation?.inputs?.currentAge) || 0;
  const fireAge = simulation?.earliestRetirementAge || 0;
  const rem = fireAge && cur ? fireAge - cur : null;

  const reanchor = () => {
    if (rem == null) { targetRef.current = null; return; }
    if (rem <= 0) { targetRef.current = 0; return; }
    const stored = readTarget();
    if (stored && Number(stored.fireAge) === fireAge && Number(stored.at) > Date.now()) {
      targetRef.current = Number(stored.at);
    } else {
      const at = Date.now() + rem * SEC_YEAR * 1000;
      targetRef.current = at;
      try { localStorage.setItem(TARGET_KEY, JSON.stringify({ at, fireAge })); } catch { /* ignore */ }
    }
  };

  useEffect(() => {
    reanchor();
    const t = setInterval(() => setTick((n) => n + 1), 1000);
    return () => clearInterval(t);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [fireAge, cur]);

  if (rem == null) return null;
  if (rem <= 0) {
    return (
      <div className="ds-countdown ds-countdown--done">
        <p className="ds-countdown__cap">파이어 카운트다운</p>
        <p className="ds-countdown__big">지금 파이어 가능!</p>
      </div>
    );
  }
  if (targetRef.current == null) reanchor();
  const d = decompose((targetRef.current || Date.now()) - Date.now());
  return (
    <div className="ds-countdown">
      <p className="ds-countdown__cap">파이어까지 남은 시간</p>
      <p className="ds-countdown__big"><b className="num">{d.yr}</b>년 <b className="num">{d.days}</b>일</p>
      <p className="ds-countdown__time num">{pad(d.h)}:{pad(d.m)}:{pad(d.s)}</p>
    </div>
  );
}
