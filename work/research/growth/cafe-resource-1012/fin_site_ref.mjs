// 사이트 /health-insurance 식(src/firemap-v2/healthInsurance.js)으로 검산 예시 값을 낸다. fin_verify.py가 부른다.
//   node fin_site_ref.mjs cases.json   (cases: [{id, fin, pension, prop}] — 원 단위)
// 화면(src/components/firemap/DependentCheck.jsx)과 같은 연결: 금융 외 소득(임대·사업) 0, 공적연금·근로는 halfRated.
import { readFileSync } from 'node:fs';
import { assessDependentEligibility, estimateLocalPremium } from '../../../../src/firemap-v2/healthInsurance.js';

const toMan = (won) => Math.round((Number(won) || 0) / 10000);
const cases = JSON.parse(readFileSync(process.argv[2], 'utf-8'));
const out = {};
for (const c of cases) {
  const fin = toMan(c.fin), half = toMan(c.pension), prop = (Number(c.prop) || 0) / 1e8;
  const r = assessDependentEligibility({ otherIncomeManwon: half, financialIncomeManwon: fin, propertyTaxBaseEok: prop });
  const est = estimateLocalPremium({ chargeableIncomeManwon: fin > 1000 ? fin : 0, halfRatedIncomeManwon: half, propertyTaxBaseEok: prop });
  const est0 = estimateLocalPremium({ chargeableIncomeManwon: 0, halfRatedIncomeManwon: half, propertyTaxBaseEok: prop });
  out[c.id] = { eligible: r.eligible, combined: r.combinedIncome * 10000, incomeMonthly: est.incomeMonthly, propMonthly: est.propMonthly, monthly: est.monthly, monthly0: est0.monthly };
}
console.log(JSON.stringify(out));
