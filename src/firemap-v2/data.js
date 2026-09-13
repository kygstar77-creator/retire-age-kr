export const STORAGE_KEY = 'firemap-inputs-v3';
export const CONTACT_EMAIL = 'retireage.kr@gmail.com';
export const BASE_URL = 'https://firemap.kr/';

export const returnAssumptions = {
  annualReturnRate: 5,
  inflationRate: 3,
  label: '지금 계산 기준 · 연 수익률 5% · 물가 3%'
};

export const investmentScenarios = [
  { key: 'conservative', label: '보수형(예적금)', annualReturnRate: 3, copy: '예금·현금성 자산 수준의 낮은 변동성' },
  { key: 'balanced', label: '균형형', annualReturnRate: 5, copy: '주식+예금·채권을 섞은 보수적 균형' },
  { key: 'schd', label: '배당다우존스(SCHD)', annualReturnRate: 9, copy: '배당 중심 · S&P500보다 변동성 낮음' },
  { key: 'sp500', label: 'S&P500형', annualReturnRate: 10, copy: '미국 대형주 장기 평균(통념 ~10%)' },
  { key: 'nasdaq100', label: '나스닥100형', annualReturnRate: 13, copy: '성장·기술주 · 고수익 고변동' }
];

export const questions = [
  { key: 'currentAge', type: 'age', label: '지금 나이', title: '지금 몇 살이에요?', helper: '여기서부터 파이어까지 남은 시간을 세요.', step: 1 },
  { key: 'targetRetirementAge', type: 'age', label: '목표 나이', title: '몇 살에 파이어하고 싶어요?', helper: '1살 차이로도 필요 자산이 많이 달라져요.', step: 1 },
  { key: 'financialAsset', type: 'money', label: '지금 자산', title: '지금 굴릴 수 있는 돈은 얼마예요?', helper: '주식·예금·현금처럼 파이어 후 생활비로 쓸 수 있는 돈이에요. 집은 빼요.', step: 1000000, presets: [0, 50000000, 100000000, 300000000], unit: '100만원 단위' },
  { key: 'monthlyInvestment', type: 'money', label: '월 저축', title: '매달 얼마를 모아요?', helper: '앞으로 매달 투자하거나 저축할 돈이에요.', step: 100000, presets: [0, 500000, 1000000, 2000000], unit: '10만원 단위' },
  { key: 'monthlyLivingCost', type: 'money', label: '파이어 후 생활비', title: '파이어 후 한 달에 얼마 써요?', helper: '주거·식비·취미·여행을 넣은 한 달 생활비예요. 건강보험료는 따로 계산해요.', step: 100000, presets: [2000000, 3000000, 4000000, 5000000], unit: '10만원 단위' }
];

export const domesticCities = [
  ['전주', 3000000, '한옥마을과 대학병원이 있는 도심 생활권이에요', '대학병원 의료 인프라 · KTX로 수도권 1.5시간 · 국민건강보험 그대로'],
  ['원주', 2800000, '수도권에서 가깝고 주거비가 낮은 지역이에요', '수도권 1시간대 · 종합병원 보유 · 건보 변동 없음'],
  ['강릉', 3300000, '바다와 도시 인프라를 같이 갖춘 지역이에요', '해안 도시 · 종합병원 보유 · 겨울 난방비 고려']
];

export const overseasCities = [
  ['치앙마이', 2200000, '카페와 코워킹 공간이 많은 태국 북부 도시예요', '비자: 관광·교육·파이어(O-A) 옵션 · 민간 의료보험 권장 · 건기 11~2월 쾌적'],
  ['다낭', 2400000, '따뜻한 기후의 베트남 중부 해안 도시예요', '비자: 관광·이주 옵션 · 사보험 필요 · 우기 9~12월 유의'],
  ['쿠알라룸푸르', 2900000, '대도시 인프라와 영어 생활권을 갖춘 도시예요', '비자: MM2H 등 장기 옵션 · 의료 수준 양호 · 연중 고온다습'],
  ['방콕', 2700000, '대형 병원과 쇼핑몰이 많은 태국 수도예요', '비자: 관광·장기(은퇴) 옵션 · 사보험 권장 · 연중 무더위(건기 11~2월)'],
  ['우붓(발리)', 2300000, '논밭과 요가 스튜디오가 많은 발리 내륙 지역이에요', '비자: 관광·B211/은퇴 옵션 · 사보험 필요 · 우기 11~3월'],
  ['세부', 2100000, '해변과 다이빙 명소가 많은 필리핀 섬이에요', '비자: 관광 연장·은퇴(SRRV) 옵션 · 사보험 필요 · 우기 6~11월 유의'],
  ['트빌리시', 2000000, '구시가와 온천·와이너리가 있는 조지아 수도예요', '비자: 다수 국적 장기 무비자 체류(요건 확인) · 사보험 권장 · 사계절 뚜렷'],
  ['리스본', 3800000, '대서양 연안의 언덕 도시, 물가는 서유럽 중 낮은 편이에요', '비자: 유럽 장기(D7 등) 옵션(요건 까다로움) · 주거비 상승세 유의 · 온화'],
  ['후쿠오카', 3300000, '한국에서 가까운 일본 규슈 도시예요', '비자: 관광·장기 옵션 · 의료·치안 우수 · 사계절 · 근거리']
];
