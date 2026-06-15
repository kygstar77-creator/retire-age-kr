// 카카오 로그인 (Authorization Code 플로우)
// 시작: Kakao.Auth.authorize → 카카오 인증 → firemap.kr/?code=... 로 복귀
// 복귀: code를 kakao-auth Edge Function에 보내 검증·계정 발급(기존 {userId,handle,token} 형식)
const KAKAO_JS_KEY = 'ab42112f15f44fd86a631e6cee694c29'; // 도메인 제한된 공개 JS 키
// ⚠️ 카카오 콘솔에 등록된 Redirect URI와 정확히 일치해야 함.
// 현재 접속 도메인(origin)을 사용 → 프리뷰·프로덕션 모두 동작(각 origin을 콘솔에 등록 필요).
const REDIRECT_URI = (typeof window !== 'undefined' && window.location && window.location.origin)
  ? window.location.origin
  : 'https://firemap.kr';

const URL_ = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const KEY_ = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || URL_;
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || KEY_;

let loadPromise;
function ensureKakao() {
  if (loadPromise) return loadPromise;
  loadPromise = new Promise((resolve, reject) => {
    if (window.Kakao) { resolve(window.Kakao); return; }
    const sc = document.createElement('script');
    sc.src = 'https://t1.kakaocdn.net/kakao_js_sdk/2.7.4/kakao.min.js';
    sc.async = true;
    sc.onload = () => resolve(window.Kakao);
    sc.onerror = () => reject(new Error('kakao sdk load fail'));
    document.head.appendChild(sc);
  }).then((K) => {
    try { if (K && !K.isInitialized()) K.init(KAKAO_JS_KEY); } catch (e) { /* ignore */ }
    return K;
  });
  return loadPromise;
}

// 로그인 시작 — 현재 화면(해시)을 state로 보존해 복귀 후 그대로 돌아옴
export async function kakaoLoginStart() {
  const K = await ensureKakao();
  if (!K || !K.Auth || !K.Auth.authorize) throw new Error('kakao unavailable');
  const state = encodeURIComponent(window.location.hash || '#home');
  K.Auth.authorize({ redirectUri: REDIRECT_URI, state });
}

// 리다이렉트 복귀 처리 — ?code 있으면 교환. 성공 시 fm_account 저장 후 {ok:true} 반환.
export async function handleKakaoRedirect() {
  let params;
  try { params = new URLSearchParams(window.location.search); } catch { return null; }
  const code = params.get('code');
  if (!code) return null;
  try {
    const res = await fetch(`${SUPABASE_URL}/functions/v1/kakao-auth`, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        apikey: SUPABASE_KEY,
        authorization: `Bearer ${SUPABASE_KEY}`,
      },
      body: JSON.stringify({ code, redirect_uri: REDIRECT_URI }),
    });
    const data = await res.json().catch(() => null);
    // 성공이든 실패든 URL에서 code는 제거(새로고침 시 재교환 방지)
    const st = params.get('state');
    const back = st ? decodeURIComponent(st) : (window.location.hash || '#home');
    try {
      const clean = window.location.origin + window.location.pathname + (back || '#home');
      window.history.replaceState({}, '', clean);
    } catch (e) { /* ignore */ }
    if (!res.ok || !data || !data.id) return { error: (data && data.error) || 'login_failed' };
    try {
      localStorage.setItem('fm_account', JSON.stringify({ userId: data.id, handle: data.handle, token: data.token }));
      localStorage.setItem('fm_nickname', data.handle);
    } catch (e) { /* ignore */ }
    return { ok: true, account: data };
  } catch (e) {
    return { error: String(e) };
  }
}
