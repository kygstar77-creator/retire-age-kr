import { account } from './identity.js';
import { inputsIsReal } from './retirementSimulator.js';

const URL = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const KEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || URL;
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || KEY;
// 서버 동기화: 기록·요약·닉네임만. 원본 금액(inputs)·정확한 자산추이는 방침대로 서버 저장 안 함(기기에만).
// 로그인(간편계정) 시에만 서버 동기화. 비로그인은 전부 기기에만 남음.
const SYNC_KEYS = ['fm_daily', 'fm_save', 'fm_rank_history_v1', 'fm_nickname', 'firemap-inputs-v3', 'fm_inputs_ts', 'fm_asset_history'];

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

// 로그인 직후: 서버값과 로컬값을 '병합'(덮어쓰기 금지) 후 양쪽에 반영 -> 두 기기 기록 안 날아감
// 입력값(계산값)은 '마지막 수정 우선(LWW)': fm_inputs_ts가 더 최근인 쪽을 채택 -> 폰<->데스크탑 결과 일치
export async function syncAfterAuth() {
  const a = authed(); if (!a) return;
  let rows = [];
  try { rows = await rpc('fm_state_get', { p_user: a.userId, p_token: a.token }) || []; } catch { return; }
  const map = {}; rows.forEach((r) => { map[r.key] = r.value; });
  const lts0 = Number(localStorage.getItem('fm_inputs_ts') || 0);
  const sts0 = Number(map['fm_inputs_ts'] || 0);
  for (const k of SYNC_KEYS) {
    let local = null; try { local = JSON.parse(localStorage.getItem(k) || 'null'); } catch { /* ignore */ }
    const server = (map[k] !== undefined ? map[k] : null);
    let merged;
    if (k === 'fm_daily') merged = mergeDaily(local, server);
    else if (k === 'fm_save') merged = mergeSave(local, server);
    // 입력값: 서버(다른 기기)가 더 최근이면 서버, 아니면 이 기기 실제 입력 우선(미편집 기본값이면 서버)
    else if (k === 'firemap-inputs-v3') merged = (server && sts0 > lts0) ? server : (inputsIsReal(local) ? (local || server) : server);
    else if (k === 'fm_inputs_ts') merged = Math.max(lts0, sts0) || null;
    else merged = local || server;
    if (merged) {
      try { localStorage.setItem(k, JSON.stringify(merged)); } catch { /* ignore */ }
      await pushState(k, merged);
    }
  }
}

// 로그인 상태로 앱을 다시 열 때: 다른 기기에서 더 최근에 수정한 입력값이 있으면 받아와 반영(LWW).
// 또는 이 기기에 아직 실제 입력이 없으면(새 폰/PWA) ts와 무관하게 서버값을 받아온다.
// 반영된 입력 객체를 반환 -> 호출부에서 화면 상태(setInputs)까지 갱신.
export async function pullInputsIfNewer() {
  const a = authed(); if (!a) return null;
  let rows = [];
  try { rows = await rpc('fm_state_get', { p_user: a.userId, p_token: a.token }) || []; } catch { return null; }
  const map = {}; rows.forEach((r) => { map[r.key] = r.value; });
  const sIn = map['firemap-inputs-v3'];
  if (!sIn || !inputsIsReal(sIn)) return null;
  const sts = Number(map['fm_inputs_ts'] || 0);
  const lts = Number(localStorage.getItem('fm_inputs_ts') || 0);
  let localReal = false;
  try { localReal = inputsIsReal(JSON.parse(localStorage.getItem('firemap-inputs-v3') || 'null')); } catch { /* ignore */ }
  // 서버값 채택 조건: (1) 서버가 더 최근에 수정됨, 또는 (2) 이 기기엔 아직 실제 입력이 없음(새 기기/PWA)
  if (sts > lts || !localReal) {
    try {
      localStorage.setItem('firemap-inputs-v3', JSON.stringify(sIn));
      if (sts > 0) localStorage.setItem('fm_inputs_ts', String(sts));
    } catch { /* ignore */ }
    return sIn;
  }
  return null;
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
const CLEAR_ON_LOGOUT = ['firemap-inputs-v3', 'fm_inputs_ts', 'fm_rank_history_v1', 'fm_asset_history', 'fm_nickname', 'fm_save', 'fm_daily', 'fm_claimed', 'fm_save_nudge_off'];

// 로그아웃: (로그인 상태면) 서버에 백업 -> 기기의 개인 데이터 전부 삭제(금융앱 프라이버시). 재로그인 시 syncAfterAuth가 복원.
export async function logoutClearLocal() {
  const a = authed();
  if (a) {
    for (const k of SYNC_KEYS) {
      let v = null; try { v = JSON.parse(localStorage.getItem(k) || 'null'); } catch { /* ignore */ }
      if (v != null && (k !== 'firemap-inputs-v3' || inputsIsReal(v))) { try { await pushState(k, v); } catch { /* ignore */ } }
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

// 회원 탈퇴 후 로컬 정리 — 서버 백업 없이(계정이 이미 파기됨) 기기 데이터만 삭제.
export function clearLocalOnly() {
  for (const k of CLEAR_ON_LOGOUT) { try { localStorage.removeItem(k); } catch { /* ignore */ } }
  try { localStorage.removeItem('fm_account'); } catch { /* ignore */ }
}
