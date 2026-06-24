import { useEffect, useState } from 'react';
import { readJSON, todayStr, yesterdayStr } from '../../firemap-v2/dailyData.js';

// 저축 습관 루프 — 연속 기록 스트릭 + 마일스톤 + 다음날 넛지.
// 표시 전용: 실제 기록 데이터를 '읽기만' 함(계산·저장 로직 무손상).
// 스트릭은 사용자가 실제로 채우는 적립 달력(fm_daily.days{날짜:금액})에서 직접 계산한다.
// (절약 달력 fm_save.daily, 오늘 절약 fm_save.today 도 함께 병합 → 어느 경로로 기록해도 반영)
// 'fm-savings-changed' 이벤트로 기록 직후 자동 갱신. 비로그인 기기 기록도 그대로 동작.
const MILES = [3, 7, 14, 30, 60, 100, 365];

function localYmd(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}

// 저축한 날짜 집합(YYYY-MM-DD) 수집
function savedDateSet() {
  const set = new Set();
  const daily = readJSON('fm_daily');
  if (daily && daily.days) for (const k in daily.days) { if (Number(daily.days[k]) > 0) set.add(k); }
  const sv = readJSON('fm_save');
  if (sv && sv.daily) for (const k in sv.daily) { if (Number(sv.daily[k]) > 0) set.add(k); }
  if (sv && sv.lastDate && Number(sv.today) > 0) set.add(sv.lastDate);
  return set;
}

function readState() {
  const set = savedDateSet();
  if (set.size === 0) return { streak: 0, status: 'none' };
  const today = todayStr();
  const yest = yesterdayStr();
  let anchor;
  if (set.has(today)) anchor = today;        // 오늘 기록 있음 → 완료
  else if (set.has(yest)) anchor = yest;     // 어제까지 연속, 오늘 아직 → 넛지(risk)
  else return { streak: 0, status: 'broken' };
  let streak = 0;
  const d = new Date(`${anchor}T00:00:00`);
  while (set.has(localYmd(d))) { streak += 1; d.setDate(d.getDate() - 1); }
  return { streak, status: anchor === today ? 'done' : 'risk' };
}

export default function SaveStreak({ onMove, compact }) {
  const [st, setSt] = useState(readState);
  useEffect(() => {
    const h = () => setSt(readState());
    window.addEventListener('fm-savings-changed', h);
    return () => window.removeEventListener('fm-savings-changed', h);
  }, []);
  const { streak, status } = st;
  if (status === 'none' && compact) return null;

  const nextMile = MILES.find((m) => m > streak) || null;
  const toNext = nextMile ? nextMile - streak : 0;
  const justHit = status === 'done' && MILES.includes(streak);
  const go = () => { if (onMove) onMove('save'); };

  if (compact) {
    const msg = status === 'done'
      ? `🔥 저축 ${streak}일 연속 · 오늘 완료 ✓`
      : status === 'risk'
        ? `🔥 ${streak}일 연속 · 오늘 기록하면 ${streak + 1}일! 이어가기 →`
        : `💪 저축 스트릭 다시 시작 · 오늘 한 건 →`;
    const hot = status === 'risk';
    return (
      <button type="button" onClick={go} style={{
        display: 'flex', alignItems: 'center', gap: 8, width: '100%', textAlign: 'left', cursor: 'pointer',
        border: hot ? '1px solid #ff8a4c' : '1px solid #ffe1d0', background: hot ? '#fff4ec' : '#fffaf6',
        borderRadius: 14, padding: '12px 14px', margin: '0 0 12px', color: '#9a3412', fontSize: 13.5, fontWeight: 700
      }}>{msg}</button>
    );
  }

  const headline = status === 'done'
    ? `🔥 ${streak}일 연속 저축 중!`
    : status === 'risk'
      ? `🔥 ${streak}일 연속 — 오늘이 고비!`
      : status === 'broken'
        ? '💪 다시 시작해요'
        : '🔥 오늘부터 연속 저축 시작!';
  const sub = status === 'done'
    ? (justHit ? `🎉 ${streak}일 달성! 대단해요 — 내일도 이어가요` : '오늘 기록 완료 ✓ 내일도 한 건이면 이어져요')
    : status === 'risk'
      ? `오늘도 기록하면 ${streak + 1}일째예요. 아래 달력에서 오늘 칸을 채워 스트릭을 지켜요!`
      : status === 'broken'
        ? '스트릭이 끊겼어요. 오늘 한 건이면 다시 1일째로 시작돼요.'
        : '오늘 한 건만 기록해도 연속 1일이 시작돼요.';

  return (
    <section className="fm-card" style={{
      background: status === 'risk' ? 'linear-gradient(180deg,#fff4ec,#fff)' : '#fffaf6',
      border: status === 'risk' ? '1px solid #ff8a4c' : '1px solid #ffe1d0', borderRadius: 16, padding: '15px 16px'
    }} aria-live="polite">
      <p style={{ margin: 0, fontSize: 17, fontWeight: 800, color: '#15151b' }}>{headline}</p>
      <p style={{ margin: '4px 0 0', fontSize: 13, color: '#9a3412', fontWeight: 600, lineHeight: 1.5 }}>{sub}</p>
      {nextMile && (streak > 0 || status === 'risk') && (
        <div style={{ marginTop: 10 }}>
          <div style={{ height: 7, borderRadius: 99, background: '#ffe1d0', overflow: 'hidden' }}>
            <div style={{ height: '100%', width: `${Math.max(6, Math.min(100, Math.round((streak / nextMile) * 100)))}%`, background: '#ff5a00' }} />
          </div>
          <p style={{ margin: '6px 0 0', fontSize: 11.5, color: '#b45309', fontWeight: 700 }}>다음 🏅 {nextMile}일까지 {toNext}일 남았어요</p>
        </div>
      )}
    </section>
  );
}
