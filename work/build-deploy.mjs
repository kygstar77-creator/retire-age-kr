import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { build } from 'vite';

const root = process.cwd();
const deploy = join(root, 'outputs', 'deploy');
const adsensePublisherId = '3225798545626010';
const adsenseClientId = `ca-pub-${adsensePublisherId}`;

await build({
  root,
  build: {
    outDir: deploy,
    emptyOutDir: true
  }
});

await mkdir(deploy, { recursive: true });

const adsenseHeadScript = `<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${adsenseClientId}"
     crossorigin="anonymous"></script>`;

try {
  const indexPath = join(deploy, 'index.html');
  let indexHtml = await readFile(indexPath, 'utf8');
  if (!indexHtml.includes('pagead2.googlesyndication.com')) {
    indexHtml = indexHtml.replace('</head>', `${adsenseHeadScript}\n</head>`);
  }
  await writeFile(indexPath, indexHtml, 'utf8');
} catch {
  // Keep the build successful even if post-processing is unavailable.
}

const today = new Date().toISOString().slice(0, 10);

const robots = `User-agent: *
Allow: /

Sitemap: https://retire-age-kr.pages.dev/sitemap.xml
`;

const adsTxt = `google.com, pub-${adsensePublisherId}, DIRECT, f08c47fec0942fa
`;

const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://retire-age-kr.pages.dev/</loc>
    <lastmod>${today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://retire-age-kr.pages.dev/privacy.html</loc>
    <lastmod>${today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
  <url>
    <loc>https://retire-age-kr.pages.dev/disclaimer.html</loc>
    <lastmod>${today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
  <url>
    <loc>https://retire-age-kr.pages.dev/contact.html</loc>
    <lastmod>${today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
</urlset>
`;

const headers = `/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
`;

await writeFile(join(deploy, 'robots.txt'), robots, 'utf8');
await writeFile(join(deploy, 'ads.txt'), adsTxt, 'utf8');
await writeFile(join(deploy, 'sitemap.xml'), sitemap, 'utf8');
await writeFile(join(deploy, '_headers'), headers, 'utf8');
