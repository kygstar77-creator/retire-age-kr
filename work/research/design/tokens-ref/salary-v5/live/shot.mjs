import { chromium } from '@playwright/test';
const out = 'work/research/design/tokens-ref/salary-v5/live/';
const b = await chromium.launch();
for (const [name, w, h, dark] of [['live-375', 375, 812, false], ['live-320', 320, 568, false], ['live-1280', 1280, 800, false], ['live-375-dark', 375, 812, true]]) {
  const p = await b.newPage({ viewport: { width: w, height: h } });
  if (dark) await p.addInitScript(() => { document.documentElement.setAttribute('data-theme', 'dark'); });
  await p.goto('https://firemap.kr/calc/salary'); await p.waitForSelector('.ds-cond'); await p.waitForTimeout(600);
  if (dark) await p.evaluate(() => document.documentElement.setAttribute('data-theme', 'dark'));
  await p.screenshot({ path: out + name + '.png' });
  const m = await p.evaluate(() => { const btn = [...document.querySelectorAll('button')].find((x) => x.textContent.includes('몇 살에 은퇴')); const r = btn.getBoundingClientRect(); return { over: document.documentElement.scrollWidth - innerWidth, btnBottom: Math.round(r.bottom), rowH: [...document.querySelectorAll('.ds-cond .ds-row-item')].map((e) => Math.round(e.getBoundingClientRect().height)), colW: Math.round(document.querySelector('.ds-salary-v5').getBoundingClientRect().width) }; });
  console.log(name, JSON.stringify(m));
  await p.close();
}
await b.close();
