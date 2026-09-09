// CSS 사용 검사 — src/**/*.jsx 에서 실제로 쓰는 클래스와 각 CSS 파일이 정의하는 클래스를 대조한다.
// node work/css-usage.mjs            → 파일별 정의/사용/미사용 개수 + 사용 중인 fm-* 클래스 목록
// node work/css-usage.mjs --unused   → 각 CSS 파일에서 한 번도 안 쓰는 클래스 목록
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const ROOT = process.cwd();
const walk = (dir, out = []) => { for (const f of readdirSync(dir)) { const p = join(dir, f); if (statSync(p).isDirectory()) walk(p, out); else out.push(p); } return out; };
const src = walk(join(ROOT, 'src')).filter((p) => /\.(jsx|js)$/.test(p));
const used = new Set();
for (const p of src) {
  const t = readFileSync(p, 'utf8');
  for (const m of t.matchAll(/className=\{?["'`]([^"'`]+)["'`]/g)) m[1].split(/\s+/).forEach((c) => used.add(c.replace(/\$\{.*\}/g, '')));
  for (const m of t.matchAll(/['"`]((?:fm|ds|sc)-[a-z0-9_-]+)['"`]/g)) used.add(m[1]);
  for (const m of t.matchAll(/(?:fm|ds|sc)-[a-z0-9_-]+/g)) used.add(m[0]);
}
const cssFiles = walk(join(ROOT, 'src')).filter((p) => p.endsWith('.css'));
const unusedMode = process.argv.includes('--unused');
let usedFm = new Set();
for (const p of cssFiles) {
  const t = readFileSync(p, 'utf8');
  const defined = new Set([...t.matchAll(/\.((?:fm|ds|sc)-[a-zA-Z0-9_-]+)/g)].map((m) => m[1]));
  const un = [...defined].filter((c) => !used.has(c));
  const imp = t.match(/!important/g) || [];
  console.log(`${p.replace(ROOT, '')}: defined ${defined.size} · unused ${un.length} · !important ${imp.length}`);
  if (unusedMode && un.length) console.log('   unused:', un.join(' '));
  [...defined].filter((c) => used.has(c) && c.startsWith('fm-')).forEach((c) => usedFm.add(c));
}
console.log('\nfm-* classes still used by JSX:', usedFm.size);
console.log([...usedFm].sort().join(' '));
