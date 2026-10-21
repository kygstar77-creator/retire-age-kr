// sevmonth1021 계산(2차, 레드팀 T1 반영) — 파이어맵 퇴직금 계산기 식(src/utils/severancePay.js)을 그대로 불러 쓴다.
// 사람 1(본보기): 월 300만원 = 기본급 250만원 + 연장근로수당 50만원(매달 같음). 통상임금은 기본급만으로 봄.
// 사람 2(대조): 월 300만원이 전부 기본급. 1일 통상임금 = 월급 ÷ 209시간 × 8시간(근로기준법 시행령 제6조②4호·③, 주 40시간+주휴 8시간 → 209)
import { severancePay } from '../../../src/utils/severancePay.js';
const won = (n) => n.toLocaleString('ko-KR');
const ord = (m) => m / 209 * 8, ordExact = (m) => m / (48 * 365 / 7 / 12) * 8;
const P1 = { wages3m: 9000000, dailyOrdinaryWage: ord(2500000) };
const P2 = { wages3m: 9000000, dailyOrdinaryWage: ord(3000000) };
console.log(`1일 통상임금: 사람1(기본급 250만) ${Math.floor(ord(2500000))}원(208.57시간이면 ${Math.floor(ordExact(2500000))}) · 사람2(기본급 300만) ${Math.floor(ord(3000000))}원(${Math.floor(ordExact(3000000))})`);
const next = (y, m) => (m === 12 ? `${y + 1}-01-01` : `${y}-${String(m + 1).padStart(2, '0')}-01`);
const last = (y, m) => new Date(Date.UTC(y, m, 0)).getUTCDate();
const HIRE = '2017-01-02';
console.log(`## A. 입사 ${HIRE}, 2027년 달마다 말일까지 일하고 그만두면`);
for (let m = 1; m <= 12; m++) {
  const a = severancePay({ hireDate: HIRE, retireDate: next(2027, m), ...P1 });
  const b = severancePay({ hireDate: HIRE, retireDate: next(2027, m), ...P2 });
  console.log(`2027-${String(m).padStart(2,'0')}-${last(2027,m)} | 석 달 ${a.periodDays}일 | 평균임금 ${Math.floor(a.avgDaily)} | 다닌 날 ${a.serviceDays} | 사람1 ${won(a.amount)}${a.usedOrdinary?'(통상)':''} | 사람2 ${won(b.amount)}${b.usedOrdinary?'(통상)':''}`);
}
console.log('## B. 사람1: 4월 말 vs 5월 말, 1월 2일 입사 다닌 햇수별');
for (const yrs of [1, 3, 5, 10, 20]) {
  const h = `${2027 - yrs}-01-02`;
  const a = severancePay({ hireDate: h, retireDate: '2027-05-01', ...P1 });
  const b = severancePay({ hireDate: h, retireDate: '2027-06-01', ...P1 });
  console.log(`${yrs}년 4개월(입사 ${h}) 4월말 ${won(a.amount)} | 5월말 ${won(b.amount)} | 차이 ${won(b.amount - a.amount)} | 통상적용 ${a.usedOrdinary}/${b.usedOrdinary}`);
}
console.log('## C. 사람2(기본급만): 4월 말 vs 5월 말 (입사 2017-01-02)');
{ const a = severancePay({ hireDate: HIRE, retireDate: '2027-05-01', ...P2 }); const b = severancePay({ hireDate: HIRE, retireDate: '2027-06-01', ...P2 });
  console.log(`4월말 ${won(a.amount)} | 5월말 ${won(b.amount)} | 차이 ${won(b.amount - a.amount)} | 하루 ${Math.floor(a.dailyWage)}`); }
console.log('## D. 경계: 31×89÷3 =', (31 * 89 / 3).toFixed(1), '일 · 2028(윤년) 4월 말 90일이면 31×90÷2 =', 31 * 90 / 2);
console.log('## E. 2028년(윤년) 사람1 입사 2018-01-02 4월말 vs 5월말');
{ const a = severancePay({ hireDate: '2018-01-02', retireDate: '2028-05-01', ...P1 }); const b = severancePay({ hireDate: '2018-01-02', retireDate: '2028-06-01', ...P1 });
  console.log(`${a.periodDays}일 ${won(a.amount)} → ${b.periodDays}일 ${won(b.amount)} 차이 ${won(b.amount - a.amount)}`); }
console.log('## F. 뉴시스 예(월 200만원 전부 평균임금으로만, 입사 2017-04-01 가정)');
const c1 = severancePay({ hireDate: '2017-04-01', retireDate: '2022-01-01', wages3m: 6000000 });
const c2 = severancePay({ hireDate: '2017-04-01', retireDate: '2022-05-01', wages3m: 6000000 });
const dA = Math.floor(6000000/89*30*c2.serviceDays/365) - Math.floor(6000000/92*30*c2.serviceDays/365);
const dB = Math.floor(6000000/89*30*c1.serviceDays/365) - Math.floor(6000000/92*30*c1.serviceDays/365);
console.log(`12/31 ${won(c1.amount)} | 4/30 ${won(c2.amount)} | 차이 ${won(c2.amount-c1.amount)} | 날수 덕분 ${won(dB)}~${won(dA)}(나누는 순서) | 1일 통상임금 ${Math.floor(ord(2000000))} vs 평균 ${Math.floor(c1.avgDaily)}·${Math.floor(c2.avgDaily)}`);
