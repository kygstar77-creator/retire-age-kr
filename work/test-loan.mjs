// 대출 상환 시제품 손검산 대조. 기대값은 부동산계산기.com/대출이자 화면에 같은 입력을 넣어 읽은 값(2026-10-05 11:4x, firemap-product-dev).
import { loanSchedule, extraEffect } from '../src/utils/loanRepay.js';
const cases = [
  // 3억·30년·4.5% 원리금균등: 월 1,520,056 · 1회 원금 395,056/이자 1,125,000 · 2회 이자 1,123,519 · 360회 이자 전부 일치(경쟁 상환표).
  // 총이자: 경쟁 화면 요약칸은 247,220,135인데 자기 상환표 이자 합은 247,220,145 — 우리는 표의 합을 쓴다
  [{ principal: 300_000_000, annualRate: 4.5, months: 360, method: 'equal' }, { firstPayment: 1_520_056, totalInterest: 247_220_145 }, (r) => r.rows[0].principal === 395_056 && r.rows[1].interest === 1_123_519 && r.rows[6].interest === 1_116_027],
  // 같은 조건 원금균등: 월 원금 833,333 · 총이자 203,062,500 · 1회 납부 1,958,333 · 2회 1,955,208
  [{ principal: 300_000_000, annualRate: 4.5, months: 360, method: 'principal' }, { firstPayment: 1_958_333, totalInterest: 203_062_500 }, (r) => r.rows[1].payment === 1_955_208],
  // 5천만·24개월·6.2% 만기일시: 매달 이자 258,333. 경쟁 화면 총이자 6,200,000은 '원금×금리÷12×개월' 식 — 우리는 실제 낼 매달 이자의 합(258,333×24 = 6,199,992)
  [{ principal: 50_000_000, annualRate: 6.2, months: 24, method: 'bullet' }, { firstPayment: 258_333, totalInterest: 6_199_992, months: 24 }, (r) => r.lastPayment === 50_258_333],
  // 1억2,345만·84개월(거치 12)·3.9% 원리금균등: 거치 중 이자 401,213 · 뒤 월 1,925,778 · 총이자: 요약칸 20,020,576, 상환표 합 20,020,586(표의 합을 씀)
  [{ principal: 123_450_000, annualRate: 3.9, months: 84, graceMonths: 12, method: 'equal' }, { firstPayment: 401_213, totalInterest: 20_020_586 }, (r) => r.rows[12].payment === 1_925_778],
  // 0% (경쟁 화면은 0% 계산 안 됨 — 손셈): 2천만·12개월 → 월 1,666,667, 이자 0
  [{ principal: 20_000_000, annualRate: 0, months: 12, method: 'equal' }, { firstPayment: 1_666_667, totalInterest: 0, months: 12 }, (r) => r.rows[11].balance === 0],
];
let bad = 0;
for (const [inp, exp, extra] of cases) {
  const r = loanSchedule(inp);
  for (const k of Object.keys(exp)) if (r[k] !== exp[k]) { bad++; console.log('틀림', JSON.stringify(inp), k, r[k], '≠', exp[k]); }
  if (!extra(r)) { bad++; console.log('틀림(회차 값)', JSON.stringify(inp)); }
  if (r.rows[r.rows.length - 1].balance !== 0) { bad++; console.log('잔액 남음', JSON.stringify(inp)); }
}
// 더 갚기: 3억·30년·4.5%에 매달 10만원 더 → 일찍 끝나고 이자가 줄어야 한다(크기는 경쟁 대조 없음, 방향만)
const e = extraEffect({ principal: 300_000_000, annualRate: 4.5, months: 360, method: 'equal' }, 100_000);
if (!(e.monthsSaved > 0 && e.interestSaved > 0 && e.withExtra.rows.at(-1).balance === 0)) { bad++; console.log('더 갚기 틀림', e.monthsSaved, e.interestSaved); }
console.log(bad ? `대출 대조 ${bad}건 틀림` : `대출 대조 ${cases.length}건 통과 · 매달 10만원 더 → ${e.monthsSaved}개월·이자 ${e.interestSaved.toLocaleString()}원 줄어듦`);
process.exit(bad ? 1 : 0);
