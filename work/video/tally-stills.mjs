// 장면마다 대표 프레임 한 장(움직임이 끝난 뒤, 장면의 AT 비율 지점) — node tally-stills.mjs <id> <props.json> <outDir> [entry] [scale]
//   node tally-stills.mjs R1 r1.json ../research/longform/ep/R-1/preview/stills src/motion/TallyRoot.tsx 1
// 크롬 경로: 환경변수 BROWSER(예: /opt/pw-browsers/chromium-1194/chrome-linux/chrome). 장면별 비율은 STILL_AT(기본 0.93).
import {bundle} from '@remotion/bundler';
import {selectComposition, renderStill} from '@remotion/renderer';
import fs from 'fs'; import path from 'path';
const [id, propsFile, outDir, entry = 'src/motion/TallyRoot.tsx', scale = '1'] = process.argv.slice(2);
const props = JSON.parse(fs.readFileSync(propsFile, 'utf-8'));
fs.mkdirSync(outDir, {recursive: true});
const browserExecutable = process.env.BROWSER || null;
const serveUrl = await bundle({entryPoint: path.resolve(entry)});
const comp = await selectComposition({serveUrl, id, inputProps: props, browserExecutable});
const at = process.env.STILL_AT ? Number(process.env.STILL_AT) : null;   // 없으면 장면 끝 3프레임 전(모든 움직임이 끝난 뒤)
const only = (process.env.ONLY || '').split(',').filter(Boolean);
let from = 0;
for (const [i, s] of props.scenes.entries()) {
  const name = `${String(i).padStart(2, '0')}_${s.key}`;
  const frame = from + Math.max(0, Math.min(s.frames - 1, at == null ? s.frames - 3 : Math.floor(s.frames * at)));
  from += s.frames;
  if (only.length && !only.includes(s.key)) continue;
  await renderStill({composition: comp, serveUrl, output: path.join(outDir, name + '.png'), frame, inputProps: props, imageFormat: 'png', scale: Number(scale), browserExecutable});
  console.log('still', name, frame);
}
