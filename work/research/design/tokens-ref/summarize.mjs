// dembrandt JSON 요약 — 색(빈도순)·글자 크기·모서리·간격·그림자를 한 화면에 뽑는다.
// 사용: node work/research/design/tokens-ref/summarize.mjs <dembrandt json>
import fs from 'node:fs';
const j = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = (k, v) => console.log(`## ${k}\n${typeof v === 'string' ? v : JSON.stringify(v, null, 0).slice(0, 2500)}\n`);
out('keys', Object.keys(j));
for (const k of Object.keys(j)) {
  if (['url', 'extractedAt', 'meta'].includes(k)) continue;
  out(k, j[k]);
}
