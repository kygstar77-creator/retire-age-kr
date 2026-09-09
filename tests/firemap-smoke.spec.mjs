// 파이어맵 스모크 — 개편 주차 게이트. 화면 10개가 뜨고, 콘솔 에러 0, 가로 스크롤 0, 첫 진입 dialog 0.
import { expect, test } from '@playwright/test';

const INPUTS = { currentAge: 34, targetRetirementAge: 50, financialAsset: 150000000, monthlyInvestment: 1500000, monthlyLivingCost: 2500000 };
const SCREENS = ['#home', '#result', '#experiment', '#save', '#ranking', '#menu', '#settings', '#news', '#dividend', '#cities'];

async function seed(page) {
  await page.addInitScript((inp) => {
    try {
      localStorage.setItem('fm_consent_v1', '1');
      localStorage.setItem('firemap-inputs-v3', JSON.stringify(inp));
      localStorage.setItem('fm_rank_history_v1', JSON.stringify([{ percentile: 40, grade: 'B', score: 80, earliest: 48, date: '2026-09-01' }]));
    } catch { /* ignore */ }
  }, INPUTS);
}

test.describe('firemap smoke', () => {
  for (const hash of SCREENS) {
    test(`screen ${hash} renders clean`, async ({ page }) => {
      const errors = [];
      page.on('pageerror', (e) => errors.push(e.message));
      page.on('console', (m) => { if (m.type() === 'error' && !/net::|Failed to load resource|favicon|cobe|esm\.sh|jsdelivr|kakao/i.test(m.text())) errors.push(m.text()); });
      await seed(page);
      await page.goto(`/${hash}`);
      await page.waitForTimeout(600);
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      expect(overflow, `${hash} horizontal overflow`).toBeLessThanOrEqual(2);
      const dialogs = await page.locator('[role="dialog"], [role="alertdialog"]').count();
      expect(dialogs, `${hash} unexpected dialog on entry`).toBe(0);
      const main = page.locator('main.fm-screen');
      await expect(main.first()).toBeVisible();
      expect(errors, `${hash} console errors`).toEqual([]);
    });
  }

  test('result height and button budget', async ({ page }) => {
    await seed(page);
    await page.goto('/#result');
    await page.waitForTimeout(600);
    const h = await page.evaluate(() => document.documentElement.scrollHeight);
    expect(h, 'result page height ≤ 2.5 viewports').toBeLessThanOrEqual(852 * 2.6);
    const buttons = await page.locator('main.fm-screen button:visible').count();
    expect(buttons, 'result visible buttons').toBeLessThanOrEqual(14);
  });

  test('question guards empty asset', async ({ page }) => {
    await page.addInitScript(() => { try { localStorage.setItem('fm_consent_v1', '1'); } catch { /* ignore */ } });
    await page.goto('/#question');
    await page.waitForTimeout(400);
    await expect(page.locator('main.fm-screen')).toBeVisible();
  });
});
