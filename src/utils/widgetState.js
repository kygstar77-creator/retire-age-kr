// 위젯 상태 1벌 — 홈 3숫자 카드와(나중에) 앱 위젯 브리지가 같은 함수를 읽는다.
// { earliestAge, dday, streak, progressPct, updatedAt } — HIG '정보 하나'·Robinhood % only 원칙.
import { computeProgress, hasCalculated } from './savingsEngine.js';
import { todayStr, yesterdayStr, ymdOf } from './dates.js';

const readJSON = (k) => { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch { return null; } };

// 절약(fm_save.daily)과 적립(fm_daily.days)을 합친 연속 기록일. 오늘 없으면 어제부터 센다.
export function streakOf() {
  const a = (readJSON('fm_daily') || {}).days || {};
  const b = (readJSON('fm_save') || {}).daily || {};
  const has = (k) => (Number(a[k]) || 0) > 0 || (Number(b[k]) || 0) > 0;
  let d = new Date();
  if (!has(todayStr())) d = new Date(Date.now() - 86400000);
  let s = 0;
  for (let i = 0; i < 3660; i += 1) {
    const k = ymdOf(d);
    if (has(k)) { s += 1; d = new Date(d.getTime() - 86400000); } else break;
  }
  return s;
}

export const loggedToday = () => {
  const a = (readJSON('fm_daily') || {}).days || {};
  const b = (readJSON('fm_save') || {}).daily || {};
  const t = todayStr();
  return (Number(a[t]) || 0) > 0 || (Number(b[t]) || 0) > 0;
};

export const loggedYesterday = () => {
  const a = (readJSON('fm_daily') || {}).days || {};
  const b = (readJSON('fm_save') || {}).daily || {};
  const t = yesterdayStr();
  return (Number(a[t]) || 0) > 0 || (Number(b[t]) || 0) > 0;
};

export function buildWidgetState(simulation) {
  const inp = (simulation && simulation.inputs) || {};
  const cur = Number(inp.currentAge) || 0;
  let fireAge = simulation && (simulation.earliestRetirementAge || inp.targetRetirementAge);
  let actual = null;
  try { const p = computeProgress(simulation); if (p && p.actualAgeYears != null) actual = p.actualAgeYears; } catch { /* ignore */ }
  const ageYears = actual != null ? actual : fireAge;
  const dday = (simulation && simulation.earliestRetirementAge && ageYears && cur) ? Math.max(0, Math.round((ageYears - cur) * 365.25)) : null;
  const asset = Number(inp.financialAsset) || 0;
  const target = Math.round((simulation && simulation.requiredFireAssetByFourPercent) || 0);
  const progressPct = target > 0 ? Math.max(0, Math.min(100, Math.round((asset / target) * 100))) : 0;
  return {
    calculated: hasCalculated(),
    earliestAge: (simulation && simulation.earliestRetirementAge) || null,
    fireAgeYears: ageYears || null,
    dday,
    streak: streakOf(),
    progressPct,
    target,
    asset,
    updatedAt: Date.now()
  };
}

// 앱(Capacitor) 단계에서 네이티브 위젯 브리지가 읽을 스냅샷. 웹에선 localStorage에만 둔다.
export function syncWidgetSnapshot(simulation) {
  try { localStorage.setItem('fm_widget', JSON.stringify(buildWidgetState(simulation))); } catch { /* ignore */ }
}
