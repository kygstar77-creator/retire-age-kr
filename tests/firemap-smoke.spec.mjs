// 파이어맵 스모크 — 개편 주차 게이트. 화면 17개가 뜨고, 콘솔 에러 0, 가로 스크롤 0, 첫 진입 dialog 0(결과·질문은 예외 없음).
import { expect, test } from '@playwright/test';

const INPUTS = { currentAge: 34, targetRetirementAge: 50, financialAsset: 150000000, monthlyInvestment: 1500000, monthlyLivingCost: 2500000 };
const SCREENS = ['#home', '#question', '#result', '#experiment', '#save', '#ranking', '#menu', '#settings', '#journey', '#account', '#cities', '#firetype', '#dependent', '#foreignTax', '#dividend', '#pension', '#news', '#wall'];

async function seed(page, seeded = true) {
  await page.addInitScript(({ inp, seeded }) => {
    try {
      localStorage.setItem('fm_consent_v1', '1');
      if (seeded) {
        localStorage.setItem('firemap-inputs-v3', JSON.stringify(inp));
        localStorage.setItem('fm_rank_history_v1', JSON.stringify([{ percentile: 40, grade: 'B', score: 80, earliest: 48, date: '2026-09-01' }]));
      }
    } catch { /* ignore */ }
  }, { inp: INPUTS, seeded });
}

const IGNORE = /net::|Failed to load resource|favicon|kakao|ERR_|404|401|403|429|500|CORS|fonts/i;

test.describe('firemap smoke', () => {
  for (const hash of SCREENS) {
    test(`screen ${hash} renders clean`, async ({ page }) => {
      const errors = [];
      page.on('pageerror', (e) => errors.push(e.message));
      page.on('console', (m) => { if (m.type() === 'error' && !IGNORE.test(m.text())) errors.push(m.text()); });
      await seed(page);
      await page.goto(`/${hash}`);
      await page.waitForTimeout(700);
      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      expect(overflow, `${hash} horizontal overflow`).toBeLessThanOrEqual(2);
      const dialogs = await page.locator('[role="dialog"], [role="alertdialog"]').count();
      expect(dialogs, `${hash} unexpected dialog on entry`).toBe(0);
      await expect(page.locator('main.fm-screen').first()).toBeVisible();
      const inline = await page.evaluate(() => document.querySelectorAll('main.fm-screen [style]').length);
      expect(inline, `${hash} inline styles`).toBeLessThanOrEqual(6);
      const wrapped = await page.evaluate(() => {
        let n = 0;
        document.querySelectorAll('main.fm-screen .ds-stat__value, main.fm-screen .num').forEach((el) => {
          if (/INPUT|TEXTAREA|BUTTON/.test(el.tagName) || el.children.length > 1) return;
          const cs = getComputedStyle(el);
          if (/flex|grid/.test(cs.display)) return;
          const lines = Math.round(el.getBoundingClientRect().height / parseFloat(cs.lineHeight || '16'));
          if (lines > 1 && !el.closest('.ds-p, .ds-caption, .ds-sh__desc, .ds-hero__sub, .ds-range__scale')) n += 1;
        });
        return n;
      });
      expect(wrapped, `${hash} numbers wrapped`).toBe(0);
      expect(errors, `${hash} console errors`).toEqual([]);
    });
  }

  test('result height and button budget', async ({ page }) => {
    await seed(page);
    await page.goto('/#result');
    await page.waitForTimeout(700);
    const h = await page.evaluate(() => document.documentElement.scrollHeight);
    expect(h, 'result page height ≤ 2.5 viewports').toBeLessThanOrEqual(852 * 2.5);
    const buttons = await page.locator('main.fm-screen button:visible').count();
    expect(buttons, 'result visible buttons').toBeLessThanOrEqual(16);
  });

  test('question blocks 0원 asset and offers example', async ({ page }) => {
    await seed(page, false);
    await page.goto('/#question');
    await page.waitForTimeout(400);
    // 나이 2문항 넘기기
    await page.getByRole('button', { name: '다음' }).click();
    await page.getByRole('button', { name: '다음' }).click();
    await page.waitForTimeout(200);
    await expect(page.getByRole('button', { name: '다음' })).toBeDisabled();
    await page.getByRole('button', { name: /예시로 채우기/ }).click();
    await expect(page.getByRole('button', { name: '다음' })).toBeEnabled();
  });

  test('landing (no data) shows no popups and 4 tabs', async ({ page }) => {
    await seed(page, false);
    await page.goto('/#home');
    await page.waitForTimeout(500);
    expect(await page.locator('.ds-tabbar__tab').count()).toBe(4);
    expect(await page.locator('[role="dialog"]').count()).toBe(0);
  });

  test('today home shows 3 numbers and rule chips', async ({ page }) => {
    await seed(page);
    await page.goto('/#home');
    await page.waitForTimeout(700);
    expect(await page.locator('.ds-three .ds-stat').count()).toBe(3);
    expect(await page.locator('.ds-rule').count()).toBeGreaterThanOrEqual(6);
  });

  test('copy rules: no 합니다/하세요, no banned system words', async ({ page }) => {
    await seed(page);
    for (const hash of ['#home', '#result', '#save', '#ranking', '#menu', '#settings']) {
      await page.goto(`/${hash}`);
      await page.waitForTimeout(500);
      const text = await page.locator('main.fm-screen').innerText();
      expect(text, `${hash} 합니다체`).not.toMatch(/합니다|하세요|십시오/);
      expect(text, `${hash} 시스템 용어`).not.toMatch(/시뮬레이션|파라미터|프리셋|세그먼트|샌드박스|커뮤니티|라운지|오픈채팅/);
    }
  });
});
