// 오늘의 절약 / 챌린지 / 명언 공통 데이터 + 누적 저장 로직
// 규칙 칩은 components/firemap/rules.js(RULES) — 옛 CHALLENGES·QUOTES·QUICK은 삭제.
// 날짜 키는 utils/dates.js 1벌(로컬 기준) — 여기서는 재수출만.
import { dayIdx, todayStr, yesterdayStr } from '../utils/dates.js';
export { dayIdx, todayStr, yesterdayStr };
export const wonStr = (n) => `${Math.round(n).toLocaleString('ko-KR')}원`;
export const readJSON = (k) => { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch { return null; } };

export function fmtAdvance(sec) {
  let x = Math.floor(sec);
  if (x < 1) return null;
  const d = Math.floor(x / 86400); x -= d * 86400;
  const h = Math.floor(x / 3600); x -= h * 3600;
  const m = Math.floor(x / 60); const s = x - m * 60;
  if (d > 0) return `${d}일 ${h}시간`;
  if (h > 0) return `${h}시간 ${m}분`;
  if (m > 0) return `${m}분 ${s}초`;
  return `${s}초`;
}

// 파이어까지 하루 평균 모아야 하는 돈(원/일). 이미 목표 달성이면 null.
export function dailyNeedOf(simulation) {
  if (!simulation || !simulation.inputs) return null;
  const inp = simulation.inputs;
  const fireAge = simulation.earliestRetirementAge || inp.targetRetirementAge;
  const target = simulation.requiredFireAssetByFourPercent || 0;
  const daysRemaining = Math.max(30, (fireAge - inp.currentAge) * 365.25);
  const gap = target - inp.financialAsset;
  return gap > 0 ? Math.max(1000, Math.round(gap / daysRemaining)) : null;
}

// 누적 저장 — 'today'/entries만 매일 리셋, total/days는 영구 누적
export function addSave(amount, label) {
  if (!amount || amount <= 0) return readJSON('fm_save');
  const t = todayStr();
  const prev = readJSON('fm_save');
  const newDay = !prev || prev.lastDate !== t;
  const prevEntries = newDay || !prev || !Array.isArray(prev.entries) ? [] : prev.entries;
  const entry = { id: `${Date.now()}_${Math.random().toString(36).slice(2, 6)}`, won: amount, label: label || '직접 입력' };
  let streak;
  if (!prev) streak = 1;
  else if (prev.lastDate === t) streak = prev.streak || 1;
  else if (prev.lastDate === yesterdayStr()) streak = (prev.streak || 0) + 1;
  else streak = 1;
  const daily = { ...(prev && prev.daily ? prev.daily : {}) };
  daily[t] = (daily[t] || 0) + amount;
  const next = {
    today: (newDay ? 0 : (prev.today || 0)) + amount,
    total: (prev ? prev.total || 0 : 0) + amount,
    days: (prev ? prev.days || 0 : 0) + (newDay ? 1 : 0),
    lastDate: t,
    streak,
    daily,
    entries: [...prevEntries, entry]
  };
  try { localStorage.setItem('fm_save', JSON.stringify(next)); } catch { /* ignore */ }
  return next;
}

// 오늘 기록 한 건 삭제 — today/total에서 빼고, 오늘이 비면 days도 1 감소
export function removeEntry(id) {
  const t = todayStr();
  const prev = readJSON('fm_save');
  if (!prev || prev.lastDate !== t || !Array.isArray(prev.entries)) return prev;
  const entry = prev.entries.find((e) => e.id === id);
  if (!entry) return prev;
  const entries = prev.entries.filter((e) => e.id !== id);
  const daily = { ...(prev.daily || {}) };
  daily[t] = Math.max(0, (daily[t] || 0) - entry.won);
  if (daily[t] === 0) delete daily[t];
  const next = {
    today: Math.max(0, (prev.today || 0) - entry.won),
    total: Math.max(0, (prev.total || 0) - entry.won),
    days: entries.length === 0 ? Math.max(0, (prev.days || 0) - 1) : (prev.days || 0),
    lastDate: t,
    streak: prev.streak || 0,
    daily,
    entries
  };
  try { localStorage.setItem('fm_save', JSON.stringify(next)); } catch { /* ignore */ }
  return next;
}

// 누적 절약액 직접 보정 (과거 실수 수정용)
export function setTotal(value) {
  const prev = readJSON('fm_save') || { today: 0, days: 0, lastDate: todayStr(), entries: [] };
  const total = Math.max(0, Math.round(Number(value) || 0));
  const next = { ...prev, total };
  try { localStorage.setItem('fm_save', JSON.stringify(next)); } catch { /* ignore */ }
  return next;
}

// GA 이벤트 (사용 측정 — 서버 불필요)
export function track(name, params = {}) {
  try { if (typeof window !== 'undefined' && window.gtag) window.gtag('event', name, { app_name: 'firemap', ...params }); } catch { /* ignore */ }
}
