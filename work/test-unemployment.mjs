// 실업급여(구직급여) 손검산 대조. 기대값은 spec.md 표(손으로 + 파이썬으로 따로 계산)와 같아야 한다.
import { unemploymentBenefit, benefitDays } from '../src/utils/unemploymentBenefit.js';
const cases = [
  // 1) 상한: 9/30 이직 → 7.1~9.30 92일, 월 500만 → 1,500만 ÷ 92 = 163,043원 > 113,500 → 113,500 × 60% = 68,100 × 210일(50세 미만, 5년)
  [{ lastWorkDay: '2026-09-30', monthlyWage: 5_000_000, insuredMonths: 60 }, { periodDays: 92, capped: true, floored: false, daily: 68_100, days: 210, total: 14_301_000 }],
  // 2) 하한: 6/30 이직 → 4.1~6.30 91일, 월 200만 → 65,934원 × 60% = 39,560 < 10,320 × 8 × 80% = 66,048 → 66,048 × 120일(1년 미만)
  [{ lastWorkDay: '2026-06-30', monthlyWage: 2_000_000, insuredMonths: 11 }, { periodDays: 91, capped: false, floored: true, daily: 66_048, days: 120, total: 7_925_760 }],
  // 3) 상·하한 사이: 3/31 이직 → 1.1~3.31 90일, 월 340만 → 1,020만 ÷ 90 = 113,333원 × 60% = 68,000 × 210일(50세 이상, 3년)
  [{ lastWorkDay: '2026-03-31', monthlyWage: 3_400_000, insuredMonths: 36, over50: true }, { periodDays: 90, capped: false, floored: false, daily: 68_000, days: 210, total: 14_280_000 }],
  // 4) 하루 4시간: 12/31 이직 → 10.1~12.31 92일, 월 100만 → 32,608원 × 60% = 19,565 < 4 × 10,320 × 80% = 33,024 → 33,024 × 150일(1년)
  [{ lastWorkDay: '2026-12-31', monthlyWage: 1_000_000, insuredMonths: 12, dailyHours: 4 }, { periodDays: 92, floored: true, daily: 33_024, days: 150, total: 4_953_600 }],
  // 5) 월 330만(90일): 110,000 × 60% = 66,000 < 66,048 → 하한이 이긴다(상한 바로 아래라도 하한 적용 구간)
  [{ lastWorkDay: '2026-03-31', monthlyWage: 3_300_000, insuredMonths: 120 }, { floored: true, daily: 66_048, days: 240, total: 15_851_520 }],
  // 6) 2026년 밖 이직은 계산하지 않는다(2027 상한 확인 안 함)
  [{ lastWorkDay: '2027-01-01', monthlyWage: 3_000_000, insuredMonths: 24 }, { supported: false }],
  [{ lastWorkDay: '2025-12-31', monthlyWage: 3_000_000, insuredMonths: 24 }, { supported: false }],
];
// 별표 1 경계: 피보험기간 개월 → [50세 미만, 50세 이상·장애인]
const table = [[0, 120, 120], [11, 120, 120], [12, 150, 180], [35, 150, 180], [36, 180, 210], [59, 180, 210], [60, 210, 240], [119, 210, 240], [120, 240, 270], [400, 240, 270]];
let bad = 0;
for (const [inp, exp] of cases) {
  const r = unemploymentBenefit(inp);
  for (const k of Object.keys(exp)) if (r[k] !== exp[k]) { bad++; console.log('틀림', inp, k, r[k], '≠', exp[k]); }
}
for (const [m, u, o] of table) {
  if (benefitDays(m, false) !== u) { bad++; console.log('틀림 별표1', m, '50세 미만', benefitDays(m, false), '≠', u); }
  if (benefitDays(m, true) !== o) { bad++; console.log('틀림 별표1', m, '50세 이상', benefitDays(m, true), '≠', o); }
}
console.log(bad ? `실업급여 대조 ${bad}건 틀림` : `실업급여 대조 ${cases.length}건 + 별표1 경계 ${table.length * 2}건 통과`);
process.exit(bad ? 1 : 0);
