import { identityId } from './identity.js';
// 실시간 접속(프레즈던) + 익명 이벤트 로깅 — 개인정보 없이 기기ID·이벤트명·익명 속성만
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');
const H = { apikey: SUPABASE_KEY, authorization: `Bearer ${SUPABASE_KEY}`, 'content-type': 'application/json' };

function nick() { try { return localStorage.getItem('fm_nickname') || ''; } catch { return ''; } }

// 접속 중임을 알림(하트비트)
export function presencePing() {
  const cid = identityId();
  if (!cid) return;
  try {
    fetch(`${SUPABASE_URL}/rest/v1/rpc/fm_presence_ping`, { method: 'POST', headers: H, body: JSON.stringify({ p_client: cid, p_nick: nick() || null }) }).catch(() => {});
  } catch { /* ignore */ }
}

// 현재 접속자 수 + 최근 닉네임
export async function fetchLivePresence() {
  try {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/fm_live_presence`, { method: 'POST', headers: H, body: JSON.stringify({}) });
    if (!res.ok) return null;
    const rows = await res.json();
    const r = rows && rows[0];
    return r ? { online: r.online || 0, names: r.names || [] } : { online: 0, names: [] };
  } catch { return null; }
}

// 최근 절약 기록(배너 활동 표시용)
export async function fetchRecentSaves(limit = 8) {
  try {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/firemap_save_events?select=client_id,nickname,today_saved,age_band,updated_at&today_saved=gt.0&order=updated_at.desc&limit=${limit}`, { headers: H });
    if (!res.ok) return [];
    return await res.json();
  } catch { return []; }
}

// 지금까지 계산한 총 인원(누적 통계)
export async function fetchTotalCalc() {
  try {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/firemap_scores?select=id`, { headers: { ...H, prefer: 'count=exact', range: '0-0' } });
    const cr = res.headers.get('content-range') || '';
    const t = cr.split('/')[1];
    return t && t !== '*' ? Number(t) : 0;
  } catch { return 0; }
}

// 익명 이벤트 기록(append-only). 개인정보·금액 원본 없이 행동 이벤트만.
export function logEvent(event, props) {
  try {
    const cid = identityId();
    fetch(`${SUPABASE_URL}/rest/v1/firemap_events`, {
      method: 'POST',
      headers: { ...H, prefer: 'return=minimal' },
      body: JSON.stringify({ client_id: cid, event: String(event).slice(0, 80), props: props || null })
    }).catch(() => {});
  } catch { /* ignore */ }
}
