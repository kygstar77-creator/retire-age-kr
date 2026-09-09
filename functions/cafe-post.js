// Cloudflare Pages Function: POST /cafe-post — 사용자의 네이버 토큰으로 파이어맵 카페 인증 게시판에 글을 올린다.
// 네이버 카페 글쓰기 API: POST https://openapi.naver.com/v1/cafe/{clubid}/menu/{menuid}/articles (multipart: subject, content, image)
// 환경변수: NAVER_CAFE_CLUB_ID, NAVER_CAFE_MENU_CERT (사장님이 카페 관리에서 API 권한을 켜고 ID를 등록). 없으면 503.
// 토큰은 요청에만 존재하고 저장하지 않는다. 봇 계정 없음 — 글쓴이는 항상 사용자 본인.
export async function onRequestPost(context) {
  const { env, request } = context;
  if (!env.NAVER_CAFE_CLUB_ID || !env.NAVER_CAFE_MENU_CERT) return json({ ok: false, reason: 'not_configured' }, 503);
  const auth = request.headers.get('authorization') || '';
  const token = auth.startsWith('Bearer ') ? auth.slice(7).trim() : '';
  if (!token) return json({ ok: false, reason: 'login' }, 401);
  let body = {};
  try { body = await request.json(); } catch { return json({ ok: false, reason: 'bad_json' }, 400); }
  const subject = String(body.subject || '').trim().slice(0, 100);
  const content = String(body.content || '').trim().slice(0, 4000);
  if (!subject || !content) return json({ ok: false, reason: 'empty' }, 400);

  const form = new FormData();
  // 네이버 API는 MS949로 URL-encode된 값을 기대하지만, multipart UTF-8도 수용한다(개발자센터 예제 기준). 실패 시 reason 반환.
  form.set('subject', encodeURIComponent(subject));
  form.set('content', encodeURIComponent(content));
  if (body.image && typeof body.image === 'string' && body.image.startsWith('data:image/')) {
    try {
      const b64 = body.image.split(',')[1] || '';
      const bin = atob(b64);
      const u8 = new Uint8Array(bin.length);
      for (let i = 0; i < bin.length; i += 1) u8[i] = bin.charCodeAt(i);
      form.set('image', new Blob([u8], { type: 'image/png' }), 'firemap-cert.png');
    } catch { /* 이미지 없이 진행 */ }
  }
  const url = `https://openapi.naver.com/v1/cafe/${encodeURIComponent(env.NAVER_CAFE_CLUB_ID)}/menu/${encodeURIComponent(env.NAVER_CAFE_MENU_CERT)}/articles`;
  try {
    const r = await fetch(url, { method: 'POST', headers: { authorization: `Bearer ${token}` }, body: form });
    const j = await r.json().catch(() => ({}));
    if (r.status === 429) return json({ ok: false, reason: 'rate_limit' }, 429);
    if (r.status === 401) return json({ ok: false, reason: 'login' }, 401);
    if (!r.ok) return json({ ok: false, reason: (j && (j.errorMessage || j.message)) || `naver_${r.status}` }, 502);
    const link = j && j.message && j.message.result && j.message.result.articleUrl;
    return json({ ok: true, url: link || null });
  } catch { return json({ ok: false, reason: 'network' }, 502); }
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });
}
