// 네이버 로그인(카페 글쓰기용). 글쓴이는 항상 사용자 본인 — 봇 계정 없음.
// 켜고 끄는 곳은 Cloudflare Pages 환경변수 한 군데(NAVER_CLIENT_ID / NAVER_CLIENT_SECRET):
// 앱은 /cafe-post 에 물어봐서 켜져 있으면 '카페에 올리기', 꺼져 있으면 '카페 인증 게시판'(복사 후 카페 열기)로 움직인다.
// 토큰은 사용자의 것이고 sessionStorage에만 잠시 둔다. 서버(Functions)는 code→token 교환과 게시 대행만 한다.
const KEY = 'fm_naver_token';

let cfgPromise = null;
// 카페 게시 설정 — 한 번만 물어보고 그 답을 재사용한다. 실패하면 꺼진 것으로 본다.
export function cafeConfig() {
  if (!cfgPromise) {
    cfgPromise = fetch('/cafe-post')
      .then((r) => (r.ok ? r.json() : null))
      .catch(() => null)
      .then((j) => (j && j.ok ? j : { enabled: false, clientId: null }));
  }
  return cfgPromise;
}

export async function cafePostEnabled() {
  const c = await cafeConfig();
  return !!(c && c.enabled && c.clientId);
}

export function naverToken() {
  try { const v = JSON.parse(sessionStorage.getItem(KEY) || 'null'); if (v && v.expires_at > Date.now()) return v.access_token; } catch { /* ignore */ }
  return null;
}

// 인가 시작 — 돌아올 때 ?naver_code=… 로 복귀. returnTo 화면을 기억해 두고 그 화면으로 돌아간다.
export async function naverLoginStart(returnTo = '#result') {
  const c = await cafeConfig();
  if (!c || !c.clientId) return false;
  const state = Math.random().toString(36).slice(2);
  try { sessionStorage.setItem('fm_naver_state', state); sessionStorage.setItem('fm_naver_return', returnTo); } catch { /* ignore */ }
  const redirect = `${window.location.origin}/naver-callback`;
  const u = new URL('https://nid.naver.com/oauth2.0/authorize');
  u.searchParams.set('response_type', 'code');
  u.searchParams.set('client_id', c.clientId);
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

// 카페에 글 올리기 — 서버 Function(/cafe-post)이 openapi.naver.com에 대행 요청.
// imageUrl은 같은 도메인의 /og 카드 주소. 서버가 그 PNG를 받아 글에 붙인다(화면에서 본 그림 그대로).
export async function postToCafe({ subject, content, imageUrl }) {
  const token = naverToken();
  if (!token) return { ok: false, reason: 'login' };
  try {
    const res = await fetch('/cafe-post', { method: 'POST', headers: { 'content-type': 'application/json', authorization: `Bearer ${token}` }, body: JSON.stringify({ subject, content, imageUrl: imageUrl || null }) });
    const j = await res.json().catch(() => ({}));
    if (res.ok && j.ok) return { ok: true, url: j.url || null };
    return { ok: false, reason: j.reason || `http_${res.status}`, detail: j.detail || '' };
  } catch { return { ok: false, reason: 'network' }; }
}
