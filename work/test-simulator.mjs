import { simulateRetirement, buildSimulation, findEarliestRetirementAge, normalizeInputs } from '../src/utils/retirementSimulator.js';
import { buildGrowthSeries } from '../src/firemap-v2/scenarios.js';
import { earlyClaim } from '../src/firemap-v2/pension.js';

const toEok = (value) => value / 100000000;

function fail(message) {
  console.error(message);
  process.exit(1);
}

function check(label, actual, expected, tolerance = 0.05) {
  const actualEok = toEok(actual);
  if (Math.abs(actualEok - expected) > tolerance) {
    fail(`${label}: expected ${expected} eok, got ${actualEok.toFixed(2)} eok`);
  }
}

function assert(condition, message) {
  if (!condition) fail(message);
}

function getRow(result, age) {
  return result.rows.find((row) => row.age === age);
}

function comparableEndAge(result, untilAge) {
  return result.depletionAge ?? untilAge + 1;
}

const scenarioA = {
  currentAge: 34,
  targetRetirementAge: 36,
  startYear: 2026,
  financialAsset: 270000000,
  realEstateValue: 240000000,
  debt: 90000000,
  monthlyInvestment: 1000000,
  monthlyLivingCost: 3000000,
  annualReturnRate: 10,
  inflationRate: 3,
  expectedPensionAge: 65,
  expectedMonthlyPension: 1000000,
  partTimeIncomeAfterRetirement: 0,
  simulationUntilAge: 80
};

const scenarioB = {
  currentAge: 34,
  targetRetirementAge: 39,
  startYear: 2026,
  financialAsset: 230000000,
  realEstateValue: 240000000,
  debt: 90000000,
  monthlyInvestment: 1000000,
  monthlyLivingCost: 5000000,
  annualReturnRate: 8,
  inflationRate: 3,
  expectedPensionAge: 65,
  expectedMonthlyPension: 1000000,
  partTimeIncomeAfterRetirement: 0,
  simulationUntilAge: 90
};

const resultA = simulateRetirement(scenarioA);
check('scenarioA age80 financialAsset', getRow(resultA, 80).financialAsset, -24.44);

const resultB = simulateRetirement(scenarioB);
check('scenarioB age80 financialAsset', getRow(resultB, 80).financialAsset, -46.51);
check('scenarioB age90 financialAsset', getRow(resultB, 90).financialAsset, -68.59);

const base = { ...scenarioB };
const workLonger = simulateRetirement(base, base.targetRetirementAge + 1);
assert(
  comparableEndAge(workLonger, base.simulationUntilAge) >= comparableEndAge(resultB, base.simulationUntilAge),
  'Invariant failed: working longer should not shorten asset runway.'
);

const lowerLivingCost = simulateRetirement({ ...base, monthlyLivingCost: base.monthlyLivingCost - 1000000 });
assert(
  comparableEndAge(lowerLivingCost, base.simulationUntilAge) >= comparableEndAge(resultB, base.simulationUntilAge),
  'Invariant failed: lower living cost should not shorten asset runway.'
);

const higherLivingCost = simulateRetirement({ ...base, monthlyLivingCost: base.monthlyLivingCost + 1000000 });
assert(
  comparableEndAge(higherLivingCost, base.simulationUntilAge) <= comparableEndAge(resultB, base.simulationUntilAge),
  'Invariant failed: higher living cost should not extend asset runway.'
);

const higherReturn = simulateRetirement({ ...base, annualReturnRate: base.annualReturnRate + 2 });
assert(
  higherReturn.finalFinancialAsset >= resultB.finalFinancialAsset,
  'Invariant failed: higher return should not reduce final financial asset.'
);

const morePartTimeIncome = simulateRetirement({ ...base, partTimeIncomeAfterRetirement: 1000000 });
assert(
  comparableEndAge(morePartTimeIncome, base.simulationUntilAge) >= comparableEndAge(resultB, base.simulationUntilAge),
  'Invariant failed: retirement side income should not shorten asset runway.'
);

// --- 추가 불변식 (물가·연금·음수복리) ---

// (1) 생활비 = 기준 × (1+물가)^경과연수  — 인플레 인덱싱 정확성
{
  const r = simulateRetirement(scenarioB); // 물가 3%, 퇴사 39
  const c50 = getRow(r, 50).baseLivingCost;
  const c70 = getRow(r, 70).baseLivingCost;
  const ratio = c70 / c50;
  const expected = Math.pow(1 + scenarioB.inflationRate / 100, 20);
  assert(Math.abs(ratio - expected) < 0.01, `Invariant failed: 생활비 인플레 인덱싱 어긋남 (ratio ${ratio.toFixed(3)} vs ${expected.toFixed(3)})`);
}

// (2) 물가를 올리면 자산수명이 절대 늘어나지 않는다
{
  const base = simulateRetirement(scenarioB);
  const higherInf = simulateRetirement({ ...scenarioB, inflationRate: scenarioB.inflationRate + 2 });
  assert(
    comparableEndAge(higherInf, scenarioB.simulationUntilAge) <= comparableEndAge(base, scenarioB.simulationUntilAge),
    'Invariant failed: 물가가 오르면 자산수명이 늘어나면 안 됨.'
  );
}

// (3) 고갈 이후 자산은 수익률로 음수 복리되지 않는다 (연 감소폭 ≈ 인출액)
{
  const r = simulateRetirement(scenarioB);
  if (r.depletionAge && r.depletionAge < scenarioB.simulationUntilAge) {
    const age = r.depletionAge + 2; // 고갈 이후 확실한 연도
    const cur = getRow(r, age), prev = getRow(r, age - 1);
    if (cur && prev && prev.financialAsset < 0) {
      const delta = cur.financialAsset - prev.financialAsset; // 음수
      assert(Math.abs(delta + cur.withdrawal) < 1, 'Invariant failed: 고갈 후 자산이 수익률로 음수 복리됨(감소폭≠인출액).');
    }
  }
}

// (4) 국민연금 개시 후 인출액이 줄어든다 (연금>0)
{
  const r = simulateRetirement(scenarioB); // 연금 65세 월100만
  const before = getRow(r, scenarioB.expectedPensionAge - 1).withdrawal;
  const after = getRow(r, scenarioB.expectedPensionAge).withdrawal;
  assert(after < before, `Invariant failed: 연금 개시 후 인출이 줄지 않음 (before ${Math.round(before)} after ${Math.round(after)}).`);
}

// (5) 적립 기간: 0(기본)=퇴사까지와 동일, 기간을 줄이면 최종자산이 늘지 않는다
{
  const full = simulateRetirement({ ...scenarioB, savingYears: 0 });
  const untilRetire = simulateRetirement({ ...scenarioB, savingYears: scenarioB.targetRetirementAge - scenarioB.currentAge });
  assert(Math.abs(full.finalFinancialAsset - untilRetire.finalFinancialAsset) < 1, 'Invariant failed: savingYears 0이 퇴사까지 저축과 다름.');
  const shorter = simulateRetirement({ ...scenarioB, savingYears: 3 });
  assert(shorter.finalFinancialAsset <= full.finalFinancialAsset + 1, 'Invariant failed: 적립 기간을 줄였는데 최종자산이 늘어남.');
}

// (6) 첫해(시작 시점) 자산은 시작 자산 그대로 — 수익률·저축 미적용
{
  const r = simulateRetirement(scenarioB);
  assert(Math.abs(r.rows[0].financialAsset - scenarioB.financialAsset) < 1, 'Invariant failed: 첫해 자산이 시작 자산과 다름(첫해 성장/저축이 적용됨).');
  assert(r.rows[0].investmentAdded === 0, 'Invariant failed: 첫해에 저축이 적용됨.');
}

// (7) 원금 vs 불어난 돈 분해: 원금+수익=총자산, 적립 구간 동안 원금 단조 비감소
{
  const sim = buildSimulation(scenarioB);
  const g = buildGrowthSeries(sim);
  assert(g.ages.length === sim.targetResult.rows.length, 'Invariant failed: growth 시리즈 길이 불일치.');
  for (let i = 0; i < g.ages.length; i += 1) {
    assert(Math.abs((g.principal[i] + g.gains[i]) - g.total[i]) < 1, `Invariant failed: 원금+수익 != 총자산 (age ${g.ages[i]}).`);
    assert(g.gains[i] >= -1 && g.principal[i] >= -1, `Invariant failed: 원금/수익 음수 (age ${g.ages[i]}).`);
  }
  for (let i = 1; i < g.ages.length; i += 1) {
    if (g.ages[i] <= scenarioB.targetRetirementAge) {
      assert(g.principal[i] >= g.principal[i - 1] - 1, `Invariant failed: 적립 구간 원금이 감소 (age ${g.ages[i]}).`);
    }
  }
}


// ── 2026-09-14 계산 감사에서 나온 오류를 다시 막는 테스트 ──────────────────────────

// (8) 배당 인출소득은 결과를 바꾸면 안 된다 — 연 수익률에 배당이 이미 들어 있다(P1)
{
  const base = { ...scenarioA };
  const withDiv = buildSimulation({ ...base, dividendIncomeMonthly: 2000000 });
  const without = buildSimulation(base);
  assert(withDiv.earliestRetirementAge === without.earliestRetirementAge,
    'Invariant failed: 배당 인출소득이 파이어 나이를 바꿈(이중 계산).');
}

// (9) 필요 자산은 오늘 화폐 — 미래 명목보다 작고, 물가로 되돌리면 명목과 같아야 한다(P3)
{
  const sim = buildSimulation(scenarioA);
  const years = Math.max(0, scenarioA.targetRetirementAge - scenarioA.currentAge);
  const f = Math.pow(1 + (scenarioA.inflationRate || 0) / 100, years);
  assert(sim.requiredFireAssetNominal > 0, 'Invariant failed: 명목 필요자산이 없음.');
  assert(sim.requiredFireAssetByFourPercent < sim.requiredFireAssetNominal,
    'Invariant failed: 오늘 가치 필요자산이 명목보다 작지 않음.');
  assert(Math.abs(sim.requiredFireAssetByFourPercent * f - sim.requiredFireAssetNominal) < 1000,
    'Invariant failed: 오늘 가치 × 물가 != 명목 필요자산.');
}

// (10) 배당세(investType 2)는 파이어 전에도 매년 떼여야 한다(P5)
{
  const sim = buildSimulation({ ...scenarioA, investType: 2, dividendYield: 4 });
  const before = sim.targetResult.rows.filter((r) => r.age < scenarioA.targetRetirementAge);
  const taxed = before.reduce((acc, r) => acc + (r.investTax || 0), 0);
  assert(taxed > 0, 'Invariant failed: 적립기 배당세가 0원.');
}

// (11) 예전 27.5% 구간 검사는 잘못된 규칙이라 삭제 — (21)에서 22% 단일로 검사한다.

// (12) 국민연금 연기수령은 가산돼야 한다(P9)
{
  const late = earlyClaim(1000000, 65, 68);
  assert(late.monthly > 1000000, 'Invariant failed: 연기수령인데 연금이 늘지 않음.');
  const early = earlyClaim(1000000, 65, 60);
  assert(early.monthly === 700000, 'Invariant failed: 조기수령 5년 감액이 30%가 아님.');
}

// (13) 회계 항등식 — 인출 = max(0, 생활비 − 부업 − 연금 − 배당 − 임대)(회귀 방지)
{
  const sim = buildSimulation({ ...scenarioA, partTimeIncomeAfterRetirement: 500000, monthlyRentalIncome: 300000 });
  for (const r of sim.targetResult.rows) {
    const expect = Math.max(0, r.livingCost - r.partTimeIncome - r.pensionIncome - (r.dividendIncome || 0) - r.rentalIncome);
    assert(Math.abs(r.withdrawal - expect) < 1, `Invariant failed: 인출 항등식 불일치 (age ${r.age}).`);
  }
}

// (14) 부동산·부채는 파이어 나이에 영향이 없어야 한다(설계 의도 고정)
{
  const a = buildSimulation(scenarioA).earliestRetirementAge;
  const b = buildSimulation({ ...scenarioA, realEstateValue: 2000000000, debt: 500000000 }).earliestRetirementAge;
  assert(a === b, 'Invariant failed: 부동산·부채가 파이어 나이를 바꿈.');
}

// (15) 건보료 반영 == 생활비에 같은 금액을 더한 것(문구 충돌을 테스트로 박제, P11)
{
  const m = 200000;
  const withHi = buildSimulation({ ...scenarioA, healthInsuranceEnabled: 1, monthlyHealthInsurance: m });
  const inCost = buildSimulation({ ...scenarioA, monthlyLivingCost: scenarioA.monthlyLivingCost + m });
  assert(withHi.earliestRetirementAge === inCost.earliestRetirementAge,
    'Invariant failed: 건보료 반영과 생활비 가산의 결과가 다름.');
}

console.log('Simulation regression and invariant tests passed.');

// (16) 필요 자산과 파이어 나이는 같은 잣대여야 한다.
// 지금 자산이 '필요 자산'에 닿으면 파이어 가능 나이가 현재 나이가 되고, 그 아래면 안 된다.
{
  const base = { currentAge: 35, targetRetirementAge: 50, financialAsset: 300000000, monthlyInvestment: 2000000, monthlyLivingCost: 2500000 };
  const need = buildSimulation(base).requiredAssetNow;
  assert(need > 0, '(16) 필요 자산이 계산되어야 한다');
  assert(findEarliestRetirementAge({ ...base, financialAsset: need }) === base.currentAge, '(16) 필요 자산만큼 있으면 지금 파이어할 수 있어야 한다');
  assert(findEarliestRetirementAge({ ...base, financialAsset: need * 0.9 }) > base.currentAge, '(16) 필요 자산에 못 미치면 지금 파이어할 수 없어야 한다');
}
console.log('(16) required-asset / fire-age same yardstick OK');

// (17) 화면에 나란히 놓는 금액은 전부 오늘 돈이어야 한다.
// 결과는 파이어 가능 나이 때 자산, 바꿔보기는 목표 나이 때 자산을 보여준다.
// 한쪽만 명목이면 '나중 나이인데 돈이 더 적은' 모순이 화면에 나온다.
{
  const s = buildSimulation({ currentAge: 35, targetRetirementAge: 49, financialAsset: 100000000, monthlyInvestment: 3000000, monthlyLivingCost: 3000000, inflationRate: 3.1 });
  const f = Math.pow(1 + 0.031, 49 - 35);
  assert(Math.abs(s.retirementFinancialAssetToday * f - s.retirementFinancialAsset) < 1000, '(17) 목표 나이 자산의 오늘 돈 × 물가 = 명목');
  assert(s.retirementFinancialAssetToday < s.atEarliest.assetToday, '(17) 목표 49세보다 파이어 가능 55세에 자산이 더 많아야 한다');
}
console.log('(17) today-money across screens OK');

// (18) 무작위 1,000건 — 사람이 짠 예제로는 안 걸리는 모순을 잡는다.
// 파이어 나이의 최소성, 목표와 가능 나이의 앞뒤 관계, 필요 자산의 경계, 오늘 돈 환산을 한꺼번에 본다.
{
  let a = 20250914 >>> 0;
  const rng = () => { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  const pick = (arr) => arr[Math.floor(rng() * arr.length)];
  for (let n = 0; n < 1000; n += 1) {
    const currentAge = 20 + Math.floor(rng() * 50);
    const i = {
      currentAge,
      targetRetirementAge: currentAge + Math.floor(rng() * 35),
      financialAsset: Math.floor(rng() * 2e9),
      monthlyInvestment: Math.floor(rng() * 8e6),
      monthlyLivingCost: 500000 + Math.floor(rng() * 7e6),
      annualReturnRate: +(rng() * 12).toFixed(1),
      inflationRate: +(rng() * 6).toFixed(1),
      expectedPensionAge: pick([60, 62, 63, 65]),
      expectedMonthlyPension: Math.floor(rng() * 2e6),
      partTimeIncomeAfterRetirement: Math.floor(rng() * 2e6),
      realEstateValue: Math.floor(rng() * 1e9),
      debt: Math.floor(rng() * 5e8),
      savingYears: pick([0, 5, 10, 20]),
      investType: pick([0, 1, 2, 3]),
      simulationUntilAge: pick([85, 90, 95])
    };
    const s = buildSimulation(i);
    const until = i.simulationUntilAge;
    const survives = (r) => !r.depletionAge || r.depletionAge > until;
    if (s.earliestRetirementAge) {
      assert(survives(simulateRetirement(i, s.earliestRetirementAge)), `(18) 가능 나이인데 자산이 마름 ${JSON.stringify(i)}`);
      if (s.earliestRetirementAge > i.currentAge) {
        assert(!survives(simulateRetirement(i, s.earliestRetirementAge - 1)), `(18) 더 이른 나이도 되는데 못 찾음 ${JSON.stringify(i)}`);
      }
    }
    if (survives(s.targetResult) && i.targetRetirementAge <= 70) {
      assert(s.earliestRetirementAge != null && s.earliestRetirementAge <= i.targetRetirementAge, `(18) 목표는 되는데 가능 나이가 더 뒤 ${JSON.stringify(i)}`);
    }
    if (s.requiredAssetNow != null) {
      assert(findEarliestRetirementAge({ ...i, financialAsset: s.requiredAssetNow }) === i.currentAge, `(18) 필요 자산인데 지금 파이어 불가 ${JSON.stringify(i)}`);
    }
    const f = Math.pow(1 + i.inflationRate / 100, Math.max(0, i.targetRetirementAge - i.currentAge));
    assert(Math.abs(s.retirementFinancialAssetToday * f - s.retirementFinancialAsset) < 1000, `(18) 오늘 돈 환산 오류 ${JSON.stringify(i)}`);
    for (const [k, v] of Object.entries(s)) {
      assert(!(typeof v === 'number' && !Number.isFinite(v)), `(18) ${k}가 숫자가 아님 ${JSON.stringify(i)}`);
    }
  }
}
console.log('(18) random 1,000-case invariants OK');

// (19) 국민연금 — 개시 나이는 출생연도로 정해지고, 청구 나이는 법정 범위를 벗어날 수 없다.
// 예전엔 공유 링크의 pen 값이 그대로 들어와 40세 개시도 통했고, 그만큼 파이어 나이가 당겨졌다.
{
  const base = { currentAge: 35, startYear: 2026, targetRetirementAge: 50, financialAsset: 300000000, monthlyInvestment: 2500000, monthlyLivingCost: 3000000, expectedMonthlyPension: 1200000 };
  assert(normalizeInputs({ ...base }).expectedPensionAge === 65, '(19) 1991년생은 65세 개시');
  assert(normalizeInputs({ ...base, currentAge: 66 }).expectedPensionAge === 62, '(19) 1960년생은 62세 개시');
  assert(normalizeInputs({ ...base, currentAge: 62 }).expectedPensionAge === 63, '(19) 1964년생은 63세 개시');
  // 바깥에서 밀어 넣은 값은 무시해야 한다
  assert(normalizeInputs({ ...base, expectedPensionAge: 40 }).expectedPensionAge === 65, '(19) 개시 나이 주입이 막혀야 한다');
  assert(buildSimulation({ ...base, expectedPensionAge: 40 }).earliestRetirementAge === buildSimulation(base).earliestRetirementAge, '(19) 개시 나이 주입으로 파이어 나이가 당겨지면 안 된다');
  // 조기·연기는 개시 나이 ±5년까지만
  assert(normalizeInputs({ ...base, pensionClaimAge: 50 }).expectedPensionAge === 60, '(19) 조기는 60세까지만');
  assert(normalizeInputs({ ...base, pensionClaimAge: 80 }).expectedPensionAge === 70, '(19) 연기는 70세까지만');
  // 감액·가산 요율 (국민연금공단: 조기 연 6%, 연기 연 7.2%)
  assert(earlyClaim(1000000, 65, 60).monthly === 700000, '(19) 5년 조기 = 30% 감액');
  assert(earlyClaim(1000000, 65, 62).monthly === 820000, '(19) 3년 조기 = 18% 감액');
  assert(earlyClaim(1000000, 65, 70).monthly === 1360000, '(19) 5년 연기 = 36% 가산');
}
console.log('(19) pension start age / claim clamp OK');

// (20) 화면에 나가는 자산 숫자는 한 벌이어야 한다.
// 히어로 'N세 때 자산' = 그래프 파이어 지점 = 표 'N세 때' = 인증 카드. 전부 displayResult에서 읽는다.
// 예전엔 히어로는 53세(오늘 돈), 그래프는 목표 55세(명목 14억), 카드는 '지금 그만두려면' 9억이 한 화면에 있었다.
{
  const s = buildSimulation({ currentAge: 35, targetRetirementAge: 55, financialAsset: 100000000, monthlyInvestment: 3000000, monthlyLivingCost: 3000000 });
  const d = s.displayResult;
  assert(d && Array.isArray(d.rows) && d.rows.length > 2, '(20) displayResult가 있어야 한다');
  assert(d.retirementAge === s.earliestRetirementAge, '(20) 화면 은퇴 나이 = 파이어 가능 나이');
  const row = d.rows.find((r) => r.age === d.retirementAge);
  assert(Math.abs(row.financialAsset - d.fireAsset) < 1, '(20) 그래프의 파이어 지점 = 히어로 금액');
  assert(Math.abs(d.fireAssetToday - s.atEarliest.assetToday) < 1, '(20) 히어로 금액 = atEarliest');
  const g = buildGrowthSeries(s);
  const gi = g.ages.indexOf(d.retirementAge);
  assert(Math.abs(g.total[gi] - d.fireAsset) < 1, '(20) 넣은 돈+불어난 돈 = 히어로 금액');
  // 오늘 돈이므로 파이어 전까지는 물가보다 빨리 불어야 한다(수익 5% > 물가 3%, 저축 중)
  assert(d.rows[0].financialAsset < row.financialAsset, '(20) 저축 중엔 자산이 는다');
  // 사람 직관: 1억 + 300만×12×18년 = 원금 7.5억. 파이어 때 자산은 그보다 커야 한다.
  assert(d.fireAsset > 100000000 + 3000000 * 12 * (d.retirementAge - 35) * 0.9, '(20) 모은 원금보다 작게 보이면 안 된다');
  // 가능 나이가 없을 때도 화면은 비지 않아야 한다
  const none = buildSimulation({ currentAge: 35, targetRetirementAge: 55, financialAsset: 0, monthlyInvestment: 100000, monthlyLivingCost: 5000000 });
  assert(none.earliestRetirementAge == null && none.displayResult.rows.length > 2, '(20) 가능 나이 없으면 목표 나이 흐름으로 대체');
}
console.log('(20) one display series across screens OK');


// (21) 해외주식 양도세는 22% 단일. 250만원 공제. (국세청·한국투자증권·유안타·하나증권 안내)
{
  const { calculateInvestmentTaxes } = await import('../src/utils/taxCalculator.js');
  const t = calculateInvestmentTaxes({ foreignStockGain: 1000000000 }).foreignStockTax;
  assert(Math.abs(t.tax - (1000000000 - 2500000) * 0.22) < 1, '(21) 10억 차익 = (10억-250만)×22%');
}
console.log('(21) foreign stock tax flat 22% OK');

// (22) 건보료 재산 점수는 법정 60등급표. 과표 3억(공제 후 2억) → 24등급 586점.
{
  const { propertyPoints, estimateLocalPremium } = await import('../src/firemap-v2/healthInsurance.js');
  assert(propertyPoints(20000) === 586, '(22) 2억 → 586점');
  assert(propertyPoints(450) === 22 && propertyPoints(451) === 44, '(22) 1·2등급 경계');
  assert(propertyPoints(10000000) === 2341, '(22) 상한 2,341점');
  // 소득 0 · 과표 3억: 최저보험료 20,160 + 586×211.5 = 144,099 → 장기요양 포함 163,0xx원 (공단 산식)
  const e = estimateLocalPremium({ chargeableIncomeManwon: 0, propertyTaxBaseEok: 3 });
  assert(Math.abs(e.monthly - 163032) < 200, '(22) 과표 3억 소득 0 → 약 163,000원, 실제 ' + e.monthly);
}
console.log('(22) health insurance property grades OK');

// (23) 목표 나이가 현재 나이보다 앞이면 현재 나이로 맞춘다.
{
  const s = buildSimulation({ currentAge: 50, targetRetirementAge: 30, financialAsset: 500000000, monthlyInvestment: 1000000, monthlyLivingCost: 2000000 });
  assert(s.inputs.targetRetirementAge === 50 && s.requiredFireAssetNominal > 0, '(23) 목표<현재 방어');
}
console.log('(23) target<current guard OK');


// (24) 금융소득종합과세 — 배당 2,000만 초과분은 누진세율, 비교과세로 15.4% 아래로는 안 내려간다.
// 감사 보고서가 독립 계산한 실효세율과 대조: 금융 1억·기타 0 → 17.47%, 금융 5,000만·기타 3,000만 → 17.74%, 금융 2억·기타 0 → 27.88%
{
  const base = { currentAge: 40, targetRetirementAge: 40, financialAsset: 2500000000, monthlyInvestment: 0, monthlyLivingCost: 1000000, investType: 2, dividendYield: 4, annualReturnRate: 4, inflationRate: 0, expectedMonthlyPension: 0 };
  // 자산 25억 × 4% = 배당 1억, 파이어 첫해(40세) 행의 investTax
  const r = simulateRetirement(base, 40);
  const row = r.rows.find((x) => x.age === 40);
  const eff = row.investTax / (2500000000 * 0.04);
  assert(Math.abs(eff - 0.1747) < 0.004, '(24) 배당 1억 실효세율 ≈17.5%, 실제 ' + (eff * 100).toFixed(2) + '%');
  const r2 = simulateRetirement({ ...base, financialAsset: 5000000000 }, 40);
  const eff2 = r2.rows.find((x) => x.age === 40).investTax / (5000000000 * 0.04);
  assert(Math.abs(eff2 - 0.2788) < 0.005, '(24) 배당 2억 실효세율 ≈27.9%, 실제 ' + (eff2 * 100).toFixed(2) + '%');
  const r3 = simulateRetirement({ ...base, financialAsset: 1250000000, partTimeIncomeAfterRetirement: 2500000 }, 40);
  const eff3 = r3.rows.find((x) => x.age === 40).investTax / (1250000000 * 0.04);
  assert(Math.abs(eff3 - 0.1774) < 0.005, '(24) 배당 5,000만+기타 3,000만 ≈17.7%, 실제 ' + (eff3 * 100).toFixed(2) + '%');
  const r4 = simulateRetirement({ ...base, financialAsset: 400000000 }, 40);
  const eff4 = r4.rows.find((x) => x.age === 40).investTax / (400000000 * 0.04);
  assert(Math.abs(eff4 - 0.154) < 0.0001, '(24) 배당 1,600만은 원천징수 15.4%');
}
console.log('(24) comprehensive financial income tax OK');

// (25) 건보료 — 근로·연금소득은 50%만 반영. 연 2,400만 공적연금만 있으면 월 81,348원(장기요양 포함, 감사 보고서 계산).
{
  const { estimateLocalPremium } = await import('../src/firemap-v2/healthInsurance.js');
  const full = estimateLocalPremium({ chargeableIncomeManwon: 2400, propertyTaxBaseEok: 0 }).monthly;
  const half = estimateLocalPremium({ chargeableIncomeManwon: 0, halfRatedIncomeManwon: 2400, propertyTaxBaseEok: 0 }).monthly;
  assert(Math.abs(half * 2 - full) < 3, '(25) 50% 반영이면 보험료도 절반');
  assert(Math.abs(half - 81348) < 300, '(25) 연금 2,400만 → 약 81,348원, 실제 ' + half);
}
console.log('(25) health insurance 50% rating OK');
