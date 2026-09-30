// 파이어맵 스모크 — 개편 주차 게이트. 화면 17개가 뜨고, 콘솔 에러 0, 가로 스크롤 0, 첫 진입 dialog 0(결과·질문은 예외 없음).
import { expect, test } from '@playwright/test';
import { TOOL_PAGES } from '../src/firemap-v2/toolPages.js';

const INPUTS = { currentAge: 34, targetRetirementAge: 50, financialAsset: 150000000, monthlyInvestment: 1500000, monthlyLivingCost: 2500000 };
const SCREENS = ['#home', '#question', '#result', '#experiment', '#ranking', '#menu', '#settings', '#account', '#cities', '#firetype', '#dependent', '#foreignTax', '#dividend', '#pension', '#severance', '#unemployment', '#salary', '#news', '#wall'];

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

  test('tool paths (/dividend …) open the screen and keep the search address', async ({ page }) => {
    await seed(page);
    for (const t of TOOL_PAGES) {
      await page.goto(t.path);
      await page.waitForTimeout(600);
      await expect(page.locator('main.fm-screen').first()).toBeVisible();
      const loc = await page.evaluate(() => `${window.location.pathname}${window.location.hash}`);
      expect(loc, `${t.path} → ${t.screen}: 주소가 검색용 경로 그대로`).toBe(t.path);
      expect(await page.locator('#sSeo').count(), `${t.path} crawler block removed`).toBe(0);
    }
  });

  test('internal visit flag: ?fm_internal=1 sticks and tags events', async ({ page }) => {
    const bodies = [];
    await page.route('**/rest/v1/firemap_events', async (route) => { try { bodies.push(JSON.parse(route.request().postData() || '{}')); } catch { /* ignore */ } await route.fulfill({ status: 201, body: '' }); });
    await page.goto('/calc/severance?fm_internal=1');
    await page.waitForTimeout(800);
    await page.goto('/#home');
    await page.waitForTimeout(800);
    const last = bodies.filter((b) => b.event === 'session_start').pop();
    expect(last && last.props && last.props.internal, 'session_start에 internal:1').toBe(1);
    expect(last.props.host, '미리보기 호스트 기록').toBe('127.0.0.1');
  });

  test('unemployment benefit: hand-check numbers, crawler text is on screen, next step to fire', async ({ page }) => {
    const bodies = [];
    await page.route('**/rest/v1/firemap_events', async (route) => { try { bodies.push(JSON.parse(route.request().postData() || '{}')); } catch { /* ignore */ } await route.fulfill({ status: 201, body: '' }); });
    await seed(page);
    await page.goto('/calc/unemployment-benefit');
    await page.waitForTimeout(700);
    await page.locator('#ub-last').fill('2026-09-30');
    const hero = page.locator('main.fm-screen');
    // 월 300만·92일 → 97,826원 × 60% = 58,695 < 하한 66,048 → 66,048 × 180일(50세 미만, 피보험기간 3년)
    await expect(hero).toContainText('11,888,640원');
    await expect(hero).toContainText('하한 66,048원');
    await page.getByRole('tab', { name: '50세 이상 · 장애인' }).click();
    await expect(hero).toContainText('13,870,080원');
    await expect(hero).toContainText('210일');
    // 크롤러 블록(#sSeo)에 넣는 문장은 화면에 그대로 있어야 한다(숨김 텍스트·다른 내용 금지).
    const tool = TOOL_PAGES.find((t) => t.path === '/calc/unemployment-benefit');
    const screenText = (await hero.innerText()).replace(/\s+/g, ' ');
    for (const b of tool.body.slice(1)) expect(screenText, `crawler text on screen: ${b.slice(0, 20)}`).toContain(b);
    await page.getByRole('button', { name: '은퇴 나이 계산' }).click();
    await page.waitForTimeout(500);
    expect(bodies.some((b) => b.event === 'unemployment_to_fire'), 'unemployment_to_fire 이벤트').toBe(true);
    expect(await page.evaluate(() => window.location.hash)).toBe('#result');
  });

  test('severance → next calc (unemployment) row counts next_calc_click; /tax·/pension show basis date', async ({ page }) => {
    const bodies = [];
    await page.route('**/rest/v1/firemap_events', async (route) => { try { bodies.push(JSON.parse(route.request().postData() || '{}')); } catch { /* ignore */ } await route.fulfill({ status: 201, body: '' }); });
    await seed(page);
    await page.goto('/calc/severance');
    await page.waitForTimeout(700);
    await page.getByRole('button', { name: /실업급여 계산기/ }).click();
    await page.waitForTimeout(500);
    expect(await page.evaluate(() => window.location.pathname)).toBe('/calc/unemployment-benefit');
    const ev = bodies.find((b) => b.event === 'next_calc_click');
    expect(ev && ev.props && ev.props.to, 'next_calc_click 이벤트').toBe('unemployment');
    for (const path of ['/tax', '/pension']) {
      await page.goto(path);
      await page.waitForTimeout(600);
      await expect(page.locator('main.fm-screen'), `${path} 기준일`).toContainText('기준 · 참고용, 실제와 다를 수 있어요');
      await expect(page.locator('main.fm-screen a[href="/disclaimer"]')).toHaveCount(1);
    }
  });

  test('salary take-home: hand-check A, crawler text is on screen, next step to fire', async ({ page }) => {
    const bodies = [];
    await page.route('**/rest/v1/firemap_events', async (route) => { try { bodies.push(JSON.parse(route.request().postData() || '{}')); } catch { /* ignore */ } await route.fulfill({ status: 201, body: '' }); });
    await seed(page);
    await page.goto('/calc/salary');
    const hero = page.locator('main.fm-screen');
    // 손검산 A(work/test-salary.mjs): 연봉 4,000만·비과세 20만·본인 1·자녀 0·100% — 사람인·잡코리아·인크루트와 줄마다 대조
    await expect(hero).toContainText('2,935,813원');
    await expect(hero).toContainText('84,620원');
    await expect(hero).toContainText('112,640원');
    const tool = TOOL_PAGES.find((t) => t.path === '/calc/salary');
    const screenText = (await hero.innerText()).replace(/\s+/g, ' ');
    for (const b of tool.body.slice(1)) expect(screenText, `crawler text on screen: ${b.slice(0, 20)}`).toContain(b);
    // 기본 화면에서 저축 0원이 되면 은퇴 연결이 막힌다(레드팀 10/1) — 기본 생활비 250만원이면 2,935,813 − 2,500,000
    await expect(hero).toContainText('남는 435,813원을 월 저축으로');
    // F3 A안: 결과 카드 안 80/100/120% 칩(경쟁 5곳에 없음) — 손검산 A의 80%·120%(salaryNet 원식) 그대로 바뀌고 되돌아온다
    await expect(hero).toContainText('공제 합계');
    await page.getByRole('tab', { name: '80%' }).click();
    await expect(hero).toContainText('2,954,443원');
    await expect(hero).toContainText('67,690원');
    await page.getByRole('tab', { name: '120%' }).click();
    await expect(hero).toContainText('2,917,203원');
    await page.getByRole('tab', { name: '100%' }).click();
    await expect(hero).toContainText('2,935,813원');
    // 결과 카드 타일 3칸이 375px 안에서 넘치지 않는다(시안 지적: 값이 붙음)
    const over = await page.locator('.ds-hero--compact-tiles .ds-tile').evaluateAll((els) => els.filter((e) => e.scrollWidth > e.clientWidth + 1).length);
    expect(over, '타일 값 넘침').toBe(0);
    await page.getByRole('button', { name: '이 돈이면 몇 살에 은퇴?' }).click();
    await page.waitForTimeout(500);
    expect(bodies.some((b) => b.event === 'salary_to_fire'), 'salary_to_fire 이벤트').toBe(true);
    expect(await page.evaluate(() => window.location.hash)).toBe('#result');
  });

  // F1 쿠팡 1칸: 링크가 있으면 바로 위에 대가성 문구, sponsored rel, 발급 주소 그대로. 링크가 없으면 칸 자체가 없어야 한다.
  test('coupang slot: disclosure above every link, nothing without an issued link', async ({ page }) => {
    await seed(page);
    for (const path of ['/calc/salary', '/calc/severance', '/calc/unemployment-benefit']) {
      await page.goto('about:blank');
      await page.goto(path);
      await expect(page.locator('main.fm-screen')).toContainText(path === '/calc/salary' ? '몇 살에 은퇴?' : '은퇴 나이 계산');
      const links = page.locator('main.fm-screen a[href*="coupang.com"]');
      const n = await links.count();
      await expect(page.locator('.fm-coupang-pick'), `${path} slot count`).toHaveCount(n ? 1 : 0);
      for (let i = 0; i < n; i += 1) {
        const a = links.nth(i);
        expect(await a.getAttribute('href')).toMatch(/^https:\/\/link\.coupang\.com\/a\/[A-Za-z0-9]+$/);
        expect(await a.getAttribute('rel')).toContain('sponsored');
        await expect(page.locator('.fm-coupang-pick__disclosure')).toContainText('쿠팡 파트너스 활동의 일환으로, 이에 따른 일정액의 수수료를 제공받습니다.');
      }
    }
  });

  // 10/1 사장님 기기: 재방문 기기가 /calc/salary#home 같은 주소로 들어와 첫 화면으로 떨어졌다. 도구 경로면 해시와 상관없이 도구 화면.
  test('tool path wins over a leftover hash on a returning device', async ({ page }) => {
    await seed(page);
    for (const path of ['/calc/salary', '/calc/severance', '/calc/unemployment-benefit', '/tax']) {
      const tool = TOOL_PAGES.find((t) => t.path === path);
      for (const hash of ['#home', '#result']) {
        await page.goto('about:blank'); // 같은 문서 안 해시 이동이 아니라 새로 여는 상황
        await page.goto(`${path}${hash}`);
        await expect(page.locator('main.fm-screen h1, main.fm-screen h2').first(), `${path}${hash}`).toContainText(tool.title);
        expect(await page.evaluate(() => window.location.pathname + window.location.hash)).toBe(path);
      }
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
