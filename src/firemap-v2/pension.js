// 국민연금 수령 시기 조정 — 조기수령은 연 6% 감액(최대 5년 30%), 연기수령은 연 7.2% 가산(최대 5년 36%).
// 둘 다 평생 유지된다. 참고용 계산이에요.
// 출처: 국민연금공단 노령연금 안내 https://www.nps.or.kr/pnsinfo/ntpsklg/getOHAF0056M0.do
export function earlyClaim(normalMonthly, normalAge, claimAge) {
  const nm = Math.max(0, Number(normalMonthly) || 0);
  const na = Number(normalAge) || 0;
  const ca = Number(claimAge) || 0;
  const yearsEarly = Math.min(5, Math.max(0, na - ca));
  const yearsLate = Math.min(5, Math.max(0, ca - na));
  const reductionPct = yearsEarly * 6;
  const bonusPct = yearsLate * 7.2;
  const factor = yearsLate > 0 ? 1 + bonusPct / 100 : Math.max(0.7, 1 - reductionPct / 100);
  return { claimAge: ca, yearsEarly, yearsLate, reductionPct, bonusPct, factor, monthly: Math.round(nm * factor) };
}

// 노령연금을 받기 시작하는 나이는 출생연도로 법에 정해져 있다(국민연금법 부칙).
// 1953~56년생 61세 · 57~60년생 62세 · 61~64년생 63세 · 65~68년생 64세 · 69년생부터 65세.
export function pensionStartAgeForBirthYear(birthYear) {
  const y = Number(birthYear) || 0;
  if (!y || y <= 1952) return 60;
  if (y <= 1956) return 61;
  if (y <= 1960) return 62;
  if (y <= 1964) return 63;
  if (y <= 1968) return 64;
  return 65;
}

// 조기수령은 개시연령 -5년까지, 연기수령은 +5년까지만 가능하다.
export function clampClaimAge(claimAge, normalAge) {
  const n = Number(normalAge) || 65;
  const c = Number(claimAge) || 0;
  if (!c) return 0;
  return Math.max(n - 5, Math.min(n + 5, Math.round(c)));
}
