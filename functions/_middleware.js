// 운영 pages.dev 및 www를 정식 도메인(firemap.kr)으로 301 통합. 미리보기(firemap-v3.*)는 그대로 둠.
export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);
  const host = url.hostname;
  if (host === 'retire-age-kr.pages.dev' || host === 'www.firemap.kr') {
    url.hostname = 'firemap.kr';
    url.protocol = 'https:';
    return Response.redirect(url.toString(), 301);
  }
  return next();
}
