// 말 줄마다 끝 프레임(줄 끝 12프레임 전)을 한 번의 번들로 뽑는다: node stills_lines.mjs P1 p1.json out/p1_lines [장면번호,장면번호…]
// U5(줄마다 판이 바뀌는지)·겹침을 줄 단위로 눈 검사할 때. 실사 장 머리가 덮는 첫 줄은 그 위 프레임이 나온다.
import {bundle} from '@remotion/bundler';
import {selectComposition, renderStill} from '@remotion/renderer';
import fs from 'fs'; import path from 'path';
const [id, propsFile, outDir, only] = process.argv.slice(2);
const props = JSON.parse(fs.readFileSync(propsFile, 'utf-8'));
const pick = only ? only.split(',').map(Number) : null;
fs.mkdirSync(outDir, {recursive: true});
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const comp = await selectComposition({serveUrl, id, inputProps: props});
let from = 0; const frames = [];
props.scenes.forEach((s, i) => { let a = from; s.lines.forEach((l, j) => { a += l.frames; if (!pick || pick.includes(i)) frames.push([`${String(i).padStart(2, '0')}_${String(j).padStart(2, '0')}`, Math.min(from + s.frames - 1, a - 12)]); }); from += s.frames; });
for (const [name, frame] of frames) await renderStill({composition: comp, serveUrl, output: path.join(outDir, name + '.png'), frame, inputProps: props, imageFormat: 'png', scale: 0.5});
console.log('stills', frames.length);
