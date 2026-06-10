// 등수 이력(로컬, 비식별) — 재방문 시 "지난번 대비" 변화를 보여주기 위함.
const KEY = 'fm_rank_history_v1';

export function getHistory() {
  try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch { return []; }
}

export function saveRankSnapshot(snap) {
  try {
    const list = getHistory();
    const date = new Date().toISOString().slice(0, 10);
    const entry = { percentile: snap.percentile, grade: snap.grade, score: snap.score, date };
    if (list.length && list[list.length - 1].date === date) list[list.length - 1] = entry;
    else list.push(entry);
    localStorage.setItem(KEY, JSON.stringify(list.slice(-12)));
  } catch { /* ignore */ }
}

export function getLatestRank() {
  const h = getHistory();
  return h.length ? h[h.length - 1] : null;
}

// 직전 스냅샷 대비 백분위 변화 (양수 = 상위 %가 줄어 더 좋아짐)
export function getRankChange() {
  const h = getHistory();
  if (h.length < 2) return null;
  return { deltaPercentile: h[h.length - 2].percentile - h[h.length - 1].percentile, prevDate: h[h.length - 2].date };
}
