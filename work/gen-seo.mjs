// sitemap.xml · robots.txt 생성 — outputs/deploy의 html을 훑는다.
// URL은 확장자 없이 적는다: Cloudflare Pages가 /x.html → /x 로 308 하므로 .html 주소는 전부 리다이렉트 주소였다(2026-09-14 확인).
// lastmod는 git의 마지막 커밋 날짜(원본 파일 기준). 매 빌드 오늘 날짜를 찍으면 검색엔진이 lastmod를 안 믿는다.
// noindex 페이지는 사이트맵에서 뺀다.
import { readdirSync, statSync, writeFileSync, readFileSync, existsSync } from 'fs';
import { execSync } from 'child_process';
import { join, relative } from 'path';
import { TOOL_PAGES } from '../src/firemap-v2/toolPages.js';

const ROOT = 'outputs/deploy';
const BASE = 'https://firemap.kr';
const SKIP = new Set(['404.html', '200.html']);
const urls = [];

// 생성 파일의 원본: 파이어 백과 본문은 public/guide, 나머지는 생성 스크립트 자체의 날짜를 쓴다.
function sourceOf(rel) {
  if (rel === 'index.html') return 'index.html';
  if (rel === '__tool__') return 'src/firemap-v2/toolPages.js';
  if (/^guide\/[^/]+\.html$/.test(rel) && existsSync(join('public', rel))) return join('public', rel);
  if (rel.startsWith('guide/regions/')) return 'work/gen-guides.mjs';
  if (rel.startsWith('guide/region-plan/')) return 'work/gen-region-plans.mjs';
  if (rel.startsWith('guide/plan/')) return 'work/gen-combos.mjs';
  if (rel.startsWith('fire-city/')) return 'work/gen-city-fire.mjs';
  if (existsSync(join('public', rel))) return join('public', rel);
  return null;
}
const dateCache = new Map();
function lastmodOf(rel) {
  const src = sourceOf(rel);
  if (!src) return today;
  if (!dateCache.has(src)) {
    let d = today;
    try { d = execSync(`git log -1 --format=%cs -- "${src}"`, { encoding: 'utf8' }).trim() || today; } catch { /* git 없으면 오늘 */ }
    dateCache.set(src, d);
  }
  return dateCache.get(src);
}
const today = new Date().toISOString().slice(0, 10);

function walk(dir) {
  for (const e of readdirSync(dir)) {
    const p = join(dir, e);
    const st = statSync(p);
    if (st.isDirectory()) { if (e === 'assets') continue; walk(p); }
    else if (e.endsWith('.html') && !SKIP.has(e)) {
      const html = readFileSync(p, 'utf8');
      if (/<meta\s+name="robots"\s+content="[^"]*noindex/i.test(html)) continue;
      const rel = relative(ROOT, p).split('\\').join('/');
      const url = rel.endsWith('index.html') ? rel.slice(0, -'index.html'.length) : rel.replace(/\.html$/, '');
      urls.push({ loc: `${BASE}/${url}`, lastmod: lastmodOf(rel) });
    }
  }
}
walk(ROOT);
// 도구 화면의 검색용 경로 — 파일이 아니라 functions/_middleware.js가 만든다.
for (const t of TOOL_PAGES) urls.push({ loc: `${BASE}${t.path}`, lastmod: lastmodOf('__tool__') });

const seen = new Set();
const clean = urls.filter((u) => (seen.has(u.loc) ? false : seen.add(u.loc))).sort((a, b) => a.loc.localeCompare(b.loc));
const TOOL_LOCS = new Set(TOOL_PAGES.map((t) => `${BASE}${t.path}`));
const pr = (u) => (u === `${BASE}/` ? '1.0' : TOOL_LOCS.has(u) ? '0.9' : u.endsWith('/guide/') ? '0.8' : u.includes('/guide/') ? '0.7' : '0.4');
const body = clean.map((u) => `  <url><loc>${u.loc}</loc><lastmod>${u.lastmod}</lastmod><changefreq>weekly</changefreq><priority>${pr(u.loc)}</priority></url>`).join('\n');
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`;
writeFileSync(join(ROOT, 'sitemap.xml'), sitemap);

const robots = `User-agent: *\nAllow: /\n\nUser-agent: Yeti\nAllow: /\n\nUser-agent: Googlebot\nAllow: /\n\nSitemap: ${BASE}/sitemap.xml\n`;
writeFileSync(join(ROOT, 'robots.txt'), robots);
console.log(`[gen-seo] sitemap ${clean.length} urls (확장자 없는 주소 · git lastmod · noindex 제외) + robots.txt`);
