export const SCREEN_ALIASES = { curation: 'city' };

export const screens = {
  home:       { hash: '#home',       title: '홈',     type: 'home' },
  question:   { hash: '#question',   title: '질문',   type: 'question' },
  result:     { hash: '#result',     title: '결과',   type: 'result', next: ['experiment', 'city', 'share', 'community'] },
  experiment: { hash: '#experiment', title: '비교',   type: 'module', back: 'result' },
  advanced:   { hash: '#advanced',   title: '고급',   type: 'module', back: 'result' },
  city:       { hash: '#city',       title: '도시',   type: 'module', back: 'result' },
  share:      { hash: '#share',      title: '공유',   type: 'module', back: 'result' },
  community:  { hash: '#community',  title: '커뮤니티', type: 'community', back: 'result' }
};

export const NEXT_ACTION_META = {
  experiment: { tag: '비교', title: '조건 바꿔 비교하기', desc: '현재 계획과 What-If를 한 그래프에서', primary: true },
  city:       { tag: '도시', title: '사는 곳 바꿔보기',   desc: '국내·해외 생활비로 자산 수명 비교' },
  share:      { tag: '공유', title: '결과 공유하기',       desc: '이미지·요약·조건 링크' },
  community:  { tag: '커뮤니티', title: '다른 사람 결과 보기', desc: '익명 한마디·스토리' }
};

export function resolveScreen(raw) {
  const id = String(raw || '').replace('#', '');
  const aliased = SCREEN_ALIASES[id] || id;
  return screens[aliased] ? aliased : 'home';
}
