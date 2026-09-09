// /naver-callback — 네이버 로그인 복귀 URL. code/state를 앱 루트 쿼리로 넘긴다(토큰 교환은 /naver-token).
export async function onRequestGet(context) {
  const url = new URL(context.request.url);
  const code = url.searchParams.get('code') || '';
  const state = url.searchParams.get('state') || '';
  const to = new URL('/', url.origin);
  if (code) { to.searchParams.set('naver_code', code); to.searchParams.set('naver_state', state); }
  return Response.redirect(to.toString(), 302);
}
