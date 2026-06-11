const DEFAULT_SUPABASE_URL = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const DEFAULT_SUPABASE_KEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || DEFAULT_SUPABASE_URL;
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || DEFAULT_SUPABASE_KEY;
const TABLE = 'firemap_scores';

function headers(extra = {}) {
  return { apikey: SUPABASE_KEY, authorization: `Bearer ${SUPABASE_KEY}`, 'content-type': 'application/json', ...extra };
}

function deviceId() {
  try {
    let id = localStorage.getItem('fm_cid');
    if (!id) {
      id = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
      localStorage.setItem('fm_cid', id);
    }
    return id;
  } catch {
    return null;
  }
}

function countFromRange(res) {
  const cr = res.headers.get('content-range') || '';
  const total = cr.split('/')[1];
  return total && total !== '*' ? Number(total) : 0;
}

export async function submitScore({ fireScore, ageBand, survivalAge, nickname, earliestAge }) {
  const base = {
    fire_score: Math.max(0, Math.min(100, Math.round(fireScore))),
    age_band: ageBand || null,
    survival_age: survivalAge || null,
    client_type: window.innerWidth <= 640 ? 'mobile' : 'desktop'
  };
  const nick = (nickname || '').trim().slice(0, 16);
  const full = {
    ...base,
    nickname: nick || null,
    earliest_age: (earliestAge != null && Number.isFinite(Number(earliestAge))) ? Math.round(Number(earliestAge)) : null
  };
  const cid = deviceId();
  const fullCid = { ...full, client_id: cid };
  const send = (body, merge) => fetch(`${SUPABASE_URL}/rest/v1/${TABLE}${merge ? '?on_conflict=client_id' : ''}`, {
    method: 'POST',
    headers: headers({ prefer: merge ? 'return=minimal,resolution=merge-duplicates' : 'return=minimal' }),
    body: JSON.stringify(body)
  });
  try {
    // 1순위: 기기ID 업서트(같은 기기는 1행 갱신 → 중복 방지)
    let res = cid ? await send(fullCid, true) : { ok: false };
    if (!res.ok) res = await send(full, false);  // 2순위: client_id 정책/유니크 없으면 닉네임+은퇴나이 insert
    if (!res.ok) res = await send(base, false);  // 3순위: 신규 컬럼 자체가 없으면 기본만 insert
    return res.ok;
  } catch {
    return false;
  }
}

// 함께 계산한 사용자 중 내 등수/백분위
export async function fetchUserRank(earliestAge) {
  try {
    const opts = { method: 'GET', headers: headers({ prefer: 'count=exact', range: '0-0' }) };
    const totalRes = await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?select=id`, opts);
    const total = countFromRange(totalRes);
    if (!total) return null;
    const hasAge = earliestAge != null && Number.isFinite(Number(earliestAge));
    // 더 이른 은퇴 가능 나이 = 더 높은 순위. 값 없으면(은퇴 불가) 값 있는 사람 모두가 상위.
    const higherQuery = hasAge
      ? `${SUPABASE_URL}/rest/v1/${TABLE}?select=id&earliest_age=lt.${Math.round(Number(earliestAge))}`
      : `${SUPABASE_URL}/rest/v1/${TABLE}?select=id&earliest_age=not.is.null`;
    const higherRes = await fetch(higherQuery, opts);
    const higher = countFromRange(higherRes);
    const position = higher + 1;
    const percentile = Math.min(99, Math.max(1, Math.round((higher / total) * 100)));
    return { total, position, percentile };
  } catch {
    return null;
  }
}

export async function fetchTopScores(limit = 10) {
  try {
    const url = `${SUPABASE_URL}/rest/v1/${TABLE}?select=nickname,fire_score,age_band,earliest_age&order=earliest_age.asc.nullslast,fire_score.desc&limit=${limit}`;
    const res = await fetch(url, { method: 'GET', headers: headers() });
    if (!res.ok) return [];
    return await res.json();
  } catch {
    return [];
  }
}

export async function fetchAggregates() {
  try {
    const opts = { method: 'GET', headers: headers({ prefer: 'count=exact', range: '0-1999' }) };
    const res = await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?select=earliest_age,age_band,fire_score`, opts);
    if (!res.ok) return null;
    const total = countFromRange(res);
    const rows = await res.json();
    const ea = rows.map((r) => r.earliest_age).filter((v) => v != null && v > 0);
    const sc = rows.map((r) => r.fire_score).filter((v) => v != null);
    const avg = (arr) => (arr.length ? Math.round(arr.reduce((a, b) => a + b, 0) / arr.length) : null);
    const bandCount = {};
    rows.forEach((r) => { if (r.age_band) bandCount[r.age_band] = (bandCount[r.age_band] || 0) + 1; });
    const topBand = Object.entries(bandCount).sort((a, b) => b[1] - a[1])[0];
    return { total, avgEarliest: avg(ea), avgScore: avg(sc), topBand: topBand ? Number(topBand[0]) : null };
  } catch {
    return null;
  }
}
