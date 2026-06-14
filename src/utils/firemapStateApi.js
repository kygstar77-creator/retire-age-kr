import { account } from './identity.js';

const URL = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const KEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || URL;
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || KEY;
const SYNC_KEYS = ['fm_daily', 'fm_save', 'firemap-inputs-v3', 'fm_rank_history_v1', 'fm_asset_history', 'fm_nickname'];

async function rpc(fn, args) {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/${fn}`, {
    method: 'POST',
    headers: { apikey: SUPABASE_KEY, authorization: `Bearer ${SUPABASE_KEY}`, 'content-type': 'application/json' },
    body: JSON.stringify(args)
  });
  const txt = await res.text();
  let data = null; try { data = txt ? JSON.parse(txt) : null; } catch { /* ignore */ }
  if (!res.ok) throw new Error((data && data.message) || `rpc_${res.status}`);
  return data;
}

function authed() { const a = account(); return a && a.userId && a.token ? a : null; }

export async function pushState(key, value) {
  const a = authed(); if (!a) return false;
  try { await rpc('fm_state_set', { p_user: a.userId, p_token: a.token, p_key: key, p_value: value }); return true; }
  catch { return false; }
}

export async function pullKey(key) {
  const a = authed(); if (!a) return null;
  try {
    const rows = await rpc('fm_state_get', { p_user: a.userId, p_token: a.token });
    const row = (rows || []).find((r) => r.key === key);
    return row ? row.value : null;
  } catch { return null; }
}

// 적립 일별 장부 병합: 날짜별 더 큰 값 채택(같은 돈 이중계산 방지, 양쪽 기록 보존)
function mergeDaily(localV, serverV) {
  const a = (localV && localV.days) || {};
  const b = (serverV && serverV.days) || {};
  const days = {};
  for (const k of new Set([...Object.keys(a), ...Object.keys(b)])) {
    days[k] = Math.max(Number(a[k]) || 0, Number(b[k]) || 0);
  }
  return { ...(serverV || {}), ...(localV || {}), days };
}
// 절약 병합: 누적/연속은 더 멀리 간 값(max), 오늘분은 오늘인 쪽의 큰 값
function mergeSave(localV, serverV) {
  if (!localV) return serverV;
  if (!serverV) return localV;
  const today = new Date().toISOString().slice(0, 10);
  const total = Math.max(Number(localV.total) || 0, Number(serverV.total) || 0);
  const streak = Math.max(Number(localV.streak) || 0, Number(serverV.streak) || 0);
  const daysCount = Math.max(Number(localV.days) || 0, Number(serverV.days) || 0);
  const lt = localV.lastDate === today ? (Number(localV.today) || 0) : 0;
  const st = serverV.lastDate === today ? (Number(serverV.today) || 0) : 0;
  const entries = (localV.lastDate === today && Array.isArray(localV.entries)) ? localV.entries
    : (serverV.lastDate === today && Array.isArray(serverV.entries)) ? serverV.entries : [];
  return { total, streak, days: daysCount, today: Math.max(lt, st), lastDate: today, entries };
}

// 로그인 직후: 서버값과 로컬값을 '병합'(덮어쓰기 금지) 후 양쪽에 반영 → 두 기기 기록 안 날아감
export async function syncAfterAuth() {
  const a = authed(); if (!a) return;
  let rows = [];
  try { rows = await rpc('fm_state_get', { p_user: a.userId, p_token: a.token }) || []; } catch { return; }
  const map = {}; rows.forEach((r) => { map[r.key] = r.value; });
  for (const k of SYNC_KEYS) {
    let local = null; try { local = JSON.parse(localStorage.getItem(k) || 'null'); } catch { /* ignore */ }
    const server = (map[k] !== undefined ? map[k] : null);
    let merged;
    if (k === 'fm_daily') merged = mergeDaily(local, server);
    else if (k === 'fm_save') merged = mergeSave(local, server);
    else merged = local || server;
    if (merged) {
      try { localStorage.setItem(k, JSON.stringify(merged)); } catch { /* ignore */ }
      await pushState(k, merged);
    }
  }
}

// 로그인 시: 이 기기의 옛 익명 기록(랭킹·절약·커뮤니티)을 계정으로 승계 + 닉네임을 핸들로 통일
export async function claimDevice() {
  const a = authed(); if (!a) return false;
  let dev = null; try { dev = localStorage.getItem('fm_cid'); } catch { /* ignore */ }
  if (!dev || dev === a.userId) { try { localStorage.setItem('fm_claimed', a.userId); } catch { /* ignore */ } return false; }
  try {
    await rpc('fm_claim', { p_user: a.userId, p_token: a.token, p_device: dev });
    try { localStorage.setItem('fm_claimed', a.userId); } catch { /* ignore */ }
    return true;
  } catch { return false; }
}

// 앱 로드 시 한 번만 자동 승계(이미 로그인된 사용자도 재로그인 없이 적용)
const CLEAR_ON_LOGOUT = ['firemap-inputs-v3', 'fm_rank_history_v1', 'fm_asset_history', 'fm_nickname', 'fm_save', 'fm_daily', 'fm_claimed', 'fm_save_nudge_off'];

// 로그아웃: (로그인 상태면) 서버에 백업 → 기기의 개인 데이터 전부 삭제(금융앱 프라이버시). 재로그인 시 syncAfterAuth가 복원.
export async function logoutClearLocal() {
  const a = authed();
  if (a) {
    for (const k of SYNC_KEYS) {
      let v = null; try { v = JSON.parse(localStorage.getItem(k) || 'null'); } catch { /* ignore */ }
      if (v != null) { try { await pushState(k, v); } catch { /* ignore */ } }
    }
  }
  for (const k of CLEAR_ON_LOGOUT) { try { localStorage.removeItem(k); } catch { /* ignore */ } }
  try { localStorage.removeItem('fm_account'); } catch { /* ignore */ }
}

export async function maybeClaimOnLoad() {
  const a = authed(); if (!a) return;
  let done = null; try { done = localStorage.getItem('fm_claimed'); } catch { /* ignore */ }
  if (done === a.userId) return;
  await claimDevice();
}
