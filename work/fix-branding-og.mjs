import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import sharp from 'sharp';

const deploy = join(process.cwd(), 'outputs', 'deploy');
const indexPath = join(deploy, 'index.html');
let html = await readFile(indexPath, 'utf8');

const siteUrl = 'https://retire-age-kr.pages.dev/';
const ogImageUrl = 'https://retire-age-kr.pages.dev/og-image.png';
const ogTitle = '퇴사나이 - 한국형 FIRE 계산기';
const ogDescription = '현재 자산, 생활비, 국민연금, 배당·세금까지 반영해 퇴사 가능 나이를 계산해보세요.';

html = html
  .replaceAll('서버 저장 없음 · 카톡 공유 최적화 · 3분 계산', '개인정보 저장 없음 · 무료 계산 · 바로 결과 확인')
  .replaceAll('og-image.png?v=4', 'og-image.png')
  .replaceAll('og-image.png?v=5', 'og-image.png')
  .replaceAll('og-image.png?v=6', 'og-image.png');

const metaBlock = `
<meta property="og:type" content="website" />
<meta property="og:site_name" content="퇴사나이" />
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
  <rect width="1200" height="630" fill="#17212c"/>
  <rect x="72" y="72" width="1056" height="486" rx="28" fill="#f8fafb"/>
  <text x="120" y="190" fill="#126044" font-family="Arial, sans-serif" font-size="44" font-weight="700">퇴사나이</text>
  <text x="120" y="288" fill="#17212c" font-family="Arial, sans-serif" font-size="66" font-weight="800">내 자산으로 몇 살에</text>
  <text x="120" y="370" fill="#17212c" font-family="Arial, sans-serif" font-size="66" font-weight="800">퇴사할 수 있을까?</text>
  <text x="120" y="462" fill="#53616c" font-family="Arial, sans-serif" font-size="32">한국형 조기은퇴·반퇴 시뮬레이터</text>
  <rect x="790" y="132" width="270" height="224" rx="24" fill="#dff3e9"/>
  <text x="925" y="198" text-anchor="middle" fill="#126044" font-family="Arial, sans-serif" font-size="28" font-weight="700">목표 퇴사</text>
  <text x="925" y="282" text-anchor="middle" fill="#126044" font-family="Arial, sans-serif" font-size="92" font-weight="800">39</text>
  <text x="925" y="329" text-anchor="middle" fill="#126044" font-family="Arial, sans-serif" font-size="34" font-weight="800">세</text>
</svg>`;

await writeFile(join(deploy, 'og-image.svg'), ogImage, 'utf8');
await sharp(Buffer.from(ogImage)).png().toFile(join(deploy, 'og-image.png'));
