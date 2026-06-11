export const SCREEN_ALIASES = { curation: 'city', advanced: 'tools' };

export const screens = {
  home:       { hash: '#home',       title: '홈',     type: 'home',     tab: 'home' },
  question:   { hash: '#question',   title: '질문',   type: 'question' },
  result:     { hash: '#result',     title: '결과',   type: 'result',   tab: 'home', next: ['ranking', 'experiment', 'share', 'tools'] },
  tools:      { hash: '#tools',      title: '도구',   type: 'tools',    tab: 'tools' },
  experiment: { hash: '#experiment', title: '조건 비교',          type: 'tool', back: 'result' },
  share:      { hash: '#share',      title: '공유',               type: 'tool', back: 'result' },
  dependent:  { hash: '#dependent',  title: '건보료 피부양자 판정', type: 'tool', back: 'tools' },
  foreignTax: { hash: '#foreignTax', title: '해외주식 양도세',     type: 'tool', back: 'tools' },
  dividend:   { hash: '#dividend',   title: '배당 건보료·종합과세', type: 'tool', back: 'tools' },
  pension:    { hash: '#pension',    title: '국민연금 조기수령',   type: 'tool', back: 'tools' },
  city:       { hash: '#city',       title: '도시·해외체류',       type: 'tool', back: 'tools' },
  community:  { hash: '#community',  title: '커뮤니티',           type: 'tool', back: 'tools' },
  ranking:    { hash: '#ranking',    title: 'FIRE 랭킹',          type: 'tool', back: 'result' },
  cities:     { hash: '#cities',     title: '해외 도시 탐색',      type: 'tool', back: 'tools' }
};

// 결과 화면 다음 행동 (MVP 메인)
export const NEXT_ACTION_META = {
  ranking:    { tag: '랭킹', title: '전체 랭킹 보기',     desc: '1등까지 몇 명? 내 순위', primary: true },
  experiment: { tag: '비교', title: '조건 바꿔 비교하기', desc: '증권앱 차트로 What-If' },
  share:      { tag: '공유', title: '등급 카드 공유',     desc: '또래 상위 %·등급 자랑' },
  tools:      { tag: '도구', title: '정밀 도구 더보기',   desc: '건보료·세금·도시·커뮤니티' }
};

// 도구 허브 목록 (메인에서 분리된 기능들)
export const TOOLS = [
  { id: 'ranking',    tag: '랭킹',   title: '전체 FIRE 랭킹',     desc: '또래 중 내 순위·상위권' },
  { id: 'experiment', tag: '비교',   title: '조건 바꿔 비교',     desc: '증권앱 차트로 What-If 비교' },
  { id: 'dependent',  tag: '건보료', title: '피부양자 자격 판정', desc: '퇴사 후 건보료 박탈 여부' },
  { id: 'foreignTax', tag: '세금',   title: '해외주식 양도세',    desc: '분할 매도 절세 계산' },
  { id: 'dividend',   tag: '배당',   title: '배당 건보료·종합과세', desc: '1,000·2,000만원 경계선' },
  { id: 'pension',    tag: '연금',   title: '국민연금 조기수령',  desc: '당겨 받기 득실' },
  { id: 'cities',     tag: '해외',   title: '해외 도시 탐색',     desc: '파이어하면 어디서 살까 · 도시별 자산수명' },
  { id: 'city',       tag: '도시',   title: '도시·해외체류',      desc: '생활비로 자산수명 비교' },
  { id: 'community',  tag: '커뮤니티', title: '다른 사람들',       desc: '익명 한마디·후기' }
];

// 하단 탭
export const TABS = [
  { id: 'home',  label: '홈',   target: 'home' },
  { id: 'tools', label: '도구', target: 'tools' },
  { id: 'guide', label: '백과', href: '/guide/' }
];

export function resolveScreen(raw) {
  const id = String(raw || '').replace('#', '');
  const aliased = SCREEN_ALIASES[id] || id;
  return screens[aliased] ? aliased : 'home';
}
