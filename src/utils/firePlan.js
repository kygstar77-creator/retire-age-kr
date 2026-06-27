// 완주 엔진 — 메인 시뮬레이터(지속가능성/연금·인출 모델)와 '같은 기준'으로 통일.
// 목표 자산을 4%룰이 아니라, "목표 나이에 은퇴해도 자산이 수명까지 안 마르는" 지속가능성 기준으로 산출.
// → '현실 가능 나이(earliestRetirementAge)'와 완주 목표가 한 기준이 되어 모순 제거.
import { simulateRetirement } from './retirementSimulator.js';

const clampPct = (x) => Math.max(0, Math.min(100, Math.round(x)));

// 목표 나이에 은퇴해도 지속가능하려면 매달 얼마를 모아야 하나(메인 엔진 재사용 탐색).
// 반환: { monthly, reachable }. 부동산=임대수익·월저축=monthlyInvestment 전제는 시뮬레이터가 그대로 처리.
function solveRequiredMonthly(inp, targetAge) {
  const simUntil = Number(inp.simulationUntilAge) || 90;
  const sustainable = (m) => {
    const r = simulateRetirement({ ...inp, monthlyInvestment: m }, targetAge);
    return !r.depletionAge || r.depletionAge > simUntil;
  };
  if (sustainable(0)) return { monthly: 0, reachable: true };
  const CAP = 100000000; // 월 1억 상한(현실적 안전장치)
  let hi = 100000;
  while (!sustainable(hi) && hi < CAP) hi = Math.min(hi * 2, CAP);
  if (!sustainable(hi)) return { monthly: CAP, reachable: false }; // 상한으로도 목표 나이엔 빠듯
  let lo = 0;
  while (hi - lo > 10000) { const mid = Math.floor((lo + hi) / 2); if (sustainable(mid)) hi = mid; else lo = mid; }
  return { monthly: hi, reachable: true };
}

function assetAtAge(inp, targetAge, monthly) {
  const r = simulateRetirement({ ...inp, monthlyInvestment: monthly }, targetAge);
  const row = r.rows.find((x) => x.age === targetAge);
  return row ? Math.max(0, row.financialAsset) : 0;
}

export function firePlan(simulation, opts = {}) {
  const inp = (simulation && simulation.inputs) || {};
  const A = Math.max(0, Number(inp.financialAsset) || 0);
  const curAge = Number(inp.currentAge) || 0;
  const targetAge = Number(inp.targetRetirementAge) || 0;
  const planMonthly = Math.max(0, Number(inp.monthlyInvestment) || 0);
  const earliest = (simulation && simulation.earliestRetirementAge != null) ? simulation.earliestRetirementAge : null;
  const annual = (opts.annualReturn != null ? opts.annualReturn : (Number(inp.annualReturnRate) || 5)) / 100;
  const yearsLeft = Math.max(0, targetAge - curAge);

  const req = solveRequiredMonthly(inp, targetAge);     // 지속가능성 기준 필요 월저축
  const reachable = req.reachable;
  const requiredMonthly = req.monthly;
  // 목표 자산 = 목표 나이 시점에 필요한 금융자산(필요 월저축으로 도달했을 때의 자산)
  const G = reachable ? Math.round(assetAtAge(inp, targetAge, requiredMonthly)) : 0;
  // 지금 계획대로 갈 때 목표 나이 시점 예상 자산
  const trajectory = Math.round((simulation && simulation.retirementFinancialAsset) || assetAtAge(inp, targetAge, planMonthly));

  const shortfall = reachable ? Math.max(0, Math.round(requiredMonthly) - planMonthly) : null;
  const coast = reachable && requiredMonthly === 0;            // 추가 저축 0으로도 가능(코스트파이어)
  const alreadyAhead = reachable && shortfall === 0;           // 지금 계획이 필요액 이상 → 목표 이하 나이에 가능
  const pmt = Math.round(requiredMonthly); // 항상 숫자(미달 시에도 상한값) — 하위 화면 null 방지
  const daily = Math.round(pmt / 30.4);
  const progress = G > 0 ? clampPct((alreadyAhead ? Math.max(trajectory, G) : trajectory) / G * 100) : (alreadyAhead ? 100 : 0);
  const remaining = Math.max(0, G - A);

  return {
    A, G, curAge, targetAge, yearsLeft, annual, earliest, reachable,
    pmt, daily, planMonthly, shortfall, progress, remaining, trajectory,
    coast, alreadyAhead, alreadyOnTrack: coast // 하위호환(기존 참조 안전)
  };
}
