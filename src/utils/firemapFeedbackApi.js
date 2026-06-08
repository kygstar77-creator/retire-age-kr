const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || '';
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || '';
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

export async function loadFeedback() {
  if (!feedbackReady) return [];
  try {
    const rows = await callFeedback(`${TABLE}?select=id,nickname,message,created_at&status=eq.visible&order=created_at.desc&limit=20`, { method: 'GET' });
    return Array.isArray(rows) ? rows : [];
  } catch {
    return [];
  }
}

export async function sendFeedback(message) {
  const clean = String(message || '').trim().slice(0, 240);
  if (!clean) return null;
  if (!feedbackReady) throw new Error('feedback storage is not configured');
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
