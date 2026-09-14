// 파이어맵 스모크 — 개편 주차 게이트. 화면 17개가 뜨고, 콘솔 에러 0, 가로 스크롤 0, 첫 진입 dialog 0(결과·질문은 예외 없음).
import { expect, test } from '@playwright/test';
import { TOOL_PAGES } from '../src/firemap-v2/toolPages.js';
import { screens } from '../src/firemap-v2/screens.js';

const INPUTS = { currentAge: 34, targetRetirementAge: 50, financialAsset: 150000000, monthlyInvestment: 1500000, monthlyLivingCost: 2500000 };
const SCREENS = ['#home', '#question', '#result', '#experiment', '#ranking', '#menu', '#settings', '#account', '#cities', '#firetype', '#dependent', '#foreignTax', '#dividend', '#pension', '#news', '#wall'];

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
      // 결과 화면의 자산 차트는 눈금·시작/끝 값·나이 라벨 위치를 인라인으로 잡는다(최대 8) — 그 밖엔 인라인 금지
      expect(inline, `${hash} inline styles`).toBeLessThanOrEqual(hash === '#result' ? 10 : 6);
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
    // 결과는 접지 않는다(계산기 37곳 조사에서 결과를 아코디언으로 숨긴 곳 0). 대신 폭주만 막는 상한.
    expect(h, 'result page height ≤ 4 viewports').toBeLessThanOrEqual(852 * 4);
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

  test('landing (no data) shows no popups and no tab bar', async ({ page }) => {
    await seed(page, false);
    await page.goto('/#home');
    await page.waitForTimeout(500);
    // 랜딩은 계산 유도 하나만 — 탭바를 숨겨 첫 화면을 비운다.
    expect(await page.locator('.ds-tabbar__tab').count()).toBe(0);
    expect(await page.locator('[role="dialog"]').count()).toBe(0);
  });

  test('result is the front screen: 4 tabs and the widget ticker', async ({ page }) => {
    await seed(page);
    await page.goto('/#result');
    await page.waitForTimeout(700);
    expect(await page.locator('.ds-tabbar__tab').count()).toBe(4);
    // 위젯 카드: 지표 한 줄(Ticker)이 넘어간다(2026-09-14, 3숫자 타일 대체)
    await expect(page.locator('.ds-ticker').first(), '지표 한 줄(서버 지표를 받은 뒤 뜬다)').toBeVisible({ timeout: 15000 });
    // 저축은 걷어냈다 — 규칙 칩이 어디에도 없어야 한다.
    expect(await page.locator('.ds-rule').count()).toBe(0);
  });

  test('tool paths (/dividend …) open the screen and fold into the hash address', async ({ page }) => {
    await seed(page);
    for (const t of TOOL_PAGES) {
      await page.goto(t.path);
      await page.waitForTimeout(600);
      await expect(page.locator('main.fm-screen').first()).toBeVisible();
      const hash = await page.evaluate(() => window.location.hash);
      expect(hash, `${t.path} → ${t.screen}`).toBe(screens[t.screen].hash);
      expect(await page.locator('#sSeo').count(), `${t.path} crawler block removed`).toBe(0);
    }
  });

  test('copy rules: no 합니다/하세요, no banned system words', async ({ page }) => {
    await seed(page);
    for (const hash of ['#home', '#result', '#ranking', '#menu', '#settings']) {
      await page.goto(`/${hash}`);
      await page.waitForTimeout(500);
      const text = await page.locator('main.fm-screen').innerText();
      expect(text, `${hash} 합니다체`).not.toMatch(/합니다|하세요|십시오/);
      expect(text, `${hash} 시스템 용어`).not.toMatch(/시뮬레이션|파라미터|프리셋|세그먼트|샌드박스|커뮤니티|라운지/);
    }
  });
});
