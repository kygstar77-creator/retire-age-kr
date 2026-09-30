// 연봉·월급 실수령 계산. 근거 원문과 손검산: work/research/calc-salary/spec.md (2026-10-01 확인)
// - 소득세: 소득세법 시행령 별표 2 근로소득 간이세액표(개정 2026.2.27) 해당란 세액(표는 salaryTaxTable2026.js, 법령 API 별표내용 그대로).
//   8세 이상 20세 이하 자녀 공제(별표 2 비고 3), 11명 초과 가족(비고 4), 월 1,000만원 초과 식(표 끝), 80·100·120% 선택(시행령 제194조①).
// - 지방소득세: 소득세의 10%.
// - 국민연금: 기준소득월액(천원 미만 버림, 시행령 제5조①) × 4.75%(국민연금법 부칙 — 2026년 1만분의 475).
//   기준소득월액 하한 41만원·상한 659만원(보건복지부 2026-01-09 발표, 2026.7~2027.6 적용).
// - 건강보험: 보수월액 × 7.19%(국민건강보험법 시행령 제44조①)의 절반. 장기요양: 건강보험료 × 13.14%
//   (노인장기요양보험법 제9조① — 장기요양보험료율 0.9448%(시행령 제4조) ÷ 7.19%, 소수점 다섯째자리 반올림).
// - 고용보험: 보수 × 실업급여 보험료율 1.8%(징수법 시행령 제12조①2호)의 2분의 1(징수법 제13조②).
// - 끝수: 10원 미만 버림(국민건강보험법 제107조 → 국고금관리법 제47조①). 국민연금·고용보험은 같은 방식으로 둔다(spec.md 참고).
import TABLE from './salaryTaxTable2026.js';

export const SALARY_RULES = {
  basisDate: '2026-10-01',
  // 요율은 정수 분수로 둔다 — 12,500,000 × 0.009 = 112,499.99…처럼 소수 곱에서 10원이 틀어진다(손검산 E·F에서 발견).
  pension: [475, 10000], pensionMin: 410000, pensionMax: 6590000,
  health: [3595, 100000], ltcOfHealth: [1314, 10000],
  employment: [9, 1000],
  mealNontaxMax: 200000 // 식사대 비과세 월 20만원 이하(소득세법 제12조제3호러목)
};

const floor10 = (n) => Math.floor(Math.max(0, n) / 10) * 10;
const mul = (n, [a, b]) => (n * a) / b;

// 간이세액표 해당란(자녀 공제 전). taxable: 월급여액(비과세 제외, 원), family: 공제대상가족 수(본인 포함, 1 이상)
export function tableTax(taxable, family) {
  const f = Math.max(1, Math.floor(family || 1));
  if (f > 11) {
    const t11 = tableTax(taxable, 11);
    const t10 = tableTax(taxable, 10);
    return Math.max(0, t11 - (t10 - t11) * (f - 11));
  }
  const k = taxable / 1000; // 천원
  const col = f - 1;
  if (k < TABLE.from[0]) return 0;
  if (k < TABLE.to) {
    let lo = 0, hi = TABLE.from.length - 1;
    while (lo < hi) { const mid = (lo + hi + 1) >> 1; if (TABLE.from[mid] <= k) lo = mid; else hi = mid - 1; }
    return TABLE.tax[lo][col];
  }
  const base = TABLE.top10000[col];
  if (taxable === TABLE.to * 1000) return base; // 표의 '10,000천원' 행 — 초과 식은 그 위부터
  const over = (limit) => (taxable - limit * 1000);
  if (k <= 14000) return base + (over(10000) * 98 * 35) / 10000 + 25000;
  if (k <= 28000) return base + 1397000 + (over(14000) * 98 * 38) / 10000;
  if (k <= 30000) return base + 6610600 + (over(28000) * 98 * 40) / 10000;
  if (k <= 45000) return base + 7394600 + (over(30000) * 40) / 100;
  if (k <= 87000) return base + 13394600 + (over(45000) * 42) / 100;
  return base + 31034600 + (over(87000) * 45) / 100;
}

export const childCredit = (n) => {
  const c = Math.max(0, Math.floor(n || 0));
  if (c === 0) return 0;
  if (c === 1) return 20830;
  return 45830 + (c - 2) * 33330;
};

// annual: 연봉(비과세 포함, 원) · nontaxMonthly: 월 비과세액 · family: 공제대상가족 수(본인 포함) · kids: 8~20세 자녀 수 · ratio: 80|100|120
export function salaryNet({ annual, nontaxMonthly = 200000, family = 1, kids = 0, ratio = 100 }) {
  const monthly = Math.floor((Number(annual) || 0) / 12);
  const nontax = Math.min(Math.max(0, Number(nontaxMonthly) || 0), monthly);
  const taxable = monthly - nontax;
  const R = SALARY_RULES;

  const pensionBase = Math.min(R.pensionMax, Math.max(R.pensionMin, Math.floor(taxable / 1000) * 1000));
  const pension = taxable > 0 ? floor10(mul(pensionBase, R.pension)) : 0;
  const health = floor10(mul(taxable, R.health));
  const ltc = floor10(mul(health, R.ltcOfHealth));
  const employment = floor10(mul(taxable, R.employment));

  const tableAmount = tableTax(taxable, family);
  const afterKids = Math.max(0, floor10(tableAmount) - childCredit(kids));
  const incomeTax = floor10((afterKids * ratio) / 100);
  const localTax = floor10(incomeTax / 10);

  const deductions = pension + health + ltc + employment + incomeTax + localTax;
  return {
    monthly, nontax, taxable, pensionBase,
    pension, health, ltc, employment, incomeTax, localTax,
    deductions, net: monthly - deductions, netAnnual: (monthly - deductions) * 12
  };
}
