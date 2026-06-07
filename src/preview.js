import { buildSimulation, defaultInputs, normalizeInputs, simulateRetirement } from './utils/retirementSimulator.js';
import { formatAge, formatCompactMoney, formatEok, formatInputNumber, formatPercent, statusMeta } from './utils/formatters.js';
import { buildShareText, buildShareUrl, decodeInputsFromHash } from './utils/shareState.js';

const storageKey = 'toesanai-inputs-v2';
const hasSharedScenario = Boolean(decodeInputsFromHash(window.location.search || window.location.hash));
const defaultTaxInputs = {
  annualDividendIncome: 12000000,
  dividendWithholdingRate: 15.4,
  financialIncomeThreshold: 20000000,
  additionalDividendTaxRate: 0,
  foreignStockGain: 10000000,
  foreignStockBasicDeduction: 2500000,
  foreignStockTaxRate: 22,
  targetMonthlyDividendAfterTax: 2000000,
  expectedDividendYield: 7,
  dividendReinvestmentRate: 0
};
const taxFields = [
  ['annualDividendIncome', '연간 배당금', '세전 기준', '원', true],
  ['dividendWithholdingRate', '배당 기본 세율', '기본값 15.4%', '%', false],
  ['financialIncomeThreshold', '금융소득 확인 기준', '기본값 2,000만 원', '원', true],
  ['additionalDividendTaxRate', '초과분 추가 추정세율', '민감도 확인용', '%', false],
  ['foreignStockGain', '해외주식 연간 양도차익', '차익 기준', '원', true],
  ['foreignStockBasicDeduction', '해외주식 기본공제', '기본값 250만 원', '원', true],
  ['foreignStockTaxRate', '해외주식 양도세율', '기본값 22%', '%', false],
  ['targetMonthlyDividendAfterTax', '목표 월 세후 배당금', '월 현금흐름 목표', '원', true],
  ['expectedDividendYield', '예상 배당률', '연 배당률', '%', false],
  ['dividendReinvestmentRate', '배당 재투자 비율', '재투자할 비율', '%', false]
];
const fields = [
  { section: '기본', name: 'currentAge', label: '현재 나이', help: '정확한 만 나이가 아니어도 괜찮습니다. 평소 쓰는 나이로 넣어보세요.', suffix: '세' },
  { section: '기본', name: 'targetRetirementAge', label: '퇴사하고 싶은 나이', help: '이 나이에 월급이 끊긴다고 보고 계산합니다.', suffix: '세' },
  { section: '기본', name: 'startYear', label: '계산 기준 연도', help: '올해 기준으로 계산하려면 그대로 두면 됩니다.', suffix: '년' },
  { section: '자산', name: 'financialAsset', label: '퇴사 후 생활비로 쓸 돈', help: '예금, 주식, ETF처럼 필요할 때 꺼내 쓸 수 있는 돈입니다.', suffix: '원', money: true },
  { section: '자산', name: 'realEstateValue', label: '집·부동산 현재 가치', help: '순자산에는 넣지만, 팔기 전에는 생활비로 바로 쓰기 어렵습니다.', suffix: '원', money: true },
  { section: '자산', name: 'debt', label: '갚아야 할 대출금', help: '주택담보대출, 신용대출 등 남아 있는 원금을 모두 더해 입력하세요.', suffix: '원', money: true },
  { section: '현금흐름', name: 'monthlyInvestment', label: '퇴사 전 매달 모으는 돈', help: '생활비를 쓰고 남아 저축·투자할 수 있는 월 금액입니다.', suffix: '원', money: true },
  { section: '현금흐름', name: 'monthlyLivingCost', label: '퇴사 후 매달 쓸 생활비', help: '오늘 돈 가치로 입력하세요. 이후 생활비 증가는 물가상승률로 계산합니다.', suffix: '원', money: true },
  { section: '현금흐름', name: 'partTimeIncomeAfterRetirement', label: '퇴사 후 매달 벌 돈', help: '부업, 프리랜서, 임대소득처럼 퇴사 후에도 들어올 월 소득입니다.', suffix: '원', money: true },
  { section: '연금', name: 'expectedPensionAge', label: '국민연금 받기 시작하는 나이', help: '예상 수령 시작 나이를 넣으세요.', suffix: '세' },
  { section: '연금', name: 'expectedMonthlyPension', label: '국민연금 월 예상액', help: '오늘 돈 가치로 입력하면, 계산 때 물가상승률만큼 함께 늘려 반영합니다.', suffix: '원', money: true },
  { section: '가정', name: 'annualReturnRate', label: '연평균 투자수익률', help: '금융자산이 매년 평균 몇 % 불어난다고 볼지입니다.', suffix: '%' },
  { section: '가정', name: 'inflationRate', label: '연평균 물가상승률', help: '생활비, 국민연금, 퇴사 후 소득이 매년 몇 %씩 오른다고 볼지입니다.', suffix: '%' },
  { section: '가정', name: 'simulationUntilAge', label: '몇 살까지 돈이 남아야 하나요?', help: '기대수명처럼 확인하고 싶은 나이를 넣으세요. 이 나이까지 마이너스가 아니면 통과로 봅니다.', suffix: '세' }
];

let inputs = loadInputs();
let taxInputs = { ...defaultTaxInputs };
let dividendOpen = false;
let inputStep = 0;

function trackAppEvent(name, params = {}) {
  if (!window.gtag) return;
  window.gtag('event', name, { app_name: 'toesanai', ...params });
}

function loadInputs() {
  try {
    const shared = decodeInputsFromHash(window.location.search || window.location.hash);
    const saved = localStorage.getItem(storageKey);
    return shared ? { ...defaultInputs, ...shared } : saved ? { ...defaultInputs, ...JSON.parse(saved) } : { ...defaultInputs };
  } catch {
    return { ...defaultInputs };
  }
}

function saveInputs() {
  localStorage.setItem(storageKey, JSON.stringify(normalizeInputs(inputs)));
}

function groupFields() {
  return Object.entries(fields.reduce((groups, item) => {
    groups[item.section] = [...(groups[item.section] || []), item];
    return groups;
  }, {}));
}

function renderInputs() {
  const grouped = groupFields();
  const currentSection = grouped[inputStep]?.[0] ?? '';
  document.querySelector('#mobileStepper').innerHTML = `<div><span>${inputStep + 1}</span><small>/ ${grouped.length}</small></div><strong>${currentSection}</strong>`;
  document.querySelector('#mobileStepActions').innerHTML = `
    <button type="button" id="prevInputStep" ${inputStep === 0 ? 'disabled' : ''}>이전</button>
    <button type="button" id="nextInputStep">${inputStep < grouped.length - 1 ? '다음' : '결과 보기'}</button>
  `;
  document.querySelector('#inputGrid').innerHTML = grouped.map(([section, sectionFields], index) => `
    <div class="input-section ${index === inputStep ? 'active-section' : ''}">
      <h3>${section}</h3>
      ${sectionFields.map(({ name, label, help, suffix, money }) => `
        <label class="field">
          <span>${label}</span>
          <b>${help}</b>
          <div class="input-wrap">
            <input type="${money ? 'text' : 'number'}" inputmode="${money ? 'numeric' : 'decimal'}" value="${money ? formatInputNumber(inputs[name]) : inputs[name]}" data-field="${name}" data-money="${money ? 'true' : 'false'}" />
            <small>${suffix}</small>
          </div>
          ${money ? `<em>${formatCompactMoney(inputs[name])}</em>` : ''}
        </label>
      `).join('')}
    </div>
  `).join('');

  document.querySelectorAll('#inputGrid input').forEach((input) => {
    input.addEventListener('input', (event) => {
      const isMoney = event.target.dataset.money === 'true';
      const nextValue = isMoney ? event.target.value.replace(/[^\d-]/g, '') : event.target.value;
      inputs[event.target.dataset.field] = nextValue;
      if (isMoney) event.target.value = formatInputNumber(nextValue);
      const helper = event.target.closest('.field').querySelector('em');
      if (helper) helper.textContent = formatCompactMoney(nextValue);
      saveInputs();
      renderResults();
    });
  });

  document.querySelector('#prevInputStep').addEventListener('click', () => {
    inputStep = Math.max(0, inputStep - 1);
    renderInputs();
  });
  document.querySelector('#nextInputStep').addEventListener('click', () => {
    if (inputStep < grouped.length - 1) {
      inputStep += 1;
      renderInputs();
      return;
    }
    document.querySelector('.input-panel').classList.remove('input-open');
    document.querySelector('#mobileInputToggle').textContent = '입력 수정';
    document.querySelector('#decisionDashboard').scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
}

function renderResults() {
  const data = normalizeInputs(inputs);
  const simulation = buildSimulation(data);
  document.querySelector('#heroTargetAge').textContent = `${data.targetRetirementAge}세`;
  renderDecision(simulation);
  renderGrowth(simulation, data);
  renderSummary(simulation);
  renderInsight(simulation);
  renderDividendCalculator();
  renderScenarios(simulation);
  renderTable(simulation.targetResult.rows);
}

function renderDecision(simulation) {
  const { inputs: data, status, survivalScore, safeWithdrawalRate, requiredFireAssetByFourPercent, fireGap, bridgeYears, retirementFinancialAsset, firstRetirementExpense, finalFinancialAsset, targetResult } = simulation;
  const survives = !targetResult.depletionAge || targetResult.depletionAge > data.simulationUntilAge;
  const title = survives ? `${data.targetRetirementAge}세에 퇴사해도 ${data.simulationUntilAge}세까지 돈이 남습니다` : `${data.targetRetirementAge}세에 퇴사하면 ${targetResult.depletionAge}세쯤 돈이 바닥날 수 있어요`;
  const gapText = fireGap <= 0 ? `${formatEok(Math.abs(fireGap))} 더 많음` : `${formatEok(fireGap)} 모자람`;
  document.querySelector('#decisionDashboard').innerHTML = `
    <div class="decision-main">
      <span class="badge badge-${status}">${statusMeta[status].label}</span>
      <h2>${title}</h2>
      <p>퇴사 시점에 생활비로 쓸 수 있는 돈은 ${formatEok(retirementFinancialAsset)}이고, 퇴사 첫해 실제로 꺼내 써야 하는 돈은 ${formatEok(firstRetirementExpense)}입니다. 퇴사나이는 먼저 ${data.simulationUntilAge}세까지 돈이 바닥나지 않는지를 보고, 25배 기준은 보수적인 참고값으로 함께 보여줍니다.</p>
      <div class="score-meter" aria-label="자산수명 점수"><span style="width: ${Math.min(100, Math.max(0, survivalScore))}%"></span></div>
    </div>
    <div class="decision-score"><small>자산수명 점수</small><strong>${survivalScore}</strong><span>/ 100</span></div>
    <div class="metric-strip">
      <article class="strip-card strip-${status}"><span>판정</span><div><small>${data.simulationUntilAge}세까지 확인</small><strong>${survives ? '돈 남음' : `${targetResult.depletionAge}세 바닥`}</strong></div></article>
      <article class="strip-card"><span>참고</span><div><small>생활비 25년치 기준</small><strong>${formatEok(requiredFireAssetByFourPercent)}</strong></div></article>
      <article class="strip-card"><span>차이</span><div><small>25년치 기준과 비교</small><strong>${gapText}</strong></div></article>
      <article class="strip-card"><span>연금</span><div><small>연금 받기 전 기간</small><strong>${bridgeYears}년</strong></div></article>
      <article class="strip-card"><span>잔액</span><div><small>${data.simulationUntilAge}세에 남는 돈</small><strong>${formatEok(finalFinancialAsset)}</strong></div></article>
    </div>
  `;
}

function renderGrowth(simulation, data) {
  document.querySelector('#growthPanel').innerHTML = `
    <div><p class="eyebrow">공유</p><h2>카톡·커뮤니티에 바로 공유하기</h2><p>입력값이 담긴 링크라 상대방도 같은 조건으로 바로 볼 수 있습니다. 자산 정보는 서버에 저장되지 않고, 링크를 받은 사람의 화면에서만 다시 계산됩니다.</p></div>
    <div class="growth-actions"><button type="button" data-copy="link">링크 복사</button><button type="button" data-copy="summary">요약 복사</button></div>
  `;
  document.querySelectorAll('[data-copy]').forEach((button) => button.addEventListener('click', async () => {
    const shareUrl = buildShareUrl(data);
    const text = button.dataset.copy === 'link' ? shareUrl : `${buildShareText(simulation)}\n\n${shareUrl}`;
    await navigator.clipboard.writeText(text);
    const original = button.textContent;
    button.textContent = '복사 완료';
    window.setTimeout(() => { button.textContent = original; }, 1600);
  }));
}

function renderSummary(simulation) {
  const { inputs: data, targetResult, earliestRetirementAge, status, retirementFinancialAsset, safeWithdrawalRate, finalFinancialAsset } = simulation;
  const survives = !targetResult.depletionAge || targetResult.depletionAge > data.simulationUntilAge;
  const requiredMonthlyInvestment = findRequiredMonthlyInvestment(data);
  const requiredMonthlyValue = requiredMonthlyInvestment === null ? '월 2,000만 원 이상' : formatCompactMoney(requiredMonthlyInvestment);
  const requiredMonthlyDetail = requiredMonthlyInvestment === null
    ? '현재 조건에서는 목표 달성이 매우 어렵습니다'
    : requiredMonthlyInvestment <= data.monthlyInvestment
      ? `현재 월 ${formatCompactMoney(data.monthlyInvestment)}이면 목표에 도달합니다`
      : `현재보다 월 ${formatCompactMoney(requiredMonthlyInvestment - data.monthlyInvestment)} 더 필요`;
  const cards = [
    ['퇴사 전 매달 모아야 할 돈', requiredMonthlyValue, requiredMonthlyDetail, requiredMonthlyInvestment === null ? 'risk' : requiredMonthlyInvestment <= data.monthlyInvestment ? 'stable' : 'caution', requiredMonthlyInvestment === null ? '위험' : requiredMonthlyInvestment <= data.monthlyInvestment ? '충분' : '추가 필요'],
    ['목표 퇴사 판정', survives ? `${data.simulationUntilAge}세까지 돈 남음` : `${targetResult.depletionAge}세쯤 바닥 예상`, `${data.targetRetirementAge}세 퇴사 기준`, status, statusMeta[status].label],
    ['가장 빠른 퇴사 가능 나이', formatAge(earliestRetirementAge), `${data.simulationUntilAge}세까지 버티는 가장 이른 나이`, earliestRetirementAge ? 'stable' : 'risk', earliestRetirementAge ? '안정' : '위험'],
    ['퇴사 첫해 꺼내 쓰는 비율', formatPercent(safeWithdrawalRate), '첫해에 쓸 돈 ÷ 퇴사 시점 금융자산', safeWithdrawalRate >= 8 ? 'caution' : 'neutral', safeWithdrawalRate >= 8 ? '주의' : '정보'],
    [`${data.simulationUntilAge}세 잔여 금융자산`, formatEok(finalFinancialAsset), '사용자가 입력한 종료 나이 기준', finalFinancialAsset > 0 ? 'stable' : 'risk', finalFinancialAsset > 0 ? '안정' : '위험'],
    ['퇴사 시점 생활비 재원', formatEok(retirementFinancialAsset), '부동산을 제외하고 실제 꺼내 쓸 수 있는 돈', 'neutral', '정보']
  ];
  document.querySelector('#summaryGrid').innerHTML = cards.map(([label, value, detail, tone, badge]) => `
    <article class="summary-card tone-${tone}"><div class="card-top"><span class="card-icon">원</span><span class="badge badge-${tone}">${badge}</span></div><p>${label}</p><strong>${value}</strong><small>${detail}</small></article>
  `).join('');
}

function findRequiredMonthlyInvestment(data) {
  const maxMonthlyInvestment = 20000000;
  const step = 10000;

  if (isStableWithMonthlyInvestment(data, 0)) return 0;
  if (!isStableWithMonthlyInvestment(data, maxMonthlyInvestment)) return null;

  let low = 0;
  let high = maxMonthlyInvestment;
  while (high - low > step) {
    const mid = Math.floor((low + high) / 2);
    if (isStableWithMonthlyInvestment(data, mid)) high = mid;
    else low = mid;
  }

  return Math.ceil(high / step) * step;
}

function isStableWithMonthlyInvestment(data, monthlyInvestment) {
  const result = simulateRetirement({ ...data, monthlyInvestment }, data.targetRetirementAge);
  return !result.depletionAge || result.depletionAge > data.simulationUntilAge;
}

function renderInsight(simulation) {
  const { inputs: data, targetResult, earliestRetirementAge, status, gainedYears, extraAssetFromOneMoreYear, safeWithdrawalRate, fireGap, bridgeYears, firstYearLivingCost, firstRetirementExpense, firstYearPartTimeIncome, firstYearPensionIncome, pensionStartWithdrawal, retirementFinancialAsset, finalFinancialAsset } = simulation;
  const survives = !targetResult.depletionAge || targetResult.depletionAge > data.simulationUntilAge;
  const pensionText = pensionStartWithdrawal === null ? '입력한 종료 나이가 국민연금 시작 전이라, 국민연금은 이번 결과에 영향을 주지 않습니다.' : `국민연금을 받기 시작한 뒤에는 연간 인출해야 하는 돈이 ${formatEok(pensionStartWithdrawal)} 수준으로 줄어듭니다. 국민연금과 퇴사 후 소득도 물가상승률만큼 같이 오른다고 보고 계산했습니다.`;
  const fourPercentText = fireGap > 0 ? `생활비 25년치 기준으로는 ${formatEok(fireGap)} 정도 모자랍니다. 이 기준은 돈을 오래 남기기 위한 보수적인 참고선이고, 실제 판정은 ${data.simulationUntilAge}세까지 돈이 바닥나는지로 봅니다.` : `생활비 25년치 기준으로도 ${formatEok(Math.abs(fireGap))} 정도 더 많습니다.`;
  const workMoreText = gainedYears > 0 ? `1년 더 근무하면 자산수명이 약 ${gainedYears}년 늘어납니다.` : `1년 더 근무해도 고갈 나이는 같지만, ${data.simulationUntilAge}세 잔여 금융자산은 약 ${formatEok(extraAssetFromOneMoreYear)} 늘어납니다.`;
  const messages = [
    survives ? `${data.targetRetirementAge}세 퇴사는 입력한 ${data.simulationUntilAge}세 기준에서 가능합니다. 이 결과는 “돈을 많이 남기는지”보다 “돈이 마이너스가 되지 않는지”를 먼저 봅니다.` : `${data.targetRetirementAge}세 퇴사는 ${targetResult.depletionAge}세쯤 금융자산이 바닥날 수 있어 조정이 필요합니다.`,
    `퇴사 첫해 생활비는 ${formatEok(firstYearLivingCost)}이고, 퇴사 후 소득과 국민연금을 뺀 뒤 실제로 꺼내 써야 하는 돈은 ${formatEok(firstRetirementExpense)}입니다.`,
    `퇴사 시점에 생활비로 쓸 수 있는 돈은 부동산을 뺀 금융자산 기준 ${formatEok(retirementFinancialAsset)}입니다.`,
    bridgeYears > 0 ? `국민연금 받기 전까지 ${bridgeYears}년을 금융자산과 퇴사 후 소득으로 버텨야 합니다. 이 기간이 길수록 초반 현금흐름이 중요합니다.` : '퇴사 시점이 국민연금 수령 이후라 초반에 연금 없이 버티는 기간은 거의 없습니다.',
    pensionText,
    fourPercentText,
    workMoreText,
    `${data.simulationUntilAge}세 기준 잔여 금융자산은 ${formatEok(finalFinancialAsset)}입니다.`,
    earliestRetirementAge ? `현재 입력값에서 가장 빠른 퇴사 가능 나이는 ${formatAge(earliestRetirementAge)}입니다.` : '현재 입력값에서는 70세까지 일해도 설정한 종료 나이까지 금융자산 유지가 어렵습니다.'
  ];
  document.querySelector('#insightReport').innerHTML = `
    <div class="section-heading"><div><p class="eyebrow">AI 리포트</p><h2>퇴사나이 해석</h2></div><span class="badge badge-${status}">${statusMeta[status].label}</span></div>
    <div class="insight-title"><span>분석</span><strong>${survives ? '고갈 기준으로는 퇴사 가능성이 높습니다' : statusMeta[status].summary}</strong></div>
    <ul>${messages.map((message) => `<li>${message}</li>`).join('')}</ul>
  `;
}

function renderDividendCalculator() {
  const target = document.querySelector('#dividendCalculator');
  if (!target) return;
  const result = calculateInvestmentTaxes(taxInputs);
  target.classList.toggle('open', dividendOpen);
  target.innerHTML = `
    <div class="section-heading tax-heading">
      <div><p class="eyebrow">Dividend</p><h2>배당금·해외주식 세금 계산기</h2></div>
      <button class="tax-open-button" type="button" id="toggleDividendCalculator">${dividendOpen ? '접기' : '계산기 열기'}</button>
    </div>
    <div class="tax-results compact-results">
      ${renderTaxCard('월 세후 배당금', formatCompactMoney(result.dividendTax.monthlyAfterTaxDividend), '배당 기본 세율 반영')}
      ${renderTaxCard('해외주식 양도세', formatCompactMoney(result.foreignStockTax.tax), '기본공제 차감 후')}
      ${renderTaxCard('필요 배당 원금', formatCompactMoney(result.requiredAsset.requiredAsset), `순수령 배당률 ${formatPercent(result.requiredAsset.netYieldRate)}`)}
    </div>
    ${dividendOpen ? `
      <p class="tax-intro">배당금, 해외주식 양도차익, 목표 월 배당금을 입력해 세후 현금흐름과 필요 원금을 대략 확인합니다.</p>
      <div class="tax-grid">
        <div class="tax-inputs">
          ${taxFields.map(([name, label, help, suffix, money]) => `
            <label class="field">
              <span>${label}</span>
              <b>${help}</b>
              <div class="input-wrap">
                <input type="${money ? 'text' : 'number'}" inputmode="${money ? 'numeric' : 'decimal'}" value="${money ? formatInputNumber(taxInputs[name]) : taxInputs[name]}" data-tax-field="${name}" data-tax-money="${money ? 'true' : 'false'}" />
                <small>${suffix}</small>
              </div>
              ${money ? `<em>${formatCompactMoney(taxInputs[name])}</em>` : ''}
            </label>
          `).join('')}
        </div>
        <div class="tax-results">
          ${renderTaxCard('연 세후 배당금', formatCompactMoney(result.dividendTax.afterTaxDividend), `월 ${formatCompactMoney(result.dividendTax.monthlyAfterTaxDividend)}`)}
          ${renderTaxCard('배당 세금 추정', formatCompactMoney(result.dividendTax.totalTax), `실효 ${formatPercent(result.dividendTax.effectiveTaxRate)}`)}
          ${renderTaxCard('해외주식 양도세 추정', formatCompactMoney(result.foreignStockTax.tax), `세후차익 ${formatCompactMoney(result.foreignStockTax.afterTaxGain)}`)}
          ${renderTaxCard('필요 배당 원금', formatCompactMoney(result.requiredAsset.requiredAsset), `순수령 배당률 ${formatPercent(result.requiredAsset.netYieldRate)}`)}
          <button class="tax-copy-button" type="button" id="copyMonthlyDividend">월 세후 배당금 복사</button>
          <button class="tax-apply-button" type="button" id="applyMonthlyDividend">세후 배당금을 추가소득으로 반영</button>
        </div>
      </div>
      <div class="tax-notice"><strong>참고용 계산</strong><p>세율, 공제, 종합과세, 계좌 종류, 환율, 손익통산에 따라 실제 금액은 달라질 수 있습니다.</p></div>
    ` : ''}
  `;

  document.querySelector('#toggleDividendCalculator')?.addEventListener('click', () => {
    dividendOpen = !dividendOpen;
    renderDividendCalculator();
  });
  document.querySelectorAll('[data-tax-field]').forEach((input) => {
    input.addEventListener('input', (event) => {
      const isMoney = event.target.dataset.taxMoney === 'true';
      const nextValue = isMoney ? event.target.value.replace(/[^\d-]/g, '') : event.target.value;
      taxInputs[event.target.dataset.taxField] = nextValue;
      renderDividendCalculator();
    });
  });
  document.querySelector('#copyMonthlyDividend')?.addEventListener('click', async () => {
    await navigator.clipboard.writeText(Math.round(result.dividendTax.monthlyAfterTaxDividend).toString());
    document.querySelector('#copyMonthlyDividend').textContent = '월 세후 배당금 복사됨';
  });
  document.querySelector('#applyMonthlyDividend')?.addEventListener('click', () => {
    inputs = {
      ...inputs,
      partTimeIncomeAfterRetirement: Math.round(result.dividendTax.monthlyAfterTaxDividend)
    };
    saveInputs();
    renderInputs();
    renderResults();
    document.querySelector('#applyMonthlyDividend')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });
}

function renderTaxCard(title, main, sub) {
  return `<article class="tax-result-card"><span>${title}</span><strong>${main}</strong><small>${sub}</small></article>`;
}

function calculateInvestmentTaxes(values = {}) {
  const data = normalizeTaxInputs({ ...defaultTaxInputs, ...values });
  const dividendTax = calculateDividendTax(data);
  const foreignStockTax = calculateForeignStockGainTax(data);
  const requiredAsset = calculateRequiredDividendAsset(data);
  return { inputs: data, dividendTax, foreignStockTax, requiredAsset };
}

function normalizeTaxInputs(values) {
  return Object.fromEntries(
    Object.entries(values).map(([key, value]) => [key, Number(String(value ?? '').replace(/[^\d.-]/g, '')) || 0])
  );
}

function calculateDividendTax(data) {
  const grossDividend = Math.max(0, data.annualDividendIncome);
  const withholdingTax = grossDividend * toRate(data.dividendWithholdingRate);
  const amountAboveThreshold = Math.max(0, grossDividend - data.financialIncomeThreshold);
  const additionalTaxEstimate = amountAboveThreshold * toRate(data.additionalDividendTaxRate);
  const totalTax = withholdingTax + additionalTaxEstimate;
  const afterTaxDividend = Math.max(0, grossDividend - totalTax);
  return {
    grossDividend,
    withholdingTax,
    amountAboveThreshold,
    additionalTaxEstimate,
    totalTax,
    afterTaxDividend,
    monthlyAfterTaxDividend: afterTaxDividend / 12,
    effectiveTaxRate: grossDividend > 0 ? (totalTax / grossDividend) * 100 : 0
  };
}

function calculateForeignStockGainTax(data) {
  const gain = Math.max(0, data.foreignStockGain);
  const taxableGain = Math.max(0, gain - data.foreignStockBasicDeduction);
  const tax = taxableGain * toRate(data.foreignStockTaxRate);
  return {
    gain,
    basicDeduction: data.foreignStockBasicDeduction,
    taxableGain,
    tax,
    afterTaxGain: Math.max(0, gain - tax),
    effectiveTaxRate: gain > 0 ? (tax / gain) * 100 : 0
  };
}

function calculateRequiredDividendAsset(data) {
  const targetAnnualAfterTaxDividend = Math.max(0, data.targetMonthlyDividendAfterTax) * 12;
  const yieldRate = toRate(data.expectedDividendYield);
  const taxRate = toRate(data.dividendWithholdingRate + data.additionalDividendTaxRate);
  const reinvestmentRate = toRate(data.dividendReinvestmentRate);
  const spendableRate = Math.max(0, 1 - taxRate - reinvestmentRate);
  const netYieldRate = yieldRate * spendableRate;
  return {
    targetAnnualAfterTaxDividend,
    expectedDividendYield: data.expectedDividendYield,
    spendableRate: spendableRate * 100,
    netYieldRate: netYieldRate * 100,
    requiredAsset: netYieldRate > 0 ? targetAnnualAfterTaxDividend / netYieldRate : 0
  };
}

function toRate(value) {
  return Number(value || 0) / 100;
}

function renderScenarios(simulation) {
  document.querySelector('#scenarioGrid').innerHTML = simulation.scenarios.map((scenario) => `
    <article class="scenario-card"><div class="scenario-header"><strong>${scenario.retirementAge}세 퇴사</strong><span class="badge badge-${scenario.status}">${statusMeta[scenario.status].label}</span></div><dl><div><dt>추가 근무</dt><dd>${scenario.extraYears}년</dd></div><div><dt>고갈 나이</dt><dd>${formatAge(scenario.depletionAge)}</dd></div><div><dt>${simulation.inputs.simulationUntilAge}세 잔여 금융자산</dt><dd>${formatEok(scenario.finalFinancialAsset)}</dd></div></dl></article>
  `).join('');
}

function renderTable(rows) {
  document.querySelector('#yearlyTable').innerHTML = `<table><thead><tr><th>연도</th><th>나이</th><th>상태</th><th>금융자산</th><th>인출액</th><th>연금</th><th>순자산</th></tr></thead><tbody>${rows.map((row) => `<tr class="${row.financialAsset <= 0 ? 'depleted-row' : ''}"><td>${row.year}</td><td>${row.age}세</td><td>${row.status}</td><td>${formatEok(row.financialAsset)}</td><td>${formatEok(row.withdrawal)}</td><td>${formatEok(row.pensionIncome)}</td><td>${formatEok(row.netWorth)}</td></tr>`).join('')}</tbody></table>`;
}

document.querySelector('#mobileInputToggle').addEventListener('click', () => {
  const panel = document.querySelector('.input-panel');
  panel.classList.toggle('input-open');
  document.querySelector('#mobileInputToggle').textContent = panel.classList.contains('input-open') ? '입력 닫기' : '입력 수정';
});
document.querySelector('#bottomEditButton').addEventListener('click', () => {
  const panel = document.querySelector('.input-panel');
  panel.classList.add('input-open');
  document.querySelector('#mobileInputToggle').textContent = '입력 닫기';
  panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
});
document.querySelector('#bottomShareButton').addEventListener('click', async () => {
  await navigator.clipboard.writeText(buildShareUrl(normalizeInputs(inputs)));
  document.querySelector('#bottomShareButton').textContent = '복사 완료';
  window.setTimeout(() => { document.querySelector('#bottomShareButton').textContent = '내 결과 공유'; }, 1600);
});
document.querySelector('#resetButton').addEventListener('click', () => {
  inputs = { ...defaultInputs };
  localStorage.removeItem(storageKey);
  renderInputs();
  renderResults();
});

renderInputs();
renderResults();
if (hasSharedScenario) {
  window.setTimeout(() => trackAppEvent('scenario_loaded'), 0);
}
