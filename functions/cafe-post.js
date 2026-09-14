// Cloudflare Pages Function: /cafe-post — 인증 카드를 파이어맵 카페에 올린다.
//   GET  : 카페 게시가 켜져 있는지 + 네이버 로그인에 쓸 클라이언트 ID(공개값)를 앱에 알려준다.
//   POST : 사용자의 네이버 토큰으로 글을 올린다. 봇 계정 없음 — 글쓴이는 항상 사용자 본인이고, 토큰은 요청에만 있고 저장하지 않는다.
// 네이버 카페 글쓰기 API: POST https://openapi.naver.com/v1/cafe/{clubid}/menu/{menuid}/articles (multipart: subject, content, image)
// 카페 ID·게시판 ID는 공개값이라 기본값을 코드에 둔다(실측 2026-09-14: cafe.naver.com/firemap = 31789001, 자유게시판 = 1).
// 인증 게시판을 따로 만들면 Pages 환경변수 NAVER_CAFE_MENU_CERT 에 그 번호만 넣는다.
const DEFAULT_CLUB = '31789001';
const DEFAULT_MENU = '1';
const MAX_IMAGE = 3 * 1024 * 1024;
const MAX_IMAGES = 5;  // 한 글에 붙일 수 있는 그림 수 — 네이버가 몇 장까지 받는지 몰라 넉넉히 잡지 않는다

const clubOf = (env) => String(env.NAVER_CAFE_CLUB_ID || DEFAULT_CLUB);
const menuOf = (env) => String(env.NAVER_CAFE_MENU_CERT || DEFAULT_MENU);
// 카페 본문은 HTML로 들어간다(2026-09-14 실제 게시로 확인) — 꺾쇠는 막고 줄바꿈만 <br>로 살린다.
// 2026-09-14: 마지막 줄 firemap.kr을 <a>로 감쌌더니 게시가 막혔다(그 변경 말고는 같은 코드로 성공했었다).
// 네이버 카페 글쓰기 API의 스팸 필터로 보인다 → 링크 없이 글자 그대로 둔다. 근거 없이 다시 넣지 말 것.
const html = (t) => String(t).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/\r?\n/g, '<br>');
// 본문 중간에 그림 넣기 — 네이버 공식 셀프체크가 맥락에 맞는 이미지를 권한다(개수 자체는 랭킹과 무관).
// 글 본문에 [[img1]] 같은 자리표시를 두면 그 자리에 <img>를 박는다.
// <a href>가 스팸 필터에 막힌 전례가 있어 <img>도 막힐 수 있다 — 막히면 자리표시만 지우고 한 번 더 보낸다.
const withInlineImages = (escaped, urls, origin) => String(escaped).replace(/\[\[img(\d+)\]\]/g, (_, n) => {
  const u = urls[Number(n) - 1];
  if (!u) return '';
  let abs = '';
  try { abs = new URL(u, origin).toString(); } catch { abs = ''; }
  return abs ? `<br><img src="${abs}"><br>` : '';
});
const stripImagePlaceholders = (escaped) => String(escaped).replace(/\[\[img\d+\]\]/g, '').replace(/(<br>){3,}/g, '<br><br>');

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

  // 본문 만들기 — [[img1]] 자리표시가 있으면 그 자리에 <img>를 박는다.
  const origin = new URL(request.url).origin;
  const escaped = html(content);
  const urls = Array.isArray(body.imageUrls) ? body.imageUrls.filter(Boolean).slice(0, MAX_IMAGES) : [];
  const hasPlaceholder = /\[\[img\d+\]\]/.test(escaped);
  const plainContent = stripImagePlaceholders(escaped);
  const inlineContent = hasPlaceholder && urls.length ? withInlineImages(escaped, urls, origin) : null;

  // 그림은 한 번만 받아온다(재시도 때 다시 받지 않도록).
  const parts = [];
  for (const one of urls) {
    const blob = await cardImage(context, { imageUrl: one });
    if (!blob) continue;
    let name = `firemap-${parts.length + 1}.jpg`;
    try { name = (new URL(one, origin).pathname.split('/').pop() || '').slice(0, 60) || name; } catch { /* 기본 이름 */ }
    parts.push([blob, name]);
  }
  if (!parts.length) {
    const img = await cardImage(context, body);
    if (img) parts.push([img, 'firemap-cert.png']);
  }

  // multipart는 필드 순서를 지킨다 — 개발자센터 예제대로 subject, content 먼저, 그다음 이미지.
  //  - subject·content: UTF-8 URL 인코딩 한 번
  //  - content는 HTML로 해석된다 → 줄바꿈은 <br>
  //  - 이미지 파트 이름은 'image'가 아니라 '0'. 여러 장은 '0','1','2'.
  //  - openyn 기본값이 false(멤버 공개)라 안 보내면 회원만 보는 글이 된다.
  // FormData는 한 번 보내면 본문 스트림이 소비되므로 재시도할 때마다 새로 만든다.
  const buildForm = (bodyHtml) => {
    const f = new FormData();
    f.set('subject', encodeURIComponent(subject));
    f.set('content', encodeURIComponent(bodyHtml));
    f.set('openyn', 'true');
    f.set('searchopen', 'true');
    f.set('replyyn', 'true');
    parts.forEach(([blob, name], i) => f.set(String(i), blob, name));
    return f;
  };

  const url = `https://openapi.naver.com/v1/cafe/${encodeURIComponent(clubOf(env))}/menu/${encodeURIComponent(menuOf(env))}/articles`;
  try {
    let r = await fetch(url, { method: 'POST', headers: { authorization: `Bearer ${token}` }, body: buildForm(inlineContent || plainContent) });
    let j = await r.json().catch(() => ({}));
    // <img>가 스팸 필터에 걸리면 네이버는 200을 주면서 글 주소를 빼놓는다(<a>일 때 그랬다).
    // 그때는 그림을 본문에서 빼고 첨부만으로 한 번 더 보낸다 — 글이 안 올라가는 것보다 낫다.
    const noLink = (x) => !(x && x.message && x.message.result && x.message.result.articleUrl);
    // 200이 아니어도(스팸 필터가 4xx로 막는 경우) 그림을 빼고 한 번 더 보낸다. 토큰 문제는 제외.
    if (inlineContent && r.status !== 401 && r.status !== 403 && r.status !== 429 && (!r.ok || noLink(j))) {
      r = await fetch(url, { method: 'POST', headers: { authorization: `Bearer ${token}` }, body: buildForm(plainContent) });
      j = await r.json().catch(() => ({}));
    }
    // 401/403도 이유가 여러 가지다(토큰 만료 · API 권한 없음 · 앱 상태). 네이버가 준 코드·메시지를 같이 넘긴다.
    const detail = (() => {
      try {
        // 네이버는 error를 객체({code, msg})로 주기도 한다 — 객체면 통째로 글자로 바꿔야 이유가 보인다.
        const m = j && j.message;
        const e = (m && (m.error || m.errorMessage)) || j.errorMessage || j.errorCode || j;
        return (typeof e === 'string' ? e : JSON.stringify(e)).slice(0, 200);
      } catch { return 'no_body'; }
    })();
    if (r.status === 401 || r.status === 403) return json({ ok: false, reason: 'login', detail: `${r.status} ${detail}` }, 401);
    if (r.status === 429) return json({ ok: false, reason: 'rate_limit', detail }, 429);
    if (!r.ok) return json({ ok: false, reason: (j && (j.errorMessage || j.message)) || `naver_${r.status}` }, 502);
    const link = j && j.message && j.message.result && j.message.result.articleUrl;
    // 네이버는 200을 주면서 본문에 에러를 담아 보내기도 한다(스팸 필터 등).
    // 글 주소가 안 오면 올라간 게 아니므로 성공으로 치지 않고, 네이버가 뭐라 했는지 그대로 넘긴다.
    if (!link) {
      const detail = (() => {
        try {
          const m = j && j.message;
          return String((m && (m.error || m.errorMessage)) || j.errorMessage || j.errorCode || JSON.stringify(j)).slice(0, 200);
        } catch { return 'no_body'; }
      })();
      return json({ ok: false, reason: `no_article ${detail}` }, 502);
    }
    return json({ ok: true, url: link });
  } catch { return json({ ok: false, reason: 'network' }, 502); }
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });
}
