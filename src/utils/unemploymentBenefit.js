// 실업급여(구직급여) 계산. 근거 원문·수치 출처: work/research/calc-unemployment/spec.md
// 법이 정한 것만 계산한다(고용보험법 2026-09-18 시행본):
//   제45조① 기초일액 = 이직 당시 평균임금(근로기준법 제2조①6호: 이직 전 3개월 임금총액 ÷ 그 기간 총일수)
//   제45조⑤ + 시행령 제68조① 기초일액 상한 113,500원(2026-01-01 이후 이직자, 시행령 부칙 2025.12.23 제4조)
//   제45조④ 최저기초일액 = 이직 전 1일 소정근로시간 × 이직일 당시 시간급 최저임금(2026년 10,320원, 고용노동부고시 제2025-47호)
//   제46조 구직급여일액 = 기초일액 × 60%, 최저기초일액이 적용되면 × 80%(최저구직급여일액), 60%가 그보다 낮으면 최저구직급여일액
//   제50조① + 별표 1 소정급여일수(이직일 현재 연령 50세 미만/이상, 장애인은 50세 이상으로 본다 × 피보험기간)
// 2026년 이직만 계산한다. 2027년 상한액·2028-01-01 기초일액 산정 개정(1년 보수 기준)은 이 파일에 없다.
const DAY = 86400000;
const utc = (ymd) => { const [y, m, d] = ymd.split('-').map(Number); return Date.UTC(y, m - 1, d); };
const minusMonths = (t, n) => {
  const x = new Date(t);
  const y = x.getUTCFullYear(); const m = x.getUTCMonth(); const d = x.getUTCDate();
  const first = new Date(Date.UTC(y, m - n, 1));
  const last = new Date(Date.UTC(first.getUTCFullYear(), first.getUTCMonth() + 1, 0)).getUTCDate();
  return Date.UTC(first.getUTCFullYear(), first.getUTCMonth(), Math.min(d, last));
};

// 원 미만 버림. 113500 × 0.6 이 부동소수로 68099.999…가 되지 않게 아주 작은 값을 더한다.
const pct = (v, r) => Math.floor(v * r + 1e-6);

export const UB_2026 = {
  from: '2026-01-01', to: '2026-12-31',
  baseDailyCap: 113500,   // 시행령 제68조①
  minWageHourly: 10320,   // 고용노동부고시 제2025-47호(2026.1.1~12.31)
  rate: 0.6,              // 법 제46조①1호
  floorRate: 0.8          // 법 제46조①2호
};

// 별표 1 — 피보험기간 1년 미만 / 1~3년 / 3~5년 / 5~10년 / 10년 이상
const TABLE = { under50: [120, 150, 180, 210, 240], over50: [120, 180, 210, 240, 270] };
export function benefitDays(insuredMonths, over50OrDisabled) {
  const m = Math.max(0, Math.floor(insuredMonths || 0));
  const band = m < 12 ? 0 : m < 36 ? 1 : m < 60 ? 2 : m < 120 ? 3 : 4;
  return TABLE[over50OrDisabled ? 'over50' : 'under50'][band];
}

// lastWorkDay: 이직일(마지막으로 근무한 날, 'YYYY-MM-DD') — 피보험자격은 그 다음 날 상실(법 제14조①3호).
// 평균임금 3개월 = 다음 날부터 거꾸로 달력 3개월(퇴직금 계산과 같은 방식, 고용노동부 퇴직금 계산 예시 92일).
// monthlyWage: 이직 전 3개월 월평균 임금(세전), insuredMonths: 피보험기간(개월), dailyHours: 이직 전 1일 소정근로시간.
export function unemploymentBenefit({ lastWorkDay, monthlyWage, insuredMonths, over50 = false, dailyHours = 8 }) {
  const inYear = typeof lastWorkDay === 'string' && lastWorkDay >= UB_2026.from && lastWorkDay <= UB_2026.to;
  if (!inYear) return { supported: false };
  const end = utc(lastWorkDay) + DAY;
  const periodDays = Math.round((end - minusMonths(end, 3)) / DAY);
  const wages3m = Math.max(0, monthlyWage || 0) * 3;
  const avgDaily = wages3m / periodDays;
  const hours = Math.min(8, Math.max(1, dailyHours || 8));
  const minBaseDaily = hours * UB_2026.minWageHourly;               // 최저기초일액
  const floorDaily = pct(minBaseDaily, UB_2026.floorRate);          // 최저구직급여일액
  const capped = avgDaily > UB_2026.baseDailyCap;
  const baseDaily = Math.min(avgDaily, UB_2026.baseDailyCap);
  const byRate = pct(baseDaily, UB_2026.rate);
  const floored = byRate < floorDaily;
  const daily = floored ? floorDaily : byRate;
  const days = benefitDays(insuredMonths, over50);
  return {
    supported: true, periodDays, avgDaily, baseDaily, capped, floored,
    capDaily: pct(UB_2026.baseDailyCap, UB_2026.rate), floorDaily,
    daily, days, total: daily * days
  };
}
