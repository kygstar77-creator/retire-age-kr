// 도구 화면의 검색용 주소 — 스꾸(seukku.cc /s/{slug}) 방식.
// 앱은 해시(#dividend)로만 움직여 검색엔진엔 첫 화면 하나로 보였다. 그래서 도구마다 진짜 경로(/dividend)를 두고,
// 서버(functions/_middleware.js)가 그 경로에서 앱 껍데기의 title·description·canonical·og를 바꾸고
// 크롤러가 읽을 본문 블록(#sSeo)을 body 앞에 넣는다. 앱은 뜨자마자 그 블록을 지우고 해시 주소로 바꾼다 — 사람 눈엔 앱 그대로.
// 문구는 전부 그 화면에 이미 있는 제목·라벨. 새 말을 짓지 않는다.
export const TOOL_PAGES = [
  { path: '/dividend', screen: 'dividend', title: '배당으로 파이어', sections: ['배당 자산과 배당수익률', '월별 배당', '배당 캘린더'] },
  { path: '/health-insurance', screen: 'dependent', title: '파이어 후 건보료', sections: ['파이어 후 조건', '가입 형태', '금융소득 · 연', '금융 외 소득 · 연', '재산세 과세표준'] },
  { path: '/tax', screen: 'foreignTax', title: '양도·배당세', sections: ['해외주식 양도세 · 1년에 얼마나 팔아요?', '배당소득 · 1년에 배당을 얼마 받아요?', '세후 월 배당'] },
  { path: '/pension', screen: 'pension', title: '국민연금 조기수령', sections: ['몇 살부터 받을까요?', '받기 시작 나이', '예상연금월액'] },
  { path: '/cities', screen: 'cities', title: '어디서 살까', sections: ['전 세계 파이어 도시 지도', '1인 월 생활비 기준 · 빠른 순', '도시별 생활비·집값', '지역·가구별 필요 자산 사례'] },
  { path: '/firetype', screen: 'firetype', title: '파이어 유형 테스트', sections: ['내게 맞는 도시 Top3', '강점', '주의', '추천 행동'] },
  { path: '/ranking', screen: 'ranking', title: '랭킹', sections: ['계산하면 내 등수가 나와요', '랭킹 종류'] },
  { path: '/experiment', screen: 'experiment', title: '바꿔보기', sections: ['나이·자산', '월 저축 · 생활비 · 수익률', '국민연금', '부동산·부채·임대수익', '고급 가정', '자산 흐름'] },
  { path: '/news', screen: 'news', title: '소식', sections: ['오늘의 참고 지표', '배당락 이번 주 · 이 날 전에 사야 배당을 받아요', '경제 · 부동산 · 투자 · 부업 · 연금·세금 · 저축 · 파이어 후'] }
];

export const toolPageByPath = (pathname) => {
  const p = String(pathname || '').replace(/\/+$/, '') || '/';
  return TOOL_PAGES.find((t) => t.path === p) || null;
};
