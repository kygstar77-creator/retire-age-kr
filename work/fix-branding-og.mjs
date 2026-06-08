import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import sharp from 'sharp';

const deploy = join(process.cwd(), 'outputs', 'deploy');
const indexPath = join(deploy, 'index.html');
let html = await readFile(indexPath, 'utf8');

const siteUrl = 'https://retire-age-kr.pages.dev/';
const ogImageUrl = 'https://retire-age-kr.pages.dev/og-image.png';
const ogTitle = '파이어맵 - 내 돈은 몇 살까지 버틸까?';
const ogDescription = '자산, 생활비, 수익률, 국민연금으로 FIRE 시점을 계산해보세요.';

html = html
  .replaceAll('서버 저장 없음 · 카톡 공유 최적화 · 3분 계산', '개인정보 저장 없음 · 무료 계산 · 바로 결과 확인')
  .replaceAll('og-image.png?v=4', 'og-image.png')
  .replaceAll('og-image.png?v=5', 'og-image.png')
  .replaceAll('og-image.png?v=6', 'og-image.png');

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
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#fff7ed"/>
      <stop offset="1" stop-color="#fed7aa"/>
    </linearGradient>
    <linearGradient id="sun" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#fb923c"/>
      <stop offset="1" stop-color="#ea580c"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <rect x="64" y="58" width="1072" height="514" rx="44" fill="#fffaf5" stroke="#fed7aa" stroke-width="3"/>
  <circle cx="980" cy="178" r="78" fill="url(#sun)" opacity="0.92"/>
  <path d="M650 438 C735 332 810 374 870 282 C934 184 1005 254 1136 128 L1136 572 L650 572 Z" fill="#9a3412" opacity="0.12"/>
  <path d="M640 474 C730 392 790 416 858 340 C930 260 1000 318 1136 220" fill="none" stroke="#ea580c" stroke-width="18" stroke-linecap="round"/>
  <path d="M640 474 C730 392 790 416 858 340 C930 260 1000 318 1136 220" fill="none" stroke="#fff7ed" stroke-width="5" stroke-linecap="round" opacity="0.72"/>
  <circle cx="640" cy="474" r="16" fill="#fff7ed" stroke="#ea580c" stroke-width="8"/>
  <circle cx="858" cy="340" r="16" fill="#fff7ed" stroke="#ea580c" stroke-width="8"/>
  <circle cx="1136" cy="220" r="16" fill="#fff7ed" stroke="#ea580c" stroke-width="8"/>
  <text x="118" y="158" fill="#ea580c" font-family="Arial, sans-serif" font-size="46" font-weight="900">파이어맵</text>
  <text x="118" y="258" fill="#18212c" font-family="Arial, sans-serif" font-size="74" font-weight="900">내 돈은 몇 살까지</text>
  <text x="118" y="344" fill="#18212c" font-family="Arial, sans-serif" font-size="74" font-weight="900">버틸 수 있을까?</text>
  <text x="118" y="430" fill="#53616c" font-family="Arial, sans-serif" font-size="31" font-weight="800">자산 · 생활비 · 수익률 · 국민연금으로</text>
  <text x="118" y="474" fill="#53616c" font-family="Arial, sans-serif" font-size="31" font-weight="800">나의 FIRE 시점을 계산해보세요</text>
  <rect x="118" y="504" width="244" height="46" rx="23" fill="#111827"/>
  <text x="240" y="535" text-anchor="middle" fill="#ffffff" font-family="Arial, sans-serif" font-size="22" font-weight="900">2분 무료 계산</text>
</svg>`;

await writeFile(join(deploy, 'og-image.svg'), ogImage, 'utf8');
await sharp(Buffer.from(ogImage)).png().toFile(join(deploy, 'og-image.png'));
