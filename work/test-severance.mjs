// 퇴직금 시제품 손검산 대조. 기대값은 spec.md 표(파이썬으로 따로 계산)와 같아야 한다.
import { severancePay } from '../src/utils/severancePay.js';
const cases = [
  [{ hireDate: '2023-01-01', retireDate: '2026-01-01', wages3m: 9_000_000 }, { serviceDays: 1096, periodDays: 92, amount: 8_812_388 }],
  [{ hireDate: '2025-03-01', retireDate: '2026-02-28', wages3m: 9_000_000 }, { eligible: false, amount: 0 }],
  [{ hireDate: '2020-05-10', retireDate: '2026-05-10', wages3m: 7_500_000, weeklyHours: 14 }, { eligible: false, amount: 0 }],
  [{ hireDate: '2021-03-02', retireDate: '2026-03-02', wages3m: 6_000_000, dailyOrdinaryWage: 80_000 }, { usedOrdinary: true, periodDays: 90, amount: 12_006_575 }],
  // 고용노동부 퇴직금 계산 페이지 예시(moel.go.kr/retirementpayCal.do): 재직 1,080일, 92일, 1일 평균임금 88,641원 31전
  [{ hireDate: '2014-10-02', retireDate: '2017-09-16', wages3m: 7_080_000, annualBonus: 4_000_000, annualLeavePay: 300_000 }, { serviceDays: 1080, periodDays: 92, wagesTotal: 8_155_000, amount: 7_868_433 }],
];
let bad = 0;
for (const [inp, exp] of cases) {
  const r = severancePay(inp);
  for (const k of Object.keys(exp)) if (r[k] !== exp[k]) { bad++; console.log('틀림', inp, k, r[k], '≠', exp[k]); }
}
console.log(bad ? `퇴직금 대조 ${bad}건 틀림` : `퇴직금 대조 ${cases.length}건 통과`);
process.exit(bad ? 1 : 0);
