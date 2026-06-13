import { account } from './identity.js';

const URL = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const KEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || URL;
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || KEY;
const SYNC_KEYS = ['fm_daily', 'fm_save'];

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

// 로그인 직후: 서버에 있으면 로컬에 내려받고, 없으면 로컬 값을 서버로 올림
export async function syncAfterAuth() {
  const a = authed(); if (!a) return;
  let rows = [];
  try { rows = await rpc('fm_state_get', { p_user: a.userId, p_token: a.token }) || []; } catch { return; }
  const map = {}; rows.forEach((r) => { map[r.key] = r.value; });
  for (const k of SYNC_KEYS) {
    if (map[k] !== undefined && map[k] !== null) {
      try { localStorage.setItem(k, JSON.stringify(map[k])); } catch { /* ignore */ }
    } else {
      let local = null; try { local = JSON.parse(localStorage.getItem(k) || 'null'); } catch { /* ignore */ }
      if (local) await pushState(k, local);
    }
  }
}
