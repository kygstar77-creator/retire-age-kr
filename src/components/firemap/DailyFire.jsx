import { QUOTES, dayIdx, todayStr, wonStr, readJSON } from '../../firemap-v2/dailyData.js';

// 홈 두 번째 기둥 — '오늘의 절약' 요약 + 절약 탭 진입
export default function DailyFire({ onMove }) {
  const quote = QUOTES[dayIdx() % QUOTES.length];
  const sv = readJSON('fm_save');
  const streak = sv ? (sv.streak || 0) : 0;
  const todaySaved = sv && sv.lastDate === todayStr() ? (sv.today || 0) : 0;
  const totalSaved = sv ? (sv.total || 0) : 0;
  const go = () => (onMove ? onMove('save') : (window.location.hash = '#save'));
  return (
    <button type="button" className="fm-home-save-card" onClick={go}>
      <span className="fm-hs-wisdom">“{quote}”</span>
      <span className="fm-hs-kicker">오늘의 절약 🔥 {streak}일 연속</span>
      <span className="fm-hs-main">오늘 아낀 <b>{wonStr(todaySaved)}</b></span>
      <span className="fm-hs-sub">{totalSaved > 0 ? `누적 ${wonStr(totalSaved)} · ` : ''}오늘의 절약 기록하기 ›</span>
    </button>
  );
}
