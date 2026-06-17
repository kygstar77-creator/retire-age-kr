export const SCREEN_ALIASES = { curation: 'city', advanced: 'tools' };

export const screens = {
  home:       { hash: '#home',       title: '홈',     type: 'home',     tab: 'home' },
  firePlan:   { hash: '#plan',       title: '내 파이어 플랜', type: 'tool', back: 'result', tab: 'home' },
  account:    { hash: '#account',    title: '내 계정', type: 'tool', back: 'home', tab: 'home' },
  question:   { hash: '#question',   title: '질문',   type: 'question' },
  result:     { hash: '#result',     title: '결과',   type: 'result',   tab: 'home', next: ['ranking', 'save', 'experiment', 'tools'] },
  save:       { hash: '#save',       title: '저축',   type: 'save',     tab: 'save' },
  tools:      { hash: '#tools',      title: '도구',   type: 'tools',    tab: 'tools' },
  journey:    { hash: '#journey',    title: '내 파이어 여정', type: 'tool', back: 'home', tab: 'home' },
  index:      { hash: '#index',      title: '대한민국 파이어 지수', type: 'tool', back: 'home' },
  experiment: { hash: '#experiment', title: '바꿔보기',          type: 'tool', back: 'result', tab: 'home' },
  share:      { hash: '#share',      title: '공유',               type: 'tool', back: 'result' },
  dependent:  { hash: '#dependent',  title: '파이어 후 건보료', type: 'tool', back: 'tools' },
  foreignTax: { hash: '#foreignTax', title: '파이어 후 세금(양도·배당)', type: 'tool', back: 'tools' },
  dividend:   { hash: '#dividend',   title: '파이어 후 현금흐름',     type: 'tool', back: 'tools' },
  pension:    { hash: '#pension',    title: '국민연금 조기수령',   type: 'tool', back: 'tools' },
  city:       { hash: '#city',       title: '도시 비교 · 해외 체류', type: 'tool', back: 'cities' },
  community:  { hash: '#community',  title: '커뮤니티',           type: 'tool', back: 'tools', tab: 'community' },
  ranking:    { hash: '#ranking',    title: 'FIRE 랭킹',          type: 'tool', back: 'result', tab: 'ranking' },
  cities:     { hash: '#cities',     title: '지역별 파이어 (국내·해외)',      type: 'tool', back: 'tools' }
};

export const NEXT_ACTION_META = {
  ranking:    { tag: '랭킹', title: '전체 랭킹 보기',     desc: '1등까지 몇 명? 내 순위', primary: true },
  save:       { tag: '저축', title: '오늘부터 저축 기록',   desc: '적립·절약이 파이어를 며칠 당기는지' },
  experiment: { tag: '비교', title: '조건 바꿔 비교하기', desc: '증권앱 차트로 What-If' },
  share:      { tag: '공유', title: '내 결과 공유',       desc: '파이어 나이·또래 비교 카드' },
  tools:      { tag: '도구', title: '정밀 도구 더보기',   desc: '건보료·세금·도시·커뮤니티' }
};

export const TOOLS = [
  { id: 'index',      tag: '데이터', title: '대한민국 파이어 지수', desc: '7천여 명 집계로 보는 또래 중 내 위치' },
  { id: 'experiment', tag: '비교',   title: '조건 바꿔 비교',     desc: '증권앱 차트로 What-If 비교' },
  { id: 'dependent',  tag: '건보료', title: '파이어 후 건보료', desc: '피부양자 박탈 여부 + 지역가입 월 건보료 추정' },
  { id: 'foreignTax', tag: '세금',   title: '양도·배당세',    desc: '해외주식 양도세 + 배당 소득세·건보료 경고' },
  { id: 'dividend',   tag: '현금흐름', title: '파이어 후 현금흐름',   desc: '배당·인출·세금·건보료까지' },
  { id: 'pension',    tag: '연금',   title: '국민연금 조기수령',  desc: '당겨 받기 득실' },
  { id: 'cities',     tag: '지역',   title: '지역별 파이어',   desc: '국내·해외 지역 생활비로 파이어 시점 비교' },
  { id: 'community',  tag: '커뮤니티', title: '다른 사람들',       desc: '익명 한마디·후기' }
];

export const TABS = [
  { id: 'home',  label: '홈',   target: 'home' },
  { id: 'save',  label: '저축', target: 'save' },
  { id: 'ranking', label: '랭킹', target: 'ranking' },
  { id: 'community', label: '커뮤니티', target: 'community' },
  { id: 'tools', label: '도구', target: 'tools' }
];

export function resolveScreen(raw) {
  const id = String(raw || '').replace('#', '');
  const aliased = SCREEN_ALIASES[id] || id;
  return screens[aliased] ? aliased : 'home';
}
