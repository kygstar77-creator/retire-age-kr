import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import sharp from 'sharp';

const deploy = join(process.cwd(), 'outputs', 'deploy');
const indexPath = join(deploy, 'index.html');
let html = await readFile(indexPath, 'utf8');

const siteUrl = 'https://retire-age-kr.pages.dev/';
const ogVersion = 'firemap-rank-v6-20260610';
const ogImageUrl = `https://retire-age-kr.pages.dev/og-image.png?v=${ogVersion}`;
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

const ogImage = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <radialGradient id="warm" cx="82%" cy="18%" r="45%">
      <stop offset="0" stop-color="#fed7aa"/>
      <stop offset="0.42" stop-color="#fff7ed"/>
      <stop offset="1" stop-color="#fffdf9" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1200" height="630" fill="#fffdf9"/>
  <rect x="34" y="30" width="1132" height="570" rx="54" fill="#ffffff" stroke="#fed7aa" stroke-width="4"/>
  <rect x="34" y="30" width="1132" height="570" rx="54" fill="url(#warm)"/>
  <circle cx="146" cy="126" r="54" fill="#fff1e7"/>
  <g transform="translate(80 62) scale(.55)">${flame}</g>
  <text x="232" y="150" fill="#111827" font-family="Arial, sans-serif" font-size="58" font-weight="900">파이어맵</text>
  <text x="106" y="300" fill="#ea580c" font-family="Arial, sans-serif" font-size="40" font-weight="900">퇴사나이 · FIRE 등수 계산기</text>
  <text x="106" y="402" fill="#111827" font-family="Arial, sans-serif" font-size="82" font-weight="900">또래 중 내 FIRE</text>
  <text x="106" y="496" fill="#ff5a00" font-family="Arial, sans-serif" font-size="82" font-weight="900">등수는 몇 등?</text>
  <rect x="106" y="532" width="332" height="58" rx="22" fill="#ff5a00"/>
  <text x="150" y="571" fill="#ffffff" font-family="Arial, sans-serif" font-size="28" font-weight="900">무료로 내 등수 확인</text>
  <text x="476" y="570" fill="#6b7280" font-family="Arial, sans-serif" font-size="26" font-weight="800">자산·생활비로 1분 · 또래 상위 %</text>
</svg>`;

await writeFile(join(deploy, 'og-image.svg'), ogImage, 'utf8');
await sharp(Buffer.from(ogImage)).png().toFile(join(deploy, 'og-image.png'));
