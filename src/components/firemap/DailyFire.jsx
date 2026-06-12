import { QUOTES, dayIdx, todayStr, wonStr, readJSON, fmtAdvance } from '../../firemap-v2/dailyData.js';

// 홈 두 번째 기둥 — '오늘의 절약' 요약 + 절약 탭 진입
export default function DailyFire({ onMove }) {
  const quote = QUOTES[dayIdx() % QUOTES.length];
  const sv = readJSON('fm_save');
  const st = readJSON('fm_challenge');
  const plan = readJSON('fm_plan');
  const streak = st ? st.count : 0;
  const todaySaved = sv && sv.lastDate === todayStr() ? (sv.today || 0) : 0;
  const totalSaved = sv ? (sv.total || 0) : 0;
  const dailyNeed = plan && plan.dailyNeed ? plan.dailyNeed : null;
  const adv = (amt) => (dailyNeed ? fmtAdvance((amt / dailyNeed) * 86400) : null);
  const todayAdv = adv(todaySaved);
  const totalAdv = adv(totalSaved);
  const go = () => (onMove ? onMove('save') : (window.location.hash = '#save'));
  return (
    <button type="button" className="fm-home-save-card" onClick={go}>
      <span className="fm-hs-wisdom">“{quote}”</span>
      <span className="fm-hs-kicker">오늘의 절약 🔥 {streak}일 연속</span>
      <span className="fm-hs-main">오늘 아낀 <b>{wonStr(todaySaved)}</b>{todayAdv ? ` · 파이어 ${todayAdv} 앞당김` : ''}</span>
      <span className="fm-hs-sub">{totalSaved > 0 ? `누적 ${wonStr(totalSaved)}${totalAdv ? ` · ${totalAdv} 앞당김` : ''} · ` : ''}오늘의 절약 기록하기 ›</span>
    </button>
  );
}
