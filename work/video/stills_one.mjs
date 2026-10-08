// 한 장면의 프레임 몇 장만: node stills_one.mjs M1 m1.json out/dir 0 0.45,0.98  (장면 번호, 장면 안 비율)
import {bundle} from '@remotion/bundler';
import {selectComposition, renderStill} from '@remotion/renderer';
import fs from 'fs'; import path from 'path';
const [id, propsFile, outDir, si, rs] = process.argv.slice(2);
const props = JSON.parse(fs.readFileSync(propsFile, 'utf-8')); fs.mkdirSync(outDir, {recursive: true});
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const comp = await selectComposition({serveUrl, id, inputProps: props});
let from = 0; props.scenes.slice(0, +si).forEach((s) => from += s.frames); const s = props.scenes[+si];
for (const r of rs.split(',').map(Number)) await renderStill({composition: comp, serveUrl, output: path.join(outDir, `${si}_${Math.round(r * 100)}.png`), frame: from + Math.floor((s.frames - 1) * r), inputProps: props, imageFormat: 'png'});
console.log('stills', rs);
