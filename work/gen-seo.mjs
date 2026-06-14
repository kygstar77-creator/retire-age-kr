import { readdirSync, statSync, writeFileSync } from 'fs';
import { join, relative } from 'path';

const ROOT = 'outputs/deploy';
const BASE = 'https://firemap.kr';
const SKIP = new Set(['404.html', '200.html']);
const urls = [];

function walk(dir) {
  for (const e of readdirSync(dir)) {
    const p = join(dir, e);
    const st = statSync(p);
    if (st.isDirectory()) { if (e === 'assets') continue; walk(p); }
    else if (e.endsWith('.html') && !SKIP.has(e)) {
      const rel = relative(ROOT, p).split('\\').join('/');
      const url = rel.endsWith('index.html') ? rel.slice(0, -'index.html'.length) : rel;
      urls.push(`${BASE}/${url}`);
    }
  }
}
walk(ROOT);

const clean = [...new Set(urls)].sort();
const today = new Date().toISOString().slice(0, 10);
const pr = (u) => (u === `${BASE}/` ? '1.0' : u.endsWith('/guide/') ? '0.8' : u.includes('/guide/') ? '0.7' : '0.4');
const body = clean.map((u) => `  <url><loc>${u}</loc><lastmod>${today}</lastmod><changefreq>weekly</changefreq><priority>${pr(u)}</priority></url>`).join('\n');
const sitemap = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${body}\n</urlset>\n`;
writeFileSync(join(ROOT, 'sitemap.xml'), sitemap);

const robots = `User-agent: *\nAllow: /\n\nUser-agent: Yeti\nAllow: /\n\nUser-agent: Googlebot\nAllow: /\n\nSitemap: ${BASE}/sitemap.xml\n`;
writeFileSync(join(ROOT, 'robots.txt'), robots);
console.log(`[gen-seo] sitemap ${clean.length} urls + robots.txt (Yeti/Googlebot allow)`);
