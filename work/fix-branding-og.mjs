import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import sharp from 'sharp';

const deploy = join(process.cwd(), 'outputs', 'deploy');
const indexPath = join(deploy, 'index.html');
let html = await readFile(indexPath, 'utf8');

const siteUrl = 'https://firemap.kr/';
const ogVersion = 'firemap-premium-v8-20260618';
const ogImageUrl = `https://firemap.kr/og-image.png?v=${ogVersion}`;
const seoTitle = '파이어맵 | 파이어 가능 나이 계산기 · 또래 중 내 등수';
const ogTitle = '또래 중 내 FIRE 등수는? — 파이어맵';
const ogDescription = '내 파이어 가능 나이와 목표 자산을 1분 만에 — 자산·연금·세금 반영. 또래 등수도. 무료.';

html = html.replaceAll(/og-image\.png\?v=[^"']+/g, `og-image.png?v=${ogVersion}`);

const metaBlock = `
<meta property="og:type" content="website" />
<meta property="og:site_name" content="파이어맵" />
<meta property="og:title" content="${ogTitle}" />
<meta property="og:description" content="${ogDescription}" />
<meta property="og:url" content="${siteUrl}" />
<meta property="og:image" content="${ogImageUrl}" />
<meta property="og:image:secure_url" content="${ogImageUrl}" />
<meta property="og:image:type" content="image/png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="${ogTitle}" />
<meta name="twitter:description" content="${ogDescription}" />
<meta name="twitter:image" content="${ogImageUrl}" />`;

html = html.replace(/\s*<meta property="og:[^"]+" content="[^"]*" \/>/g, '');
html = html.replace(/\s*<meta name="twitter:[^"]+" content="[^"]*" \/>/g, '');
html = html.replace(/<title>.*?<\/title>/, `<title>${seoTitle}</title>\n${metaBlock}`);
html = html.replace(/<link rel="canonical" href="[^"]*" \/>/, `<link rel="canonical" href="${siteUrl}" />`);

await writeFile(indexPath, html, 'utf8');

const flame = `
  <path d="M256 84 C 232 150, 188 172, 188 256 C 188 322, 218 360, 256 360 C 294 360, 324 322, 324 256 C 324 212, 300 188, 286 162 C 282 192, 268 204, 252 210 C 268 166, 262 116, 256 84 Z" fill="#ff5a00"/>
  <path d="M256 250 C 246 276, 232 286, 232 312 C 232 336, 242 352, 256 352 C 270 352, 280 336, 280 312 C 280 292, 270 280, 264 268 C 262 282, 258 286, 252 290 C 258 274, 258 262, 256 250 Z" fill="#fdba74"/>
`;

const brand = `
  <circle cx="118" cy="116" r="44" fill="#fff1e7"/>
  <g transform="translate(61.7 63.5) scale(.22)">${flame}</g>
  <text x="180" y="130" fill="#111827" font-family="Arial, sans-serif" font-size="44" font-weight="900">파이어맵</text>
`;

const ogResult = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff8f1"/><stop offset="1" stop-color="#ffffff"/></linearGradient>
    <radialGradient id="glow" cx="0.82" cy="0.18" r="0.6"><stop offset="0" stop-color="#ffd9c2" stop-opacity="0.55"/><stop offset="1" stop-color="#ffd9c2" stop-opacity="0"/></radialGradient>
    <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff8a4c"/><stop offset="1" stop-color="#ee4a1f"/></linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect width="1200" height="630" fill="url(#glow)"/>
  <g opacity="0.05"><g transform="translate(760 120) scale(1.55)">${flame}</g></g>
  <circle cx="96" cy="86" r="30" fill="#fff1e7"/>
  <g transform="translate(73.5 63.5) scale(.088)">${flame}</g>
  <text x="138" y="98" fill="#15151b" font-family="Arial, sans-serif" font-size="34" font-weight="900">파이어맵</text>
  <rect x="72" y="150" width="470" height="48" rx="24" fill="#fff0ea"/>
  <text x="96" y="182" fill="#e8431c" font-family="Arial, sans-serif" font-size="23" font-weight="800">무료 1분 · 자산·연금·세금까지 반영</text>
  <text x="72" y="312" fill="#15151b" font-family="Arial, sans-serif" font-size="82" font-weight="900" letter-spacing="-3">나는 몇 살에</text>
  <text x="72" y="406" fill="#15151b" font-family="Arial, sans-serif" font-size="82" font-weight="900" letter-spacing="-3"><tspan fill="#ff5a00">파이어</tspan>할 수 있을까?</text>
  <text x="74" y="466" fill="#6b7280" font-family="Arial, sans-serif" font-size="27" font-weight="700">또래 중 내 FIRE 등수까지 한 번에</text>
  <rect x="72" y="506" width="250" height="74" rx="18" fill="#ffffff" stroke="#f0e3d9" stroke-width="2"/>
  <text x="92" y="540" fill="#9aa3bf" font-family="Arial, sans-serif" font-size="20" font-weight="800">비용</text>
  <text x="92" y="570" fill="#15151b" font-family="Arial, sans-serif" font-size="28" font-weight="900">완전 무료</text>
  <rect x="336" y="506" width="250" height="74" rx="18" fill="#fff7ed" stroke="#fed7aa" stroke-width="2"/>
  <text x="356" y="540" fill="#9a3412" font-family="Arial, sans-serif" font-size="20" font-weight="800">또래 중 내 등수</text>
  <text x="356" y="570" fill="#ff5a00" font-family="Arial, sans-serif" font-size="28" font-weight="900">바로 확인</text>
  <circle cx="965" cy="300" r="172" fill="#ffffff" stroke="#f3ece6" stroke-width="2"/>
  <circle cx="965" cy="300" r="132" fill="none" stroke="#efe9e3" stroke-width="26"/>
  <circle cx="965" cy="300" r="132" fill="none" stroke="url(#ring)" stroke-width="26" stroke-linecap="round" stroke-dasharray="597 232" transform="rotate(-90 965 300)"/>
  <text x="965" y="262" text-anchor="middle" fill="#9aa3bf" font-family="Arial, sans-serif" font-size="24" font-weight="800">예상 파이어</text>
  <text x="965" y="338" text-anchor="middle" fill="#ff5a00" font-family="Arial, sans-serif" font-size="92" font-weight="900">47세</text>
  <rect x="889" y="356" width="152" height="40" rx="20" fill="#fff0ea"/>
  <text x="965" y="383" text-anchor="middle" fill="#e8431c" font-family="Arial, sans-serif" font-size="21" font-weight="800">또래 상위 12%</text>
</svg>`;
const ogSave = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="#fffdf9"/>
  <rect x="34" y="30" width="1132" height="570" rx="54" fill="#ffffff" stroke="#fed7aa" stroke-width="4"/>
  ${brand}
  <text x="80" y="232" fill="#ff5a00" font-family="Arial, sans-serif" font-size="33" font-weight="900">오늘의 절약 · 파이어 앞당기기</text>
  <text x="80" y="318" fill="#111827" font-family="Arial, sans-serif" font-size="66" font-weight="900">아낌 돈이 <tspan fill="#ff5a00">파이어를 앞당겨요</tspan></text>
  <text x="80" y="430" fill="#6b7280" font-family="Arial, sans-serif" font-size="28" font-weight="800">지금</text>
  <text x="1120" y="430" text-anchor="end" fill="#6b7280" font-family="Arial, sans-serif" font-size="28" font-weight="800">예상 파이어</text>
  <rect x="80" y="452" width="1040" height="24" rx="12" fill="#eef2f7"/>
  <rect x="845" y="452" width="275" height="24" rx="12" fill="#ff5a00"/>
  <line x1="845" y1="430" x2="845" y2="484" stroke="#111827" stroke-width="5"/>
  <path d="M845 430 L887 444 L845 458 Z" fill="#ff5a00"/>
  <text x="80" y="548" fill="#111827" font-family="Arial, sans-serif" font-size="34" font-weight="900">커피 한 잔 아껰도 <tspan fill="#ff5a00">파이어가 빨라져요</tspan></text>
</svg>`;

await writeFile(join(deploy, 'og-image.svg'), ogResult, 'utf8');
await sharp(Buffer.from(ogResult)).png().toFile(join(deploy, 'og-image.png'));
await writeFile(join(deploy, 'og-save.svg'), ogSave, 'utf8');
await sharp(Buffer.from(ogSave)).png().toFile(join(deploy, 'og-save.png'));
