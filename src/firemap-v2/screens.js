// 화면 테이블 — 개편 최종본 §2. 탭 4(오늘·저축·랭킹·전체), 화면 17. 라우터는 이 표만 읽는다.
// 별칭: 옛 해시(#tools·#city·#plan·#index·#share·#community·#curation)는 새 화면으로 흡수.
export const SCREEN_ALIASES = {
  curation: 'cities', city: 'cities', advanced: 'menu', tools: 'menu', firePlan: 'home', plan: 'home',
  index: 'ranking', share: 'result', community: 'wall'
};

export const screens = {
  home:       { hash: '#home',       title: '오늘',              tab: 'home' },
  question:   { hash: '#question',   title: '질문' },
  result:     { hash: '#result',     title: '결과',              tab: 'home' },
  experiment: { hash: '#experiment', title: '바꿔보기',          tab: 'home', back: 'result' },
  save:       { hash: '#save',       title: '저축',              tab: 'save' },
  ranking:    { hash: '#ranking',    title: '랭킹',              tab: 'ranking' },
  menu:       { hash: '#menu',       title: '전체',              tab: 'menu' },
  settings:   { hash: '#settings',   title: '설정',              tab: 'menu', back: 'menu' },
  journey:    { hash: '#journey',    title: '내 파이어 여정',    tab: 'home', back: 'home' },
  account:    { hash: '#account',    title: '계정',              tab: 'menu', back: 'settings' },
  cities:     { hash: '#cities',     title: '지역별 파이어',     back: 'menu' },
  firetype:   { hash: '#firetype',   title: '파이어 유형 테스트', back: 'result' },
  dependent:  { hash: '#dependent',  title: '파이어 후 건보료',  back: 'menu' },
  foreignTax: { hash: '#foreignTax', title: '파이어 후 세금',    back: 'menu' },
  dividend:   { hash: '#dividend',   title: '배당으로 파이어',   back: 'menu' },
  pension:    { hash: '#pension',    title: '국민연금 조기수령', back: 'menu' },
  news:       { hash: '#news',       title: '소식',              back: 'home' },
  wall:       { hash: '#wall',       title: '방명록',            back: 'home' }
};

export const TABS = [
  { id: 'home',    label: '오늘', target: 'home' },
  { id: 'save',    label: '저축', target: 'save' },
  { id: 'ranking', label: '랭킹', target: 'ranking' },
  { id: 'menu',    label: '전체', target: 'menu' }
];

export function resolveScreen(raw) {
  const id = String(raw || '').replace('#', '').split('?')[0];
  const aliased = SCREEN_ALIASES[id] || id;
  return screens[aliased] ? aliased : 'home';
}
