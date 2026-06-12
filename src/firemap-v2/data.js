export const STORAGE_KEY = 'firemap-inputs-v3';
export const CONTACT_EMAIL = 'retireage.kr@gmail.com';
export const BASE_URL = 'https://firemap.kr/';

export const returnAssumptions = {
  annualReturnRate: 5,
  inflationRate: 3,
  label: '현재 계산 기준 · 연 수익률 5% · 물가 3%'
};

export const investmentScenarios = [
  { key: 'conservative', label: '보수형', annualReturnRate: 3, copy: '예금·현금성 자산에 가까운 낮은 변동성 가정' },
  { key: 'balanced', label: '균형형', annualReturnRate: 5, copy: '예금과 투자자산을 섞어보는 기본 가정' },
  { key: 'sp500', label: 'S&P500형', annualReturnRate: 8, copy: '미국 대형주 지수 장기투자에 가까운 공격 가정' },
  { key: 'nasdaq100', label: '나스닥100형', annualReturnRate: 10, copy: '성장주·기술주 비중이 높은 고변동 가정' }
];

export const questions = [
  { key: 'currentAge', type: 'age', label: '현재 나이', title: '지금 몇 살인가요?', helper: '현재 나이를 기준으로 퇴사까지 남은 시간을 계산해요.', step: 1 },
  { key: 'targetRetirementAge', type: 'age', label: '퇴사 희망 나이', title: '몇 살에 퇴사하고 싶나요?', helper: '1살 차이도 결과에 크게 영향을 줘요.', step: 1 },
  { key: 'financialAsset', type: 'money', label: '금융자산', title: '지금 금융자산은 얼마인가요?', helper: '주식, 예금, 현금처럼 퇴사 후 생활비에 쓸 수 있는 돈 기준이에요.', step: 1000000, presets: [0, 50000000, 100000000, 300000000], unit: '100만 원 단위' },
  { key: 'monthlyInvestment', type: 'money', label: '월 저축액', title: '퇴사 전 매달 얼마를 모을까요?', helper: '앞으로 매달 투자하거나 저축할 금액을 입력해주세요.', step: 100000, presets: [0, 500000, 1000000, 2000000], unit: '10만 원 단위' },
  { key: 'monthlyLivingCost', type: 'money', label: '퇴사 후 월 생활비', title: '퇴사 후 한 달 생활비는?', helper: '주거비, 식비, 보험료, 취미, 여행비를 포함한 월 생활비예요.', step: 100000, presets: [2000000, 3000000, 4000000, 5000000], unit: '10만 원 단위' }
];

export const domesticCities = [
  ['전주', 3000000, '한옥마을·대학병원·도심 생활권을 함께 보는 국내 장기 거주 후보지', '대학병원 의료 인프라 · KTX로 수도권 1.5시간 · 국민건강보험 그대로'],
  ['원주', 2800000, '수도권 접근성과 낮은 주거비를 같이 노리는 반퇴 생활 후보지', '수도권 1시간대 · 종합병원 보유 · 건보 변동 없음'],
  ['강릉', 3300000, '바다와 도시 인프라를 포기하지 않으면서 생활비를 낮추는 시나리오', '해안 도시 · 종합병원 보유 · 겨울 난방비 고려']
];

export const overseasCities = [
  ['치앙마이', 2200000, '카페·코워킹·장기체류 커뮤니티가 강한 대표 저비용 FIRE 후보지', '비자: 관광·교육·은퇴(O-A) 옵션 · 민간 의료보험 권장 · 건기 11~2월 쾌적'],
  ['다낭', 2400000, '따뜻한 기후와 낮은 체류비를 활용하는 단기 해외살이 시나리오', '비자: 관광·이주 옵션 · 사보험 필요 · 우기 9~12월 유의'],
  ['쿠알라룸푸르', 2900000, '대도시 인프라와 영어 생활권을 함께 보는 해외 FIRE 후보지', '비자: MM2H 등 장기 옵션 · 의료 수준 양호 · 연중 고온다습']
];
