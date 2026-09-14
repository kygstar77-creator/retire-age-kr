// 빌드 산출물의 canonical·og:url·내부 링크에서 .html을 뗀다.
// Cloudflare Pages는 /guide/x.html 을 /guide/x 로 308 리다이렉트한다. 그런데 백과 486쪽의 canonical과
// 내부 링크가 전부 .html 주소라, 검색엔진이 보기엔 "정식 주소 = 리다이렉트 주소"였다(2026-09-14 확인).
// index.html은 디렉터리 주소(/guide/)로, 나머지는 확장자만 뗀다. 외부 링크는 손대지 않는다.
import { readdirSync, statSync, readFileSync, writeFileSync } from 'fs';
import { join } from 'path';

const ROOT = 'outputs/deploy';
const BASE = 'https://firemap.kr';
const strip = (u) => u.replace(/\/index\.html$/, '/').replace(/\.html$/, '');
// 같은 사이트 주소만: 절대(https://firemap.kr/...)와 루트 상대(/...)
const isOurs = (u) => u.startsWith(`${BASE}/`) || (u.startsWith('/') && !u.startsWith('//'));
const skipFile = (u) => /\/(404|200)\.html$/.test(u);

let files = 0; let edits = 0;
function walk(dir) {
  for (const e of readdirSync(dir)) {
    const p = join(dir, e);
    if (statSync(p).isDirectory()) { if (e !== 'assets') walk(p); continue; }
    if (!e.endsWith('.html')) continue;
    const before = readFileSync(p, 'utf8');
    let n = 0;
    const after = before
      .replace(/(<link\s+rel="canonical"\s+href=")([^"]+)(")/g, (m, a, u, b) => (isOurs(u) && !skipFile(u) ? (n += 1, a + strip(u) + b) : m))
      .replace(/(<meta\s+property="og:url"\s+content=")([^"]+)(")/g, (m, a, u, b) => (isOurs(u) && !skipFile(u) ? (n += 1, a + strip(u) + b) : m))
      .replace(/(href=")((?:https:\/\/firemap\.kr)?\/[^"#?]*\.html)((?:[?#][^"]*)?")/g, (m, a, u, b) => (skipFile(u) ? m : (n += 1, a + strip(u) + b)));
    if (n) { writeFileSync(p, after, 'utf8'); edits += n; }
    files += 1;
  }
}
walk(ROOT);
console.log(`[fix-seo-links] ${files}개 html 검사 · .html 주소 ${edits}곳을 확장자 없는 주소로`);
