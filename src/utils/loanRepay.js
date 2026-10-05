// 대출 상환 계산(시제품, 아직 화면에 안 붙임). 근거: work/research/calc-competition/loan.md
// 법이 정한 식이 아니라 상환 방식의 산식이다. 월 이자 = 남은 원금 × 연 금리 ÷ 12(대조: work/test-loan.mjs).
// method: 'equal'(원리금균등) · 'principal'(원금균등) · 'bullet'(만기일시)
// graceMonths: 거치 기간(그동안 이자만), extraMonthly: 매달 더 갚는 원금(원금이 다 갚아지면 일찍 끝난다)
const pmt = (p, r, n) => (r === 0 ? p / n : (p * r * (1 + r) ** n) / ((1 + r) ** n - 1));

export function loanSchedule({ principal, annualRate, months, method = 'equal', graceMonths = 0, extraMonthly = 0 }) {
  const P = Math.max(0, Math.round(Number(principal) || 0));
  const n = Math.max(1, Math.round(Number(months) || 0));
  const g = Math.min(n - 1, Math.max(0, Math.round(Number(graceMonths) || 0)));
  const r = Math.max(0, Number(annualRate) || 0) / 100 / 12;
  const extra = Math.max(0, Math.round(Number(extraMonthly) || 0));
  const amortN = n - g;
  const pay = method === 'equal' ? pmt(P, r, amortN) : 0;
  const fixedPrin = method === 'principal' ? P / amortN : 0;
  // 안에서는 원 미만까지 들고 가고, 표에 보일 때만 원 단위 반올림한다(부동산계산기.com 상환표와 360회 전부 일치하는 방식, work/test-loan.mjs)
  const rows = [];
  let bal = P;
  for (let m = 1; m <= n && bal > 0.5; m++) {
    const i = bal * r;
    let prin = 0;
    if (m > g) {
      if (method === 'equal') prin = pay - i + extra;
      else if (method === 'principal') prin = fixedPrin + extra;
      else prin = extra; // 만기일시: 이자만 내다가 마지막 달에 원금(아래 줄)
    }
    if (m === n || prin >= bal - 0.5) prin = bal; // 마지막 달에 남은 원금을 다 갚는다
    bal -= prin;
    const payment = Math.round(prin + i);
    const interest = Math.round(i);
    rows.push({ month: m, payment, principal: payment - interest, interest, balance: Math.max(0, Math.round(bal)) });
  }
  const totalInterest = rows.reduce((s, x) => s + x.interest, 0); // 표에 보이는 매달 이자의 합
  return {
    rows,
    months: rows.length,
    firstPayment: rows[0] ? rows[0].payment : 0,
    lastPayment: rows.length ? rows[rows.length - 1].payment : 0,
    totalInterest,
    totalPaid: P + totalInterest,
  };
}

// 세 방식 총이자를 한 번에(결과 한 줄 비교용)
export function compareMethods(input) {
  return ['equal', 'principal', 'bullet'].map((method) => {
    const s = loanSchedule({ ...input, method, extraMonthly: 0 });
    return { method, totalInterest: s.totalInterest, firstPayment: s.firstPayment };
  });
}

// 매달 extra원을 더 갚으면 몇 달 일찍 끝나고 이자가 얼마 줄어드나
export function extraEffect(input, extra) {
  const base = loanSchedule({ ...input, extraMonthly: 0 });
  const withExtra = loanSchedule({ ...input, extraMonthly: extra });
  return { monthsSaved: base.months - withExtra.months, interestSaved: base.totalInterest - withExtra.totalInterest, base, withExtra };
}
