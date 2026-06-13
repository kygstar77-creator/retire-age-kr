const URL = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const KEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || URL;
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || KEY;

async function rpc(fn, args) {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/${fn}`, {
    method: 'POST',
    headers: { apikey: SUPABASE_KEY, authorization: `Bearer ${SUPABASE_KEY}`, 'content-type': 'application/json' },
    body: JSON.stringify(args)
  });
  const data = await res.json().catch(() => null);
  if (!res.ok) { const e = new Error((data && data.message) || `rpc_${res.status}`); e.code = data && data.message; throw e; }
  return Array.isArray(data) ? data[0] : data;
}

function persist(r) {
  if (!r || !r.id) return null;
  try {
    localStorage.setItem('fm_account', JSON.stringify({ userId: r.id, handle: r.handle }));
    localStorage.setItem('fm_nickname', r.handle);
  } catch { /* ignore */ }
  return r;
}

export async function signup(handle, password) {
  const r = await rpc('fm_signup', { p_handle: handle, p_password: password });
  return persist(r);
}
export async function login(handle, password) {
  const r = await rpc('fm_login', { p_handle: handle, p_password: password });
  if (!r || !r.id) { const e = new Error('bad_credentials'); e.code = 'bad_credentials'; throw e; }
  return persist(r);
}
export function logout() {
  try { localStorage.removeItem('fm_account'); } catch { /* ignore */ }
}
