import { chromium } from '@playwright/test';
const out = 'work/research/design/tokens-ref/salary-v5/impl/';
const b = await chromium.launch();
for (const [name, w, h, dark] of [['impl-375', 375, 812, false], ['impl-320', 320, 568, false], ['impl-1280', 1280, 800, false], ['impl-375-dark', 375, 812, true]]) {
  const p = await b.newPage({ viewport: { width: w, height: h } });
  if (dark) await p.addInitScript(() => { document.documentElement.setAttribute('data-theme', 'dark'); });
  await p.goto('http://127.0.0.1:4199/calc/salary'); await p.waitForSelector('.ds-cond'); await p.waitForTimeout(600);
  if (dark) await p.evaluate(() => document.documentElement.setAttribute('data-theme', 'dark'));
  await p.screenshot({ path: out + name + '.png' });
  const m = await p.evaluate(() => { const btn = [...document.querySelectorAll('button')].find((x) => x.textContent.includes('몇 살에 은퇴')); const r = btn.getBoundingClientRect(); return { over: document.documentElement.scrollWidth - innerWidth, btnBottom: Math.round(r.bottom), rowH: [...document.querySelectorAll('.ds-cond .ds-row-item')].map((e) => Math.round(e.getBoundingClientRect().height)), colW: Math.round(document.querySelector('.ds-salary-v5').getBoundingClientRect().width) }; });
  console.log(name, JSON.stringify(m));
  await p.close();
}
await b.close();
