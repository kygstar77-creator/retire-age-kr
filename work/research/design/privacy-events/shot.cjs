const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const url = 'file:///' + path.resolve('public/privacy.html').split(path.sep).join('/');
  for (const [w, n] of [[375, '375'], [1280, 'desktop']]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.goto(url);
    const box = await p.evaluate(() => { const t = document.querySelectorAll('table')[1]; const r = t.getBoundingClientRect(); return { y: r.top + scrollY - 70, h: r.height + 110, sw: document.documentElement.scrollWidth }; });
    console.log(n, JSON.stringify(box));
    await p.screenshot({ fullPage: true, path: `work/research/design/privacy-events/privacy-events-${n}.png`, clip: { x: 0, y: box.y, width: w, height: box.h } });
  }
  await b.close();
})();
