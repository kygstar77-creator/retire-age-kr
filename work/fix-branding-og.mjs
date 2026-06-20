import { readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import sharp from 'sharp';
import { buildCardSvg } from '../functions/og-card.js';

const deploy = join(process.cwd(), 'outputs', 'deploy');
const indexPath = join(deploy, 'index.html');
let html = await readFile(indexPath, 'utf8');

const siteUrl = 'https://firemap.kr/';
const ogVersion = 'firemap-navy-v9-20260619';
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
<meta property="og:image:height" content="600" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="${ogTitle}" />
<meta name="twitter:description" content="${ogDescription}" />
<meta name="twitter:image" content="${ogImageUrl}" />`;

html = html.replace(/\s*<meta property="og:[^"]+" content="[^"]*" \/>/g, '');
html = html.replace(/\s*<meta name="twitter:[^"]+" content="[^"]*" \/>/g, '');
html = html.replace(/<title>.*?<\/title>/, `<title>${seoTitle}</title>\n${metaBlock}`);
html = html.replace(/<link rel="canonical" href="[^"]*" \/>/, `<link rel="canonical" href="${siteUrl}" />`);

await writeFile(indexPath, html, 'utf8');

const FONT = "Arial, 'Noto Sans CJK KR', 'Noto Sans KR', 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif";
const ogGeneric = buildCardSvg({ mode: 'generic', font: FONT });
const ogSave = buildCardSvg({ mode: 'save', font: FONT });

await writeFile(join(deploy, 'og-image.svg'), ogGeneric, 'utf8');
await sharp(Buffer.from(ogGeneric)).png().toFile(join(deploy, 'og-image.png'));
await sharp(Buffer.from(ogSave)).png().toFile(join(deploy, 'og-save.png'));
