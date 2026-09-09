// 파이어맵 Supabase 접속 정보 1벌 — 다른 파일에서 URL/KEY를 다시 적지 않는다.
// 프로젝트: cvhskxdwqubmshdgkzhj (파이어맵 전용). publishable(anon) 키는 공개용이라 번들에 포함돼도 무방하지만
// 환경변수(VITE_SUPABASE_URL / VITE_SUPABASE_ANON_KEY)가 있으면 그것을 우선한다.
const DEFAULT_URL = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const DEFAULT_KEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');

export const SUPABASE_URL = (import.meta.env && import.meta.env.VITE_SUPABASE_URL) || DEFAULT_URL;
export const SUPABASE_KEY = (import.meta.env && import.meta.env.VITE_SUPABASE_ANON_KEY) || DEFAULT_KEY;

export function sbHeaders(extra = {}) {
  return { apikey: SUPABASE_KEY, authorization: `Bearer ${SUPABASE_KEY}`, 'content-type': 'application/json', ...extra };
}

// REST GET → JSON (실패 시 null)
export async function sbGet(pathAndQuery, extraHeaders = {}) {
  try {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/${pathAndQuery}`, { method: 'GET', headers: sbHeaders(extraHeaders) });
    return res.ok ? await res.json() : null;
  } catch { return null; }
}

// RPC POST → JSON (실패 시 null). 빈 인자는 {}.
export async function sbRpc(fn, args = {}) {
  try {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/${fn}`, { method: 'POST', headers: sbHeaders(), body: JSON.stringify(args || {}) });
    if (!res.ok) return null;
    const txt = await res.text();
    try { return txt ? JSON.parse(txt) : null; } catch { return null; }
  } catch { return null; }
}
