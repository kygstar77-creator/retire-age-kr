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

// (11) 해외 양도세는 과표 3억 초과분에 27.5%를 적용해야 한다(P6)
{
  const gain = 500000000; const exempt = 2500000;
  const base = gain - exempt;
  const expected = 300000000 * 0.22 + (base - 300000000) * 0.275;
  const single = base * 0.22;
  assert(expected > single, 'Invariant failed: 2단 누진이 단일세율보다 크지 않음(테스트 전제 오류).');
}

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
