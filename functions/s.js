// Cloudflare Pages Function: /s
// 공유 링크 미리보기(OG)에 그 사람의 또래 등수·등급을 띄우고,
// 실제 사용자는 입력 조건 그대로 앱으로 이동시킨다.
export async function onRequest(context) {
  const url = new URL(context.request.url);
  const q = url.searchParams;
  const site = 'https://firemap.kr';

  const esc = (s) =>
    String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');

  const p = (q.get('p') || '').replace(/[^0-9]/g, '');
  const g = (q.get('g') || '').replace(/[^A-Za-z]/g, '').slice(0, 2);
  const rw = q.get('rw') || '';
  const sd = (q.get('sd') || '').replace(/[^0-9]/g, '');
  const ea = (q.get('ea') || '').replace(/[^0-9]/g, '').slice(0, 3);
  const ad = (q.get('ad') || '').slice(0, 24);
  const pos = (q.get('pos') || '').replace(/[^0-9]/g, '');
  const tot = (q.get('tot') || '').replace(/[^0-9]/g, '');
  const tgt = (q.get('target') || '').replace(/[^0-9]/g, '').slice(0, 3);
  const rwy = (q.get('rwy') || '').slice(0, 12);
  const ret = (q.get('ret') || '').replace(/[^0-9]/g, '').slice(0, 2);
  const inf = (q.get('inf') || '').replace(/[^0-9]/g, '').slice(0, 2);
  const ogImg = (ea && pos && tot)
    ? `${site}/og?ea=${ea}&pos=${pos}&tot=${tot}&target=${tgt}&rw=${encodeURIComponent(rwy)}&ret=${ret}&inf=${inf}`
    : `${site}/${(sd && ad) ? 'og-save.png' : 'og-image.png'}?v=firemap-screens-v7-20260613`;

  const title = (sd && ad)
    ? `절약으로 파이어 ${ad} 앞당겼어요 — 파이어맵`
    : ea
      ? `나는 ${ea}세에 퇴사할 수 있어요 — 파이어맵`
      : p && g
        ? `또래 상위 ${p}% — 파이어맵`
        : '나는 몇 살에 퇴사할 수 있을까? — 파이어맵';
  const desc = (sd && ad)
    ? '하루하루 아낀 돈이 퇴사를 앞당겨요. 나도 1분 계산하고 절약 적립 시작하기.'
    : ea
      ? `또래 중 내 등수와 내 돈 버티는 나이까지 1분 계산. 너는 몇 살에 가능?`
      : `${rw ? rw + ' · ' : ''}내 퇴사 가능 나이와 또래 중 내 등수를 1분 만에 확인하세요.`;

  // 사람은 앱 루트로(같은 조건 파라미터 유지) 이동 → 결과 화면 표시
  const redirect = `${site}/?${q.toString()}#result`;

  const html = `<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="파이어맵">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(desc)}">
<meta property="og:url" content="${esc(redirect)}">
<meta property="og:image" content="${ogImg}">
<meta property="og:image:secure_url" content="${ogImg}">
<meta property="og:image:type" content="image/png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${esc(title)}">
<meta name="twitter:description" content="${esc(desc)}">
<meta name="twitter:image" content="${ogImg}">
<link rel="canonical" href="${site}/">
<meta http-equiv="refresh" content="0; url=${esc(redirect)}">
<script>location.replace(${JSON.stringify(redirect)});</script>
</head><body style="font-family:-apple-system,sans-serif;text-align:center;padding:40px;color:#1e2859">
파이어맵으로 이동 중… <a href="${esc(redirect)}">계속하기</a>
</body></html>`;

  return new Response(html, {
    headers: {
      'content-type': 'text/html; charset=utf-8',
      'cache-control': 'public, max-age=300'
    }
  });
}
