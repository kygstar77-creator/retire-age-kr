// 성과급 원천징수 — 소득세법 제136조①1·2호, 시행령 제195조. 간이세액표는 firemap 연봉 실수령 계산기(src/utils/salaryNet.js tableTax, 별표2 2026)를 그대로 쓴다.
import { tableTax, salaryNet } from '../../../src/utils/salaryNet.js';
const won = n => n.toLocaleString('ko-KR');
function bonusTax(monthlyTaxable, bonus, months, fam = 1) {
  const reg = tableTax(monthlyTaxable, fam);                 // 평소 달 소득세
  const withBonus = tableTax(monthlyTaxable + Math.floor(bonus / months), fam) * months; // (상여/월수 + 월평균급여) 세액 × 월수
  const already = reg * (months - 1);                         // 지급 달 전까지 이미 뗀 세액(지급 달 급여와 같이 낼 때)
  const thisMonth = withBonus - already;                      // 지급 달에 떼는 소득세(그 달 급여분 포함)
  const bonusOnly = thisMonth - reg;                          // 성과급 몫
  return { reg, thisMonth, bonusOnly, local: Math.floor(bonusOnly / 10 / 10) * 10 };
}
const out = [];
for (const [label, m] of [['월 과세급여 400만원', 4_000_000], ['월 과세급여 250만원', 2_500_000], ['월 과세급여 600만원', 6_000_000]]) {
  for (const [when, months] of [['10월(1~10월=10개월)', 10], ['3월(1~3월=3개월)', 3], ['12월(12개월)', 12]]) {
    const r = bonusTax(m, 10_000_000, months);
    out.push(`${label} · 성과급 1,000만원 ${when}: 평소 소득세 ${won(r.reg)} · 성과급 몫 소득세 ${won(r.bonusOnly)} · 지방소득세 ${won(r.local)} · 합계 ${won(r.bonusOnly + r.local)} · 통장(세금만 뺀) ${won(10_000_000 - r.bonusOnly - r.local)}`);
  }
}
// 잘못 알려진 방식: 그 달 급여+성과급을 한 달 소득으로 보고 간이세액표 적용
const wrong = tableTax(4_000_000 + 10_000_000, 1) - tableTax(4_000_000, 1);
out.push(`비교(법 방식 아님) 월 400만+1,000만을 한 달치로 표 적용 시 성과급 몫 소득세 ${won(wrong)}`);
console.log(out.join('\n'));
