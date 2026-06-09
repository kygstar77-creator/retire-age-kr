// Provisional FIRE rank/percentile derived from survivalScore.
// TODO(task #16): replace with (1) national-statistics percentile by age band
// and (2) live rank from anonymized Supabase scores.
const PLACEHOLDER_TOTAL = 1284;

export function gradeFromScore(score) {
  if (score >= 80) return 'S';
  if (score >= 65) return 'A';
  if (score >= 50) return 'B';
  if (score >= 35) return 'C';
  return 'D';
}

function ageBandLabel(age) {
  if (!age) return '30대';
  const band = Math.floor(age / 10) * 10;
  return `${band}대`;
}

export function estimateRank(simulation) {
  const score = Math.max(0, Math.min(100, Number(simulation.survivalScore) || 0));
  const percentile = Math.min(99, Math.max(1, Math.round(100 - score * 0.9)));
  const total = PLACEHOLDER_TOTAL;
  const position = Math.max(1, Math.round((percentile / 100) * total));
  return {
    percentile,
    grade: gradeFromScore(score),
    total,
    position,
    ageBandLabel: ageBandLabel(simulation.inputs && simulation.inputs.currentAge),
    trendText: '▲ 이번 주 5계단 상승 — 계속 관리하면 더 올라가요',
    provisional: true
  };
}
