import { identityId } from './identity.js';
// 오늘의 절약 — Supabase 연동 (기기당 하루 한 줄 upsert)
const DEFAULT_SUPABASE_URL = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const DEFAULT_SUPABASE_KEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');
const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL || DEFAULT_SUPABASE_URL;
const SUPABASE_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY || DEFAULT_SUPABASE_KEY;
const TABLE = 'firemap_save_events';

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

function todayStr() {
  return new Date().toISOString().slice(0, 10);
}

function countFromRange(res) {
  const cr = res.headers.get('content-range') || '';
  const total = cr.split('/')[1];
  return total && total !== '*' ? Number(total) : 0;
}

// 오늘 내 절약 한 줄을 upsert (client_id + date 기준 갱신)
export async function submitSave({ todaySaved, totalSaved, advancedDays, streak, nickname, ageBand, depositTotal, depositMonth }) {
  const cid = identityId();
  if (!cid) return false;
  const nick = (nickname || '').trim().slice(0, 16) || null;
  const body = {
    client_id: cid,
    date: todayStr(),
    today_saved: Math.max(0, Math.round(todaySaved || 0)),
    total_saved: Math.max(0, Math.round(totalSaved || 0)),
    advanced_days: (advancedDays != null && Number.isFinite(Number(advancedDays))) ? Number(Number(advancedDays).toFixed(5)) : null,
    streak: (streak != null && Number.isFinite(Number(streak))) ? Math.round(streak) : null,
    nickname: nick,
    age_band: ageBand != null ? String(ageBand) : null,
    deposit_total: Math.max(0, Math.round(depositTotal || 0)),
    deposit_month: Math.max(0, Math.round(depositMonth || 0)),
    updated_at: new Date().toISOString()
  };
  const post = (b) => fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?on_conflict=client_id,date`, {
    method: 'POST',
    headers: headers({ prefer: 'return=minimal,resolution=merge-duplicates' }),
    body: JSON.stringify(b)
  });
  try {
    let res = await post(body);
    if (!res.ok) {
      // 적립 컬럼(deposit_*) 마이그레이션 전이면 해당 필드 빼고 재시도 → 절약 저장은 항상 성공
      const { deposit_total, deposit_month, ...rest } = body;
      res = await post(rest);
    }
    return res.ok;
  } catch {
    return false;
  }
}

// 오늘 가장 많이 아낀 사람 top N
export async function fetchSaveTop(limit = 10) {
  try {
    const url = `${SUPABASE_URL}/rest/v1/${TABLE}?select=client_id,nickname,today_saved,age_band&date=eq.${todayStr()}&today_saved=gt.0&order=today_saved.desc&limit=${limit}`;
    const res = await fetch(url, { method: 'GET', headers: headers() });
    if (!res.ok) return [];
    return await res.json();
  } catch {
    return [];
  }
}

// 보드별 절약 랭킹 — today(오늘) / total(누적) / streak(연속일)
export async function fetchSaveBoard(metric = 'today', limit = 10) {
  try {
    if (metric === 'deposit') {
      const first = `${todayStr().slice(0, 7)}-01`;
      const url = `${SUPABASE_URL}/rest/v1/${TABLE}?select=client_id,nickname,deposit_month,age_band&date=gte.${first}&deposit_month=gt.0&order=deposit_month.desc&limit=80`;
      const res = await fetch(url, { method: 'GET', headers: headers() });
      const rows = res.ok ? await res.json() : [];
      const seen = new Set();
      const out = [];
      for (const r of rows) {
        if (seen.has(r.client_id)) continue;
        seen.add(r.client_id);
        out.push({ ...r, value: r.deposit_month });
        if (out.length >= limit) break;
      }
      return out;
    }
    if (metric === 'today') {
      const url = `${SUPABASE_URL}/rest/v1/${TABLE}?select=client_id,nickname,today_saved,age_band&date=eq.${todayStr()}&today_saved=gt.0&order=today_saved.desc&limit=${limit}`;
      const res = await fetch(url, { method: 'GET', headers: headers() });
      const rows = res.ok ? await res.json() : [];
      return rows.map((r) => ({ ...r, value: r.today_saved }));
    }
    if (metric === 'advance' || metric === 'streak') {
      // 앞당김·연속일은 줄어들 수 있으므로 '과거 최고치'가 아니라 '최신값(최근 날짜)'으로 랭킹
      const c = metric === 'streak' ? 'streak' : 'advanced_days';
      const u = `${SUPABASE_URL}/rest/v1/${TABLE}?select=client_id,nickname,${c},age_band,date&${c}=gt.0&order=date.desc&limit=600`;
      const r2 = await fetch(u, { method: 'GET', headers: headers() });
      const rs = r2.ok ? await r2.json() : [];
      const seen2 = new Set();
      const latest = [];
      for (const r of rs) { if (seen2.has(r.client_id)) continue; seen2.add(r.client_id); latest.push({ ...r, value: r[c] }); }
      latest.sort((a, b) => (b.value || 0) - (a.value || 0));
      return latest.slice(0, limit);
    }
    const col = metric === 'streak' ? 'streak' : metric === 'advance' ? 'advanced_days' : 'total_saved';
    const url = `${SUPABASE_URL}/rest/v1/${TABLE}?select=client_id,nickname,${col},age_band&${col}=gt.0&order=${col}.desc&limit=80`;
    const res = await fetch(url, { method: 'GET', headers: headers() });
    const rows = res.ok ? await res.json() : [];
    const seen = new Set();
    const out = [];
    for (const r of rows) {
      if (seen.has(r.client_id)) continue;
      seen.add(r.client_id);
      out.push({ ...r, value: r[col] });
      if (out.length >= limit) break;
    }
    return out;
  } catch {
    return [];
  }
}

// 오늘 기록자 중 내 순위
export async function fetchMySaveRank(todaySaved) {
  try {
    const date = todayStr();
    const opts = { method: 'GET', headers: headers({ prefer: 'count=exact', range: '0-0' }) };
    const totalRes = await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?select=id&date=eq.${date}&today_saved=gt.0`, opts);
    const total = countFromRange(totalRes);
    const mine = Math.max(0, Math.round(todaySaved || 0));
    if (mine <= 0) return { total, position: total + 1, mine: 0 };
    const higherRes = await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?select=id&date=eq.${date}&today_saved=gt.${mine}`, opts);
    const higher = countFromRange(higherRes);
    return { total, position: higher + 1, mine };
  } catch {
    return null;
  }
}
