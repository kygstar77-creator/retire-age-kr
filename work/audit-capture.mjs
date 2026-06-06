import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';

const url = 'http://127.0.0.1:4173/';
await mkdir('audit-output', { recursive: true });

const browser = await chromium.launch();

const mobile = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
await mobile.goto(url, { waitUntil: 'networkidle' });
await mobile.screenshot({ path: 'audit-output/mobile-initial.png', fullPage: true });
for (let i = 0; i < 5; i += 1) {
  await mobile.click('#nextInputStep');
}
await mobile.screenshot({ path: 'audit-output/mobile-results.png', fullPage: true });

const desktop = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
await desktop.goto(url, { waitUntil: 'networkidle' });
await desktop.screenshot({ path: 'audit-output/desktop-initial.png', fullPage: true });
const text = await desktop.locator('body').innerText();
await writeFile('audit-output/body-text.txt', text, 'utf8');

await browser.close();
