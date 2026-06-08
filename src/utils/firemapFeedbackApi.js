const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || '';
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || '';
const TABLE = 'firemap_feedback';

export const feedbackReady = Boolean(SUPABASE_URL && SUPABASE_KEY);

const mockItems = [
  { id: 'mock-1', nickname: '익명', message: '질문 5로 다시 돌아갈 수 있으면 좋겠어요.', created_at: new Date(Date.now() - 1000 * 60 * 24).toISOString() },
  { id: 'mock-2', nickname: '익명', message: '국민연금 조건을 바꿔서 비교하고 싶어요.', created_at: new Date(Date.now() - 1000 * 60 * 58).toISOString() }
];

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

export async function loadFeedback() {
  if (!feedbackReady) return mockItems;
  try {
    const rows = await callFeedback(`${TABLE}?select=id,nickname,message,created_at&status=eq.visible&order=created_at.desc&limit=20`, { method: 'GET' });
    return Array.isArray(rows) ? rows : mockItems;
  } catch {
    return mockItems;
  }
}

export async function sendFeedback(message) {
  const clean = String(message || '').trim().slice(0, 240);
  if (!clean) return null;
  if (!feedbackReady) {
    return { id: `local-${Date.now()}`, nickname: '익명', message: clean, created_at: new Date().toISOString() };
  }
  const rows = await callFeedback(TABLE, {
    method: 'POST',
    headers: { prefer: 'return=representation' },
    body: JSON.stringify({
      message: clean,
      page_path: window.location.hash || window.location.pathname || '/',
      client_type: window.innerWidth <= 640 ? 'mobile' : 'desktop'
    })
  });
  return rows?.[0] || null;
}
