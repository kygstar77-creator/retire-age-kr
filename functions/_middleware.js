// 1) 운영 pages.dev 및 www를 정식 도메인(firemap.kr)으로 301 통합. 미리보기(firemap-v3.*)는 그대로 둠.
// 2) 도구 화면의 검색용 경로(/dividend·/health-insurance·/tax·/pension·/cities·/firetype·/ranking·/experiment) —
//    스꾸(seukku.cc /s/{slug}) 방식. 앱 껍데기(index.html)를 그대로 내되 title·description·canonical·og를 그 도구 것으로 바꾸고,
//    크롤러가 읽을 본문 블록(#sSeo: 제목·그 화면의 항목·다른 도구 링크)을 body 앞에 넣는다.
//    앱은 뜨자마자 #sSeo를 지우고 주소를 해시(#dividend)로 바꾼다(src/components/FireMapMVP.jsx) — 사람 눈엔 앱 그대로, 클로킹 아님.
/* global HTMLRewriter */
import { TOOL_PAGES, toolPageByPath } from '../src/firemap-v2/toolPages.js';

const esc = (v) => String(v == null ? '' : v).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

function seoBlock(tool, site) {
  const items = tool.sections.map((s) => `<li>${esc(s)}</li>`).join('');
  const others = TOOL_PAGES.filter((t) => t.path !== tool.path).map((t) => `<a href="${site}${t.path}">${esc(t.title)}</a>`).join(' · ');
  return `<div id="sSeo" style="max-width:640px;margin:24px auto;padding:0 16px;font-family:sans-serif"><h1>${esc(tool.title)}</h1><ul>${items}</ul><p><a href="${site}/">1분이면 나도 계산</a></p><p>${others} · <a href="${site}/guide/">파이어 백과</a></p></div>`;
}

export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);
  const host = url.hostname;
  if (host === 'retire-age-kr.pages.dev' || host === 'www.firemap.kr') {
    url.hostname = 'firemap.kr';
    url.protocol = 'https:';
    return Response.redirect(url.toString(), 301);
  }

  const tool = request.method === 'GET' ? toolPageByPath(url.pathname) : null;
  if (!tool) return next();

  // 앱 껍데기를 그대로 받아서(SPA 폴백 = index.html) 머리와 본문만 바꾼다.
  const shell = await next();
  const ct = shell.headers.get('content-type') || '';
  if (!ct.includes('text/html')) return shell;
  const site = url.origin;
  const pageUrl = `${site}${tool.path}`;
  const title = `${tool.title} | 파이어맵`;
  const desc = `${tool.sections.join(' · ')} · 1분이면 나도 계산`;
  const res = new Response(shell.body, shell);
  res.headers.set('cache-control', 'public, max-age=0, must-revalidate');
  return new HTMLRewriter()
    .on('title', { element(el) { el.setInnerContent(title); } })
    .on('meta[name="description"]', { element(el) { el.setAttribute('content', desc); } })
    .on('link[rel="canonical"]', { element(el) { el.setAttribute('href', pageUrl); } })
    .on('meta[property="og:title"]', { element(el) { el.setAttribute('content', title); } })
    .on('meta[property="og:description"]', { element(el) { el.setAttribute('content', desc); } })
    .on('meta[property="og:url"]', { element(el) { el.setAttribute('content', pageUrl); } })
    .on('meta[name="twitter:title"]', { element(el) { el.setAttribute('content', title); } })
    .on('meta[name="twitter:description"]', { element(el) { el.setAttribute('content', desc); } })
    .on('body', { element(el) { el.prepend(seoBlock(tool, site), { html: true }); } })
    .transform(res);
}
