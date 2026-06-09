import { statsTopPercentile, ageBandOf, NETWORTH_STATS } from './stats.js';

export function gradeFromScore(score) {
  if (score >= 80) return 'S';
  if (score >= 65) return 'A';
  if (score >= 50) return 'B';
  if (score >= 35) return 'C';
  return 'D';
}

// 통계(또래 순자산 분포) 기반 즉시 백분위 + 등급
export function statsRank(simulation) {
  const score = Math.max(0, Math.min(100, Number(simulation.survivalScore) || 0));
  const age = simulation.inputs && simulation.inputs.currentAge;
  const band = ageBandOf(age);
  return {
    percentile: statsTopPercentile(simulation.netWorth, age),
    grade: gradeFromScore(score),
    ageBand: band,
    ageBandLabel: `${band}대`,
    source: `${NETWORTH_STATS.source} 기준 또래 비교`
  };
}
