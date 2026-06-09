// 또래 대비 순자산 백분위 추정용 분포 데이터.
// 출처: 통계청 2024 가계금융복지조사 (평균 순자산 4.49억, 3억 미만 56.9%, 10억 이상 10.9%, 연령대별 평균).
// 주의: 정확한 분위 경계 미공개 구간은 공개 요약치로 보간한 근사 모델. 2025 조사 반영 + 정밀 분위로 보정 예정(task #15).
export const NETWORTH_STATS = {
  source: '통계청 2024 가계금융복지조사',
  asOf: '2024-03',
  approximate: true,
  nationalAvgManwon: 44894,
  ageBandAvgManwon: { 20: 22158, 30: 22158, 40: 45064, 50: 51131, 60: 51922 },
  // [순자산(만원), 누적 백분위(%)] — 오름차순
  cumulativeCurve: [
    [-1000, 5], [0, 11], [10000, 32], [30000, 57],
    [50000, 71], [100000, 89], [150000, 95], [300000, 99]
  ]
};

function interpolate(curve, x) {
  if (x <= curve[0][0]) return curve[0][1];
  const last = curve[curve.length - 1];
  if (x >= last[0]) return last[1];
  for (let i = 1; i < curve.length; i += 1) {
    const [x0, y0] = curve[i - 1];
    const [x1, y1] = curve[i];
    if (x <= x1) return y0 + ((y1 - y0) * (x - x0)) / (x1 - x0);
  }
  return last[1];
}

export function ageBandOf(age) {
  if (!age) return 30;
  return Math.min(60, Math.max(20, Math.floor(age / 10) * 10));
}

// 또래 기준 상위 X% (작을수록 상위)
export function statsTopPercentile(netWorthWon, age) {
  const band = ageBandOf(age);
  const bandAvg = NETWORTH_STATS.ageBandAvgManwon[band] || NETWORTH_STATS.nationalAvgManwon;
  const ratio = NETWORTH_STATS.nationalAvgManwon / bandAvg;
  const adjManwon = (Number(netWorthWon) || 0) / 10000 * ratio;
  const cumulative = interpolate(NETWORTH_STATS.cumulativeCurve, adjManwon);
  return Math.min(99, Math.max(1, Math.round(100 - cumulative)));
}
