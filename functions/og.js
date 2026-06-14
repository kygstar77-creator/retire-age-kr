// Cloudflare Pages Function: /og
// 공유 링크 미리보기(카톡 등)에 그 사람의 '파이어 랭킹 · 파이어 나이'를 박은 PNG 카드를 그때그때 렌더.
// 실패 시 정적 og-image.png로 폴백 → 미리보기가 절대 깨지지 않게.
import { initWasm, Resvg } from '@resvg/resvg-wasm';
import resvgWasm from '@resvg/resvg-wasm/index_bg.wasm';
import { BOLD_B64, REGULAR_B64 } from './og-fonts.js';

const KR = 'Noto Sans CJK KR';
let wasmReady;

function b64ToBytes(b64) {
  const bin = atob(b64);
  const u = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i += 1) u[i] = bin.charCodeAt(i);
  return u;
}
const BOLD = b64ToBytes(BOLD_B64);
const REGULAR = b64ToBytes(REGULAR_B64);

const comma = (n) => String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
const intOr = (v, d, lo, hi) => {
  const n = parseInt(String(v == null ? '' : v), 10);
  if (!Number.isFinite(n)) return d;
  return Math.max(lo, Math.min(hi, n));
};
const safeRunway = (v) => {
  const s = String(v == null ? '' : v).replace(/[^0-9세이상\s]/g, '').trim().slice(0, 12);
  return s || '—';
};

function buildSvg(q) {
  const ea = intOr(q.get('ea'), 0, 0, 120);
  const pos = intOr(q.get('pos'), 0, 0, 9999999);
  const tot = Math.max(1, intOr(q.get('tot'), 1, 1, 9999999));
  const runway = safeRunway(q.get('rw'));
  const p = Math.max(1, Math.min(99, Math.round((pos / tot) * 100)));
  const parts = [];
  if (ea > 0) parts.push(ea + '세 파이어 가능');
  if (runway && runway !== '—') parts.push(runway.indexOf('이상') >= 0 ? runway + ' 버팀' : runway + '까지 버팀');
  const mid = parts.join(' · ');
  return `<svg width="1200" height="600" viewBox="0 0 1200 600" xmlns="http://www.w3.org/2000/svg">
<rect width="1200" height="600" fill="#18224d"/>
<svg x="497" y="92" width="30" height="60" viewBox="188 84 136 276"><path d="M256 84 C 232 150, 188 172, 188 256 C 188 322, 218 360, 256 360 C 294 360, 324 322, 324 256 C 324 212, 300 188, 286 162 C 282 192, 268 204, 252 210 C 268 166, 262 116, 256 84 Z" fill="#ff5a00"/><path d="M256 250 C 246 276, 232 286, 232 312 C 232 336, 242 352, 256 352 C 270 352, 280 336, 280 312 C 280 292, 270 280, 264 268 C 262 282, 258 286, 252 290 C 258 274, 258 262, 256 250 Z" fill="#fdba74"/></svg>
<text x="537" y="138" font-family="${KR}" font-weight="700" font-size="40" fill="#ffffff">파이어맵</text>
<text x="600" y="208" font-family="${KR}" font-weight="400" font-size="34" fill="#9aa4d4" text-anchor="middle">파이어 랭킹 · 또래 상위</text>
<text x="600" y="358" font-family="${KR}" font-weight="700" font-size="150" fill="#ff5a00" text-anchor="middle">${p}%</text>
<text x="600" y="418" font-family="${KR}" font-weight="700" font-size="40" fill="#ffffff" text-anchor="middle">전체 <tspan fill="#ff8a4c">${comma(tot)}명</tspan> 중 <tspan fill="#ff8a4c">${comma(pos)}등</tspan></text>
<text x="600" y="470" font-family="${KR}" font-weight="600" font-size="30" fill="#9aa4d4" text-anchor="middle">${mid}</text>
<text x="600" y="540" font-family="${KR}" font-weight="700" font-size="30" fill="#ffffff" text-anchor="middle">나도 1분 만에 확인  →  <tspan fill="#ff8a4c">firemap.kr</tspan></text>
</svg>`;
}

export async function onRequest(context) {
  const site = 'https://firemap.kr';
  try {
    if (!wasmReady) wasmReady = initWasm(resvgWasm);
    await wasmReady;
    const url = new URL(context.request.url);
    const svg = buildSvg(url.searchParams);
    const resvg = new Resvg(svg, {
      fitTo: { mode: 'width', value: 1200 },
      font: { fontBuffers: [BOLD, REGULAR], defaultFontFamily: KR, loadSystemFonts: false }
    });
    const png = resvg.render().asPng();
    return new Response(png, {
      headers: { 'content-type': 'image/png', 'cache-control': 'public, max-age=86400, s-maxage=604800' }
    });
  } catch (e) {
    return Response.redirect(`${site}/og-image.png?v=fallback`, 302);
  }
}
