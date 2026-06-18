// 파이어 여정 데일리 엔진 — 매일 바뀌는 한 걸음/지식 + 연속 출석.
import { dayIdx, todayStr } from './dailyData.js';
import { pickDaily, pickTip } from './journeyPlaybook.js';

export const TIPS = [
  '저축률이 50%면 약 17년, 25%면 약 32년 만에 파이어 — 수익률보다 저축률이 먼저예요.',
  '생활비를 한 번 줄이면 효과가 두 배: 필요 자산도 줄고, 모으는 속도도 빨라져요.',
  '코스트파이어 — 더 안 모아도 굴리기만 하면 목표에 닿는 시점. 생각보다 빨리 와요.',
  '국민연금 받기 전 ‘소득 공백기(크레바스)’를 어떻게 버틸지가 조기 파이어의 핵심.',
  '퇴사하면 건강보험이 지역가입자로 — 소득·재산 기준이라 부담이 커질 수 있어요.',
  '해외주식 양도세는 250만원 공제 후 22%. 매년 나눠서 팔면 세금이 줄어요.',
  '배당이 연 2,000만원을 넘으면 금융소득종합과세 대상 — 건보료도 함께 올라요.',
  'ISA·연금저축·IRP는 세금을 미루거나 줄여줘요. 파이어 종잣돈의 가속 페달.',
  '4% 룰은 미국 가정 — 한국은 물가·세금·건보까지 따로 봐야 현실적이에요.',
  '물가 3%면 30년 뒤 생활비는 약 2.4배. 인플레이션은 조용한 도둑이에요.',
  '지방으로 옮겨 생활비를 월 50만 줄이면 필요 자산이 수억 줄기도 해요.',
  '동남아 한 달살이로 겨울 난방·생활비를 아끼는 반해외 파이어도 방법.',
  '커피 한 잔(5천원)을 매일 아끼면 1년 180만원 — 투자하면 더 커져요.',
  '자산보다 인출 순서가 세금을 좌우해요. 어떤 계좌부터 빼느냐가 중요.',
  '바리스타 파이어 — 일을 완전히 놓지 않고 좋아하는 일로 일부 버는 방식.',
  '살고 있는 집은 생활비를 못 만들어요. 임대수익이 있어야 파이어 나이가 당겨져요.',
  '시장이 1주에 1% 움직이면, 자산이 클수록 파이어 날짜도 며칠씩 움직여요.',
  '연봉이 올라도 생활비를 그대로 두면 파이어가 확 빨라져요(라이프스타일 동결).',
  '고정비(통신·구독·보험)부터 줄이세요 — 한 번 줄이면 매달 평생 저축이 늘어요.',
  '목표 자산 = 연 생활비 ÷ 인출률. 생활비를 줄이면 목표 자체가 내려가요.',
  '퇴직금은 IRP로 받으면 퇴직소득세를 미루고 운용수익까지 노릴 수 있어요.',
  '비상금 6개월치를 먼저 — 파이어 후 시장 급락기에 자산을 안 팔아도 되게.',
  '환율도 변수예요. 해외 체류·해외주식이 많다면 환헤지·분산을 생각해요.',
  '얼마 모았나보다 몇 년치 생활비를 모았나로 보면 진도가 또렷해요.',
  '세액공제(연금저축+IRP 연 900만 한도)는 사실상 확정 수익 — 안 쓰면 손해.',
  '파이어는 숫자가 아니라 선택지예요. 일을 안 해도 되는 자유가 목적.',
  '작은 자동이체가 의지보다 강해요. 월급날 저축부터 자동으로 빼두세요.',
  '또래보다 빠른지 느린지는 동기부여일 뿐 — 내 속도로 꾸준한 게 이겨요.'
];

export const DAILY_ACTIONS = [
  { ico: '⏱️', label: '오늘 저축 한 번 기록하기', to: 'save' },
  { ico: '📈', label: '이번 달 자산 한 번 업데이트하기', to: 'home' },
  { ico: '🎛️', label: '바꿔보기로 조건 하나 바꿔 실험하기', to: 'experiment' },
  { ico: '🏆', label: '또래 중 내 파이어 등수 확인하기', to: 'ranking' },
  { ico: '📍', label: '지방 살면 몇 년 빨라지나 보기', to: 'cities' },
  { ico: '📊', label: '대한민국 파이어 지수에서 내 위치 보기', to: 'index' },
  { ico: '🩺', label: '파이어 후 건보료 점검하기', to: 'dependent' },
  { ico: '💬', label: '파이어족 커뮤니티 둘러보기', to: 'community' }
];

// 단계(stage)를 주면 해당 단계 맞춤, 없거나 격자에 없으면 전역 폴백.
export function todayTip(stage) { return (stage != null && pickTip(stage)) || TIPS[dayIdx() % TIPS.length]; }
export function todayAction(stage) { return (stage != null && pickDaily(stage)) || DAILY_ACTIONS[dayIdx() % DAILY_ACTIONS.length]; }

const KEY = 'fm_jcheckin';
export function getCheckin() {
  try { return JSON.parse(localStorage.getItem(KEY) || 'null') || { count: 0, last: null }; }
  catch { return { count: 0, last: null }; }
}
export function isCheckedToday() { return getCheckin().last === todayStr(); }
export function checkInToday() {
  const c = getCheckin();
  const t = todayStr();
  if (c.last === t) return c;
  const y = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
  const count = (c.last === y) ? (Number(c.count) || 0) + 1 : 1;
  const nc = { count, last: t };
  try { localStorage.setItem(KEY, JSON.stringify(nc)); } catch { /* ignore */ }
  return nc;
}
