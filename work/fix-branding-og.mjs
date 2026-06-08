import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import sharp from 'sharp';

const deploy = join(process.cwd(), 'outputs', 'deploy');
const indexPath = join(deploy, 'index.html');
let html = await readFile(indexPath, 'utf8');

const siteUrl = 'https://retire-age-kr.pages.dev/';
const ogImageUrl = 'https://retire-age-kr.pages.dev/og-image.png?v=firemap-v3-20260609';
const ogTitle = '파이어맵 - 내 돈은 몇 살까지 버틸까?';
const ogDescription = '자산, 생활비, 수익률, 국민연금으로 FIRE 시점을 계산해보세요.';

html = html
  .replaceAll('서버 저장 없음 · 카톡 공유 최적화 · 3분 계산', '개인정보 저장 없음 · 무료 계산 · 바로 결과 확인')
  .replaceAll(/og-image\.png\?v=[^\"']+/g, 'og-image.png?v=firemap-v3-20260609');

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
html = html.replace(/<title>.*?<\/title>/, `<title>${ogTitle}</title>\n${metaBlock}`);
html = html.replace(/<link rel="canonical" href="[^"]*" \/>/, `<link rel="canonical" href="${siteUrl}" />`);

await writeFile(indexPath, html, 'utf8');

const ogImage = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff7ed"/><stop offset="1" stop-color="#fed7aa"/></linearGradient>
    <linearGradient id="line" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff7a1a"/><stop offset="1" stop-color="#ea580c"/></linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect x="60" y="56" width="1080" height="518" rx="48" fill="#fffdf9" stroke="#fed7aa" stroke-width="3"/>
  <circle cx="998" cy="166" r="86" fill="#ffedd5"/>
  <path d="M650 462 C730 350 800 382 874 296 C946 210 1005 278 1136 178 L1136 574 L650 574 Z" fill="#9a3412" opacity="0.10"/>
  <path d="M646 466 C730 382 792 406 862 332 C938 252 1002 314 1136 214" fill="none" stroke="url(#line)" stroke-width="18" stroke-linecap="round"/>
  <circle cx="646" cy="466" r="15" fill="#fffdf9" stroke="#ea580c" stroke-width="8"/>
  <circle cx="862" cy="332" r="15" fill="#fffdf9" stroke="#ea580c" stroke-width="8"/>
  <circle cx="1136" cy="214" r="15" fill="#fffdf9" stroke="#ea580c" stroke-width="8"/>
  <text x="118" y="150" fill="#ea580c" font-family="Arial, sans-serif" font-size="48" font-weight="900">파이어맵</text>
  <text x="118" y="254" fill="#111827" font-family="Arial, sans-serif" font-size="78" font-weight="900">내 돈은 몇 살까지</text>
  <text x="118" y="344" fill="#111827" font-family="Arial, sans-serif" font-size="78" font-weight="900">버틸 수 있을까?</text>
  <text x="118" y="426" fill="#53616c" font-family="Arial, sans-serif" font-size="32" font-weight="800">자산 · 생활비 · 수익률 · 국민연금으로 계산</text>
  <rect x="118" y="488" width="232" height="52" rx="26" fill="#ea580c"/>
  <text x="234" y="523" text-anchor="middle" fill="#ffffff" font-family="Arial, sans-serif" font-size="23" font-weight="900">무료 계산하기</text>
</svg>`;

await writeFile(join(deploy, 'og-image.svg'), ogImage, 'utf8');
await sharp(Buffer.from(ogImage)).png().toFile(join(deploy, 'og-image.png'));
