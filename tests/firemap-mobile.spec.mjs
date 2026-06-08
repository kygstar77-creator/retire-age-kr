import { expect, test } from '@playwright/test';
import { mkdir } from 'node:fs/promises';

const shotDir = 'test-results/firemap-screenshots';

async function screenshot(page, name) {
  await mkdir(shotDir, { recursive: true });
  await page.screenshot({ path: `${shotDir}/${name}.png`, fullPage: true });
}

async function clickVisible(page, text) {
  await page.getByRole('button', { name: text }).first().click();
}

async function expectNoHorizontalOverflow(page) {
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  expect(overflow).toBeLessThanOrEqual(2);
}

async function expectTapTarget(locator, label) {
  const box = await locator.boundingBox();
  expect(box, `${label} should be visible`).not.toBeNull();
  expect(box.width, `${label} width`).toBeGreaterThanOrEqual(44);
  expect(box.height, `${label} height`).toBeGreaterThanOrEqual(44);
}

async function expectBottomCtaUsable(page, name) {
  const button = page.getByRole('button', { name }).first();
  await expectTapTarget(button, `${name} CTA`);
  const box = await button.boundingBox();
  const viewport = page.viewportSize();
  expect(box.y + box.height, `${name} CTA should not sit under browser chrome`).toBeLessThanOrEqual(viewport.height + 1);
}

test('FireMap mobile core flow and PMO QA smoke test', async ({ page }) => {
  const consoleErrors = [];
  page.on('pageerror', (error) => consoleErrors.push(error.message));
  page.on('console', (message) => {
    if (message.type() === 'error') consoleErrors.push(message.text());
  });

  await page.goto('/#home');
  await expect(page.getByText('파이어맵').first()).toBeVisible();
  await expect(page.getByText('내 돈은 몇 살까지 버틸까?')).toBeVisible();
  await expect(page.getByText('투자·세무·법률 자문 아님')).toBeVisible();
  await expect(page.getByRole('button', { name: '초기화' })).toBeHidden();
  await expectNoHorizontalOverflow(page);
  await expectBottomCtaUsable(page, '시작하기');
  await screenshot(page, '01-home');

  await clickVisible(page, '시작하기');
  await expect(page).toHaveURL(/#question$/);
  await expect(page.getByText('질문 1/5')).toBeVisible();
  await expect(page.getByText('지금 몇 살인가요?')).toBeVisible();
  await expect(page.getByRole('button', { name: '초기화' })).toBeHidden();
  await expectNoHorizontalOverflow(page);
  await expectBottomCtaUsable(page, '다음');
  await expectTapTarget(page.getByRole('button', { name: '이전' }).first(), 'previous button');
  await screenshot(page, '02-question-age');

  await clickVisible(page, '다음');
  await expect(page.getByText('질문 2/5')).toBeVisible();
  await clickVisible(page, '이전');
  await expect(page.getByText('질문 1/5')).toBeVisible();
  await clickVisible(page, '다음');
  await clickVisible(page, '다음');
  await expect(page.getByText('질문 3/5')).toBeVisible();
  await expect(page.getByText('지금 금융자산은 얼마인가요?')).toBeVisible();
  await expect(page.getByText('100만 원 단위로 조절돼요. 가운데 금액을 누르면 직접 입력할 수 있어요.')).toBeVisible();
  await expectNoHorizontalOverflow(page);
  await screenshot(page, '03-question-financial-asset');

  const financialValue = page.getByRole('button', { name: /억|만/ }).filter({ hasText: /억/ }).first();
  const before = await financialValue.textContent();
  await page.getByRole('button', { name: '+' }).last().click();
  await expect(financialValue).not.toHaveText(before || '');

  await clickVisible(page, '다음');
  await expect(page.getByText('질문 4/5')).toBeVisible();
  await clickVisible(page, '다음');
  await expect(page.getByText('질문 5/5')).toBeVisible();
  await expectBottomCtaUsable(page, '결과 보기');
  await clickVisible(page, '결과 보기');

  await expect(page).toHaveURL(/#result$/);
  await expect(page.getByText('내 FIRE 현재 위치')).toBeVisible();
  await expect(page.getByText('현재 계산 기준 · 연 수익률 8% · 물가 3%')).toBeVisible();
  await expect(page.getByText('FIRE를 앞당기는 방법')).toBeVisible();
  await expect(page.getByText('FIRE 진단')).toBeVisible();
  await expect(page.getByText('광고')).toBeVisible();
  await expect(page.getByRole('button', { name: '초기화' })).toBeHidden();
  await expectNoHorizontalOverflow(page);
  await expectTapTarget(page.getByRole('button', { name: '조건 바꿔보기' }).first(), 'experiment button');
  await expectTapTarget(page.getByRole('button', { name: '고급 실험' }).first(), 'advanced button');
  await screenshot(page, '04-result');

  await clickVisible(page, '조건 바꿔보기');
  await expect(page).toHaveURL(/#experiment$/);
  await expect(page.getByText('조건 바꿔보기')).toBeVisible();
  await expect(page.getByText('이 화면에서는 퇴사 나이, 생활비, 월 저축액, 수익률처럼 기본 숫자만 조정해요.')).toBeVisible();
  await expect(page.getByText('투자 성향별로 다시 계산해보기')).toBeVisible();
  await expect(page.getByText('현재 적용 수익률은 연 8%예요.')).toBeVisible();
  await expectTapTarget(page.getByRole('button', { name: '결과로' }).first(), 'back to result button');
  await clickVisible(page, '나스닥100형 · 연 10%');
  await expect(page.getByText('현재 적용 수익률은 연 10%예요.')).toBeVisible();
  await expect(page.getByText('MVP 이후 고급 실험')).toBeHidden();
  await expect(page.getByText('건보료·해외체류·현금흐름까지 같이 보기')).toBeHidden();
  await expect(page.getByText('내 미래 자산 차트')).toBeVisible();
  await expect(page.getByText(/현재 계획/).first()).toBeVisible();
  await expect(page.getByText(/생활비 절감안/).first()).toBeVisible();
  await expectNoHorizontalOverflow(page);

  const chart = page.locator('.fm-touch-chart').first();
  const box = await chart.boundingBox();
  expect(box).not.toBeNull();
  expect(box.width, 'chart touch width').toBeGreaterThanOrEqual(300);
  expect(box.height, 'chart touch height').toBeGreaterThanOrEqual(170);
  await page.mouse.move(box.x + box.width * 0.3, box.y + box.height * 0.5);
  await page.mouse.down();
  await page.mouse.move(box.x + box.width * 0.72, box.y + box.height * 0.5, { steps: 5 });
  await page.mouse.up();
  await expect(page.getByText(/세 예상 자산/).first()).toBeVisible();
  await expect(page.getByText('점 맞히기 방식이 아니라 차트 아무 곳이나 누르면 가장 가까운 나이를 보여줘요.')).toBeVisible();
  await expect(page.getByText(/현재 절감안 기준 생활비는/)).toBeVisible();
  await expect(page.getByRole('button', { name: '초기화' })).toBeHidden();
  await screenshot(page, '05-experiment-graph');

  await page.goBack();
  await expect(page).toHaveURL(/#result$/);
  await expect(page.getByText('내 FIRE 현재 위치')).toBeVisible();

  await clickVisible(page, '고급 실험');
  await expect(page).toHaveURL(/#advanced$/);
  await expect(page.getByText('복잡한 가정은 따로 비교해요')).toBeVisible();
  await expect(page.getByText('퇴사 후 고정비 반영')).toBeVisible();
  await expect(page.getByRole('heading', { name: '생활비를 낮추는 시나리오' })).toBeVisible();
  await expect(page.getByText('퇴사 후 월수입 실험')).toBeVisible();
  await expect(page.getByText('지역가입 건보료 월 23만 원 반영')).toBeVisible();
  await expect(page.getByText('치앙마이 3개월 살기')).toBeVisible();
  await clickVisible(page, '건보료 반영');
  await clickVisible(page, '해외체류 반영');
  await clickVisible(page, '현금흐름 반영');
  await expectNoHorizontalOverflow(page);
  await screenshot(page, '06-advanced');

  await clickVisible(page, '결과로');
  await expect(page).toHaveURL(/#result$/);
  await clickVisible(page, '도시 시나리오');
  await expect(page).toHaveURL(/#curation$/);
  await expect(page.getByText('사는 곳을 바꾸면 FIRE가 얼마나 가까워질까?')).toBeVisible();
  await expect(page.getByText('도시별 예상 생활비를 내 조건에 바로 대입해')).toBeVisible();
  await expect(page.getByText('전주')).toBeVisible();
  await expect(page.getByText('치앙마이')).toBeVisible();
  await expect(page.getByText(/예상 월/).first()).toBeVisible();
  await expect(page.getByText(/이 생활비로 계산하면/).first()).toBeVisible();
  await expect(page.getByText(/까지 버틸 수 있어요/).first()).toBeVisible();
  await expect(page.getByText('생활비를 낮추는 건 수익률을 올리는 것만큼 강력해요')).toBeVisible();
  await expect(page.getByRole('button', { name: '초기화' })).toBeHidden();
  await expectNoHorizontalOverflow(page);
  await screenshot(page, '07-curation');

  await clickVisible(page, '결과로');
  await expect(page).toHaveURL(/#result$/);
  await clickVisible(page, '공유하기');
  await expect(page).toHaveURL(/#share$/);
  await expect(page.getByText('내 FIRE 결과 공유하기')).toBeVisible();
  await expect(page.getByRole('button', { name: '결과 이미지 공유하기' })).toBeVisible();
  await expect(page.getByText('입력값은 서버로 전송하지 않고 이 브라우저에 저장됩니다.')).toBeVisible();
  await expect(page.getByText('retireage.kr@gmail.com')).toBeVisible();
  await expect(page.getByRole('button', { name: '초기화' })).toBeHidden();
  await expectNoHorizontalOverflow(page);
  await expectTapTarget(page.getByRole('button', { name: '결과 이미지 공유하기' }).first(), 'share image button');
  await expectTapTarget(page.getByRole('button', { name: '결과 문구 복사' }).first(), 'copy summary button');
  await screenshot(page, '08-share');

  expect(consoleErrors).toEqual([]);
});
