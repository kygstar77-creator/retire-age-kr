import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { join } from 'node:path';
import { build } from 'vite';
import { spawnSync } from 'node:child_process';

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

// 자동 가이드 AI 티 관문(2026-10-01). '[auto] guide'는 클라우드 루틴이 main에 바로 커밋 → Cloudflare Pages가 이 빌드를 돈다.
// 관문 건 뒤 새로 생긴·바뀐 public/guide/*.html 중 기준을 넘고 편집 통과 표시가 없는 것은 배포 폴더에서 뺀다
// (아래 사이트맵·링크 치환보다 먼저라 사이트맵에도 안 들어감). 파이썬이 없으면 경고만 하고 넘어간다.
{
  const tries = process.platform === 'win32' ? [['py', ['-3.12']], ['python', []]] : [['python3', []], ['python', []]];
  let ran = false;
  for (const [cmd, pre] of tries) {
    const r = spawnSync(cmd, [...pre, 'work/guidegate.py', 'ci', '@base', 'HEAD', '--drop', 'outputs/deploy'],
      { cwd: root, stdio: 'inherit', env: { ...process.env, PYTHONIOENCODING: 'utf-8' } });
    if (r.error) continue;
    ran = true;
    if (r.status !== 0) { console.error(`guidegate 관문 오류(종료코드 ${r.status}) — 빌드를 멈춘다`); process.exit(1); }
    break;
  }
  if (!ran) console.warn('경고: 파이썬이 없어 guidegate 관문을 못 돌렸다 — 자동 가이드 AI 티 검사 안 됨');
}

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

User-agent: Yeti
Allow: /

User-agent: Googlebot
Allow: /

Sitemap: https://firemap.kr/sitemap.xml
`;

const adsTxt = `google.com, pub-${adsensePublisherId}, DIRECT, f08c47fec0942fa
`;

const { readdir } = await import('node:fs/promises');
const guideFiles = (await readdir(join(root, 'public', 'guide'))).filter((f) => f.endsWith('.html'));
const site = 'https://firemap.kr';
const urlEntries = [
  { loc: `${site}/`, freq: 'weekly', pri: '1.0' },
  { loc: `${site}/guide/`, freq: 'weekly', pri: '0.8' },
  ...guideFiles.filter((f) => f !== 'index.html').sort().map((f) => ({ loc: `${site}/guide/${f}`, freq: 'weekly', pri: '0.7' })),
  { loc: `${site}/privacy.html`, freq: 'monthly', pri: '0.4' },
  { loc: `${site}/disclaimer.html`, freq: 'monthly', pri: '0.4' },
  { loc: `${site}/contact.html`, freq: 'monthly', pri: '0.4' }
];
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urlEntries.map((u) => `  <url><loc>${u.loc}</loc><lastmod>${today}</lastmod><changefreq>${u.freq}</changefreq><priority>${u.pri}</priority></url>`).join('\n')}\n</urlset>\n`;

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
