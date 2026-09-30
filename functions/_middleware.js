// 1) 운영 pages.dev 및 www를 정식 도메인(firemap.kr)으로 301 통합. 미리보기(firemap-v3.*)는 그대로 둠.
// 2) 도구 화면의 검색용 경로(/dividend·/health-insurance·/tax·/pension·/cities·/firetype·/ranking·/experiment) —
//    스꾸(seukku.cc /s/{slug}) 방식. 앱 껍데기(index.html)를 그대로 내되 title·description·canonical·og를 그 도구 것으로 바꾸고,
//    크롤러가 읽을 본문 블록(#sSeo: 제목·그 화면의 항목·다른 도구 링크)을 body 앞에 넣는다.
//    앱은 뜨자마자 #sSeo를 지우고 주소를 해시(#dividend)로 바꾼다(src/components/FireMapMVP.jsx) — 사람 눈엔 앱 그대로, 클로킹 아님.
/* global HTMLRewriter */
import { TOOL_PAGES, toolPageByPath } from '../src/firemap-v2/toolPages.js';

const esc = (v) => String(v == null ? '' : v).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

const NOTE = '파이어맵은 입력값을 기계적으로 계산하는 참고용 시뮬레이션이며 투자·세무 자문이 아니에요.';
function footHtml(site) {
  return `<p>${esc(NOTE)} <a href="${site}/disclaimer">면책</a> · <a href="${site}/privacy">개인정보처리방침</a> · <a href="${site}/contact">문의</a></p>`;
}
const BOX = 'style="max-width:640px;margin:24px auto;padding:0 16px;font-family:sans-serif"';
// 2026-09-30 사장님: "파이어맵 들어갈 때 설명글이 0.5초 보인다." 숨기면(CSS로 가리기) 구글 숨김 텍스트 위반이 된다(스꾸 총무 조언과 같음).
// 그래서 숨기지 않고 모양을 바꾼다. 앱이 뜨기 전 첫 화면에는 제목과 한 줄 소개만 로딩 화면처럼 가운데 보이고,
// 나머지 설명은 그 아래(스크롤하면 보이는 자리)에 둔다. 사람과 봇이 같은 글을 받는다.
const HERO = 'style="min-height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;gap:8px;color:#1f1f1f"';
const HERO_H1 = 'style="font-size:22px;font-weight:700;margin:0;color:#ff5a00"';
const HERO_P = 'style="font-size:14px;margin:0;color:#6b6b6b"';

function seoBlock(tool, site) {
  const items = tool.sections.map((s) => `<li>${esc(s)}</li>`).join('');
  const others = TOOL_PAGES.filter((t) => t.path !== tool.path).map((t) => `<a href="${site}${t.path}">${esc(t.title)}</a>`).join(' · ');
  const body = (tool.body || []).map((b) => `<p>${esc(b)}</p>`).join('');
  return `<div id="sSeo" ${BOX}><div ${HERO}><h1 ${HERO_H1}>${esc(tool.title)}</h1><p ${HERO_P}>파이어맵 · 1분이면 나도 계산</p></div><ul>${items}</ul>${body}<p><a href="${site}/">1분이면 나도 계산</a></p><p>${others} · <a href="${site}/guide/">파이어 백과</a></p>${footHtml(site)}</div>`;
}

// 첫 화면(/) — 2026-09-30까지는 크롤러가 제목 한 줄(34자)만 받았다. 문구는 index.html의 description·JSON-LD와 도구 화면 라벨 그대로.
// 이 블록은 앱 화면에 있는 것만 담는다(스꾸 총무 2026-09-30: 크롤러 블록은 회색 지대 — 앱 화면과 다른 내용을 넣거나 CSS로 숨기면 위반). 글은 /guide 독립 페이지로.
function homeBlock(site) {
  const tools = TOOL_PAGES.map((t) => `<h3><a href="${site}${t.path}">${esc(t.title)}</a></h3><p>${t.sections.map(esc).join(' · ')}</p>`).join('');
  return `<div id="sSeo" ${BOX}><div ${HERO}><h1 ${HERO_H1}>파이어맵 — FIRE·조기은퇴 계산기</h1>` +
    `<p ${HERO_P}>내 파이어(조기은퇴) 가능 나이와 목표 자산을 1분 만에 계산. 자산·연금·세금 반영. 또래 중 내 등수도.</p></div>` +
    `<p>FIRE·조기은퇴 계산기. 내 자산·저축으로 퇴사 가능 나이와 또래 중 내 등수를 계산하는 파이어맵.</p>` +
    `<h2>도구</h2>${tools}` +
    `<p><a href="${site}/guide/">파이어 백과</a> · <a href="${site}/fire-city/">어디서 파이어할까</a></p>${footHtml(site)}</div>`;
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

  const isHome = request.method === 'GET' && (url.pathname === '/' || url.pathname === '/index.html');
  const tool = request.method === 'GET' && !isHome ? toolPageByPath(url.pathname) : null;
  if (isHome) {
    const shell = await next();
    if (!(shell.headers.get('content-type') || '').includes('text/html')) return shell;
    const home = new Response(shell.body, shell);
    return new HTMLRewriter().on('body', { element(el) { el.prepend(homeBlock(url.origin), { html: true }); } }).transform(home);
  }
  if (!tool) return next();

  // 앱 껍데기를 그대로 받아서(SPA 폴백 = index.html) 머리와 본문만 바꾼다.
  const shell = await next();
  const ct = shell.headers.get('content-type') || '';
  if (!ct.includes('text/html')) return shell;
  const site = url.origin;
  const pageUrl = `${site}${tool.path}`;
  const title = `${tool.seoTitle || tool.title} | 파이어맵`;
  const desc = tool.desc || `${tool.sections.join(' · ')} · 1분이면 나도 계산`;
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
