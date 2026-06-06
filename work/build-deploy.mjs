import { copyFile, mkdir, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

const root = process.cwd();
const outputs = join(root, 'outputs');
const deploy = join(outputs, 'deploy');

await import('./build-standalone.mjs');
await mkdir(deploy, { recursive: true });
await copyFile(join(outputs, 'toesanai-standalone.html'), join(deploy, 'index.html'));

const readme = `# 퇴사나이 배포본

이 폴더는 정적 호스팅에 바로 올릴 수 있는 배포용 파일입니다.

## 파일

- index.html

## 배포 방법

Netlify, Vercel, Cloudflare Pages, GitHub Pages 같은 정적 호스팅 서비스에 이 폴더의 내용을 업로드하면 됩니다.

이 버전은 서버, 로그인, DB 없이 브라우저 안에서 계산하고 localStorage에 입력값을 저장합니다.
`;

const robots = `User-agent: *
Allow: /

Sitemap: https://retire-age-kr.netlify.app/sitemap.xml
`;

const today = new Date().toISOString().slice(0, 10);
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://retire-age-kr.netlify.app/</loc>
    <lastmod>${today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
`;

const headers = `/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: no-referrer
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'
`;

const ogImage = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="#17212c"/>
  <rect x="72" y="72" width="1056" height="486" rx="28" fill="#f8fafb"/>
  <text x="120" y="190" fill="#126044" font-family="Arial, sans-serif" font-size="44" font-weight="700">퇴사나이</text>
  <text x="120" y="288" fill="#17212c" font-family="Arial, sans-serif" font-size="66" font-weight="800">내 자산으로 몇 살에</text>
  <text x="120" y="370" fill="#17212c" font-family="Arial, sans-serif" font-size="66" font-weight="800">퇴사할 수 있을까?</text>
  <text x="120" y="462" fill="#53616c" font-family="Arial, sans-serif" font-size="32">한국형 조기은퇴·반퇴 시뮬레이터</text>
  <rect x="818" y="136" width="210" height="210" rx="18" fill="#dff3e9"/>
  <text x="854" y="266" fill="#126044" font-family="Arial, sans-serif" font-size="92" font-weight="800">39</text>
  <text x="940" y="266" fill="#126044" font-family="Arial, sans-serif" font-size="42" font-weight="700">세</text>
</svg>`;

await writeFile(join(deploy, 'README.md'), readme, 'utf8');
await writeFile(join(deploy, 'robots.txt'), robots, 'utf8');
await writeFile(join(deploy, 'sitemap.xml'), sitemap, 'utf8');
await writeFile(join(deploy, '_headers'), headers, 'utf8');
await writeFile(join(deploy, 'og-image.svg'), ogImage, 'utf8');
try {
  const sharpPath = 'C:/Users/강영준/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/.pnpm/sharp@0.34.5/node_modules/sharp/lib/index.js';
  const sharpModule = await import(pathToFileURL(sharpPath).href);
  const sharp = sharpModule.default;
  await sharp(Buffer.from(ogImage)).png().toFile(join(deploy, 'og-image.png'));
} catch {
  // Netlify builds can use the SVG directly when the local PNG renderer is unavailable.
}
