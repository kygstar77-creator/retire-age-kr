// 겹침 검사(2026-10-11 motion, U5): node ovcheck.mjs <컴포지션 ID 예 M1> <props.json> <결과.json> [재는 간격 초=0.5] [첫프레임-끝프레임]
// 편 컴포지션 옆에 OverlapProbe를 붙인 임시 입구(src/_ovprobe.tsx)를 만들어, 간격마다 한 프레임씩 작게(scale 0.25) 렌더하며
// 숫자 글자가 다른 것에 가려진 곳을 모은다. 결과 json: {id, every, checked_frames, hits:[{t, f, num, by, how, x, y, w, h}]}
// lfrender.py가 부른다(렌더 전 관문). 직접 부를 때도 같다.
import {bundle} from '@remotion/bundler';
import {selectComposition, renderFrames} from '@remotion/renderer';
import fs from 'fs'; import path from 'path'; import os from 'os';
const [id, propsFile, outFile, everyArg, rangeArg] = process.argv.slice(2);
if (!id || !propsFile || !outFile) { console.log('node ovcheck.mjs <ID> <props.json> <out.json> [초=0.5] [a-b]'); process.exit(2); }
const props = JSON.parse(fs.readFileSync(propsFile, 'utf-8'));
const fps = props.fps || 30;
const every = Math.max(1, Math.round(parseFloat(everyArg || '0.5') * fps));
const low = id.toLowerCase();
const entry = path.resolve('src/_ovprobe.tsx');
fs.writeFileSync(entry, `// ovcheck.mjs가 매번 새로 쓰는 임시 입구 — 고치지 않는다
import React from 'react';
import {registerRoot, Composition} from 'remotion';
import {${id}, ${low}Frames} from './${id}';
import {OverlapProbe} from './motion/OverlapProbe';
import p from '../${path.basename(propsFile)}';
const C = ${id} as unknown as React.FC<Record<string, unknown>>;
const W: React.FC<Record<string, unknown>> = (q) => <><C {...q} /><OverlapProbe every={${every}} /></>;
registerRoot(() => <Composition id="OV" component={W} durationInFrames={${low}Frames(p as never)} fps={${fps}}
  width={1920} height={1080} defaultProps={p as unknown as Record<string, unknown>}
  calculateMetadata={({props: pp}) => ({durationInFrames: ${low}Frames(pp as never)})} />);
`);
const serveUrl = await bundle({entryPoint: entry});
const comp = await selectComposition({serveUrl, id: 'OV', inputProps: props});
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'ovp-'));
const logs = [];
let frameRange = null;
if (rangeArg) { const [a, b] = rangeArg.split('-').map(Number); frameRange = [Math.ceil(a / every) * every, Math.min(b, comp.durationInFrames - 1)]; }   // 탐침은 every의 배수 프레임에서만 잰다
try {
  await renderFrames({
    composition: comp, serveUrl, inputProps: props, outputDir: tmp, imageFormat: 'jpeg', jpegQuality: 30, scale: 0.25,
    everyNthFrame: every, frameRange, timeoutInMilliseconds: 120000, concurrency: 2,   // 10/19 PD: PC가 바쁠 때 실사 영상 한 프레임 꺼내기가 28초를 넘어 H-2 겹침 검사가 죽음 — 기다림을 2분으로
    onStart: () => {}, onFrameUpdate: () => {},
    onBrowserLog: (l) => { if (l.text.startsWith('OVPROBE ')) logs.push(JSON.parse(l.text.slice(8))); },
  });
} finally {
  // 번들은 public(오디오 수 GB)을 Temp에 통째로 복사한다 — 10/11 12:0x 번들 43개가 C: 476G를 꽉 채웠다. 쓰고 바로 지운다.
  fs.rmSync(tmp, {recursive: true, force: true}); fs.rmSync(serveUrl, {recursive: true, force: true});
}
const hits = [];
for (const l of logs.sort((a, b) => a.f - b.f)) for (const h of (l.hits || [])) hits.push({t: +(l.f / fps).toFixed(2), f: l.f, ...h});
const errs = logs.filter((l) => l.err);
const res = {id, props: path.basename(propsFile), every_frames: every, checked_frames: logs.length, errors: errs.length, hits};
fs.writeFileSync(outFile, JSON.stringify(res, null, 1));
console.log(`겹침 검사 ${id}: 잰 프레임 ${logs.length} · 겹침 ${hits.length}건${errs.length ? ` · 탐침 오류 ${errs.length}` : ''}`);
