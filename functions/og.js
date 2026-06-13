// Cloudflare Pages Function: /og
// 공유 링크 미리보기(카톡 등)에 그 사람의 '파이어 랭킹 · 퇴사 나이'를 박은 PNG 카드를 그때그때 렌더.
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
  const target = intOr(q.get('target'), 0, 0, 120);
  const pos = intOr(q.get('pos'), 0, 0, 9999999);
  const tot = Math.max(1, intOr(q.get('tot'), 1, 1, 9999999));
  const ret = intOr(q.get('ret'), 5, 0, 99);
  const inf = intOr(q.get('inf'), 3, 0, 99);
  const runway = safeRunway(q.get('rw'));
  const p = Math.max(1, Math.min(99, Math.round((pos / tot) * 100)));
  const barW = 640;
  const markerX = 84 + Math.max(8, Math.min(barW - 8, (p / 100) * barW));
  const eaText = ea > 0 ? ea + '세' : '—';
  const targetText = target > 0 ? target + '세' : '—';
  return `<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
<rect width="1200" height="630" fill="#18224d"/>
<svg x="64" y="50" width="26" height="52" viewBox="188 84 136 276"><path d="M256 84 C 232 150, 188 172, 188 256 C 188 322, 218 360, 256 360 C 294 360, 324 322, 324 256 C 324 212, 300 188, 286 162 C 282 192, 268 204, 252 210 C 268 166, 262 116, 256 84 Z" fill="#ff5a00"/><path d="M256 250 C 246 276, 232 286, 232 312 C 232 336, 242 352, 256 352 C 270 352, 280 336, 280 312 C 280 292, 270 280, 264 268 C 262 282, 258 286, 252 290 C 258 274, 258 262, 256 250 Z" fill="#fdba74"/></svg>
<text x="104" y="92" font-family="${KR}" font-weight="700" font-size="42" fill="#ffffff">파이어맵</text>
<rect x="946" y="50" width="186" height="48" rx="24" fill="none" stroke="#ff5a00" stroke-width="2"/>
<text x="1039" y="82" font-family="${KR}" font-weight="700" font-size="22" fill="#ff8a4c" text-anchor="middle">FIRE 등수 인증</text>
<text x="84" y="170" font-family="${KR}" font-weight="400" font-size="32" fill="#9aa4d4">파이어 랭킹 · 내 순위</text>
<text x="84" y="240" font-family="${KR}" font-weight="700" font-size="54" fill="#ffffff">상위</text>
<text x="80" y="396" font-family="${KR}" font-weight="700" font-size="150" fill="#ff5a00">${p}%</text>
<text x="88" y="452" font-family="${KR}" font-weight="700" font-size="36" fill="#ffffff">전체 <tspan fill="#ff8a4c">${comma(tot)}명</tspan> 중 <tspan fill="#ff8a4c">${comma(pos)}등</tspan></text>
<rect x="84" y="486" width="${barW}" height="14" rx="7" fill="#2a3568"/>
<rect x="84" y="486" width="${Math.max(10, (p / 100) * barW)}" height="14" rx="7" fill="#ff5a00"/>
<circle cx="${markerX}" cy="493" r="13" fill="#ffffff"/>
<text x="84" y="534" font-family="${KR}" font-weight="400" font-size="21" fill="#9aa4d4">상위</text>
<text x="724" y="534" font-family="${KR}" font-weight="400" font-size="21" fill="#6b76a8" text-anchor="end">하위</text>
<rect x="812" y="150" width="320" height="300" rx="20" fill="#212c5e"/>
<text x="844" y="210" font-family="${KR}" font-weight="400" font-size="26" fill="#9aa4d4">퇴사 가능</text>
<text x="1100" y="214" font-family="${KR}" font-weight="700" font-size="44" fill="#ffffff" text-anchor="end">${eaText}</text>
<line x1="844" y1="242" x2="1100" y2="242" stroke="#2f3a6e" stroke-width="1.5"/>
<text x="844" y="300" font-family="${KR}" font-weight="400" font-size="26" fill="#9aa4d4">목표 퇴사</text>
<text x="1100" y="304" font-family="${KR}" font-weight="700" font-size="44" fill="#ffffff" text-anchor="end">${targetText}</text>
<line x1="844" y1="332" x2="1100" y2="332" stroke="#2f3a6e" stroke-width="1.5"/>
<text x="844" y="390" font-family="${KR}" font-weight="400" font-size="26" fill="#9aa4d4">자산 수명</text>
<text x="1100" y="394" font-family="${KR}" font-weight="700" font-size="44" fill="#34d399" text-anchor="end">${runway}</text>
<text x="84" y="598" font-family="${KR}" font-weight="700" font-size="30" fill="#ffffff">나도 확인하고 전체 랭킹 보기  →  <tspan fill="#ff8a4c">firemap.kr</tspan></text>
<text x="1116" y="598" font-family="${KR}" font-weight="400" font-size="22" fill="#6b76a8" text-anchor="end">연 수익률 ${ret}% · 물가 ${inf}% 가정 · 세전</text>
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
