// 정한 프레임만 jpg로: node stills_at.mjs DETF1 detf1.json frames.json outDir [scale]  (frames.json = [[이름, 프레임], ...]) — visual 10/27
import {bundle} from '@remotion/bundler';
import {selectComposition, renderStill} from '@remotion/renderer';
import fs from 'fs'; import path from 'path';
const [id, propsFile, framesFile, outDir, sc] = process.argv.slice(2);
const props = JSON.parse(fs.readFileSync(propsFile, 'utf-8')); fs.mkdirSync(outDir, {recursive: true});
const list = JSON.parse(fs.readFileSync(framesFile, 'utf-8'));
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const comp = await selectComposition({serveUrl, id, inputProps: props});
for (const [name, frame] of list) await renderStill({composition: comp, serveUrl, output: path.join(outDir, name + '.jpg'), frame, inputProps: props, imageFormat: 'jpeg', jpegQuality: 82, scale: +(sc || 0.5)});
console.log('stills', list.length);
