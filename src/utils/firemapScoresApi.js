const DEFAULT_SUPABASE_URL = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const DEFAULT_SUPABASE_KEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || DEFAULT_SUPABASE_URL;
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || DEFAULT_SUPABASE_KEY;
const TABLE = 'firemap_scores';

function headers(extra = {}) {
  return { apikey: SUPABASE_KEY, authorization: `Bearer ${SUPABASE_KEY}`, 'content-type': 'application/json', ...extra };
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
  const post = (body) => fetch(`${SUPABASE_URL}/rest/v1/${TABLE}`, {
    method: 'POST',
    headers: headers({ prefer: 'return=minimal' }),
    body: JSON.stringify(body)
  });
  try {
    let res = await post(full);
    if (!res.ok) res = await post(base); // 신규 컬럼이 없으면 기본 컬럼만으로 재시도
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
