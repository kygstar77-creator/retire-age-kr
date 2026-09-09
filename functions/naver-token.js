// Cloudflare Pages Function: POST /naver-token — 네이버 인가 코드 → 액세스 토큰 교환(클라이언트 시크릿은 서버에만).
// 환경변수: NAVER_CLIENT_ID, NAVER_CLIENT_SECRET (사장님이 Pages 설정에 등록). 없으면 503.
export async function onRequestPost(context) {
  const { env, request } = context;
  if (!env.NAVER_CLIENT_ID || !env.NAVER_CLIENT_SECRET) return json({ ok: false, reason: 'not_configured' }, 503);
  let body = {};
  try { body = await request.json(); } catch { return json({ ok: false, reason: 'bad_json' }, 400); }
  const code = String(body.code || '').slice(0, 200);
  const state = String(body.state || '').slice(0, 64);
  if (!code) return json({ ok: false, reason: 'no_code' }, 400);
  const u = new URL('https://nid.naver.com/oauth2.0/token');
  u.searchParams.set('grant_type', 'authorization_code');
  u.searchParams.set('client_id', env.NAVER_CLIENT_ID);
  u.searchParams.set('client_secret', env.NAVER_CLIENT_SECRET);
  u.searchParams.set('code', code);
  u.searchParams.set('state', state);
  try {
    const r = await fetch(u.toString());
    const j = await r.json();
    if (!j.access_token) return json({ ok: false, reason: j.error || 'exchange_failed' }, 502);
    return json({ ok: true, access_token: j.access_token, expires_in: j.expires_in });
  } catch { return json({ ok: false, reason: 'network' }, 502); }
}


function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });
}
