// 대표 프레임 여러 장을 한 번의 번들로 뽑는다: node stills.mjs A1 a1.json out/a1_stills  (장마다 끝 20프레임 전 + 중간)
import {bundle} from '@remotion/bundler';
import {selectComposition, renderStill} from '@remotion/renderer';
import fs from 'fs'; import path from 'path';
const [id, propsFile, outDir] = process.argv.slice(2);
const props = JSON.parse(fs.readFileSync(propsFile, 'utf-8'));
fs.mkdirSync(outDir, {recursive: true});
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const comp = await selectComposition({serveUrl, id, inputProps: props});
let from = 0; const frames = [];
const extra = (process.env.STILL_AT || "").split(",").filter(Boolean).map(Number);
props.scenes.forEach((s, i) => { extra.forEach((r) => frames.push([`${String(i).padStart(2, "0")}_${Math.round(r * 100)}`, from + Math.floor(s.frames * r)])); frames.push([`${String(i).padStart(2, '0')}_mid`, from + Math.floor(s.frames * 0.45)]); frames.push([`${String(i).padStart(2, '0')}_end`, from + s.frames - 20]); from += s.frames; });
for (const [name, frame] of frames) {
  await renderStill({composition: comp, serveUrl, output: path.join(outDir, name + '.png'), frame, inputProps: props, imageFormat: 'png'});
}
console.log('stills', frames.length);
