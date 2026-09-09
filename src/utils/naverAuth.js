// 네이버 로그인(카페 글쓰기용) — 사장님이 네이버 개발자센터에 앱을 등록하고 VITE_NAVER_CLIENT_ID를 넣으면 켜진다.
// 토큰은 사용자의 것(글쓴이 계정)이며 sessionStorage에만 잠시 둔다. 서버(Functions)는 code→token 교환만 대행한다.
const CLIENT_ID = (import.meta.env && import.meta.env.VITE_NAVER_CLIENT_ID) || '';
const KEY = 'fm_naver_token';

export const naverEnabled = () => !!CLIENT_ID;

export function naverToken() {
  try { const v = JSON.parse(sessionStorage.getItem(KEY) || 'null'); if (v && v.expires_at > Date.now()) return v.access_token; } catch { /* ignore */ }
  return null;
}

// 인가 시작 — 돌아올 때 ?naver_code=… 로 복귀
export function naverLoginStart(returnTo = '#result') {
  if (!CLIENT_ID) return false;
  const state = Math.random().toString(36).slice(2);
  try { sessionStorage.setItem('fm_naver_state', state); sessionStorage.setItem('fm_naver_return', returnTo); } catch { /* ignore */ }
  const redirect = `${window.location.origin}/naver-callback`;
  const u = new URL('https://nid.naver.com/oauth2.0/authorize');
  u.searchParams.set('response_type', 'code');
  u.searchParams.set('client_id', CLIENT_ID);
  u.searchParams.set('redirect_uri', redirect);
  u.searchParams.set('state', state);
  window.location.href = u.toString();
  return true;
}

// 복귀 처리 — /naver-callback Function이 ?naver_code=&naver_state= 로 넘겨준다
export async function handleNaverRedirect() {
  try {
    const q = new URLSearchParams(window.location.search || '');
    const code = q.get('naver_code'); const state = q.get('naver_state');
    if (!code) return null;
    const saved = sessionStorage.getItem('fm_naver_state');
    if (!saved || saved !== state) return { ok: false, reason: 'state' };
    const res = await fetch('/naver-token', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ code, state }) });
    if (!res.ok) return { ok: false, reason: `token_${res.status}` };
    const j = await res.json();
    if (!j.access_token) return { ok: false, reason: 'no_token' };
    sessionStorage.setItem(KEY, JSON.stringify({ access_token: j.access_token, expires_at: Date.now() + (Number(j.expires_in) || 3600) * 1000 }));
    const back = sessionStorage.getItem('fm_naver_return') || '#result';
    window.history.replaceState(null, '', `/${back}`);
    return { ok: true };
  } catch { return { ok: false, reason: 'error' }; }
}

// 카페 인증 게시판에 글 올리기 — 서버 Function(/cafe-post)이 openapi.naver.com에 대행 요청
export async function postToCafe({ subject, content, imageDataUrl }) {
  const token = naverToken();
  if (!token) return { ok: false, reason: 'login' };
  try {
    const res = await fetch('/cafe-post', { method: 'POST', headers: { 'content-type': 'application/json', authorization: `Bearer ${token}` }, body: JSON.stringify({ subject, content, image: imageDataUrl || null }) });
    const j = await res.json().catch(() => ({}));
    if (res.ok && j.ok) return { ok: true, url: j.url || null };
    return { ok: false, reason: j.reason || `http_${res.status}` };
  } catch { return { ok: false, reason: 'network' }; }
}
