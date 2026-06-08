export const STORAGE_KEY = 'firemap-inputs-v2';
export const CONTACT_EMAIL = 'retireage.kr@gmail.com';
export const BASE_URL = 'https://retire-age-kr.pages.dev/';

export const returnAssumptions = {
  annualReturnRate: 8,
  inflationRate: 3,
  label: '현재 계산 기준 · 연 수익률 8% · 물가 3%'
};

export const investmentScenarios = [
  { key: 'conservative', label: '보수형', annualReturnRate: 4, copy: '예금·현금성 자산에 가까운 낮은 변동성 가정' },
  { key: 'sp500', label: 'S&P500형', annualReturnRate: 8, copy: '미국 대형주 지수 장기투자에 가까운 기본 가정' },
  { key: 'nasdaq100', label: '나스닥100형', annualReturnRate: 10, copy: '성장주·기술주 비중이 높은 공격형 가정' },
  { key: 'dividendDow', label: '배당다우존스형', annualReturnRate: 7, copy: '배당과 현금흐름을 함께 보는 중간 가정' }
];

export const questions = [
  { key: 'currentAge', type: 'age', label: '현재 나이', title: '지금 몇 살인가요?', helper: '현재 나이를 기준으로 퇴사까지 남은 시간을 계산해요.', step: 1 },
  { key: 'targetRetirementAge', type: 'age', label: '퇴사 희망 나이', title: '몇 살에 퇴사하고 싶나요?', helper: '1살 차이도 결과에 크게 영향을 줘요.', step: 1 },
  { key: 'financialAsset', type: 'money', label: '금융자산', title: '지금 금융자산은 얼마인가요?', helper: '주식, 예금, 현금처럼 퇴사 후 생활비에 쓸 수 있는 돈 기준이에요.', step: 1000000, presets: [100000000, 300000000, 500000000, 1000000000], unit: '100만 원 단위' },
  { key: 'monthlyInvestment', type: 'money', label: '월 저축액', title: '퇴사 전 매달 얼마를 모을까요?', helper: '앞으로 매달 투자하거나 저축할 금액을 입력해주세요.', step: 100000, presets: [500000, 1000000, 2000000, 3000000], unit: '10만 원 단위' },
  { key: 'monthlyLivingCost', type: 'money', label: '퇴사 후 월 생활비', title: '퇴사 후 한 달 생활비는?', helper: '주거비, 식비, 보험료, 취미, 여행비를 포함한 월 생활비예요.', step: 100000, presets: [2500000, 3500000, 5000000, 7000000], unit: '10만 원 단위' }
];

export const domesticCities = [
  ['전주', 3500000, '한옥마을·대학병원·도심 생활권을 함께 보는 국내 장기 거주 후보지'],
  ['원주', 3300000, '수도권 접근성과 낮은 주거비를 같이 노리는 반퇴 생활 후보지'],
  ['강릉', 3700000, '바다와 도시 인프라를 포기하지 않으면서 생활비를 낮추는 시나리오']
];

export const overseasCities = [
  ['치앙마이', 2600000, '카페·코워킹·장기체류 커뮤니티가 강한 대표 저비용 FIRE 후보지'],
  ['다낭', 2800000, '따뜻한 기후와 낮은 체류비를 활용하는 단기 해외살이 시나리오'],
  ['쿠알라룸푸르', 3200000, '대도시 인프라와 영어 생활권을 함께 보는 해외 FIRE 후보지']
];
