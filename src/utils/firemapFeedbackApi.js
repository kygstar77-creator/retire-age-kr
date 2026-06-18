import { identityId } from './identity.js';
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
function ffDeviceId() {
  try {
    let id = localStorage.getItem('fm_cid');
    if (!id) { id = (crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random().toString(16).slice(2)); localStorage.setItem('fm_cid', id); }
    return id;
  } catch { return null; }
}
async function commGet(query) {
  try { const rows = await callFeedback(query, { method: 'GET' }); return Array.isArray(rows) ? rows : []; }
  catch { return null; }
}

// 게시글 + 답글을 한 번에 불러옴(파생 컬럼 없으면 평면으로 폴백)
export async function loadCommunityThread() {
  // 1순위: category·client_id 포함(마이그레이션 후) → 2순위: 스레드 컬럼만 → 3순위: 평면(레거시)
  let rows = await commGet(`${TABLE}?select=id,nickname,message,created_at,parent_id,likes,client_id,category,stage&kind=eq.community&status=eq.visible&order=created_at.asc&limit=300`);
  if (rows === null) {
    rows = await commGet(`${TABLE}?select=id,nickname,message,created_at,parent_id,likes,client_id&kind=eq.community&status=eq.visible&order=created_at.asc&limit=300`);
  }
  if (rows === null) {
    rows = await commGet(`${TABLE}?select=id,nickname,message,created_at,parent_id,likes&kind=eq.community&status=eq.visible&order=created_at.asc&limit=300`);
  }
  if (rows === null) {
    const flat = await commGet(`${TABLE}?select=id,nickname,message,created_at&kind=eq.community&status=eq.visible&order=created_at.asc&limit=300`);
    rows = (flat || []).map((r) => ({ ...r, parent_id: null, likes: 0 }));
  }
  return rows || [];
}

// 커뮤니티 최근 원글 미리보기(라운지 유도용)
export async function fetchCommunityPeek(limit = 3) {
  let rows = await commGet(`${TABLE}?select=id,nickname,message,created_at,parent_id&kind=eq.community&status=eq.visible&parent_id=is.null&order=created_at.desc&limit=${limit}`);
  if (rows === null) {
    rows = await commGet(`${TABLE}?select=id,nickname,message,created_at&kind=eq.community&status=eq.visible&order=created_at.desc&limit=${limit}`);
  }
  return rows || [];
}

// 내 커뮤니티 기여(펫 꼾미기용): 내가 쓴 글·답글 수 + 받은 공감 합. 진화와 무관한 별도 철립.
export async function fetchMyContribution(clientIds) {
  try {
    const ids = (clientIds || []).filter(Boolean);
    if (!ids.length) return { posts: 0, likes: 0, cp: 0 };
    const inList = ids.map((x) => `\"${x}\"`).join(',');
    const rows = await commGet(`${TABLE}?select=likes&kind=eq.community&client_id=in.(${inList})`);
    const arr = rows || [];
    const posts = arr.length;
    const likes = arr.reduce((a, r) => a + (Number(r.likes) || 0), 0);
    return { posts, likes, cp: posts + likes };
  } catch { return { posts: 0, likes: 0, cp: 0 }; }
}

export async function sendCommunity(message, parentId = null, category = null, stage = null) {
  const clean = String(message || '').trim().slice(0, 240);
  if (!clean) return null;
  let nick = '';
  try { nick = localStorage.getItem('fm_nickname') || ''; } catch { /* ignore */ }
  const cid = identityId();
  const base = {
    message: clean, kind: 'community',
    page_path: '#community', client_type: window.innerWidth <= 640 ? 'mobile' : 'desktop'
  };
  if (parentId) base.parent_id = parentId;
  if (category && !parentId) base.category = category;
  if (stage && !parentId) base.stage = stage;
  const withCid = cid ? { ...base, client_id: cid } : base;
  const post = async (b) => {
    try { const rows = await callFeedback(TABLE, { method: 'POST', headers: { prefer: 'return=representation' }, body: JSON.stringify(b) }); return rows?.[0] || null; }
    catch { return null; }
  };
  // client_id·category 컬럼/닉네임 정책 유무와 무관하게 글은 항상 올라가도록 단계적으로 시도
  const noCat = (o) => { const { category: _c, stage: _s, ...rest } = o; return rest; };
  const candidates = [];
  if (nick) candidates.push({ ...withCid, nickname: nick });
  candidates.push(withCid);
  if (nick) candidates.push({ ...noCat(withCid), nickname: nick });
  candidates.push(noCat(withCid));
  if (cid) { if (nick) candidates.push({ ...noCat(base), nickname: nick }); candidates.push(noCat(base)); }
  for (const b of candidates) { const r = await post(b); if (r) return r; }
  return null;
}

// ===== 안전한 변경(204 빈응답도 성공 처리, json 파싱 안 함) =====
async function mutate(path, method, body) {
  try {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/${path}`, {
      method,
      headers: baseHeaders({ prefer: 'return=minimal' }),
      ...(body ? { body: JSON.stringify(body) } : {})
    });
    return res.ok;
  } catch { return false; }
}

// 공감(좋아요) — read-modify-write
export async function likeCommunity(id, currentLikes) {
  return mutate(`${TABLE}?id=eq.${id}`, 'PATCH', { likes: (Number(currentLikes) || 0) + 1 });
}

// 내 글 수정 — PATCH message
export async function editCommunity(id, message) {
  const clean = String(message || '').trim().slice(0, 240);
  if (!clean) return false;
  return mutate(`${TABLE}?id=eq.${id}`, 'PATCH', { message: clean });
}

// 내 글 삭제 — 실제 DELETE(소프트삭제 status=hidden은 RLS 정책에 막혀 401). 글이면 답글까지 함께 삭제.
export async function deleteCommunity(id) {
  return mutate(`${TABLE}?or=(id.eq.${id},parent_id.eq.${id})`, 'DELETE');
}
