import { buildSimulation, defaultInputs, normalizeInputs, simulateRetirement } from './utils/retirementSimulator.js';
import { formatAge, formatCompactMoney, formatEok, formatInputNumber, formatPercent, statusMeta } from './utils/formatters.js';
import { buildShareText, buildShareUrl, decodeInputsFromHash } from './utils/shareState.js';

const storageKey = 'toesanai-inputs-v2';
const fields = [
  { section: '기본', name: 'currentAge', label: '지금 내 나이', help: '만 나이에 가깝게 입력하면 됩니다.', suffix: '세' },
  { section: '기본', name: 'targetRetirementAge', label: '퇴사하고 싶은 나이', help: '이 나이에 회사를 그만둔다고 가정합니다.', suffix: '세' },
  { section: '기본', name: 'startYear', label: '계산 시작 연도', help: '올해 기준이면 그대로 두면 됩니다.', suffix: '년' },
  { section: '자산', name: 'financialAsset', label: '생활비로 쓸 수 있는 금융자산', help: '예금, 주식, ETF처럼 퇴사 후 생활비로 인출할 수 있는 돈입니다.', suffix: '원', money: true },
  { section: '자산', name: 'realEstateValue', label: '보유 부동산 가치', help: '순자산에는 넣지만 생활비 인출 재원으로는 보지 않습니다.', suffix: '원', money: true },
  { section: '자산', name: 'debt', label: '총 대출 잔액', help: '주택담보대출, 신용대출 등 갚아야 할 원금 총액입니다.', suffix: '원', money: true },
  { section: '현금흐름', name: 'monthlyInvestment', label: '퇴사 전 월 추가투자액', help: '월급에서 생활비를 쓰고 남아 매달 투자할 수 있는 금액입니다.', suffix: '원', money: true },
  { section: '현금흐름', name: 'monthlyLivingCost', label: '퇴사 후 월 생활비', help: '현재 돈 가치로 입력하세요. 앱이 물가상승률을 반영해 매년 늘립니다.', suffix: '원', money: true },
  { section: '현금흐름', name: 'partTimeIncomeAfterRetirement', label: '퇴사 후 월 추가소득', help: '부업, 프리랜서, 임대소득 등 퇴사 후에도 예상되는 월 소득입니다.', suffix: '원', money: true },
  { section: '연금', name: 'expectedPensionAge', label: '국민연금 시작 나이', help: '예상 수령 시작 나이를 넣으세요.', suffix: '세' },
  { section: '연금', name: 'expectedMonthlyPension', label: '국민연금 월 예상액', help: '현재 돈 가치로 입력하세요. 계산 때 물가상승률을 반영합니다.', suffix: '원', money: true },
  { section: '가정', name: 'annualReturnRate', label: '연평균 투자수익률', help: '금융자산이 매년 평균 몇 % 불어난다고 볼지입니다.', suffix: '%' },
  { section: '가정', name: 'inflationRate', label: '연평균 물가상승률', help: '생활비와 연금·부업 소득이 매년 몇 %씩 늘어난다고 봅니다.', suffix: '%' },
  { section: '가정', name: 'simulationUntilAge', label: '계산 종료 나이', help: '이 나이까지 금융자산이 버티는지 확인합니다.', suffix: '세' }
];

let inputs = loadInputs();
let inputStep = 0;

function loadInputs() {
  try {
    const shared = decodeInputsFromHash(window.location.hash);
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
  renderScenarios(simulation);
  renderTable(simulation.targetResult.rows);
}

function renderDecision(simulation) {
  const { inputs: data, status, survivalScore, safeWithdrawalRate, requiredFireAssetByFourPercent, fireGap, bridgeYears, retirementFinancialAsset, firstRetirementExpense, finalFinancialAsset, targetResult } = simulation;
  const survives = !targetResult.depletionAge || targetResult.depletionAge > data.simulationUntilAge;
  const title = survives ? `${data.targetRetirementAge}세 퇴사 가능성이 높습니다` : `${data.targetRetirementAge}세 퇴사 시 ${targetResult.depletionAge}세에 고갈될 수 있습니다`;
  const gapText = fireGap <= 0 ? `${formatEok(Math.abs(fireGap))} 여유` : `${formatEok(fireGap)} 부족`;
  document.querySelector('#decisionDashboard').innerHTML = `
    <div class="decision-main">
      <span class="badge badge-${status}">${statusMeta[status].label}</span>
      <h2>${title}</h2>
      <p>목표 퇴사 시점 금융자산은 ${formatEok(retirementFinancialAsset)}이고, 첫해 예상 인출액은 ${formatEok(firstRetirementExpense)}입니다. 이 앱은 연 생활비 25배 기준과 함께, 사용자가 정한 ${data.simulationUntilAge}세까지 실제 고갈 여부를 우선 봅니다.</p>
      <div class="score-meter" aria-label="자산수명 점수"><span style="width: ${Math.min(100, Math.max(0, survivalScore))}%"></span></div>
    </div>
    <div class="decision-score"><small>자산수명 점수</small><strong>${survivalScore}</strong><span>/ 100</span></div>
    <div class="metric-strip">
      <article class="strip-card strip-${status}"><span>결과</span><div><small>계산 종료 나이 기준</small><strong>${survives ? '고갈 없음' : `${targetResult.depletionAge}세 고갈`}</strong></div></article>
      <article class="strip-card"><span>안전</span><div><small>연 생활비 25배 기준</small><strong>${formatEok(requiredFireAssetByFourPercent)}</strong></div></article>
      <article class="strip-card"><span>차이</span><div><small>안전 기준 대비 차이</small><strong>${gapText}</strong></div></article>
      <article class="strip-card"><span>연금 전</span><div><small>국민연금 전까지의 기간</small><strong>${bridgeYears}년</strong></div></article>
      <article class="strip-card"><span>잔액</span><div><small>계산 종료 나이의 금융자산</small><strong>${formatEok(finalFinancialAsset)}</strong></div></article>
    </div>
  `;
}

function renderGrowth(simulation, data) {
  document.querySelector('#growthPanel').innerHTML = `
    <div><p class="eyebrow">공유</p><h2>링크 하나로 바로 계산하게 만들기</h2><p>카톡, 커뮤니티, 블로그에서 누르면 앱 설치 없이 모바일 화면에서 바로 열립니다. 입력값도 링크에 담아 비교 시나리오로 공유할 수 있습니다.</p></div>
    <div class="growth-actions"><button type="button" data-copy="link">계산 링크 복사</button><button type="button" data-copy="summary">결과 요약 복사</button></div>
  `;
  document.querySelectorAll('[data-copy]').forEach((button) => button.addEventListener('click', async () => {
    const text = button.dataset.copy === 'link' ? buildShareUrl(data) : `${buildShareText(simulation)}\n\n${buildShareUrl(data)}`;
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
    ['목표까지 필요한 월 투자액', requiredMonthlyValue, requiredMonthlyDetail, requiredMonthlyInvestment === null ? 'risk' : requiredMonthlyInvestment <= data.monthlyInvestment ? 'stable' : 'caution', requiredMonthlyInvestment === null ? '위험' : requiredMonthlyInvestment <= data.monthlyInvestment ? '충분' : '추가 필요'],
    ['목표 퇴사 판정', survives ? `${data.simulationUntilAge}세까지 고갈 없음` : `${targetResult.depletionAge}세 고갈 예상`, `${data.targetRetirementAge}세 퇴사 기준`, status, statusMeta[status].label],
    ['가장 빠른 퇴사 가능 나이', formatAge(earliestRetirementAge), `${data.simulationUntilAge}세까지 버티는 가장 이른 나이`, earliestRetirementAge ? 'stable' : 'risk', earliestRetirementAge ? '안정' : '위험'],
    ['퇴사 첫해 인출률', formatPercent(safeWithdrawalRate), '첫해 인출액 ÷ 퇴사 시점 금융자산', safeWithdrawalRate >= 8 ? 'caution' : 'neutral', safeWithdrawalRate >= 8 ? '주의' : '정보'],
    [`${data.simulationUntilAge}세 잔여 금융자산`, formatEok(finalFinancialAsset), '사용자가 입력한 종료 나이 기준', finalFinancialAsset > 0 ? 'stable' : 'risk', finalFinancialAsset > 0 ? '안정' : '위험'],
    ['퇴사 시점 금융자산', formatEok(retirementFinancialAsset), '부동산을 제외하고 실제 인출 가능한 자산', 'neutral', '정보']
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
  const pensionText = pensionStartWithdrawal === null ? '입력한 종료 나이가 국민연금 시작 전이라, 연금 효과는 이번 계산에 들어가지 않습니다.' : `국민연금 시작 이후 예상 연간 인출액은 ${formatEok(pensionStartWithdrawal)}입니다. 연금과 부업 소득도 물가상승률을 반영해 계산했습니다.`;
  const fourPercentText = fireGap > 0 ? `연 생활비 25배 기준으로 보면 ${formatEok(fireGap)} 정도 부족합니다. 다만 퇴사나이의 핵심 판정은 이 기준만이 아니라 ${data.simulationUntilAge}세까지 고갈 여부입니다.` : `연 생활비 25배 기준으로도 ${formatEok(Math.abs(fireGap))} 정도 여유가 있습니다.`;
  const workMoreText = gainedYears > 0 ? `1년 더 근무하면 자산수명이 약 ${gainedYears}년 늘어납니다.` : `1년 더 근무해도 고갈 나이는 같지만, ${data.simulationUntilAge}세 잔여 금융자산은 약 ${formatEok(extraAssetFromOneMoreYear)} 늘어납니다.`;
  const messages = [
    survives ? `${data.targetRetirementAge}세 퇴사는 입력한 ${data.simulationUntilAge}세 기준에서 가능성이 높습니다. 남는 돈을 크게 남기는 계산이 아니라, 고갈되지 않는지를 먼저 보는 방식입니다.` : `${data.targetRetirementAge}세 퇴사는 ${targetResult.depletionAge}세에 금융자산이 고갈될 수 있어 조정이 필요합니다.`,
    `퇴사 첫해 생활비는 ${formatEok(firstYearLivingCost)}, 부업 소득은 ${formatEok(firstYearPartTimeIncome)}, 국민연금 반영액은 ${formatEok(firstYearPensionIncome)}입니다. 실제 인출해야 하는 돈은 ${formatEok(firstRetirementExpense)}입니다.`,
    `퇴사 시점 실제 FIRE 가능 자산은 부동산을 뺀 금융자산 기준 ${formatEok(retirementFinancialAsset)}입니다.`,
    bridgeYears > 0 ? `연금 전 공백기는 ${bridgeYears}년입니다. 여기서 말하는 공백기는 퇴사 후 국민연금을 받기 전까지 금융자산과 부업 소득으로 생활비를 버티는 기간입니다.` : '퇴사 시점이 국민연금 수령 이후라 연금 전 공백기는 거의 없습니다.',
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
  window.setTimeout(() => { document.querySelector('#bottomShareButton').textContent = '링크 복사'; }, 1600);
});
document.querySelector('#resetButton').addEventListener('click', () => {
  inputs = { ...defaultInputs };
  localStorage.removeItem(storageKey);
  renderInputs();
  renderResults();
});

renderInputs();
renderResults();
document.querySelector('.input-panel').classList.add('input-open');
document.querySelector('#mobileInputToggle').textContent = '입력 닫기';
