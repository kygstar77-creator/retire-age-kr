// 파이어 여정 플레이북 — [단계 1~6] × [주기 일/주/월/년] 격자.
// 각 칸: 다음 행동(action)·추천 콘텐츠(reads, 실제 /guide 페이지)·점검 항목.
// 순수 함수·결정적 선택(날짜 기반). 데이터 수집 없음. 기존 todayAction/todayTip의 단계 인지 버전을 제공.
import { dayIdx } from './dailyData.js';

const g = (slug, title) => ({ title, href: `/guide/${slug}.html` });
const hub = (path, title) => ({ title, href: path });

// 단계별 격자. action = {ico,label,to(내부화면)} | {ico,label,href(가이드)} 둘 다 지원.
export const PLAYBOOK = {
  1: { // 각성 — 내 파이어 나이 알기
    daily: [
      { ico: '📊', label: '내 결과·또래 등수 자세히 보기', to: 'result' },
      { ico: '🔥', label: '파이어 종류(린·팻·코스트·바리스타) 읽기', href: '/guide/fire-types.html' },
      { ico: '🏆', label: '또래 중 내 파이어 등수 확인하기', to: 'ranking' },
      { ico: '🔒', label: '내 프로필 만들어 기록 지키기', to: 'account' }
    ],
    weekly: { mission: { ico: '🧭', label: '내 파이어 유형 정하고 결과 저장하기', to: 'result' },
      reads: [g('fire-types', '파이어 종류 — 린·팻·코스트·바리스타'), g('fire-by-age', '나이별 파이어 전략'), g('four-percent-rule', '4% 룰이란?'), g('inflation-retirement', '물가와 은퇴 자금')] },
    monthly: { title: '이번 달 점검 · 각성', to: 'result',
      items: ['내 파이어 나이를 다시 확인했나요?', '결과를 프로필에 저장했나요?', '파이어 유형(린/팻/코스트)을 정했나요?'] },
    yearly: { title: '올해 회고 · 각성', to: 'result',
      items: ['올해 파이어 목표를 글로 적어봤나요?', '내 파이어 유형이 바뀌었나요?'] },
    tips: [
      '4% 룰은 미국 가정 — 한국은 물가·세금·건보까지 따로 봐야 현실적이에요.',
      '파이어는 숫자가 아니라 선택지예요. 일을 안 해도 되는 자유가 목적.',
      '얼마 모았나보다 몇 년치 생활비를 모았나로 보면 진도가 또렷해요.'
    ] },
  2: { // 설계 — 목표까지의 길
    daily: [
      { ico: '🎛️', label: '바꿔보기로 조건 하나 바꿔 실험하기', to: 'experiment' },
      { ico: '🎯', label: '목표 자산·목표 나이 정해보기', to: 'result' },
      { ico: '🧾', label: 'ISA·연금계좌 절세법 읽기', href: '/guide/isa-pension-accounts.html' },
      { ico: '📚', label: '플랜 시나리오 모음 둘러보기', href: '/guide/plan/' }
    ],
    weekly: { mission: { ico: '🗺️', label: '바꿔보기로 목표 달성 경로 1개 찾기', to: 'experiment' },
      reads: [g('asset-target-scenarios', '목표 자산 시나리오'), g('coast-fire-calculation', '코스트파이어 계산'), g('isa-pension-accounts', 'ISA·연금계좌 절세'), hub('/guide/plan/', '내 조건별 플랜 계산 모음')] },
    monthly: { title: '이번 달 점검 · 설계', to: 'experiment',
      items: ['월 저축 계획을 세웠나요?', '목표 자산 대비 지금 몇 %인가요?', 'ISA·연금저축 한도를 챙기고 있나요?'] },
    yearly: { title: '올해 회고 · 설계', to: 'experiment',
      items: ['올해 목표 저축액을 채웠나요?', '내년 목표 나이·금액을 다시 잡아볼까요?'] },
    tips: [
      'ISA·연금저축·IRP는 세금을 미루거나 줄여줘요. 파이어 종잣돈의 가속 페달.',
      '목표 자산 = 연 생활비 ÷ 인출률. 생활비를 줄이면 목표 자체가 내려가요.',
      '코스트파이어 — 더 안 모아도 굴리기만 하면 목표에 닿는 시점. 생각보다 빨리 와요.'
    ] },
  3: { // 실행 — 추적 시작
    daily: [
      { ico: '💰', label: '오늘 저축 기록하기', to: 'save' },
      { ico: '📈', label: '이번 달 자산 한 번 업데이트하기', to: 'home' },
      { ico: '✂️', label: '생활비 구조적으로 줄이는 법 읽기', href: '/guide/cut-living-cost.html' },
      { ico: '🍚', label: '알뜰한 식비 절약법 읽기', href: '/guide/frugal-food-tips.html' }
    ],
    weekly: { mission: { ico: '🌱', label: '이번 주 저축 4일 이상 기록하기', to: 'save' },
      reads: [g('cut-living-cost', '생활비 구조적으로 줄이기'), g('frugal-food-tips', '알뜰한 식비 절약법'), g('monthly-saving-fire-timeline', '월 저축이 파이어를 당기는 타임라인'), g('dividend-monthly-income', '배당으로 월 현금흐름')] },
    monthly: { title: '이번 달 점검 · 실행', to: 'save',
      items: ['이번 달 자산을 기록했나요?', '계획만큼 저축했나요?', '고정비(통신·구독·보험)를 다시 봤나요?'] },
    yearly: { title: '올해 회고 · 실행', to: 'save',
      items: ['올해 저축률은 몇 %였나요?', '작년보다 자산이 얼마나 늘었나요?', '내년 저축률 목표를 올려볼까요?'] },
    tips: [
      '저축률이 50%면 약 17년, 25%면 약 32년 만에 파이어 — 수익률보다 저축률이 먼저예요.',
      '고정비(통신·구독·보험)부터 줄이세요 — 한 번 줄이면 매달 평생 절약돼요.',
      '작은 자동이체가 의지보다 강해요. 월급날 저축부터 자동으로 빼두세요.'
    ] },
  4: { // 가속 — 진짜 전진
    daily: [
      { ico: '📍', label: '지방 살면 몇 년 빨라지나 보기', to: 'cities' },
      { ico: '💵', label: '배당으로 월 현금흐름 만들어보기', to: 'dividend' },
      { ico: '📊', label: '또래 추월했는지 파이어 지수에서 확인', to: 'index' },
      { ico: '🏠', label: '지방·주택 다운사이징 읽기', href: '/guide/real-estate-downsizing.html' }
    ],
    weekly: { mission: { ico: '📈', label: '지역·부업·세금 레버 1개 적용해보기', to: 'tools' },
      reads: [g('real-estate-downsizing', '지방·주택 다운사이징'), g('southeast-asia-retirement', '동남아 은퇴'), g('post-retirement-side-jobs', '파이어 후 부업'), hub('/guide/region-plan/', '지역×가구별 파이어 플랜'), hub('/guide/regions/', '지역별 생활비·필요자산')] },
    monthly: { title: '이번 달 점검 · 가속', to: 'tools',
      items: ['이번 달 순자산이 늘었나요?', '생활비를 더 낮출 지역을 살펴봤나요?', '부업·배당 현금흐름을 점검했나요?'] },
    yearly: { title: '올해 회고 · 가속', to: 'tools',
      items: ['올해 파이어 나이를 몇 년 당겼나요?', '거주지·부업 전략을 바꿔볼까요?'] },
    tips: [
      '지방으로 옮겨 생활비를 월 50만 줄이면 필요 자산이 수억 줄기도 해요.',
      '살고 있는 집은 생활비를 못 만들어요. 임대수익이 있어야 파이어 나이가 당겨져요.',
      '연봉이 올라도 생활비를 그대로 두면 파이어가 확 빨라져요(라이프스타일 동결).'
    ] },
  5: { // 임박 — 코스트파이어·검증
    daily: [
      { ico: '🩺', label: '파이어 후 건보료 점검하기', to: 'dependent' },
      { ico: '🧾', label: '양도·배당세 점검하기', to: 'foreignTax' },
      { ico: '🕳️', label: '소득 크레바스(연금 공백) 읽기', href: '/guide/income-crevasse.html' },
      { ico: '🪜', label: '인출 순서 전략 읽기', href: '/guide/withdrawal-order-strategy.html' }
    ],
    weekly: { mission: { ico: '🎯', label: '파이어 리얼리티 체크 1개 끝내기(건보/세금/연금)', to: 'dependent' },
      reads: [g('health-insurance-dependent', '파이어 후 건보료·피부양자'), g('income-crevasse', '소득 크레바스(연금 공백)'), g('national-pension-early', '국민연금 조기수령'), g('withdrawal-order-strategy', '인출 순서 전략'), g('foreign-stock-tax', '해외주식 양도세')] },
    monthly: { title: '이번 달 점검 · 임박', to: 'dependent',
      items: ['퇴사 후 건보료(지역가입자)를 추정해봤나요?', '연금 받기 전 소득 공백 대비가 됐나요?', '인출 순서(계좌별)를 정했나요?'] },
    yearly: { title: '올해 회고 · 임박', to: 'dividend',
      items: ['올해 코스트파이어 시점에 닿았나요?', '세금·건보 최적화를 점검했나요?'] },
    tips: [
      '국민연금 받기 전 ‘소득 공백기(크레바스)’를 어떻게 버틸지가 조기 파이어의 핵심.',
      '퇴사하면 건강보험이 지역가입자로 — 소득·재산 기준이라 부담이 커질 수 있어요.',
      '자산보다 인출 순서가 세금을 좌우해요. 어떤 계좌부터 빼느냐가 중요.'
    ] },
  6: { // 파이어 — 도달 & 이후
    daily: [
      { ico: '🪜', label: '인출 전략 점검하기', to: 'dividend' },
      { ico: '💬', label: '파이어족 커뮤니티 둘러보기', to: 'community' },
      { ico: '🧾', label: '배당과 건강보험료 관계 읽기', href: '/guide/dividend-health-insurance.html' }
    ],
    weekly: { mission: { ico: '🏝️', label: '인출 전략 점검 + 커뮤니티에 한 줄 남기기', to: 'community' },
      reads: [g('withdrawal-order-strategy', '인출 순서 전략'), g('dividend-health-insurance', '배당과 건강보험료'), g('dividend-tax-thresholds', '배당 소득세 기준')] },
    monthly: { title: '이번 달 점검 · 파이어', to: 'dividend',
      items: ['이번 달 현금흐름이 생활비를 덮었나요?', '인출이 계획 범위 안이었나요?', '건보료·세금 변동을 확인했나요?'] },
    yearly: { title: '올해 회고 · 파이어', to: 'dividend',
      items: ['올해 자산이 인플레이션을 이겼나요?', '인출률(4%)을 지켰나요?', '내년 현금흐름 계획을 세웠나요?'] },
    tips: [
      '비상금 6개월치를 먼저 — 파이어 후 시장 급락기에 자산을 안 팔아도 되게.',
      '배당이 연 2,000만원을 넘으면 금융소득종합과세 대상 — 건보료도 함께 올라요.',
      '환율도 변수예요. 해외 체류·해외주식이 많다면 환헤지·분산을 생각해요.'
    ] }
};

// 결정적 주기 인덱스
export const weekIdx = () => Math.floor(dayIdx() / 7);
export const monthKey = (d = new Date()) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
export const yearOf = (d = new Date()) => d.getFullYear();

const arr = (stage, key) => { const s = PLAYBOOK[stage]; return s && Array.isArray(s[key]) ? s[key] : null; };

// 단계 인지 선택자 — 단계 없거나 격자에 없으면 null(호출부에서 전역 폴백)
export function pickDaily(stage) { const a = arr(stage, 'daily'); return a && a.length ? a[dayIdx() % a.length] : null; }
export function pickTip(stage) { const s = PLAYBOOK[stage]; const a = s && Array.isArray(s.tips) ? s.tips : null; return a && a.length ? a[dayIdx() % a.length] : null; }
export function pickWeekly(stage) {
  const s = PLAYBOOK[stage]; if (!s || !s.weekly) return null;
  const reads = s.weekly.reads || [];
  // 추천글은 주차별로 2개씩 회전 노출
  const i = (weekIdx() * 2) % Math.max(1, reads.length);
  const picks = reads.length <= 2 ? reads : [reads[i % reads.length], reads[(i + 1) % reads.length]];
  return { mission: s.weekly.mission, reads: picks, allReads: reads };
}
export function pickMonthly(stage) { const s = PLAYBOOK[stage]; return s && s.monthly ? s.monthly : null; }
export function pickYearly(stage) { const s = PLAYBOOK[stage]; return s && s.yearly ? s.yearly : null; }

// 오늘의 한 걸음(단계 반영) — 호출부 폴백을 위해 null 가능
export function pickForToday(stage) {
  return { action: pickDaily(stage), tip: pickTip(stage), weekly: pickWeekly(stage), monthly: pickMonthly(stage), yearly: pickYearly(stage) };
}
