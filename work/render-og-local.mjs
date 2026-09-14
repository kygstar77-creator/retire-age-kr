// 로컬에서 /og 인증 카드를 resvg-wasm으로 그려 PNG로 저장 — 폰트 서브셋(functions/og-fonts-pd.js)이 resvg에서 읽히는지,
// 카드 글자가 빠짐없이 보이는지 배포 전에 확인한다. 실행: node work/render-og-local.mjs [출력경로]
import { readFileSync, writeFileSync } from 'node:fs';
import { initWasm, Resvg } from '@resvg/resvg-wasm';
import { PD_BOLD_B64, PD_REGULAR_B64 } from '../functions/og-fonts-pd.js';
import { buildCertWideSvg, seriesFromRows } from '../functions/og-card.js';
import { buildSimulation } from '../src/utils/retirementSimulator.js';

const out = process.argv[2] || 'outputs/og-cert-local.png';
const b64 = (s) => Uint8Array.from(Buffer.from(s, 'base64'));
const bold = b64(PD_BOLD_B64);
const magic = Buffer.from(bold.slice(0, 4)).toString('hex');
console.log('font magic', magic, magic === '00010000' ? '(TTF)' : '(TTF 아님!)');
await initWasm(readFileSync('node_modules/@resvg/resvg-wasm/index_bg.wasm'));
const sim = buildSimulation({ currentAge: 35, targetRetirementAge: 55, financialAsset: 100000000, monthlyInvestment: 3000000, monthlyLivingCost: 3000000, annualReturnRate: 5, inflationRate: 3, expectedPensionAge: 65, expectedMonthlyPension: 1000000 });
const series = seriesFromRows(sim.displayResult.rows, sim.displayResult.retirementAge);
const svg = buildCertWideSvg({ year: 1991, ea: sim.earliestRetirementAge, target: 55, need: '14.1억', asset: '1억', save: '300만', cost: '300만', ret: '5', inf: '3', pen: '65', round: 1, series, font: 'Pretendard' });
const r = new Resvg(svg, { fitTo: { mode: 'width', value: 1200 }, font: { fontBuffers: [bold, b64(PD_REGULAR_B64)], defaultFontFamily: 'Pretendard', loadSystemFonts: false } });
writeFileSync(out, r.render().asPng());
console.log('wrote', out);
