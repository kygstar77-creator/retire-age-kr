// 측정 가드(10/5 [지시] X-CP-1·X-HOME-1): coupang_view·home_leave·실험군 ab가 빠지면 빌드를 멈춘다.
import { readFileSync } from 'node:fs';
import { randomUUID } from 'node:crypto';

const read = (p) => readFileSync(new URL(`../${p}`, import.meta.url), 'utf8');
const fail = (m) => { console.error(`test-events 실패: ${m}`); process.exit(1); };

const live = read('src/utils/live.js');
const pick = read('src/components/firemap/CoupangPick.jsx');
const app = read('src/components/FireMapMVP.jsx');

if (!/logEvent\('coupang_view'/.test(pick) || !/IntersectionObserver/.test(pick) || !/0\.5/.test(pick) || !/1000\)/.test(pick)) fail('CoupangPick에 coupang_view(50%·1초) 없음');
if (!/logEvent\('home_leave'/.test(app) || !/started:/.test(app)) fail('FireMapMVP에 home_leave(sec·started) 없음');
if (!/extra\.ab = ab/.test(live) || !/keepalive: true/.test(live)) fail('logEvent에 ab·keepalive 없음');

// abArm 본문만 떼어 실행해 반반인지·같은 id면 같은 군인지 본다.
const m = live.match(/export function abArm\(cid\) \{[\s\S]*?\n\}/);
if (!m) fail('abArm 없음');
const abArm = new Function(`${m[0].replace('export ', '')}; return abArm;`)();
let a = 0; const N = 20000;
for (let i = 0; i < N; i += 1) { const id = randomUUID(); const g = abArm(id); if (g !== abArm(id)) fail('같은 id가 다른 군'); if (g === 'a') a += 1; }
const share = a / N;
if (share < 0.48 || share > 0.52) fail(`a군 비율 ${share.toFixed(3)} — 반반 아님`);
if (abArm('') !== null) fail('빈 id에 군 배정');
console.log(`test-events 통과: a군 ${(share * 100).toFixed(1)}% (${N}개)`);
