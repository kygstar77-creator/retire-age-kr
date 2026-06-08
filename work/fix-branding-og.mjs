import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import sharp from 'sharp';

const deploy = join(process.cwd(), 'outputs', 'deploy');
const indexPath = join(deploy, 'index.html');
let html = await readFile(indexPath, 'utf8');

const siteUrl = 'https://retire-age-kr.pages.dev/';
const ogImageUrl = 'https://retire-age-kr.pages.dev/og-image.png?v=firemap-home-v4-20260609';
const ogTitle = '파이어맵 - 내 돈은 몇 살까지 버틸 수 있을까?';
const ogDescription = '자산, 생활비, 수익률, 국민연금으로 나의 FIRE 시점을 계산해보세요.';

html = html
  .replaceAll('서버 저장 없음 · 카톡 공유 최적화 · 3분 계산', '개인정보 저장 없음 · 무료 계산 · 바로 결과 확인')
  .replaceAll(/og-image\.png\?v=[^\"']+/g, 'og-image.png?v=firemap-home-v4-20260609');

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
    <radialGradient id="sun" cx="82%" cy="16%" r="38%"><stop offset="0" stop-color="#fed7aa"/><stop offset="1" stop-color="#fffdf9" stop-opacity="0"/></radialGradient>
  </defs>
  <rect width="1200" height="630" fill="#fffdf9"/>
  <rect x="34" y="30" width="1132" height="570" rx="54" fill="#ffffff" stroke="#fed7aa" stroke-width="4"/>
  <rect x="34" y="30" width="1132" height="570" rx="54" fill="url(#sun)"/>
  <circle cx="158" cy="128" r="54" fill="#fff1e7"/>
  <text x="128" y="150" font-family="Arial, sans-serif" font-size="62" font-weight="900">🔥</text>
  <text x="240" y="150" fill="#111827" font-family="Arial, sans-serif" font-size="58" font-weight="900">파이어맵</text>
  <text x="106" y="318" fill="#ea580c" font-family="Arial, sans-serif" font-size="42" font-weight="900">퇴사나이 계산기</text>
  <text x="106" y="418" fill="#111827" font-family="Arial, sans-serif" font-size="84" font-weight="900">내 돈은 몇 살까지</text>
  <text x="106" y="512" fill="#111827" font-family="Arial, sans-serif" font-size="84" font-weight="900">버틸 수 있을까?</text>
  <text x="106" y="570" fill="#6b7280" font-family="Arial, sans-serif" font-size="30" font-weight="800">자산 · 생활비 · 수익률 · 국민연금으로 계산</text>
</svg>`;

await writeFile(join(deploy, 'og-image.svg'), ogImage, 'utf8');
await sharp(Buffer.from(ogImage)).png().toFile(join(deploy, 'og-image.png'));
