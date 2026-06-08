export const STORAGE_KEY = 'firemap-inputs-v2';
export const CONTACT_EMAIL = 'retireage.kr@gmail.com';
export const BASE_URL = 'https://retire-age-kr.pages.dev/';

export const questions = [
  { key: 'currentAge', type: 'age', label: '현재 나이', title: '지금 몇 살인가요?', helper: '현재 나이를 기준으로 퇴사까지 남은 시간을 계산해요.', step: 1 },
  { key: 'targetRetirementAge', type: 'age', label: '퇴사 희망 나이', title: '몇 살에 퇴사하고 싶나요?', helper: '1살 차이도 결과에 크게 영향을 줘요.', step: 1 },
  { key: 'financialAsset', type: 'money', label: '금융자산', title: '지금 금융자산은 얼마인가요?', helper: '주식, 예금, 현금처럼 퇴사 후 생활비에 쓸 수 있는 돈 기준이에요.', step: 1000000, presets: [100000000, 300000000, 500000000, 1000000000], unit: '100만 원 단위' },
  { key: 'monthlyInvestment', type: 'money', label: '월 저축액', title: '퇴사 전 매달 얼마를 모을까요?', helper: '앞으로 매달 투자하거나 저축할 금액을 입력해주세요.', step: 100000, presets: [500000, 1000000, 2000000, 3000000], unit: '10만 원 단위' },
  { key: 'monthlyLivingCost', type: 'money', label: '퇴사 후 월 생활비', title: '퇴사 후 한 달 생활비는?', helper: '주거비, 식비, 보험료, 취미, 여행비를 포함한 월 생활비예요.', step: 100000, presets: [2500000, 3500000, 5000000, 7000000], unit: '10만 원 단위' }
];

export const domesticCities = [
  ['전주', 3500000, '주거비와 생활비를 낮추면서 도시 인프라를 유지하는 국내형 시나리오'],
  ['원주', 3300000, '수도권 접근성과 낮은 주거비를 함께 보는 반퇴형 시나리오'],
  ['강릉', 3700000, '해안 생활 선호자를 위한 생활비 절감·삶의 만족도 균형 시나리오']
];

export const overseasCities = [
  ['치앙마이', 2600000, '연 3개월 체류 기준. 생활비 절감과 건보료 조정 가능성을 함께 확인'],
  ['다낭', 2800000, '따뜻한 기후와 낮은 체류비를 반영한 단기 해외살이 시나리오'],
  ['쿠알라룸푸르', 3200000, '도시 인프라와 영어 생활권을 고려한 해외 FIRE 후보지']
];
