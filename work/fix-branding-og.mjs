import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import sharp from 'sharp';

const deploy = join(process.cwd(), 'outputs', 'deploy');
const indexPath = join(deploy, 'index.html');
let html = await readFile(indexPath, 'utf8');

const siteUrl = 'https://firemap.kr/';
const ogVersion = 'firemap-screens-v7-20260613';
const ogImageUrl = `https://firemap.kr/og-image.png?v=${ogVersion}`;
const seoTitle = '파이어맵 | FIRE·조기은퇴 계산기 · 퇴사 가능 나이';
const ogTitle = '또래 중 내 FIRE 등수는? — 파이어맵';
const ogDescription = '퇴사 가능 나이, 또래 중 내 등수, 절약으로 파이어 앞당기기까지 — 무료 1분.';

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
  <path d="M105 153c-31-18-33-57-8-86 7 22 21 28 31 42 10-31 32-48 59-70-2 33 17 45 31 69 23 39 3 87-37 105 14-18 13-42-2-58-8-9-16-17-18-31-11 18-31 29-37 51-5 17 2 32 13 44-13-3-25-8-32-16z" fill="#ff5a00"/>
  <path d="M142 218c-26-26-13-62 17-91 2 20 18 31 26 47 9 18 2 41-16 53-16 10-29 7-27-9z" fill="#fed7aa"/>
`;

const brand = `
  <circle cx="118" cy="116" r="44" fill="#fff1e7"/>
  <g transform="translate(86 74) scale(.40)">${flame}</g>
  <text x="180" y="130" fill="#111827" font-family="Arial, sans-serif" font-size="44" font-weight="900">파이어맵</text>
`;

const ogResult = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="#fffdf9"/>
  <rect x="34" y="30" width="1132" height="570" rx="54" fill="#ffffff" stroke="#fed7aa" stroke-width="4"/>
  <g opacity="0.07"><g transform="translate(940 360) scale(1.7)">${flame}</g></g>
  ${brand}
  <text x="80" y="248" fill="#ea580c" font-family="Arial, sans-serif" font-size="33" font-weight="900">내 FIRE 결과 · 무료 1분 계산</text>
  <text x="80" y="346" fill="#111827" font-family="Arial, sans-serif" font-size="74" font-weight="900"><tspan fill="#ff5a00">42세</tspan>에 퇴사하면</text>
  <text x="80" y="432" fill="#111827" font-family="Arial, sans-serif" font-size="74" font-weight="900"><tspan fill="#ff5a00">50세</tspan>까지 버텨요</text>
  <rect x="80" y="478" width="486" height="92" rx="20" fill="#f8fafc"/>
  <text x="106" y="516" fill="#6b7280" font-family="Arial, sans-serif" font-size="24" font-weight="800">퇴사 나이</text>
  <text x="106" y="554" fill="#111827" font-family="Arial, sans-serif" font-size="36" font-weight="900">42세</text>
  <rect x="582" y="478" width="538" height="92" rx="20" fill="#fff7ed"/>
  <text x="608" y="516" fill="#9a3412" font-family="Arial, sans-serif" font-size="24" font-weight="800">또래 중 내 등수</text>
  <text x="608" y="554" fill="#ff5a00" font-family="Arial, sans-serif" font-size="36" font-weight="900">1분이면 확인</text>
</svg>`;

const ogSave = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="#fffdf9"/>
  <rect x="34" y="30" width="1132" height="570" rx="54" fill="#ffffff" stroke="#fed7aa" stroke-width="4"/>
  ${brand}
  <text x="80" y="232" fill="#ea580c" font-family="Arial, sans-serif" font-size="33" font-weight="900">오늘의 절약 · 파이어 앞당기기</text>
  <text x="80" y="318" fill="#111827" font-family="Arial, sans-serif" font-size="66" font-weight="900">아낀 돈이 <tspan fill="#ff5a00">퇴사를 앞당겨요</tspan></text>
  <text x="80" y="430" fill="#6b7280" font-family="Arial, sans-serif" font-size="28" font-weight="800">지금 35세</text>
  <text x="1120" y="430" text-anchor="end" fill="#6b7280" font-family="Arial, sans-serif" font-size="28" font-weight="800">예상 퇴사 62세</text>
  <rect x="80" y="452" width="1040" height="24" rx="12" fill="#eef2f7"/>
  <rect x="905" y="452" width="215" height="24" rx="12" fill="#ff5a00"/>
  <line x1="905" y1="430" x2="905" y2="484" stroke="#111827" stroke-width="5"/>
  <path d="M905 430 L947 444 L905 458 Z" fill="#ff5a00"/>
  <text x="80" y="548" fill="#111827" font-family="Arial, sans-serif" font-size="34" font-weight="900">커피 한 잔 아끼면 <tspan fill="#ff5a00">퇴사가 2시간</tspan> 빨라져요</text>
</svg>`;

await writeFile(join(deploy, 'og-image.svg'), ogResult, 'utf8');
await sharp(Buffer.from(ogResult)).png().toFile(join(deploy, 'og-image.png'));
await writeFile(join(deploy, 'og-save.svg'), ogSave, 'utf8');
await sharp(Buffer.from(ogSave)).png().toFile(join(deploy, 'og-save.png'));
