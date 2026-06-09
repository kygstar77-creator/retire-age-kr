// 환율 등 시장 데이터 주기 갱신 스크립트.
// cron 또는 GitHub Actions에서 실행: node work/refresh-data.mjs
// 공개 무키 API(open.er-api.com) 사용. 실패해도 기존 marketData.json 유지(앱 영향 없음).
import { readFile, writeFile } from 'node:fs/promises';

const TARGET = new URL('../src/firemap-v2/marketData.json', import.meta.url);

async function main() {
  const current = JSON.parse(await readFile(TARGET, 'utf8'));
  try {
    const res = await fetch('https://open.er-api.com/v6/latest/USD');
    const j = await res.json();
    const krwPerUsd = j?.rates?.KRW;
    if (!krwPerUsd) throw new Error('no KRW rate');
    const per = (cur) => j.rates[cur] ? krwPerUsd / j.rates[cur] : null;
    const fx = {
      USD: Math.round(krwPerUsd),
      THB: round2(per('THB')),
      VND: round4(per('VND')),
      MYR: Math.round(per('MYR'))
    };
    const next = { ...current, asOf: new Date().toISOString().slice(0, 7), source: 'open.er-api.com (auto)', fxToKrw: { ...current.fxToKrw, ...clean(fx) } };
    await writeFile(TARGET, JSON.stringify(next, null, 2) + '\n');
    console.log('marketData.json updated:', next.fxToKrw);
  } catch (e) {
    console.warn('refresh skipped (keeping existing):', e.message);
  }
}
const clean = (o) => Object.fromEntries(Object.entries(o).filter(([, v]) => typeof v === 'number' && v > 0));
const round2 = (v) => v ? Math.round(v * 100) / 100 : null;
const round4 = (v) => v ? Math.round(v * 10000) / 10000 : null;
main();
