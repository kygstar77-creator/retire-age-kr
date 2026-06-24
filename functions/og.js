// Cloudflare Pages Function: /og
// 공유 링크 미리보기(카톡 등)에 그 사람의 '파이어 랭킹 · 파이어 나이'를 박은 PNG 카드를 그때그때 렌더.
// 실패 시 정적 og-image.png로 폴백 → 미리보기가 절대 깨지지 않게.
import { initWasm, Resvg } from '@resvg/resvg-wasm';
import resvgWasm from '@resvg/resvg-wasm/index_bg.wasm';
import { BOLD_B64, REGULAR_B64 } from './og-fonts.js';
import { buildCardSvg } from './og-card.js';

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
const safeText = (v, max) => String(v == null ? '' : v).replace(/[<>&"]/g, '').trim().slice(0, max);

function buildSvg(q) {
  if ((q.get('mode') || '') === 'firetype') {
    return buildCardSvg({ mode: 'firetype', tname: safeText(q.get('tn'), 16), nick: safeText(q.get('nk'), 16), cities: safeText(q.get('ct'), 40), font: KR });
  }
  const ea = intOr(q.get('ea'), 0, 0, 120);
  const pos = intOr(q.get('pos'), 0, 0, 9999999);
  const tot = Math.max(1, intOr(q.get('tot'), 1, 1, 9999999));
  const runway = safeRunway(q.get('rw'));
  return buildCardSvg({ mode: 'rank', ea, pos, tot, runway, font: KR });
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
