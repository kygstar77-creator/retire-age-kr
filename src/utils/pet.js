// 펫(알뜰한 너구리) — 누적 저축·절약액으로 진화하는 리워드
// 데이터: 절약 누적(fm_save.total) + 적립 누적(fm_daily.days 합) — 서버 추가 없이 기존 기록 재사용
const readJSON = (k) => { try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch { return null; } };

export const PET_STAGES = [
  { idx: 0, name: '너구리 알', min: 0 },
  { idx: 1, name: '아기 너구리', min: 10000 },
  { idx: 2, name: '꼬마 너구리', min: 100000 },
  { idx: 3, name: '너구리', min: 500000 },
  { idx: 4, name: '알뜰 너구리', min: 2000000 },
  { idx: 5, name: '황금 너구리', min: 10000000 }
];

// 펫 성장치 = 절약 누적 + 적립 누적(원)
export function petTotal() {
  const sv = readJSON('fm_save');
  const save = sv ? Math.max(0, Number(sv.total) || 0) : 0;
  const fd = readJSON('fm_daily');
  const days = (fd && fd.days) || {};
  const dep = Object.values(days).reduce((a, b) => a + (Number(b) || 0), 0);
  return save + Math.max(0, dep);
}

export function computePet(total) {
  const t = total != null ? total : petTotal();
  let idx = 0;
  for (let i = 0; i < PET_STAGES.length; i++) { if (t >= PET_STAGES[i].min) idx = i; }
  const stage = PET_STAGES[idx];
  const next = PET_STAGES[idx + 1] || null;
  const span = next ? (next.min - stage.min) : 1;
  const pct = next ? Math.max(0, Math.min(100, Math.round(((t - stage.min) / span) * 100))) : 100;
  const toNext = next ? Math.max(0, next.min - t) : 0;
  return { idx, stage, next, pct, toNext, total: t };
}
