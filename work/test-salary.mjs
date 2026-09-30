// 연봉 실수령 손검산 대조. 기대값은 work/research/calc-salary/handcheck.py(법령 API 별표 원문 글자 + Fraction)로 따로 계산한 값.
// A는 사람인·잡코리아·인크루트 결과와도 줄마다 맞춰 봤다(calc-competition/salary.md): 국민연금만 사람인 148,830(천원 미만 안 버림)·잡코리아 148,810(같음).
import { salaryNet, tableTax, childCredit } from '../src/utils/salaryNet.js';
const cases = [
  ['A', { annual: 40_000_000, nontaxMonthly: 200_000, family: 1, kids: 0, ratio: 100 }, { pension: 148_810, health: 112_640, ltc: 14_800, employment: 28_190, incomeTax: 84_620, localTax: 8_460, net: 2_935_813 }],
  ['B', { annual: 30_000_000, nontaxMonthly: 200_000, family: 1, kids: 0, ratio: 100 }, { pension: 109_250, health: 82_680, ltc: 10_860, employment: 20_700, incomeTax: 29_160, localTax: 2_910, net: 2_244_440 }],
  ['C', { annual: 60_000_000, nontaxMonthly: 200_000, family: 4, kids: 2, ratio: 100 }, { pension: 228_000, health: 172_560, ltc: 22_670, employment: 43_200, incomeTax: 147_470, localTax: 14_740, net: 4_371_360 }],
  ['D', { annual: 100_000_000, nontaxMonthly: 200_000, family: 1, kids: 0, ratio: 80 }, { pension: 313_020, health: 292_390, ltc: 38_420, employment: 73_190, incomeTax: 789_370, localTax: 78_930, net: 6_748_013 }],
  ['E', { annual: 150_000_000, nontaxMonthly: 0, family: 2, kids: 1, ratio: 120 }, { pension: 313_020, health: 449_370, ltc: 59_040, employment: 112_500, incomeTax: 2_751_880, localTax: 275_180, net: 8_539_010 }],
  ['F', { annual: 24_000_000, nontaxMonthly: 200_000, family: 1, kids: 0, ratio: 100 }, { pension: 85_500, health: 64_710, ltc: 8_500, employment: 16_200, incomeTax: 15_110, localTax: 1_510, net: 1_808_470 }],
];
let bad = 0;
for (const [name, inp, exp] of cases) {
  const r = salaryNet(inp);
  for (const k of Object.keys(exp)) if (r[k] !== exp[k]) { bad++; console.log('틀림', name, k, r[k], '≠', exp[k]); }
}
// 표 경계: 770천원 미만 0, 구간 '이상·미만', 1,000만원 정확히, 11명 초과 식(비고 4), 자녀 공제(비고 3)
const edge = [
  [tableTax(769_999, 1), 0], [tableTax(3_000_000, 1), 74_350], [tableTax(10_000_000, 1), 1_507_400],
  [tableTax(9_999_999, 1), 1_503_990], [tableTax(10_000_000, 12), 960_840 - (990_840 - 960_840)],
  [childCredit(1), 20_830], [childCredit(2), 45_830], [childCredit(4), 45_830 + 2 * 33_330],
];
edge.forEach(([got, want], i) => { if (got !== want) { bad++; console.log('경계 틀림', i, got, '≠', want); } });
console.log(bad ? `실수령 대조 ${bad}건 틀림` : `실수령 대조 ${cases.length}건 + 경계 ${edge.length}건 통과`);
process.exit(bad ? 1 : 0);
