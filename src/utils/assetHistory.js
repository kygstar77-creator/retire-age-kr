// 월별 금융자산 스냅샷 (파이어 플랜 추이용). 로컬 저장.
const KEY = 'fm_asset_history';
const ym = (d = new Date()) => d.toISOString().slice(0, 7);

export function getAssetHistory() {
  try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch { return []; }
}

export function logAsset(amount) {
  const v = Math.max(0, Math.round(Number(amount) || 0));
  if (!v) return getAssetHistory();
  const m = ym();
  let h = getAssetHistory().filter((x) => x.ym !== m);
  h.push({ ym: m, v });
  h.sort((a, b) => (a.ym < b.ym ? -1 : 1));
  h = h.slice(-24);
  try { localStorage.setItem(KEY, JSON.stringify(h)); } catch { /* ignore */ }
  return h;
}
