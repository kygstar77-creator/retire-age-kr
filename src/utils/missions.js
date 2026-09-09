// 단계별 미션 — 임의 XP가 아니라 진짜 재무 마일스톤. 자동 판정(auto) + 수동 체크(manual, localStorage).
// 데이터 위험 없음(별도 키 fm_missions, additive).
const KEY = 'fm_missions';

function readManual() {
  try { return JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch { return {}; }
}
export function setManual(id, val) {
  const m = readManual();
  if (val) m[id] = Date.now(); else delete m[id];
  try { localStorage.setItem(KEY, JSON.stringify(m)); } catch { /* ignore */ }
  return m;
}

// ctx: { calculated, histLen, saveTotal, loggedIn, rateOK, asset, notif }
export const MISSION_POOL = {
  1: [
    { id: 'calc', label: '내 파이어 나이 계산하기', hint: '출발점이에요', auto: (c) => !!c.calculated },
    { id: 'asset1', label: '지금 자산 한 번 기록하기', hint: '추이의 첫 점이에요', auto: (c) => c.histLen >= 1, to: 'home' },
    { id: 'login', label: '로그인해서 기록 지키기', hint: '기기를 바꿔도 이어져요', auto: (c) => !!c.loggedIn, to: 'account' }
  ],
  2: [
    { id: 'save1', label: '오늘 한 걸음 첫 기록', hint: '파이어를 며칠 당겨요', auto: (c) => c.saveTotal > 0, to: 'save' },
    { id: 'asset2', label: '두 번째 달 자산 기록', hint: '추이 선이 그려져요', auto: (c) => c.histLen >= 2, to: 'home' },
    { id: 'emergency', label: '비상금 목표 정하기', hint: '생활비 6개월치예요', manual: true }
  ],
  3: [
    { id: 'rate', label: '목표 저축률 채우기', hint: '지금 속도로 충분한지 봐요', auto: (c) => !!c.rateOK },
    { id: 'alloc', label: '자산 배분 점검하기', hint: '성장·배당·안전 비중이에요', manual: true },
    { id: 'side', label: '부업 1건 만들기', hint: '부족분을 메워요', manual: true }
  ],
  4: [
    { id: 'mil1', label: '순자산 1억 넘기기', hint: '첫 큰 고비예요', auto: (c) => c.asset >= 100000000 },
    { id: 'region', label: '지역별 파이어 비교하기', hint: '사는 곳이 시점을 바꿔요', manual: true, to: 'cities' },
    { id: 'notif', label: '아침 파이어 시계 켜기', hint: '매일 D-day를 받아요', auto: (c) => !!c.notif }
  ],
  5: [
    { id: 'hi', label: '파이어 후 건보료 확인하기', hint: '회사 없이 혼자 내는 보험료예요', manual: true, to: 'dependent' },
    { id: 'withdraw', label: '인출 순서 정하기', hint: '세금 덜 내는 순서예요', manual: true, to: 'foreignTax' },
    { id: 'cashflow', label: '배당으로 월 현금 만들기', hint: '인출 부담이 줄어요', manual: true, to: 'dividend' }
  ],
  6: [
    { id: 'fire', label: '파이어 실행 체크리스트', hint: '인출·건보·세금 마지막 점검이에요', manual: true }
  ]
};

export function missionsFor(stage, ctx) {
  const manual = readManual();
  const pool = MISSION_POOL[Math.max(1, Math.min(6, stage || 1))] || [];
  const items = pool.map((m) => ({
    ...m,
    done: m.auto ? !!m.auto(ctx) : !!manual[m.id],
    kind: m.auto ? 'auto' : 'manual'
  }));
  const doneCount = items.filter((x) => x.done).length;
  return { items, doneCount, total: items.length, allDone: doneCount === items.length && items.length > 0 };
}
