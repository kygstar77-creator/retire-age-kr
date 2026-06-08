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

test('FireMap mobile core flow and PMO QA smoke test', async ({ page }) => {
  const consoleErrors = [];
  page.on('pageerror', (error) => consoleErrors.push(error.message));
  page.on('console', (message) => {
    if (message.type() === 'error') consoleErrors.push(message.text());
  });

  await page.goto('/#home');
  await expect(page.getByText('파이어맵').first()).toBeVisible();
  await expect(page.getByText('내 돈으로 몇 살까지 버틸 수 있을까?')).toBeVisible();
  await screenshot(page, '01-home');

  await clickVisible(page, '시작하기');
  await expect(page.getByText('질문 1/5')).toBeVisible();
  await expect(page.getByText('지금 몇 살인가요?')).toBeVisible();
  await screenshot(page, '02-question-age');

  await clickVisible(page, '다음');
  await expect(page.getByText('질문 2/5')).toBeVisible();
  await clickVisible(page, '다음');
  await expect(page.getByText('질문 3/5')).toBeVisible();
  await expect(page.getByText('지금 금융자산은 얼마인가요?')).toBeVisible();
  await expect(page.getByText('100만 원 단위로 조절돼요. 가운데 금액을 누르면 직접 입력할 수 있어요.')).toBeVisible();
  await screenshot(page, '03-question-financial-asset');

  const financialValue = page.getByRole('button', { name: /억|만/ }).filter({ hasText: /억/ }).first();
  const before = await financialValue.textContent();
  await page.getByRole('button', { name: '+' }).last().click();
  await expect(financialValue).not.toHaveText(before || '');

  await clickVisible(page, '다음');
  await expect(page.getByText('질문 4/5')).toBeVisible();
  await clickVisible(page, '다음');
  await expect(page.getByText('질문 5/5')).toBeVisible();
  await clickVisible(page, '결과 보기');

  await expect(page.getByText('내 FIRE 현재 위치')).toBeVisible();
  await expect(page.getByText('FIRE를 앞당기는 방법')).toBeVisible();
  await expect(page.getByText('광고')).toBeVisible();
  await screenshot(page, '04-result');

  await clickVisible(page, '조건 바꿔보기');
  await expect(page.getByText('조건 바꿔보기')).toBeVisible();
  await expect(page.getByText('연도별 자산 그래프')).toBeVisible();
  await expect(page.getByText('현재 마지막 자산')).toBeVisible();
  await expect(page.getByText('개선안 마지막 자산')).toBeVisible();
  await screenshot(page, '05-experiment-graph');

  await clickVisible(page, '결과로');
  await expect(page.getByText('내 FIRE 현재 위치')).toBeVisible();

  await clickVisible(page, '도시 시나리오');
  await expect(page.getByText('사는 곳을 바꾸면 FIRE가 얼마나 가까워질까?')).toBeVisible();
  await expect(page.getByText('전주')).toBeVisible();
  await expect(page.getByText('치앙마이')).toBeVisible();
  await screenshot(page, '06-curation');

  await clickVisible(page, '결과로');
  await clickVisible(page, '공유하기');
  await expect(page.getByText('결과카드 이미지 또는 링크 공유')).toBeVisible();
  await expect(page.getByRole('button', { name: '이미지 카드 만들기/공유' })).toBeVisible();
  await expect(page.getByText('입력값은 서버로 전송하지 않고 이 브라우저에 저장됩니다.')).toBeVisible();
  await expect(page.getByText('retireage.kr@gmail.com')).toBeVisible();
  await screenshot(page, '07-share');

  const forbiddenTexts = ['TODO', '임시', '테스트', '준비 중', 'API 연동', 'mock', 'dummy', 'hardcoded'];
  const body = await page.locator('body').innerText();
  for (const text of forbiddenTexts) {
    expect(body).not.toContain(text);
  }

  expect(consoleErrors).toEqual([]);
});
