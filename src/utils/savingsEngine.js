// 실제저축 ↔ 퇴사나이 엔진
// 모델: 계획(월 저축액)이 퇴사 나이의 뼈대. 적립·절약으로 만든 "계획 대비 차액(D)"만
//       자산에 더하거나 빼서 실제 퇴사 나이를 양방향으로 움직인다. 저축률을 다시 추정하지 않는다.
// - 적립(fm_daily.days): 월 단위 확정. 완료된 달 Σ(실제−계획). 진행 중인 달은 양수 초과분만(밀림 보류).
// - 절약(fm_save.total): 계획과 무관한 전액 보너스(항상 +). 즉시 반영.
// - 중복 0: 계획분은 저축률로 1번(earliestRetirementAge), 차액은 자산으로 1번. 안 겹침.
import { dailyNeedOf } from '../firemap-v2/dailyData.js';
import { statsRank } from '../firemap-v2/rank.js';
import { submitSave } from './firemapSaveApi.js';

const readJSON = (k) => { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch { return null; } };
const monthStr = () => new Date().toISOString().slice(0, 7);

// 적립 일별 장부 → 월별 합계
function depositByMonth() {
  const cfg = readJSON('fm_daily');
  const days = (cfg && cfg.days) || {};
  const byMonth = {};
  Object.entries(days).forEach(([d, amt]) => {
    const mk = String(d).slice(0, 7);
    byMonth[mk] = (byMonth[mk] || 0) + (Number(amt) || 0);
  });
  return byMonth;
}

function savingTotal() {
  const sv = readJSON('fm_save');
  return sv ? Math.max(0, Number(sv.total) || 0) : 0;
}

// 계획 대비 누적 차액(원)
export function computeDeviation(monthlyPlan) {
  const plan = Math.max(0, Number(monthlyPlan) || 0);
  const byMonth = depositByMonth();
  const m = monthStr();
  let depDev = 0;
  Object.entries(byMonth).forEach(([mk, total]) => {
    if (mk < m) depDev += (total - plan);                // 완료된 달: 정직하게 +/-
    else if (mk === m) depDev += Math.max(0, total - plan); // 진행 중인 달: 양수만(밀림 보류)
  });
  const saveBonus = savingTotal();
  return { D: depDev + saveBonus, depDev, saveBonus, monthDeposit: byMonth[m] || 0, months: Object.keys(byMonth).length };
}

// 실제저축을 반영한 진행 상황
export function computeProgress(simulation) {
  const inp = (simulation && simulation.inputs) || {};
  const monthlyPlan = Number(inp.monthlyInvestment) || 0;
  const planAgeRaw = (simulation && simulation.earliestRetirementAge) || inp.targetRetirementAge || null;
  const dailyNeed = dailyNeedOf(simulation); // 원/일, 목표 달성이면 null
  const dev = computeDeviation(monthlyPlan);
  const atGoal = dailyNeed == null;

  // 차액 D를 일 단위로 환산(계획 주변 1차 선형 근사). +면 앞당김, -면 밀림.
  let advanceDays = 0;
  if (!atGoal && dailyNeed > 0) advanceDays = dev.D / dailyNeed;

  let actualAgeYears = planAgeRaw != null ? planAgeRaw - advanceDays / 365.25 : null;
  if (actualAgeYears != null) {
    const floor = Number(inp.currentAge) || 0;
    const ceil = Number(inp.simulationUntilAge) || 90;
    actualAgeYears = Math.max(floor, Math.min(ceil, actualAgeYears));
  }

  return {
    monthlyPlan,
    planAge: planAgeRaw,
    actualAgeYears,
    advanceDays,        // 양수=앞당김, 음수=밀림
    direction: advanceDays > 0.5 ? 'ahead' : advanceDays < -0.5 ? 'behind' : 'even',
    atGoal,
    D: dev.D,
    depDev: dev.depDev,
    saveBonus: dev.saveBonus,
    monthDeposit: dev.monthDeposit,
    hasData: dev.D !== 0 || dev.monthDeposit > 0 || dev.saveBonus > 0 || dev.months > 0,
  };
}

// 나이(소수) → "54세 3개월"
export function ageLabel(years) {
  if (years == null || Number.isNaN(years)) return '–';
  let y = Math.floor(years);
  let mo = Math.round((years - y) * 12);
  if (mo >= 12) { y += 1; mo = 0; }
  return mo > 0 ? `${y}세 ${mo}개월` : `${y}세`;
}

// 격차(일, 절대값 입력) → "1년 8개월" / "3개월" / "5일" / "4시간"
export function gapLabel(days) {
  const a = Math.abs(days);
  if (a < 1) {
    const hours = Math.round(a * 24);
    return hours >= 1 ? `${hours}시간` : '거의 그대로';
  }
  const totalMonths = a / 30.44;
  if (totalMonths < 1) return `${Math.round(a)}일`;
  const y = Math.floor(totalMonths / 12);
  const mo = Math.round(totalMonths - y * 12);
  if (y > 0) return mo > 0 ? `${y}년 ${mo}개월` : `${y}년`;
  return `${Math.round(totalMonths)}개월`;
}

// 저축 기록이 바뀌었음을 알림(헤드라인 즉시 갱신용)
export function notifySavingsChanged() {
  try { window.dispatchEvent(new Event('fm-savings-changed')); } catch { /* ignore */ }
}

// 리더보드에 '실제 저축' 한 줄 보고: 오늘/누적 절약 + 합친 앞당김(적립+절약)
export async function reportBoard(simulation) {
  try {
    let sv = null; try { sv = JSON.parse(localStorage.getItem('fm_save') || 'null'); } catch { /* ignore */ }
    const today = new Date().toISOString().slice(0, 10);
    const todaySaved = sv && sv.lastDate === today ? (sv.today || 0) : 0;
    const totalSaved = sv ? (sv.total || 0) : 0;
    const streak = sv ? (sv.streak || 0) : 0;
    const p = computeProgress(simulation);
    let depTotal = 0;
    try { const fd = JSON.parse(localStorage.getItem('fm_daily') || 'null'); const dd = (fd && fd.days) || {}; depTotal = Object.values(dd).reduce((a, b) => a + (Number(b) || 0), 0); } catch { /* ignore */ }
    let nick = ''; try { nick = localStorage.getItem('fm_nickname') || ''; } catch { /* ignore */ }
    let band = null; try { band = statsRank(simulation).ageBand; } catch { /* ignore */ }
    await submitSave({ todaySaved, totalSaved, advancedDays: p.advanceDays, streak, nickname: nick, ageBand: band, depositTotal: depTotal, depositMonth: p.monthDeposit });
  } catch { /* ignore */ }
}
