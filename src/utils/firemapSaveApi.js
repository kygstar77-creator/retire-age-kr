import { identityId, accountHandle } from './identity.js';
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

// 랭킹 표시: client_id가 계정이면 그 계정의 '현재 handle'로 닉네임을 덮어씀(기기/익명은 행 nickname 폴백).
// → 과거 행에 박힌 스테일 닉네임 대신 항상 현재 이름이 보임. 실패해도 원본 그대로 반환(무해).
async function applyAccountHandles(rows) {
  try {
    const list = rows || [];
    const ids = [...new Set(list.map((r) => r.client_id).filter(Boolean))];
    if (!ids.length) return list;
    const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/fm_account_handles`, { method: 'POST', headers: headers(), body: JSON.stringify({ p_ids: ids }) });
    if (!res.ok) return list;
    const map = {};
    for (const r of (await res.json()) || []) { if (r && r.client_id) map[r.client_id] = r.handle; }
    return list.map((r) => (map[r.client_id] ? { ...r, nickname: map[r.client_id] } : r));
  } catch { return rows || []; }
}

// 오늘 내 절약 한 줄을 upsert (client_id + date 기준 갱신)
export async function submitSave({ todaySaved, totalSaved, advancedDays, streak, nickname, ageBand, depositTotal, depositMonth, targetAge, goalPct, currentAge }) {
  const cid = identityId();
  if (!cid) return false;
  // 로그인 상태면 계정의 현재 handle을 우선 사용(다른 계정 닉네임이 localStorage에 남아 섞이는 것 차단). 비로그인은 전달된 닉네임 폴백.
  const liveHandle = (accountHandle && accountHandle()) || '';
  const nick = (liveHandle || nickname || '').trim().slice(0, 16) || null;
  const body = {
    client_id: cid,
    date: todayStr(),
    today_saved: Math.max(0, Math.round(todaySaved || 0)),
    total_saved: Math.max(0, Math.round(totalSaved || 0)),
    advanced_days: (advancedDays != null && Number.isFinite(Number(advancedDays))) ? Number(Number(advancedDays).toFixed(5)) : null,
    streak: (streak != null && Number.isFinite(Number(streak))) ? Math.round(streak) : null,
    nickname: nick,
    age_band: ageBand != null ? String(ageBand) : null,
    target_age: (targetAge != null && Number.isFinite(Number(targetAge))) ? Math.round(Number(targetAge)) : null,
    current_age: (currentAge != null && Number.isFinite(Number(currentAge))) ? Math.round(Number(currentAge)) : null,
    goal_pct: (goalPct != null && Number.isFinite(Number(goalPct))) ? Math.max(0, Math.min(100, Math.round(Number(goalPct)))) : null,
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
      const { current_age, ...noAge } = body;
      res = await post(noAge);
    }
    if (!res.ok) {
      const { goal_pct, current_age, ...noGoal } = body;
      res = await post(noGoal);
    }
    if (!res.ok) {
      const { deposit_total, deposit_month, goal_pct, current_age, ...rest } = body;
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
    return await applyAccountHandles(await res.json());
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
      return await applyAccountHandles(out);
    }
    if (metric === 'today') {
      const url = `${SUPABASE_URL}/rest/v1/${TABLE}?select=client_id,nickname,today_saved,age_band&date=eq.${todayStr()}&today_saved=gt.0&order=today_saved.desc&limit=${limit}`;
      const res = await fetch(url, { method: 'GET', headers: headers() });
      const rows = res.ok ? await res.json() : [];
      return await applyAccountHandles(rows.map((r) => ({ ...r, value: r.today_saved })));
    }
    if (metric === 'advance' || metric === 'streak') {
      const c = metric === 'streak' ? 'streak' : 'advanced_days';
      const u = `${SUPABASE_URL}/rest/v1/${TABLE}?select=client_id,nickname,${c},age_band,date&${c}=gt.0&order=date.desc&limit=600`;
      const r2 = await fetch(u, { method: 'GET', headers: headers() });
      const rs = r2.ok ? await r2.json() : [];
      const seen2 = new Set();
      const latest = [];
      for (const r of rs) { if (seen2.has(r.client_id)) continue; seen2.add(r.client_id); latest.push({ ...r, value: r[c] }); }
      latest.sort((a, b) => (b.value || 0) - (a.value || 0));
      return await applyAccountHandles(latest.slice(0, limit));
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
    return await applyAccountHandles(out);
  } catch {
    return [];
  }
}

// 코호트(같은 나이·목표 또래) 누적 저축 리더보드 — RPC 호출, 자동 폴백
export async function fetchCohortSaveBoard(ageBand, targetAge, limit = 10) {
  try {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/fm_cohort_save_board`, {
      method: 'POST',
      headers: headers(),
      body: JSON.stringify({ p_age_band: ageBand || 30, p_target_age: targetAge || 0, p_limit: limit })
    });
    if (!res.ok) return [];
    const rows = await res.json();
    return (rows || []).map((r) => ({ client_id: r.uid, nickname: r.nick, value: r.val, scope: r.scope, goalPct: r.gpct != null ? Number(r.gpct) : null }));
  } catch {
    return [];
  }
}

// 코호트 '파이어 당김(advanced_days)' 리더보드 — exact(정확나이)→cohort(나이밴드)→age→all 폴백
export async function fetchCohortAdvanceBoard(ageBand, tLo, tHi, limit = 10, currentAge = null) {
  const sel = 'select=client_id,nickname,advanced_days,age_band,target_age,goal_pct,date';
  const ageNum = (currentAge != null && Number.isFinite(Number(currentAge))) ? Math.round(Number(currentAge)) : null;
  const dedupeLatest = (rows) => {
    const seen = new Set();
    const out = [];
    for (const r of rows) {
      if (seen.has(r.client_id)) continue;
      seen.add(r.client_id);
      out.push({
        client_id: r.client_id,
        nickname: r.nickname,
        value: Number(r.advanced_days) || 0,
        age_band: r.age_band,
        target_age: r.target_age,
        goalPct: r.goal_pct != null ? Number(r.goal_pct) : null
      });
    }
    out.sort((a, b) => (b.value || 0) - (a.value || 0));
    return out.slice(0, limit);
  };
  const q = async (filter) => {
    const url = `${SUPABASE_URL}/rest/v1/${TABLE}?${sel}&advanced_days=gt.0${filter ? `&${filter}` : ''}&order=date.desc&limit=600`;
    const res = await fetch(url, { method: 'GET', headers: headers() });
    return res.ok ? await res.json() : [];
  };
  try {
    if (ageNum != null && tLo != null && tHi != null) {
      const rows = dedupeLatest(await q(`current_age=eq.${ageNum}&target_age=gte.${tLo}&target_age=lte.${tHi}`));
      if (rows.length >= 3) return rows.map((r) => ({ ...r, scope: 'exact' }));
    }
    if (ageBand != null && tLo != null && tHi != null) {
      const rows = dedupeLatest(await q(`age_band=eq.${encodeURIComponent(String(ageBand))}&target_age=gte.${tLo}&target_age=lte.${tHi}`));
      if (rows.length >= 3) return rows.map((r) => ({ ...r, scope: 'cohort' }));
    }
    if (ageBand != null) {
      const rows = dedupeLatest(await q(`age_band=eq.${encodeURIComponent(String(ageBand))}`));
      if (rows.length >= 3) return rows.map((r) => ({ ...r, scope: 'age' }));
    }
    const rows = dedupeLatest(await q(''));
    return rows.map((r) => ({ ...r, scope: 'all' }));
  } catch {
    return [];
  }
}

// 주간 절약 랭킹 — offset 0=이번주, 1=지난주 (월요일 리셋)
export async function fetchWeeklySaveBoard(limit = 10, offset = 0) {
  try {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/fm_weekly_save_board`, {
      method: 'POST',
      headers: headers(),
      body: JSON.stringify({ p_limit: limit, p_offset: offset })
    });
    if (!res.ok) return [];
    const rows = await res.json();
    return (rows || []).map((r) => ({ client_id: r.uid, nickname: r.nick, age_band: r.band, value: r.val }));
  } catch {
    return [];
  }
}

// 명예의 전당 — 지난 주차별 절약왕(1위)
export async function fetchWeeklyHall(weeks = 8) {
  try {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/fm_weekly_hall`, {
      method: 'POST',
      headers: headers(),
      body: JSON.stringify({ p_weeks: weeks })
    });
    if (!res.ok) return [];
    const rows = await res.json();
    return (rows || []).map((r) => ({ weekLabel: r.week_label, weekStart: r.week_start, client_id: r.uid, nickname: r.nick, value: r.val }));
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
