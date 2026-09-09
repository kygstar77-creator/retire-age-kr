// 설정·소액 키 1벌. 새 키는 여기에만 추가한다.
const get = (k) => { try { return localStorage.getItem(k); } catch { return null; } };
const set = (k, v) => { try { if (v == null) localStorage.removeItem(k); else localStorage.setItem(k, String(v)); } catch { /* ignore */ } };
const getJSON = (k, d = null) => { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch { return d; } };
const setJSON = (k, v) => set(k, JSON.stringify(v));

export const prefs = {
  hideAmount: () => get('fm_hide_amount') === '1',
  setHideAmount: (v) => set('fm_hide_amount', v ? '1' : null),
  theme: () => get('fm_theme') || 'light',
  setTheme: (t) => { set('fm_theme', t === 'dark' ? 'dark' : null); applyTheme(); },
  dailyGoal: () => Number(get('fm_daily_goal')) || 0,
  setDailyGoal: (n) => set('fm_daily_goal', n > 0 ? n : null),
  pot: () => getJSON('fm_pot', { name: '내 파이어 통', emoji: '🔥' }),
  setPot: (p) => setJSON('fm_pot', p),
  certCount: () => Number(get('fm_cert_count')) || 0,
  bumpCert: () => set('fm_cert_count', (Number(get('fm_cert_count')) || 0) + 1),
  wallSeen: () => Number(get('fm_wall_seen')) || 0,
  setWallSeen: (id) => set('fm_wall_seen', id),
  freezeUsed: () => get('fm_streak_freeze') || '',
  setFreezeUsed: (ym) => set('fm_streak_freeze', ym),
  missions: () => getJSON('fm_missions_done', {}),
  setMissionDone: (id) => { const m = getJSON('fm_missions_done', {}); m[id] = Date.now(); setJSON('fm_missions_done', m); },
  week26: () => getJSON('fm_26w', null),
  setWeek26: (v) => setJSON('fm_26w', v),
  consent: () => get('fm_consent_v1') === '1',
  setConsent: () => set('fm_consent_v1', '1')
};

export function applyTheme() {
  try { document.documentElement.setAttribute('data-theme', prefs.theme() === 'dark' ? 'dark' : 'light'); } catch { /* ignore */ }
}
