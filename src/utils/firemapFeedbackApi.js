const DEFAULT_SUPABASE_URL = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const DEFAULT_SUPABASE_KEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || DEFAULT_SUPABASE_URL;
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || DEFAULT_SUPABASE_KEY;
const TABLE = 'firemap_feedback';

export const feedbackReady = Boolean(SUPABASE_URL && SUPABASE_KEY);

function baseHeaders(extra = {}) {
  return {
    apikey: SUPABASE_KEY,
    authorization: `Bearer ${SUPABASE_KEY}`,
    'content-type': 'application/json',
    ...extra
  };
}

async function callFeedback(path, options = {}) {
  const response = await fetch(`${SUPABASE_URL}/rest/v1/${path}`, {
    ...options,
    headers: baseHeaders(options.headers || {})
  });
  if (!response.ok) throw new Error(`feedback request failed: ${response.status}`);
  return response.json();
}

export async function loadFeedback(kind = 'feedback') {
  try {
    const rows = await callFeedback(`${TABLE}?select=id,nickname,message,created_at&kind=eq.${kind}&status=eq.visible&order=created_at.desc&limit=30`, { method: 'GET' });
    return Array.isArray(rows) ? rows : [];
  } catch {
    return [];
  }
}

export async function sendFeedback(message, kind = 'feedback') {
  const clean = String(message || '').trim().slice(0, 240);
  if (!clean) return null;
  const base = {
    message: clean,
    page_path: window.location.hash || window.location.pathname || '/',
    client_type: window.innerWidth <= 640 ? 'mobile' : 'desktop'
  };
  const post = (body) => callFeedback(TABLE, {
    method: 'POST',
    headers: { prefer: 'return=representation' },
    body: JSON.stringify(body)
  });
  try {
    const rows = await post({ ...base, kind });
    return rows?.[0] || null;
  } catch {
    // kind 컬럼이 아직 없으면(마이그레이션 전) kind 없이 재시도
    try { const rows = await post(base); return rows?.[0] || null; } catch { return null; }
  }
}

// ===== 커뮤니티(스레드형) =====
async function commGet(query) {
  try { const rows = await callFeedback(query, { method: 'GET' }); return Array.isArray(rows) ? rows : []; }
  catch { return null; }
}

// 게시글 + 답글을 한 번에 불러옴(파생 컬럼 없으면 평면으로 폴백)
export async function loadCommunityThread() {
  let rows = await commGet(`${TABLE}?select=id,client_id,nickname,message,created_at,parent_id,likes&kind=eq.community&status=eq.visible&order=created_at.asc&limit=300`);
  if (rows === null) {
    const flat = await commGet(`${TABLE}?select=id,client_id,nickname,message,created_at&kind=eq.community&status=eq.visible&order=created_at.asc&limit=300`);
    rows = (flat || []).map((r) => ({ ...r, parent_id: null, likes: 0 }));
  }
  return rows || [];
}

export async function sendCommunity(message, parentId = null) {
  const clean = String(message || '').trim().slice(0, 240);
  if (!clean) return null;
  let nick = '';
  try { nick = localStorage.getItem('fm_nickname') || ''; } catch { /* ignore */ }
  let cid = null;
  try { cid = localStorage.getItem('fm_cid'); } catch { /* ignore */ }
  const body = {
    message: clean, kind: 'community', nickname: nick || null, client_id: cid,
    page_path: '#community', client_type: window.innerWidth <= 640 ? 'mobile' : 'desktop'
  };
  if (parentId) body.parent_id = parentId;
  const post = async (b) => {
    try { const rows = await callFeedback(TABLE, { method: 'POST', headers: { prefer: 'return=representation' }, body: JSON.stringify(b) }); return rows?.[0] || null; }
    catch { return null; }
  };
  let r = await post(body);
  if (!r && parentId == null) { const { parent_id, ...rest } = body; r = await post(rest); }
  return r;
}

// 공감(좋아요) — read-modify-write
export async function likeCommunity(id, currentLikes) {
  try {
    await callFeedback(`${TABLE}?id=eq.${id}`, { method: 'PATCH', headers: { prefer: 'return=minimal' }, body: JSON.stringify({ likes: (Number(currentLikes) || 0) + 1 }) });
    return true;
  } catch { return false; }
}
