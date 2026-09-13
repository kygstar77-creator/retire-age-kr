// 화면 테이블 — 탭 4(결과·바꿔보기·랭킹·전체), 화면 15. 라우터는 이 표만 읽는다.
// 2026-09-13 슬림화: 저축(파이어 통·규칙 칩·26주·달력)과 오늘 홈, 여정 지도를 걷어냈다.
// 근거 — 저축 화면에 행이 생긴 736명 중 금액이 남은 사람 8명·최장 연속 3일, 여정 103명. 결과 3,821명·바꿔보기 1,219명이 앞으로 나온다.
// 별칭: 옛 해시(#tools·#city·#plan·#index·#share·#community·#curation·#save·#journey)는 새 화면으로 흡수.
export const SCREEN_ALIASES = {
  curation: 'cities', city: 'cities', advanced: 'menu', tools: 'menu', firePlan: 'result', plan: 'result',
  index: 'ranking', share: 'result', community: 'wall', save: 'result', journey: 'result', today: 'result'
};

export const screens = {
  home:       { hash: '#home',       title: '파이어맵' },
  question:   { hash: '#question',   title: '질문' },
  result:     { hash: '#result',     title: '결과',              tab: 'result' },
  experiment: { hash: '#experiment', title: '바꿔보기',          tab: 'experiment', back: 'result' },
  ranking:    { hash: '#ranking',    title: '랭킹',              tab: 'ranking' },
  menu:       { hash: '#menu',       title: '전체',              tab: 'menu' },
  settings:   { hash: '#settings',   title: '설정',              tab: 'menu', back: 'menu' },
  account:    { hash: '#account',    title: '계정',              tab: 'menu', back: 'settings' },
  cities:     { hash: '#cities',     title: '지역별 파이어',     back: 'menu' },
  firetype:   { hash: '#firetype',   title: '파이어 유형 테스트', back: 'result' },
  dependent:  { hash: '#dependent',  title: '파이어 후 건보료',  back: 'menu' },
  foreignTax: { hash: '#foreignTax', title: '파이어 후 세금',    back: 'menu' },
  dividend:   { hash: '#dividend',   title: '배당으로 파이어',   back: 'menu' },
  pension:    { hash: '#pension',    title: '국민연금 조기수령', back: 'menu' },
  news:       { hash: '#news',       title: '소식',              back: 'result' },
  wall:       { hash: '#wall',       title: '방명록',            back: 'result' }
};

export const TABS = [
  { id: 'result',     label: '결과',     target: 'result' },
  { id: 'experiment', label: '바꿔보기', target: 'experiment' },
  { id: 'ranking',    label: '랭킹',     target: 'ranking' },
  { id: 'menu',       label: '전체',     target: 'menu' }
];

export function resolveScreen(raw) {
  const id = String(raw || '').replace('#', '').split('?')[0];
  const aliased = SCREEN_ALIASES[id] || id;
  return screens[aliased] ? aliased : 'home';
}
