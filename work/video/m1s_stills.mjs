// M1S 쇼츠 장면마다 스틸 몇 장(한 번 번들): node m1s_stills.mjs out/m1s_stills m1s_need100.json [m1s_minmonth.json …]   (장면마다 0.05·0.5·0.95)
import {bundle} from '@remotion/bundler';
import {selectComposition, renderStill} from '@remotion/renderer';
import fs from 'fs'; import path from 'path';
const [outDir, ...files] = process.argv.slice(2);
fs.mkdirSync(outDir, {recursive: true});
const serveUrl = await bundle({entryPoint: path.resolve('src/m1s_index.ts')});
for (const pf of files) {
  const props = JSON.parse(fs.readFileSync(pf, 'utf-8'));
  const comp = await selectComposition({serveUrl, id: 'M1S', inputProps: props});
  let from = 0;
  for (const [si, s] of props.scenes.entries()) {
    for (const r of [0.05, 0.5, 0.95]) {
      const fr = from + Math.floor((s.frames - 1) * r);
      await renderStill({composition: comp, serveUrl, output: path.join(outDir, `${props.name}_${si}_${Math.round(r * 100)}.png`), frame: fr, inputProps: props, imageFormat: 'png', scale: 0.5});
    }
    from += s.frames;
  }
  console.log('stills', props.name);
}
