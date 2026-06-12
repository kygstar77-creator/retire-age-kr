// 오늘의 절약 / 챌린지 / 명언 공통 데이터 + 누적 저장 로직
export const CHALLENGES = [
  { t: '오늘 배달·외식 0번 도전', s: 15000 },
  { t: '커피 집에서 내려 마시기', s: 5000 },
  { t: '충동구매 1건 참기', s: 30000 },
  { t: '안 쓰는 구독 서비스 1개 점검', s: 10000 },
  { t: '점심 도시락 싸기', s: 8000 },
  { t: '장보기 목록 정하고 그것만 사기', s: 12000 },
  { t: '택시 대신 대중교통 타기', s: 8000 },
  { t: '편의점 대신 마트 이용', s: 5000 },
  { t: '오늘 하루 무지출 도전', s: 25000 },
  { t: '카페 대신 텀블러 챙기기', s: 5000 },
  { t: '쿠폰·세일 1개 찾아 쓰기', s: 7000 },
  { t: '살 물건 중고로 알아보기', s: 20000 },
  { t: '통신·보험 고정비 1개 점검', s: 10000 },
  { t: '간식 대신 물 마시기', s: 3000 },
  { t: '오늘 지출 가계부에 기록', s: 0 },
  { t: '한 끼는 집밥으로', s: 8000 },
  { t: '가까운 거리 걸어가기', s: 3000 },
  { t: '배달앱 장바구니 비우기', s: 18000 },
  { t: '주말 약속 하나 홈카페로', s: 20000 },
  { t: '안 입는 옷 1벌 중고 판매', s: 10000 },
  { t: '자동결제 목록 한 번 훑기', s: 9000 },
  { t: '오늘 술·담배 0', s: 12000 },
  { t: '대용량으로 단가 낮추기', s: 6000 },
  { t: '외식 대신 밀키트', s: 9000 },
  { t: '하루 예산 정하고 지키기', s: 15000 },
  { t: '냉장고 털어 한 끼 해결', s: 8000 },
  { t: '필요 없는 알림·쇼핑앱 정리', s: 0 },
  { t: '커피값을 저축통장에 이체', s: 5000 },
  { t: '이번 달 가장 큰 지출 점검', s: 0 },
  { t: '내일 점심 미리 준비', s: 8000 }
];

export const QUOTES = [
  '오늘 아낀 만원이 10년 뒤엔 자유의 하루가 된다.',
  '부는 많이 버는 것이 아니라 덜 쓰고 남기는 데서 시작된다.',
  '미래의 나에게 매달 월급을 먼저 보내자.',
  '소비를 줄이면 필요한 노후 자금도 함께 줄어든다.',
  '돈이 나 대신 일하게 만드는 것, 그게 파이어다.',
  '쓰지 않은 돈이 가장 확실한 수익률이다.',
  '자유는 잔고가 아니라 습관에서 나온다.',
  '남의 소비를 따라가면 남의 속도로 늙는다.',
  '복리는 시간을 먹고 자란다. 일찍 시작한 사람이 이긴다.',
  '작은 절약이 모여 퇴사 날짜를 앞당긴다.',
  '필요한 것과 갖고 싶은 것을 구분하는 순간 부자가 된다.',
  '버는 속도보다 모으는 속도가 자유를 결정한다.',
  '오늘의 한 끼 집밥이 내일의 하루치 자유다.',
  '조급해 말되 멈추지도 말자. 방향이 맞으면 도착한다.',
  '가장 비싼 지출은 남에게 보여주려는 지출이다.'
];

export const QUICK = [
  { label: '커피 참기', emoji: '☕', won: 5000 },
  { label: '외식 대신 집밥', emoji: '🍱', won: 20000 },
  { label: '택시 대신 대중교통', emoji: '🚌', won: 12000 },
  { label: '충동구매 멈춤', emoji: '🛑', won: 30000 }
];

export const dayIdx = () => Math.floor(Date.now() / 86400000);
export const todayStr = () => new Date().toISOString().slice(0, 10);
export const yesterdayStr = () => new Date(Date.now() - 86400000).toISOString().slice(0, 10);
export const wonStr = (n) => `${Math.round(n).toLocaleString('ko-KR')}원`;
export const readJSON = (k) => { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch { return null; } };

export function fmtAdvance(sec) {
  let x = Math.floor(sec);
  if (x < 1) return null;
  const d = Math.floor(x / 86400); x -= d * 86400;
  const h = Math.floor(x / 3600); x -= h * 3600;
  const m = Math.floor(x / 60); const s = x - m * 60;
  if (d > 0) return `${d}일 ${h}시간`;
  if (h > 0) return `${h}시간 ${m}분`;
  if (m > 0) return `${m}분 ${s}초`;
  return `${s}초`;
}

// 파이어까지 하루 평균 모아야 하는 돈(원/일). 이미 목표 달성이면 null.
export function dailyNeedOf(simulation) {
  if (!simulation || !simulation.inputs) return null;
  const inp = simulation.inputs;
  const fireAge = simulation.earliestRetirementAge || inp.targetRetirementAge;
  const target = simulation.requiredFireAssetByFourPercent || 0;
  const daysRemaining = Math.max(30, (fireAge - inp.currentAge) * 365.25);
  const gap = target - inp.financialAsset;
  return gap > 0 ? Math.max(1000, Math.round(gap / daysRemaining)) : null;
}

// 누적 저장 — 'today'만 매일 리셋, total/days는 영구 누적
export function addSave(amount) {
  if (!amount || amount <= 0) return readJSON('fm_save');
  const t = todayStr();
  const prev = readJSON('fm_save');
  const newDay = !prev || prev.lastDate !== t;
  const next = {
    today: (newDay ? 0 : (prev.today || 0)) + amount,
    total: (prev ? prev.total || 0 : 0) + amount,
    days: (prev ? prev.days || 0 : 0) + (newDay ? 1 : 0),
    lastDate: t
  };
  try { localStorage.setItem('fm_save', JSON.stringify(next)); } catch { /* ignore */ }
  return next;
}
