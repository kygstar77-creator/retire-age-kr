// 건강보험 피부양자 자격 판정 (현행 제도 근사, 참고용 — 출처: 국민건강보험공단).
// 단위: 소득 만원, 재산세 과세표준 억원.
export function assessDependentEligibility({ otherIncomeManwon = 0, financialIncomeManwon = 0, propertyTaxBaseEok = 0, hasBusinessIncome = false, hasRentalIncome = false }) {
  const finIncome = Math.max(0, Number(financialIncomeManwon) || 0);
  const other = Math.max(0, Number(otherIncomeManwon) || 0);
  const prop = Math.max(0, Number(propertyTaxBaseEok) || 0);
  // 금융소득 1,000만원 이하면 합산서 전액 제외, 초과 시 전액 합산
  const combinedIncome = other + (finIncome > 1000 ? finIncome : 0);

  const reasons = [];
  let eligible = true;
  if (hasBusinessIncome) { eligible = false; reasons.push('사업자등록 있고 사업소득 있으면 제외돼요'); }
  if (hasRentalIncome) { eligible = false; reasons.push('주택임대소득이 있으면 제외돼요'); }
  if (prop > 9) { eligible = false; reasons.push('재산세 과세표준 9억을 넘으면 제외돼요'); }
  else if (prop > 5.4) {
    if (combinedIncome > 1000) { eligible = false; reasons.push('재산 과표 5.4억~9억이면 합산소득 1,000만원 이하만 유지돼요'); }
  } else if (combinedIncome > 2000) {
    eligible = false; reasons.push('합산소득 2,000만원을 넘으면 제외돼요');
  }
  if (finIncome > 1000) reasons.push(`금융소득 ${finIncome.toLocaleString()}만원(1,000만원 초과) 이라 전액 합산소득에 들어가요`);
  if (eligible) reasons.unshift('지금 조건이면 피부양자 자격을 유지해요');
  return { eligible, combinedIncome, reasons };
}

// 2026 기준 요율 (출처: 보건복지부·국민건강보험공단)
const RATE_2026 = 0.0719;           // 2026 건강보험료율 7.19%
const LTC_2026 = 0.9448 / 7.19;     // 2026 장기요양보험료(건보료 대비) ≈ 13.14%
const POINT_2026 = 211.5;           // 2026 재산보험료 부과점수당 금액(원)
const EMP_SHARE = 0.5;              // 직장가입자 보수월액보험료 근로자 부담 50%
const LOCAL_MIN = 20160;            // 2026 지역가입자 소득 최저보험료(원)

// 재산보험료 부과점수 — 국민건강보험법 시행령 [별표 4], 60등급 계단표(재산세 과표 만원 → 점수).
// 출처: 국민건강보험공단 재산등급별 점수 https://www.nhis.or.kr/nhis/policy/wbhada07910p01.do
const PROPERTY_GRADES = [
  [450, 22], [900, 44], [1350, 66], [1800, 97], [2250, 122], [2700, 146], [3150, 171], [3600, 195], [4050, 219], [4500, 244],
  [5020, 268], [5590, 294], [6220, 320], [6930, 344], [7710, 365], [8590, 386], [9570, 412], [10700, 439], [11900, 465], [13300, 490],
  [14800, 516], [16400, 535], [18300, 559], [20400, 586], [22700, 611], [25300, 637], [28100, 659], [31300, 681], [34900, 706], [38800, 731],
  [43200, 757], [48100, 785], [53600, 812], [59700, 841], [66500, 881], [74000, 921], [82400, 961], [91800, 1001], [103000, 1041], [114000, 1091],
  [127000, 1141], [142000, 1191], [158000, 1241], [176000, 1291], [196000, 1341], [218000, 1391], [242000, 1451], [270000, 1511], [300000, 1571], [330000, 1641],
  [363000, 1711], [399300, 1781], [439230, 1851], [483153, 1921], [531468, 1991], [584615, 2061], [643077, 2131], [707385, 2201], [778124, 2271], [Infinity, 2341]
];
export function propertyPoints(taxBaseManwon) {
  const v = Math.max(0, Number(taxBaseManwon) || 0);
  if (v <= 0) return 0;
  for (const [upper, pts] of PROPERTY_GRADES) if (v <= upper) return pts;
  return 2341;
}

// 지역가입자 월 건강보험료 근사 추정 (2026: 7.19%, 점수단가 211.5원, 재산 1억 공제, 장기요양 포함)
// 정확한 금액은 국민건강보험공단 확인 필요 — 참고용 근사치.
// halfRatedIncomeManwon: 근로소득·연금소득 — 지역가입자 소득월액 산정 때 50%만 반영된다(2022.9 부과체계 2단계 개편).
// 출처: 보건복지부 보도자료 '건강보험료 부과체계 2단계 개편 9월부터 시행'(2022-08-29, 근로·연금소득 평가율 50%)
//       https://www.mohw.go.kr/board.es?mid=a10503010100&bid=0027&act=view&list_no=372730
export function estimateLocalPremium({ chargeableIncomeManwon = 0, halfRatedIncomeManwon = 0, propertyTaxBaseEok = 0 }) {
  const ratedManwon = Math.max(0, Number(chargeableIncomeManwon) || 0) + Math.max(0, Number(halfRatedIncomeManwon) || 0) * 0.5;
  const incomeMonthly = (ratedManwon * 10000) * RATE_2026 / 12;
  const baseManwon = Math.max(0, ((Number(propertyTaxBaseEok) || 0) - 1) * 10000); // 만원, 재산 1억 기본공제
  const propMonthly = baseManwon > 0 ? propertyPoints(baseManwon) * POINT_2026 : 0;
  // 공단 산식: 소득보험료(최저보험료 하한) + 재산보험료. 재산보험료가 최저보험료를 흡수하지 않는다.
  const health = Math.max(LOCAL_MIN, incomeMonthly) + propMonthly;
  return { incomeMonthly: Math.round(incomeMonthly), propMonthly: Math.round(propMonthly), monthly: Math.round(health * (1 + LTC_2026)) };
}

// 바리스타 파이어(파트타임 4대보험 → 직장가입자) 월 건강보험료 근사 추정 (2026 기준).
// - 보수월액보험료: 보수월액 × 7.19% × 50%(근로자부담) + 장기요양
// - 소득월액보험료(보수외): 금융소득 1,000만원 이하면 합산 제외, 초과 시 전액 합산 →
//   합산 보수외소득(금융소득+임대·연금·사업 등)이 연 2,000만원 초과 시 그 초과분에만
//   ((합산−2,000만)÷12) × 7.19%(본인 100%) + 장기요양 추가.
// - 분리과세 등 일부 예외는 단순화. 정확한 금액은 국민건강보험공단 확인 — 참고용 근사치.
export function estimateBaristaPremium({ wageMonthlyManwon = 0, otherIncomeManwon = 0, financialIncomeManwon = 0 }) {
  const wage = Math.max(0, Number(wageMonthlyManwon) || 0) * 10000; // 원/월 보수월액
  const fin = Math.max(0, Number(financialIncomeManwon) || 0);      // 만원/년 금융소득
  const other = Math.max(0, Number(otherIncomeManwon) || 0);        // 만원/년 금융 외 보수외소득
  const finCounted = fin > 1000;                                    // 1,000만원 게이트
  const combinedOther = other + (finCounted ? fin : 0);            // 만원/년 합산 보수외소득
  const overThreshold = combinedOther > 2000;                       // 2,000만원 임계
  const overManwon = Math.max(0, combinedOther - 2000);            // 초과분(만원/년)

  const wagePremiumBase = wage * RATE_2026 * EMP_SHARE;            // 보수월액보험료(본인 50%)
  const incomePremiumBase = ((overManwon * 10000) / 12) * RATE_2026; // 소득월액보험료(본인 100%)
  const wagePremium = Math.round(wagePremiumBase * (1 + LTC_2026));
  const incomePremium = Math.round(incomePremiumBase * (1 + LTC_2026));
  return {
    combinedOther,
    overThreshold,
    finCounted,
    wagePremium,
    incomePremium,
    monthly: Math.round((wagePremiumBase + incomePremiumBase) * (1 + LTC_2026)),
  };
}
