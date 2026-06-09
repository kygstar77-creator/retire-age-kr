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

export async function submitScore({ fireScore, ageBand, survivalAge }) {
  try {
    await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}`, {
      method: 'POST',
      headers: headers({ prefer: 'return=minimal' }),
      body: JSON.stringify({
        fire_score: Math.max(0, Math.min(100, Math.round(fireScore))),
        age_band: ageBand || null,
        survival_age: survivalAge || null,
        client_type: window.innerWidth <= 640 ? 'mobile' : 'desktop'
      })
    });
    return true;
  } catch {
    return false;
  }
}

// 함께 계산한 사용자 중 내 등수/백분위
export async function fetchUserRank(fireScore) {
  try {
    const score = Math.max(0, Math.min(100, Math.round(fireScore)));
    const opts = { method: 'GET', headers: headers({ prefer: 'count=exact', range: '0-0' }) };
    const [totalRes, higherRes] = await Promise.all([
      fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?select=id`, opts),
      fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?select=id&fire_score=gt.${score}`, opts)
    ]);
    const total = countFromRange(totalRes);
    const higher = countFromRange(higherRes);
    if (!total) return null;
    const position = higher + 1;
    const percentile = Math.min(99, Math.max(1, Math.round((higher / total) * 100)));
    return { total, position, percentile };
  } catch {
    return null;
  }
}
