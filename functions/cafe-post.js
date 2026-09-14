// Cloudflare Pages Function: /cafe-post — 인증 카드를 파이어맵 카페에 올린다.
//   GET  : 카페 게시가 켜져 있는지 + 네이버 로그인에 쓸 클라이언트 ID(공개값)를 앱에 알려준다.
//   POST : 사용자의 네이버 토큰으로 글을 올린다. 봇 계정 없음 — 글쓴이는 항상 사용자 본인이고, 토큰은 요청에만 있고 저장하지 않는다.
// 네이버 카페 글쓰기 API: POST https://openapi.naver.com/v1/cafe/{clubid}/menu/{menuid}/articles (multipart: subject, content, image)
// 카페 ID·게시판 ID는 공개값이라 기본값을 코드에 둔다(실측 2026-09-14: cafe.naver.com/firemap = 31789001, 자유게시판 = 1).
// 인증 게시판을 따로 만들면 Pages 환경변수 NAVER_CAFE_MENU_CERT 에 그 번호만 넣는다.
const DEFAULT_CLUB = '31789001';
const DEFAULT_MENU = '1';
const MAX_IMAGE = 3 * 1024 * 1024;

const clubOf = (env) => String(env.NAVER_CAFE_CLUB_ID || DEFAULT_CLUB);
const menuOf = (env) => String(env.NAVER_CAFE_MENU_CERT || DEFAULT_MENU);

export async function onRequestGet(context) {
  const { env } = context;
  // clientId는 로그인 주소에 그대로 실리는 공개값이다. 시크릿(NAVER_CLIENT_SECRET)은 서버 밖으로 내보내지 않는다.
  return json({
    ok: true,
    enabled: !!(env.NAVER_CLIENT_ID && env.NAVER_CLIENT_SECRET),
    clientId: env.NAVER_CLIENT_ID || null,
    club: clubOf(env),
    menu: menuOf(env)
  });
}

// 카드 이미지: 앱이 보내온 /og 주소(같은 도메인)를 서버가 직접 받아 붙인다 — 화면에서 본 그림 그대로, 폰트도 서버 것.
async function cardImage(context, body) {
  const origin = new URL(context.request.url).origin;
  const raw = String(body.imageUrl || '');
  if (raw) {
    try {
      const u = new URL(raw, origin);
      if (u.origin !== origin) return null;  // 우리 도메인 밖 주소는 받지 않는다
      const r = await fetch(u.toString());
      if (!r.ok) return null;
      const buf = await r.arrayBuffer();
      if (!buf.byteLength || buf.byteLength > MAX_IMAGE) return null;
      return new Blob([buf], { type: 'image/png' });
    } catch { return null; }
  }
  const data = String(body.image || '');
  if (!data.startsWith('data:image/')) return null;
  try {
    const bin = atob(data.split(',')[1] || '');
    if (!bin.length || bin.length > MAX_IMAGE) return null;
    const u8 = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i += 1) u8[i] = bin.charCodeAt(i);
    return new Blob([u8], { type: 'image/png' });
  } catch { return null; }
}

export async function onRequestPost(context) {
  const { env, request } = context;
  if (!env.NAVER_CLIENT_ID || !env.NAVER_CLIENT_SECRET) return json({ ok: false, reason: 'not_configured' }, 503);
  const auth = request.headers.get('authorization') || '';
  const token = auth.startsWith('Bearer ') ? auth.slice(7).trim() : '';
  if (!token) return json({ ok: false, reason: 'login' }, 401);
  let body = {};
  try { body = await request.json(); } catch { return json({ ok: false, reason: 'bad_json' }, 400); }
  const subject = String(body.subject || '').trim().slice(0, 100);
  const content = String(body.content || '').trim().slice(0, 4000);
  if (!subject || !content) return json({ ok: false, reason: 'empty' }, 400);

  const form = new FormData();
  // 네이버 문서는 MS949로 URL-encode한 값을 예로 들지만 multipart UTF-8도 받는다(개발자센터 예제 기준).
  // 글자가 깨지면 앱이 폴백(복사 후 카페 열기)으로 돌아가게 해 뒀다.
  form.set('subject', encodeURIComponent(subject));
  form.set('content', encodeURIComponent(content));
  const img = await cardImage(context, body);
  if (img) form.set('image', img, 'firemap-cert.png');

  const url = `https://openapi.naver.com/v1/cafe/${encodeURIComponent(clubOf(env))}/menu/${encodeURIComponent(menuOf(env))}/articles`;
  try {
    const r = await fetch(url, { method: 'POST', headers: { authorization: `Bearer ${token}` }, body: form });
    const j = await r.json().catch(() => ({}));
    if (r.status === 401 || r.status === 403) return json({ ok: false, reason: 'login' }, 401);
    if (r.status === 429) return json({ ok: false, reason: 'rate_limit' }, 429);
    if (!r.ok) return json({ ok: false, reason: (j && (j.errorMessage || j.message)) || `naver_${r.status}` }, 502);
    const link = j && j.message && j.message.result && j.message.result.articleUrl;
    return json({ ok: true, url: link || null });
  } catch { return json({ ok: false, reason: 'network' }, 502); }
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });
}
