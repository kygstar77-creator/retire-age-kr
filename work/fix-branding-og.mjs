import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import sharp from 'sharp';

const deploy = join(process.cwd(), 'outputs', 'deploy');
const indexPath = join(deploy, 'index.html');
let html = await readFile(indexPath, 'utf8');

const siteUrl = 'https://retire-age-kr.pages.dev/';
const ogImageUrl = 'https://retire-age-kr.pages.dev/og-image.png';
const ogTitle = '파이어맵 - 내 돈은 몇 살까지 버틸까?';
const ogDescription = '자산, 생활비, 수익률, 국민연금 조건을 바꿔 퇴사 후 자산수명을 계산해보세요.';

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
  <rect width="1200" height="630" fill="#111827"/>
  <rect x="70" y="70" width="1060" height="490" rx="42" fill="#fff7ed"/>
  <text x="118" y="168" fill="#ea580c" font-family="Arial, sans-serif" font-size="44" font-weight="800">파이어맵</text>
  <text x="118" y="276" fill="#17212c" font-family="Arial, sans-serif" font-size="72" font-weight="900">내 돈은 몇 살까지</text>
  <text x="118" y="362" fill="#17212c" font-family="Arial, sans-serif" font-size="72" font-weight="900">버틸 수 있을까?</text>
  <text x="118" y="452" fill="#53616c" font-family="Arial, sans-serif" font-size="32" font-weight="700">생활비 · 수익률 · 국민연금 조건 비교</text>
  <rect x="805" y="136" width="230" height="220" rx="32" fill="#fed7aa"/>
  <text x="920" y="204" text-anchor="middle" fill="#9a3412" font-family="Arial, sans-serif" font-size="28" font-weight="800">FIRE</text>
  <text x="920" y="288" text-anchor="middle" fill="#9a3412" font-family="Arial, sans-serif" font-size="86" font-weight="900">V3</text>
  <text x="920" y="334" text-anchor="middle" fill="#9a3412" font-family="Arial, sans-serif" font-size="30" font-weight="800">계산기</text>
</svg>`;

await writeFile(join(deploy, 'og-image.svg'), ogImage, 'utf8');
await sharp(Buffer.from(ogImage)).png().toFile(join(deploy, 'og-image.png'));
