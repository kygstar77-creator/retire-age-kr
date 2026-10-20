// work/capcheck.py가 esbuild로 묶어 node로 돌린다 — 화면 자막과 같은 capChunks(parts/capchunks.ts)로 대본을 쪼개 조사·의존명사로 시작하는 조각(A50)을 센다.
import {capChunksCore, badStart} from '../src/parts/capchunks';
import * as fs from 'fs';
const [target, limit] = [10, 14]; // parts/safeframe.tsx DS.capTarget·capLimit과 같은 값
let bad = 0, n = 0;
for (const f of process.argv.slice(2)) {
  for (const raw of fs.readFileSync(f, 'utf8').split(/\r?\n/)) {
    const l = raw.replace(/^\s*\[[^\]]*\]\s*/, '').trim(); if (!l || l.startsWith('#')) continue;
    const cs = capChunksCore(l, target, limit); n += cs.length;
    const hit = cs.filter((c, i) => i > 0 && badStart(cs[i - 1].split(' ').pop()!, c.split(' ')[0]));
    bad += hit.length;
    if (process.env.CAP_LIST || hit.length) console.log((hit.length ? '!! ' : '   ') + cs.join(' / '));
  }
}
console.log(JSON.stringify({chunks: n, bad}));
process.exit(bad ? 1 : 0);
