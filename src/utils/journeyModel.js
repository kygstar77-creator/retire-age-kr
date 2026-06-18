// 스파인 — 한 사용자의 목표·단계 타깃·상황별 정보를 한 곳에서 정의.
// 모든 화면이 이 하나를 읽는다. firePlan(순수)에만 의존 → node 테스트 가능.
// '특정 종목 추천' 아님: 카테고리 배분·재무 타깃·상황별 정보 제공(합법).
import { firePlan } from './firePlan.js';

const r0 = (n) => Math.round(n || 0);
const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

// 나이·단계 기반 카테고리 배분(종목 아님). 합이 100.
function allocationFor(age, stage) {
  const a = Number(age) || 40;
  let growth = clamp(Math.round(110 - a), 20, 75); // 성장(주식/ETF)
  const remain = 100 - growth;
  // 파이어 임박/후(5단계+)엔 인컴(배당·임대) 비중을 높이고 안전자산 확보
  const incomeRatio = stage >= 5 ? 0.6 : 0.35;
  let income = Math.round(remain * incomeRatio); // 배당/인컴
  let safe = remain - income;                    // 채권/예금/현금
  if (safe < 5) { safe = 5; income = remain - safe; }
  return { growth, income, safe };
}

// 단계별 주기 가이드(무엇을 언제). 종목 아님 — 행동 안내.
function cadenceFor(stage) {
  const base = {
    daily: '오늘 저축·절약 1건 기록하고 파이어 시간 벌기',
    weekly: '이번 주 시장 반영 진도 확인 · 주간 미션 1개',
    monthly: '자산 업데이트 · 이번 달 저축 목표 점검 · 배분 리밸런싱 점검',
    yearly: '목표 재설정 · 단계 승급 점검 · 연말 세금/건보 체크'
  };
  if (stage >= 5) {
    base.monthly = '인출액·현금흐름 점검 · 건보료 확인 · 배분 점검';
    base.yearly = '인출 순서 재점검 · 건보 피부양자 자격 · 연금 수령 전략';
  }
  return base;
}

// 상황별 '필요한 정보'(투자 추천 아님 — 정보 제공). 현재 단계·입력 플래그로 가장 맞는 것 2~3개.
function situationInfo(inp, stage, sim) {
  const pool = [];
  const hiOn = Number(inp.healthInsuranceEnabled) === 1 && Number(inp.monthlyHealthInsurance) > 0;
  const divOn = Number(inp.dividendIncomeMonthly) > 0 || Number(inp.investType) === 2 || Number(inp.investType) === 3;
  const rentOn = Number(inp.monthlyRentalIncome) > 0;
  const overseasOn = Number(inp.overseasStayEnabled) === 1;

  // 주거·지역(전 단계 공통, 적립기엔 특히 강력)
  pool.push({ ico: '📍', title: '내 지역 주거비로 파이어 앞당기기', desc: '같은 자산이어도 사는 곳에 따라 파이어가 몇 년 빨라져요.', to: 'cities', w: stage <= 4 ? 9 : 5 });

  // 건강보험(파이어 임박/후 핵심)
  pool.push(hiOn
    ? { ico: '🩺', title: '건강보험료 더 줄이는 법', desc: `지금 월 ${r0(inp.monthlyHealthInsurance / 10000)}만 반영 중 · 피부양자·임의계속으로 절감 여지`, to: 'dependent', w: stage >= 4 ? 9 : 4 }
    : { ico: '🩺', title: '파이어 후 건강보험료, 피부양자로 아끼기', desc: '직장 그만두면 지역가입자로 보험료가 확 올라요. 미리 설계해요.', to: 'dependent', w: stage >= 4 ? 8 : 4 });

  // 인출 순서(자산 형성 후)
  pool.push({ ico: '💸', title: '어느 계좌부터 빼 써야 세금이 덜 나오나', desc: '인출 순서만 바꿔도 세금이 달라져요. 파이어 후 현금흐름 설계.', to: 'foreignTax', w: stage >= 4 ? 8 : 3 });

  // 배당 현금흐름
  pool.push(divOn
    ? { ico: '💵', title: '배당 현금흐름 점검하기', desc: '배당으로 받는 월 소득과 세금을 계산에 반영해요.', to: 'dividend', w: 6 }
    : { ico: '💵', title: '배당으로 월 현금흐름 만들기', desc: '자산 일부를 배당으로 돌리면 인출 부담이 줄어요.', to: 'dividend', w: stage >= 3 ? 6 : 4 });

  // 임대소득
  if (rentOn || stage >= 3) {
    pool.push({ ico: '🏠', title: '임대소득으로 버티는 시나리오', desc: '부동산을 안 팔고 월세로 생활비를 메우는 경로를 비교해요.', to: 'experiment', w: rentOn ? 7 : 4 });
  }

  // 해외 체류
  pool.push(overseasOn
    ? { ico: '✈️', title: '해외 체류 기간·생활비 점검', desc: '체류 비중에 따라 생활비와 건보가 달라져요.', to: 'experiment', w: 6 }
    : { ico: '✈️', title: '파이어 후 해외 체류로 생활비 줄이기', desc: '물가 낮은 곳에서 일정 기간 살면 자산 수명이 늘어요.', to: 'experiment', w: stage >= 5 ? 6 : 3 });

  return pool.sort((a, b) => b.w - a.w).slice(0, 3).map(({ w, ...x }) => x);
}

export function journeyModel(simulation, { stage = 1, incomeOverride } = {}) {
  const inp = (simulation && simulation.inputs) || {};
  const plan = firePlan(simulation);
  const age = Number(inp.currentAge) || 0;
  const living = Math.max(0, Number(inp.monthlyLivingCost) || 0);
  const invest = Math.max(0, Number(inp.monthlyInvestment) || 0);
  const proxyIncome = living + invest; // 가용소득(월) 추정: 쓰거나 모으거나
  const incomeIsReal = Number(incomeOverride) > 0;
  const income = incomeIsReal ? Number(incomeOverride) : proxyIncome; // 실제 월 소득 입력 시 그 값 사용
  const curSavingsRate = income > 0 ? Math.round((invest / income) * 100) : 0;
  const needMonthly = plan.pmt;
  // 지금 저축률과 같은 소득 기준으로 비교(사과 대 사과). 목표 도달에 필요한 저축이 소득의 몇 %인지.
  const needSavingsRate = income > 0 ? Math.min(100, Math.round((needMonthly / income) * 100)) : 0;

  const targets = {
    income,
    incomeIsReal,
    curSavingsRate,
    needMonthly,
    needSavingsRate,
    housingMax: r0(living * 0.30),     // 주거비 권장 상한(월) — 생활비의 30%
    emergencyFund: r0(living * 6),     // 비상금 6개월
    allocation: allocationFor(age, stage),
    sideIncomeGoal: Math.max(0, needMonthly - invest) // 부족분을 부업으로 메운다면(월)
  };

  return {
    stage,
    plan,
    targets,
    situation: situationInfo(inp, stage, simulation),
    cadence: cadenceFor(stage)
  };
}
