import { buildSimulation, defaultInputs, normalizeInputs } from './utils/retirementSimulator.js';
import { formatAge, formatCompactMoney, formatEok, formatPercent, statusMeta } from './utils/formatters.js';
import { buildShareText, buildShareUrl, decodeInputsFromHash } from './utils/shareState.js';

const storageKey = 'toesanai-inputs-v1';

const fields = [
  { section: '기본', name: 'currentAge', label: '지금 내 나이', help: '만 나이 기준으로 입력하세요.', suffix: '세' },
  { section: '기본', name: 'targetRetirementAge', label: '퇴사하고 싶은 나이', help: '이 나이에 회사를 그만둔다고 가정합니다.', suffix: '세' },
  { section: '기본', name: 'startYear', label: '계산 시작 연도', help: '올해 기준이면 그대로 두면 됩니다.', suffix: '년' },
  { section: '자산', name: 'financialAsset', label: '바로 쓸 수 있는 투자·현금 자산', help: '예금, 주식, ETF, 펀드, 연금저축처럼 금융자산만 넣으세요.', suffix: '원', money: true },
  { section: '자산', name: 'realEstateValue', label: '내 집·부동산 예상 가치', help: '실거주 집도 순자산 계산에는 포함하지만 생활비 인출 재원은 아닙니다.', suffix: '원', money: true },
  { section: '자산', name: 'debt', label: '아직 남은 대출금', help: '주택담보대출, 신용대출 등 갚아야 할 총액입니다.', suffix: '원', money: true },
  { section: '현금흐름', name: 'monthlyInvestment', label: '퇴사 전 매달 모을 돈', help: '월급에서 생활비를 쓰고 남겨 투자할 수 있는 금액입니다.', suffix: '원', money: true },
  { section: '현금흐름', name: 'monthlyLivingCost', label: '퇴사 후 매달 쓸 생활비', help: '주거비, 식비, 보험료, 취미비까지 포함한 월 지출입니다.', suffix: '원', money: true },
  { section: '현금흐름', name: 'partTimeIncomeAfterRetirement', label: '퇴사 후 매달 벌 수 있는 돈', help: '현재 돈 가치로 입력하세요. 앱이 물가상승률을 반영해 계산합니다.', suffix: '원', money: true },
  { section: '연금', name: 'expectedPensionAge', label: '국민연금 받기 시작하는 나이', help: '예상 수령 시작 나이를 넣으세요.', suffix: '세' },
  { section: '연금', name: 'expectedMonthlyPension', label: '국민연금 월 예상 수령액', help: '현재 돈 가치로 입력하세요. 65세 이후에는 물가상승률을 반영해 계산합니다.', suffix: '원', money: true },
  { section: '가정', name: 'annualReturnRate', label: '투자 수익률', help: '금융자산이 매년 평균 몇 % 불어난다고 볼지입니다.', suffix: '%' },
  { section: '가정', name: 'inflationRate', label: '물가상승률', help: '생활비가 매년 몇 %씩 늘어난다고 볼지입니다.', suffix: '%' },
  { section: '가정', name: 'simulationUntilAge', label: '몇 살까지 버티는지 볼까요?', help: '보통 90세 기준으로 확인합니다.', suffix: '세' }
];

let inputs = loadInputs();
let inputStep = 0;

function loadInputs() {
  try {
    const saved = localStorage.getItem(storageKey);
    const shared = decodeInputsFromHash(window.location.hash);
    return shared ? { ...defaultInputs, ...shared } : saved ? { ...defaultInputs, ...JSON.parse(saved) } : { ...defaultInputs };
  } catch {
    return { ...defaultInputs };
  }
}

function saveInputs() {
  localStorage.setItem(storageKey, JSON.stringify(normalizeInputs(inputs)));
}

function renderInputs() {
  const inputGrid = document.querySelector('#inputGrid');
  const groupedFields = groupFields(fields);
  const currentSection = groupedFields[inputStep]?.[0] ?? '';
  document.querySelector('#mobileStepper').innerHTML = `
    <div><span>${inputStep + 1}</span><small>/ ${groupedFields.length}</small></div>
    <strong>${currentSection}</strong>
  `;
  document.querySelector('#mobileStepActions').innerHTML = `
    <button type="button" id="prevInputStep" ${inputStep === 0 ? 'disabled' : ''}>이전</button>
    <button type="button" id="nextInputStep">${inputStep < groupedFields.length - 1 ? '다음' : '결과 보기'}</button>
  `;

  inputGrid.innerHTML = groupedFields.map(([section, sectionFields], index) => `
    <div class="input-section ${index === inputStep ? 'active-section' : ''}">
      <h3>${section}</h3>
      ${sectionFields.map(({ name, label, help, suffix, money }) => `
        <label class="field">
          <span>${label}</span>
          <b>${help}</b>
          <div class="input-wrap">
            <input type="${money ? 'text' : 'number'}" inputmode="${money ? 'numeric' : ''}" value="${money ? formatInputNumber(inputs[name]) : inputs[name]}" data-field="${name}" data-money="${money ? 'true' : 'false'}" />
            <small>${suffix}</small>
          </div>
          ${money ? `<em>${formatCompactMoney(inputs[name])}</em>` : ''}
        </label>
      `).join('')}
    </div>
  `).join('');

  inputGrid.querySelectorAll('input').forEach((input) => {
    input.addEventListener('input', (event) => {
      const isMoney = event.target.dataset.money === 'true';
      const nextValue = isMoney ? event.target.value.replace(/[^\d-]/g, '') : event.target.value;
      inputs[event.target.dataset.field] = nextValue;
      if (isMoney) event.target.value = formatInputNumber(nextValue);
      saveInputs();
      const helper = event.target.closest('.field').querySelector('em');
      if (helper) helper.textContent = formatCompactMoney(nextValue);
      renderResults();
    });
  });

  document.querySelector('#prevInputStep').addEventListener('click', () => {
    inputStep = Math.max(0, inputStep - 1);
    renderInputs();
  });

  document.querySelector('#nextInputStep').addEventListener('click', () => {
    if (inputStep < groupedFields.length - 1) {
      inputStep += 1;
      renderInputs();
    } else {
      document.querySelector('.input-panel').classList.remove('input-open');
      document.querySelector('#mobileInputToggle').textContent = '입력 수정';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  });
}

function groupFields(items) {
  return Object.entries(
    items.reduce((groups, item) => {
      groups[item.section] = [...(groups[item.section] || []), item];
      return groups;
    }, {})
  );
}

function formatInputNumber(value) {
  const raw = String(value ?? '').replace(/[^\d-]/g, '');
  if (!raw || raw === '-') return raw;
  const sign = raw.startsWith('-') ? '-' : '';
  const digits = raw.replace('-', '');
  return `${sign}${Number(digits).toLocaleString('ko-KR')}`;
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
  document.querySelector('#bottomShareButton').textContent = '복사됨';
  window.setTimeout(() => {
    document.querySelector('#bottomShareButton').textContent = '링크 복사';
  }, 1600);
});

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

function renderGrowth(simulation, data) {
  document.querySelector('#growthPanel').innerHTML = `
    <div>
      <p class="eyebrow">공유</p>
      <h2>내 결과를 링크로 저장하기</h2>
      <p>
        입력값이 담긴 링크를 만들어 친구나 커뮤니티에서 바로 비교할 수 있습니다.
        앱 설치나 회원가입은 필요 없습니다.
      </p>
    </div>
    <div class="growth-actions">
      <button type="button" data-copy="link">계산 링크 복사</button>
      <button type="button" data-copy="summary">결과 요약 복사</button>
      <a href="#legal">안내 보기</a>
    </div>
  `;

  document.querySelectorAll('[data-copy]').forEach((button) => {
    button.addEventListener('click', async () => {
      const type = button.dataset.copy;
      const text = type === 'link'
        ? buildShareUrl(data)
        : `${buildShareText(simulation)}\n\n${buildShareUrl(data)}`;
      await navigator.clipboard.writeText(text);
      button.textContent = type === 'link' ? '링크 복사됨' : '요약 복사됨';
      window.setTimeout(() => {
        button.textContent = type === 'link' ? '계산 링크 복사' : '결과 요약 복사';
      }, 1800);
    });
  });
}

function renderDecision(simulation) {
  const {
    inputs: data,
    status,
    survivalScore,
    safeWithdrawalRate,
    requiredFireAssetByFourPercent,
    fireGap,
    bridgeYears,
    runwayYears,
    retirementFinancialAsset,
    targetResult
  } = simulation;
  const survivesTargetAge = !targetResult.depletionAge || targetResult.depletionAge > data.simulationUntilAge;
  const title = survivesTargetAge
    ? `${data.targetRetirementAge}세 퇴사 후 ${data.simulationUntilAge}세까지 고갈되지 않습니다`
    : `${data.targetRetirementAge}세 퇴사 시 ${targetResult.depletionAge}세에 고갈될 수 있습니다`;
  const gapText = fireGap <= 0 ? `${formatEok(Math.abs(fireGap))} 여유` : `${formatEok(fireGap)} 낮음`;
  const survivalText = survivesTargetAge ? '통과' : `${runwayYears}년`;

  document.querySelector('#decisionDashboard').innerHTML = `
    <div class="decision-main">
      <span class="badge badge-${status}">${statusMeta[status].label}</span>
      <h2>${title}</h2>
      <p>
        퇴사 시점 금융자산은 ${formatEok(retirementFinancialAsset)}이고 첫해 예상 인출률은 ${formatPercent(safeWithdrawalRate)}입니다.
        판정은 입력한 종료 나이까지 금융자산이 마이너스가 되는지로 계산합니다.
      </p>
      <div class="score-meter" aria-label="자산수명 점수">
        <span style="width: ${Math.min(100, Math.max(0, survivalScore))}%"></span>
      </div>
    </div>
    <div class="decision-score">
      <small>자산수명 점수</small>
      <strong>${survivalScore}</strong>
      <span>/ 100</span>
    </div>
    <div class="metric-strip">
      <article class="strip-card strip-${status}"><span>↗</span><div><small>${data.simulationUntilAge}세까지 자산수명</small><strong>${survivalText}</strong></div></article>
      <article class="strip-card"><span>✓</span><div><small>4% 룰 참고자산</small><strong>${formatEok(requiredFireAssetByFourPercent)}</strong></div></article>
      <article class="strip-card"><span>₩</span><div><small>보수 기준 차이</small><strong>${gapText}</strong></div></article>
      <article class="strip-card"><span>~</span><div><small>국민연금 전 공백기</small><strong>${bridgeYears}년</strong></div></article>
    </div>
  `;
}

function renderSummary(simulation) {
  const { inputs: data, targetResult, earliestRetirementAge, status, retirementFinancialAsset, safeWithdrawalRate } = simulation;
  const survivesTargetAge = !targetResult.depletionAge || targetResult.depletionAge > data.simulationUntilAge;
  const verdictText = survivesTargetAge ? `${data.simulationUntilAge}세까지 고갈 없음` : `${targetResult.depletionAge}세 고갈 예상`;
  const depletionText = targetResult.depletionAge ? `${targetResult.depletionAge}세` : `${data.simulationUntilAge}세 이후`;
  const cards = [
    ['목표 퇴사 판정', verdictText, `${data.targetRetirementAge}세 퇴사 기준`, status, statusMeta[status].label],
    ['자산 고갈 나이', depletionText, targetResult.depletionAge ? '금융자산이 0원 이하가 되는 시점' : '시뮬레이션 기간 내 고갈 없음', status, statusMeta[status].label],
    ['가장 빠른 퇴사 가능 나이', formatAge(earliestRetirementAge), `${data.simulationUntilAge}세까지 금융자산 유지 기준`, earliestRetirementAge ? 'stable' : 'risk', earliestRetirementAge ? '안정' : '위험'],
    ['퇴사 시점 금융자산', formatEok(retirementFinancialAsset), `첫해 예상 인출률 ${formatPercent(safeWithdrawalRate)}`, 'neutral', '정보']
  ];

  document.querySelector('#summaryGrid').innerHTML = cards.map(([label, value, detail, tone, badge]) => `
    <article class="summary-card tone-${tone}">
      <div class="card-top">
        <span class="card-icon">₩</span>
        <span class="badge badge-${tone}">${badge}</span>
      </div>
      <p>${label}</p>
      <strong>${value}</strong>
      <small>${detail}</small>
    </article>
  `).join('');
}

function renderInsight(simulation) {
  const {
    inputs: data,
    targetResult,
    earliestRetirementAge,
    status,
    gainedYears,
    extraAssetFromOneMoreYear,
    safeWithdrawalRate,
    fireGap,
    bridgeYears,
    retirementFinancialAsset
  } = simulation;
  const survivesTargetAge = !targetResult.depletionAge || targetResult.depletionAge > data.simulationUntilAge;
  const isPensionGapRisk = targetResult.depletionAge && targetResult.depletionAge < data.expectedPensionAge;
  const oneMoreYearMessage = gainedYears > 0
    ? `1년 더 근무하면 자산수명이 약 ${gainedYears}년 늘어납니다.`
    : `1년 더 근무해도 고갈 나이는 같지만, ${data.simulationUntilAge}세 잔여 금융자산은 약 ${formatEok(extraAssetFromOneMoreYear)} 늘어납니다.`;
  const fourPercentMessage = fireGap > 0
    ? `4% 룰만 단독으로 보면 퇴사 시점 금융자산이 참고 기준보다 약 ${formatEok(fireGap)} 낮습니다. 다만 이 앱의 퇴사 판정은 4% 룰이 아니라 입력한 수익률, 물가, 국민연금, 종료 나이를 모두 반영한 자산 고갈 여부입니다.`
    : `4% 룰 기준으로도 퇴사 시점 금융자산이 약 ${formatEok(Math.abs(fireGap))} 더 많습니다.`;
  const pensionGapMessage = bridgeYears > 0
    ? isPensionGapRisk
      ? `국민연금을 받기 전 ${bridgeYears}년 동안 생활비를 금융자산으로 버텨야 하는데, 이 기간 전에 자산이 먼저 고갈될 수 있습니다.`
      : `국민연금을 받기 전 ${bridgeYears}년은 월급과 연금이 모두 없는 공백기입니다. 현재 입력값에서는 이 구간을 통과합니다.`
    : '퇴사 시점이 국민연금 수령 이후라 연금 전 공백기는 거의 없습니다.';
  const messages = [
    survivesTargetAge
      ? `사용자가 입력한 종료 나이인 ${data.simulationUntilAge}세까지 금융자산이 고갈되지 않습니다. 이 기준에서는 ${data.targetRetirementAge}세 퇴사가 가능합니다.`
      : `${data.targetRetirementAge}세에 퇴사하면 ${targetResult.depletionAge}세에 금융자산이 고갈될 수 있어 입력한 ${data.simulationUntilAge}세까지 버티기 어렵습니다.`,
    `목표 퇴사 첫해 예상 인출률은 ${formatPercent(safeWithdrawalRate)}이고, 퇴사 시점 금융자산은 약 ${formatEok(retirementFinancialAsset)}입니다.`,
    pensionGapMessage,
    oneMoreYearMessage,
    fourPercentMessage,
    '국민연금과 퇴사 후 소득은 현재 돈 가치로 입력한 금액에 물가상승률을 반영해 계산합니다.',
    earliestRetirementAge
      ? `${data.simulationUntilAge}세까지 고갈되지 않는 가장 빠른 퇴사 가능 나이는 ${formatAge(earliestRetirementAge)}입니다.`
      : '현재 가정에서는 70세까지 근무해도 목표 종료 나이까지 금융자산 유지가 어렵습니다.'
  ];

  document.querySelector('#insightReport').innerHTML = `
    <div class="section-heading">
      <div>
        <p class="eyebrow">AI 리포트</p>
        <h2>퇴사나이 해석</h2>
      </div>
      <span class="badge badge-${status}">${statusMeta[status].label}</span>
    </div>
    <div class="insight-title">
      <span>▤</span>
      <strong>${survivesTargetAge ? '입력한 나이까지는 자산수명이 충분합니다' : statusMeta[status].summary}</strong>
    </div>
    <ul>${messages.map((message) => `<li>${message}</li>`).join('')}</ul>
  `;
}

function renderScenarios(simulation) {
  document.querySelector('#scenarioGrid').innerHTML = simulation.scenarios.map((scenario) => `
    <article class="scenario-card">
      <div class="scenario-header">
        <strong>${scenario.retirementAge}세 퇴사</strong>
        <span class="badge badge-${scenario.status}">${statusMeta[scenario.status].label}</span>
      </div>
      <dl>
        <div><dt>추가 근무</dt><dd>${scenario.extraYears}년</dd></div>
        <div><dt>고갈 나이</dt><dd>${formatAge(scenario.depletionAge)}</dd></div>
        <div><dt>${simulation.inputs.simulationUntilAge}세 잔여 금융자산</dt><dd>${formatEok(scenario.finalFinancialAsset)}</dd></div>
      </dl>
    </article>
  `).join('');
}

function renderTable(rows) {
  document.querySelector('#yearlyTable').innerHTML = `
    <table>
      <thead>
        <tr>
          <th>연도</th>
          <th>나이</th>
          <th>상태</th>
          <th>금융자산</th>
          <th>인출액</th>
          <th>순자산</th>
        </tr>
      </thead>
      <tbody>
        ${rows.map((row) => `
          <tr class="${row.financialAsset <= 0 ? 'depleted-row' : ''}">
            <td>${row.year}</td>
            <td>${row.age}세</td>
            <td>${row.status}</td>
            <td>${formatEok(row.financialAsset)}</td>
            <td>${formatEok(row.withdrawal)}</td>
            <td>${formatEok(row.netWorth)}</td>
          </tr>
        `).join('')}
      </tbody>
    </table>
  `;
}

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
