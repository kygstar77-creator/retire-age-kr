// N-3 계산 — 연봉 사다리(3천~1억): 통장에 월 얼마(세후) + 국세청 줄에서 어디쯤
// 세후: firemap 월급 계산기와 같은 함수(src/utils/salaryNet.js, 간이세액표 2026.2.27 개정·4대보험 2026 요율)
// 줄: 국세청 근로소득 백분위(천분위) 2024년 귀속(data.go.kr 15082063, 수정 2026-05-08) = ep/N-1/nts_pct.json
//   원자료는 구간마다 '그 1% 사람들의 평균 총급여'만 준다(경계값 없음) → 보간하지 않고 '평균이 바로 위·아래인 두 구간'만 읽는다.
//   국세청 총급여 = 비과세(식대 등) 뺀 금액 → 연봉에서 비과세 연 240만원을 뺀 값으로 줄에 세운다.
import fs from 'fs';
import { salaryNet } from '../../../../../src/utils/salaryNet.js';
const NT = JSON.parse(fs.readFileSync(new URL('../N-1/nts_pct.json', import.meta.url), 'utf8'));
const pct = NT.rows.filter(r => !r.k.includes('.') || r.k === '상위 1.0%').map(r => ({ p: r.k === '상위 1.0%' ? 1 : +r.k.replace(/[^0-9]/g, ''), avg: r.avg_man }));
const LADDER = [3000, 4000, 5000, 6000, 7000, 8000, 10000];
const won = n => n.toLocaleString('ko-KR');
console.log('# A. 1인(본인만)·식대 비과세 월 20만·자녀 0·간이세액 100% (firemap 계산기 기본값)');
for (const m of LADDER) {
  const r = salaryNet({ annual: m * 10000 });
  const gross = m - 240; // 국세청 총급여(만원)
  let hi = null, lo = null; // hi: 평균이 gross 이상인 가장 아래 구간, lo: 평균이 gross 미만인 가장 위 구간
  for (const b of pct) { if (b.avg >= gross) hi = b; else { lo = b; break; } }
  console.log(`연봉 ${won(m)}만 | 월 세전 ${won(r.monthly)} | 공제 ${won(r.deductions)} (연금 ${won(r.pension)}·건강 ${won(r.health)}·요양 ${won(r.ltc)}·고용 ${won(r.employment)}·소득세 ${won(r.incomeTax)}·지방 ${won(r.localTax)}) | 통장 월 ${won(r.net)} (${(r.net / r.monthly * 100).toFixed(1)}%) | 국세청 총급여 ${won(gross)}만 → 상위 ${hi?.p}% 구간 평균 ${won(hi?.avg)}만 ~ 상위 ${lo?.p}% 구간 평균 ${won(lo?.avg)}만 사이`);
}
console.log('\n# B. 누구라면 — 4인(본인·배우자·8~20세 자녀 2)·같은 비과세');
for (const m of LADDER) {
  const a = salaryNet({ annual: m * 10000 }), b = salaryNet({ annual: m * 10000, family: 4, kids: 2 });
  console.log(`연봉 ${won(m)}만 | 1인 ${won(a.net)} | 4인·자녀2 ${won(b.net)} | 차 ${won(b.net - a.net)} (소득세+지방 ${won(a.incomeTax + a.localTax)} → ${won(b.incomeTax + b.localTax)})`);
}
console.log('\n# C. 오를 때 덜 느는 몫 — 연봉 1천만원 오를 때 통장 월 증가');
for (let i = 1; i < LADDER.length; i++) {
  const a = salaryNet({ annual: LADDER[i - 1] * 10000 }), b = salaryNet({ annual: LADDER[i] * 10000 });
  const dm = b.monthly - a.monthly, dn = b.net - a.net;
  console.log(`${won(LADDER[i - 1])}→${won(LADDER[i])}만 | 세전 월 +${won(dm)} | 통장 월 +${won(dn)} (${(dn / dm * 100).toFixed(1)}%가 남음)`);
}
console.log('\n# D. 국세청 줄 기준점(2024년 귀속, 구간 평균 총급여 만원): 전체 평균', won(Math.round(NT.G_eok * 1e8 / NT.N / 1e4)), '· 인원', won(NT.N));
for (const p of [1, 10, 20, 30, 40, 50]) { const b = pct.find(x => x.p === p); console.log(`상위 ${p}% 구간 평균 ${won(b.avg)}만`); }
// 10/27 youtube-loop: 댓글 질문(kEXcudKBf8A '5000이 355라구요? 훨씬 적을 텐데' → 답글 '비과세 아예 없는 기준 348')에 답하려고 비과세 0 칸을 더함
console.log('\n# E. 비과세(식대) 없는 회사라면 — 같은 연봉, 1인');
for (const m of LADDER) {
  const a = salaryNet({ annual: m * 10000 }), z = salaryNet({ annual: m * 10000, nontaxMonthly: 0 });
  console.log(`연봉 ${won(m)}만 | 식대 비과세 20만 ${won(a.net)} | 비과세 0 ${won(z.net)} | 차 ${won(a.net - z.net)}`);
}
// 댓글 '난 왜 상위25%인데' → 상위 25% 구간 평균 총급여의 연봉(+240만)이 통장에 얼마
console.log('\n# F. 국세청 구간 평균 총급여를 연봉(+비과세 240만)으로 놓으면 통장 월(1인)');
for (const p of [10, 25, 50]) { const b = pct.find(x => x.p === p); const r = salaryNet({ annual: (b.avg + 240) * 10000 }); console.log(`상위 ${p}% 구간 평균 총급여 ${won(b.avg)}만 → 연봉 ${won(b.avg + 240)}만 → 통장 월 ${won(r.net)}`); }
// 10/27 youtube-loop: 간이세액 80·100·120% 선택(소득세법 시행령 제194조①) — 미리 떼는 몫만 바뀜
console.log('\n# G. 간이세액 80%·120%를 고르면 통장 월(1인)');
for (const m of [5000, 10000]) { const [a, b, c] = [80, 100, 120].map(ratio => salaryNet({ annual: m * 10000, ratio })); console.log(`연봉 ${won(m)}만 | 80% ${won(a.net)} | 100% ${won(b.net)} | 120% ${won(c.net)} | 80%와 100% 차 ${won(a.net - b.net)}`); }
// 3천과 1억, 공제 중 소득세+지방 몫
console.log('\n# H. 공제 중 소득세+지방소득세가 차지하는 몫(1인)');
for (const m of [3000, 10000]) { const r = salaryNet({ annual: m * 10000 }); console.log(`연봉 ${won(m)}만 | 공제 ${won(r.deductions)} 중 소득세+지방 ${won(r.incomeTax + r.localTax)} (${((r.incomeTax + r.localTax) / r.deductions * 100).toFixed(1)}%) · 4대보험 ${won(r.deductions - r.incomeTax - r.localTax)}`); }
// 10/28 youtube-loop: 8분 바닥 보강 — 거꾸로 묻는 검색(세후300연봉 1,420·세후400연봉 1,210·실수령300연봉 930·실수령500연봉 800, kwvol 10/28)
//   통장 월 목표 → 같은 함수로 연봉을 10만원 단위로 올려 처음 넘는 값(1인·식대 20만·간이세액 100%)
console.log('\n# I. 거꾸로 — 통장 월 300·400·500·600만원이 되려면 연봉 얼마(1인, 10만원 단위로 처음 넘는 연봉)');
for (const goal of [3000000, 4000000, 5000000, 6000000]) {
  let m = 2000; while (salaryNet({ annual: m * 10000 }).net < goal) m += 10;
  const r = salaryNet({ annual: m * 10000 }); const gross = m - 240;
  let hi = null, lo = null; for (const b of pct) { if (b.avg >= gross) hi = b; else { lo = b; break; } }
  console.log(`통장 월 ${won(goal)} → 연봉 ${won(m)}만 (통장 ${won(r.net)}, 세전 월 ${won(r.monthly)}, 세전의 ${(r.net / r.monthly * 100).toFixed(1)}%) · 국세청 총급여 ${won(gross)}만 → 상위 ${hi?.p}%~${lo?.p}% 구간 평균 사이`);
}
// 1억 위 두 칸(연봉1억2천실수령액 790·연봉1억5천실수령액 1,060, kwvol 10/28)
console.log('\n# J. 1억 위 — 1억 2천·1억 5천(1인)과 1억에서 오를 때');
let prev = salaryNet({ annual: 100000000 });
for (const m of [12000, 15000]) {
  const r = salaryNet({ annual: m * 10000 }); const gross = m - 240;
  let hi = null, lo = null; for (const b of pct) { if (b.avg >= gross) hi = b; else { lo = b; break; } }
  const dm = r.monthly - prev.monthly, dn = r.net - prev.net;
  console.log(`연봉 ${won(m)}만 | 월 세전 ${won(r.monthly)} | 통장 ${won(r.net)} (${(r.net / r.monthly * 100).toFixed(1)}%) | 연금 ${won(r.pension)}·소득세 ${won(r.incomeTax)} | 앞 칸에서 세전 월 +${won(dm)} → 통장 +${won(dn)} (${(dn / dm * 100).toFixed(1)}%) | 총급여 ${won(gross)}만 → 상위 ${hi?.p}%~${lo?.p}% 구간 평균 사이`);
  prev = r;
}
// 10/28 youtube-loop: 거꾸로 칸의 '누구라면' — 같은 통장 목표에 식대 비과세 없음·4인(자녀 2)이면 필요한 연봉
console.log('\n# K. 거꾸로 — 조건이 다르면 필요한 연봉(10만원 단위로 처음 넘는 값)');
for (const goal of [3000000, 4000000, 5000000]) {
  const need = opt => { let m = 2000; while (salaryNet({ annual: m * 10000, ...opt }).net < goal) m += 10; return m; };
  const a = need({}), z = need({ nontaxMonthly: 0 }), f = need({ family: 4, kids: 2 });
  console.log(`통장 월 ${won(goal)} | 1인·식대 20만 ${won(a)}만 | 식대 비과세 0 ${won(z)}만 (+${won(z - a)}만) | 4인·자녀2 ${won(f)}만 (${won(f - a)}만)`);
}
// 연봉 두 배(5천→1억)일 때 통장 배수
{ const a = salaryNet({ annual: 50000000 }), b = salaryNet({ annual: 100000000 }); console.log(`\n# L. 연봉 5천→1억(2배) | 세전 월 ${(b.monthly / a.monthly).toFixed(3)}배 | 통장 ${won(a.net)} → ${won(b.net)} = ${(b.net / a.net).toFixed(3)}배 (+${won(b.net - a.net)})`); }
