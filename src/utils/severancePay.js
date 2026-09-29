// 퇴직금 계산(시험 A 시제품, 아직 화면에 안 붙임). 근거 원문: work/research/calc-severance/spec.md
// 법이 정한 것만 계산한다: 근로자퇴직급여 보장법 제8조①(1년에 30일분 평균임금), 제4조①(1년 미만·주 15시간 미만 제외),
// 근로기준법 제2조①6호(평균임금 = 사유 발생일 이전 3개월 임금총액 ÷ 그 기간 총일수)·②(통상임금보다 적으면 통상임금).
// 상여금·연차수당 3/12 반영은 원문 확인 전이라 넣지 않았다.
const DAY = 86400000;
const utc = (ymd) => { const [y, m, d] = ymd.split('-').map(Number); return Date.UTC(y, m - 1, d); };
const minusMonths = (ymd, n) => {
  const [y, m, d] = ymd.split('-').map(Number);
  const t = new Date(Date.UTC(y, m - 1 - n, 1));
  const last = new Date(Date.UTC(t.getUTCFullYear(), t.getUTCMonth() + 1, 0)).getUTCDate();
  return Date.UTC(t.getUTCFullYear(), t.getUTCMonth(), Math.min(d, last));
};

// hireDate: 입사일, retireDate: 퇴직일(마지막 근무일 다음 날) — 'YYYY-MM-DD'
// wages3m: 퇴직일 이전 3개월 동안 받은 임금 총액(원), dailyOrdinaryWage: 1일 통상임금(모르면 0)
export function severancePay({ hireDate, retireDate, wages3m, weeklyHours = 40, dailyOrdinaryWage = 0 }) {
  const serviceDays = Math.round((utc(retireDate) - utc(hireDate)) / DAY);
  const periodDays = Math.round((utc(retireDate) - minusMonths(retireDate, 3)) / DAY);
  const avgDaily = periodDays > 0 ? wages3m / periodDays : 0;
  const dailyWage = Math.max(avgDaily, dailyOrdinaryWage);
  const eligible = serviceDays >= 365 && weeklyHours >= 15;
  const amount = eligible ? Math.floor(dailyWage * 30 * serviceDays / 365) : 0;
  return { eligible, serviceDays, periodDays, avgDaily, dailyWage, usedOrdinary: dailyOrdinaryWage > avgDaily, amount };
}
