import { identityId, identityIds } from './identity.js';
import { statsRank } from '../firemap-v2/rank.js';
import { journeyStage } from './journeyStage.js';
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

export async function submitScore({ fireScore, ageBand, survivalAge, nickname, earliestAge, assetBand, targetAge, currentAge, stage }) {
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
    earliest_age: (earliestAge != null && Number.isFinite(Number(earliestAge))) ? Math.round(Number(earliestAge)) : null,
    target_age: (targetAge != null && Number.isFinite(Number(targetAge))) ? Math.round(Number(targetAge)) : null,
    current_age: (currentAge != null && Number.isFinite(Number(currentAge))) ? Math.round(Number(currentAge)) : null
  };
  const cid = identityId();
  const fullAsset = (assetBand != null) ? { ...full, asset_band: assetBand } : full;
  const withStage = (o) => (stage != null && Number.isFinite(Number(stage))) ? { ...o, stage: Math.max(1, Math.min(6, Math.round(Number(stage)))) } : o;
  const send = (body, merge) => fetch(`${SUPABASE_URL}/rest/v1/${TABLE}${merge ? '?on_conflict=client_id' : ''}`, {
    method: 'POST',
    headers: headers({ prefer: merge ? 'return=minimal,resolution=merge-duplicates' : 'return=minimal' }),
    body: JSON.stringify(body)
  });
  // current_age 컬럼 미존재(구 DB) 보존 폴백용
  const dropAge = (o) => { const { current_age, ...rest } = o; return rest; };
  try {
    if (cid) {
      let res = await send({ ...withStage(fullAsset), client_id: cid }, true);
      if (!res.ok) res = await send({ ...fullAsset, client_id: cid }, true);          // stage 컬럼 미존재 폴백
      if (!res.ok) res = await send({ ...dropAge(fullAsset), client_id: cid }, true); // current_age 컬럼 미존재 폴백
      if (!res.ok) res = await send({ ...dropAge(full), client_id: cid }, true);        // asset_band 컬럼 미존재 폴백
      if (res.ok) return true;
    }
    let res = await send(withStage(fullAsset), false);
    if (!res.ok) res = await send(fullAsset, false);
    if (!res.ok) res = await send(dropAge(fullAsset), false);
    if (!res.ok) res = await send(dropAge(full), false);
    if (!res.ok) res = await send(base, false);
    return res.ok;
  } catch {
    return false;
  }
}

// 점수 제출 페이로드를 한 곳에서 생성 — 결과·순위 등 모든 호출부가 동일 필드를 보내도록(stage 등 누락 방지).
// rankingSimulation(공정비교용) 기준 순위 필드 + simulation 기준 여정 단계(stage).
export function submitScoreFromSim({ rankingSimulation, simulation, nickname = '' }) {
  const rs = rankingSimulation || simulation;
  if (!rs || !rs.inputs) return Promise.resolve(false);
  const base = statsRank(rs);
  let stage = null;
  try { const js = journeyStage(simulation || rs); stage = js ? js.stage : null; } catch { /* ignore */ }
  return submitScore({
    fireScore: rs.survivalScore,
    ageBand: base.ageBand,
    survivalAge: (rs.targetResult && rs.targetResult.depletionAge) || rs.inputs.simulationUntilAge,
    nickname,
    earliestAge: rs.earliestRetirementAge,
    assetBand: assetBandOf(rs.netWorth),
    targetAge: rs.inputs.targetRetirementAge,
    currentAge: rs.inputs.currentAge,
    stage
  });
}

// 함께 계산한 사용자 중 내 등수/백분위
export async function fetchUserRank(earliestAge, ageBand, advancedDays) {
  try {
    const opts = { method: 'GET', headers: headers({ prefer: 'count=exact', range: '0-0' }) };
    const band = ageBand ? `&age_band=eq.${ageBand}` : '';
    const totalRes = await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?select=id${band}`, opts);
    const total = countFromRange(totalRes);
    if (!total) return null;
    const hasAge = earliestAge != null && Number.isFinite(Number(earliestAge));
    const mine = hasAge ? Math.round(Number(earliestAge)) : null;
    // 더 이른 파이어 가능 나이 = 더 높은 순위. 값 없으면(파이어 불가) 값 있는 사람 모두가 상위.
    const higherQuery = hasAge
      ? `${SUPABASE_URL}/rest/v1/${TABLE}?select=id&earliest_age=lt.${mine}${band}`
      : `${SUPABASE_URL}/rest/v1/${TABLE}?select=id&earliest_age=not.is.null${band}`;
    const higherRes = await fetch(higherQuery, opts);
    let higher = countFromRange(higherRes);
    // 같은 파이어나이(동점)는 실제 저축으로 더 많이 당긴 사람이 상위 → 매일 저축하면 같은 나이대를 제침
    if (hasAge) {
      const adv = Number.isFinite(Number(advancedDays)) ? Number(advancedDays) : 0;
      const tieRes = await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?select=id&earliest_age=eq.${mine}&advanced_days=gt.${adv}${band}`, opts);
      higher += countFromRange(tieRes);
    }
    const position = higher + 1;
    const percentile = Math.min(99, Math.max(1, Math.round((higher / total) * 100)));
    return { total, position, percentile };
  } catch {
    return null;
  }
}

// 또래(같은 나이) 순위 — current_age 표본이 충분하면 '정확 나이', 아니면 '나이밴드(N0대)'로 자동 폴백.
// 들어온 사람의 핵심 질문("내 나이 중 몇 등?")에 바로 답하는 보드. 자산 아님 — 파이어 가능 나이 기준.
export async function fetchPeerBoard({ currentAge, ageBand, earliestAge, advancedDays, limit = 10 }) {
  const MIN_AGE_SAMPLE = 20; // 같은 나이가 이만큼 모이면 '정확 나이'로 좁힘
  const opts = { method: 'GET', headers: headers({ prefer: 'count=exact', range: '0-0' }) };
  const ageNum = (currentAge != null && Number.isFinite(Number(currentAge))) ? Math.round(Number(currentAge)) : null;
  try {
    // 1) 같은 나이 표본 수 확인
    let useAge = false;
    let ageTotal = 0;
    if (ageNum != null) {
      const r = await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?select=id&current_age=eq.${ageNum}`, opts);
      ageTotal = countFromRange(r);
      useAge = ageTotal >= MIN_AGE_SAMPLE;
    }
    const filter = useAge ? `&current_age=eq.${ageNum}` : (ageBand ? `&age_band=eq.${ageBand}` : '');
    const scope = useAge ? 'age' : (ageBand ? 'band' : 'all');
    const ageLabel = useAge ? `${ageNum}세` : (ageBand ? `${ageBand}대` : '전체');
    // 2) 모수
    const total = useAge ? ageTotal : countFromRange(await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?select=id${filter}`, opts));
    // 3) 내 등수 (fetchUserRank와 동일 규칙: 빠른 파이어 → 동점은 당긴 일수)
    let position = null;
    let percentile = null;
    if (total > 0) {
      const hasAge = earliestAge != null && Number.isFinite(Number(earliestAge));
      const mine = hasAge ? Math.round(Number(earliestAge)) : null;
      const higherQ = hasAge
        ? `${SUPABASE_URL}/rest/v1/${TABLE}?select=id&earliest_age=lt.${mine}${filter}`
        : `${SUPABASE_URL}/rest/v1/${TABLE}?select=id&earliest_age=not.is.null${filter}`;
      let higher = countFromRange(await fetch(higherQ, opts));
      if (hasAge) {
        const adv = Number.isFinite(Number(advancedDays)) ? Number(advancedDays) : 0;
        higher += countFromRange(await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?select=id&earliest_age=eq.${mine}&advanced_days=gt.${adv}${filter}`, opts));
      }
      position = higher + 1;
      percentile = Math.min(99, Math.max(1, Math.round((higher / total) * 100)));
    }
    // 4) 상위 10
    const sel = `select=client_id,nickname,fire_score,age_band,current_age,earliest_age${filter}`;
    let topRes = await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?${sel}&order=earliest_age.asc.nullslast,advanced_days.desc,fire_score.desc&limit=${limit}`, { method: 'GET', headers: headers() });
    if (!topRes.ok) {
      topRes = await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?${sel}&order=earliest_age.asc.nullslast,fire_score.desc&limit=${limit}`, { method: 'GET', headers: headers() });
    }
    const top = topRes.ok ? await topRes.json() : [];
    return { scope, ageLabel, total, position, percentile, top };
  } catch {
    return null;
  }
}

// 여정 단계별 경쟁 — 나와 같은 FIRE 여정 단계(1~6)에 있는 사람들끼리 순위(파이어 빠른 순, 동점은 더 당긴 사람).
export async function fetchStageBoard({ stage, earliestAge, advancedDays, limit = 10 }) {
  if (stage == null) return null;
  const st = Math.max(1, Math.min(6, Math.round(Number(stage))));
  const filter = `&stage=eq.${st}`;
  const opts = { method: 'GET', headers: headers({ prefer: 'count=exact', range: '0-0' }) };
  try {
    const total = countFromRange(await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?select=id${filter}`, opts));
    let position = null; let percentile = null;
    if (total > 0) {
      const hasAge = earliestAge != null && Number.isFinite(Number(earliestAge));
      const mine = hasAge ? Math.round(Number(earliestAge)) : null;
      const higherQ = hasAge
        ? `${SUPABASE_URL}/rest/v1/${TABLE}?select=id&earliest_age=lt.${mine}${filter}`
        : `${SUPABASE_URL}/rest/v1/${TABLE}?select=id&earliest_age=not.is.null${filter}`;
      let higher = countFromRange(await fetch(higherQ, opts));
      if (hasAge) {
        const adv = Number.isFinite(Number(advancedDays)) ? Number(advancedDays) : 0;
        higher += countFromRange(await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?select=id&earliest_age=eq.${mine}&advanced_days=gt.${adv}${filter}`, opts));
      }
      position = higher + 1;
      percentile = Math.min(99, Math.max(1, Math.round((higher / total) * 100)));
    }
    const sel = `select=client_id,nickname,fire_score,age_band,current_age,earliest_age,stage${filter}`;
    let topRes = await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?${sel}&order=earliest_age.asc.nullslast,advanced_days.desc,fire_score.desc&limit=${limit}`, { method: 'GET', headers: headers() });
    if (!topRes.ok) {
      topRes = await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?${sel}&order=earliest_age.asc.nullslast,fire_score.desc&limit=${limit}`, { method: 'GET', headers: headers() });
    }
    const top = topRes.ok ? await topRes.json() : [];
    return { total, position, percentile, top };
  } catch { return null; }
}

// 순자산 구간(금액 비공개, 구간만 저장) — 0:<1억 1:1~3억 2:3~5억 3:5~10억 4:10~20억 5:20억+
export function assetBandOf(netWorth) {
  const eok = (Number(netWorth) || 0) / 100000000;
  if (eok < 1) return 0;
  if (eok < 3) return 1;
  if (eok < 5) return 2;
  if (eok < 10) return 3;
  if (eok < 20) return 4;
  return 5;
}

// 파이어맵 사용자(연령대 또래) 중 내 자산 상위 X% — 구간 기준 익명 비교(앱 내 랭킹)
export async function fetchAssetPercentile(ageBand, assetBand) {
  if (assetBand == null) return null;
  try {
    const band = ageBand ? `&age_band=eq.${ageBand}` : '';
    const opts = { method: 'GET', headers: headers({ prefer: 'count=exact', range: '0-0' }) };
    const totalRes = await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?select=id&asset_band=not.is.null${band}`, opts);
    const total = countFromRange(totalRes);
    if (!total) return null;
    const higherRes = await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?select=id&asset_band=gt.${assetBand}${band}`, opts);
    const higher = countFromRange(higherRes);
    const percentile = Math.max(1, Math.min(99, Math.round(((higher + 0.5) / total) * 100)));
    return { total, percentile };
  } catch { return null; }
}

// 내 점수행의 advanced_days만 갱신(저축 변동 시) → 동점 분리에 즉시 반영
export async function updateScoreAdvance(advancedDays) {
  // 계정ID + 기기ID 양쪽 점수행을 모두 갱신(로그인 전 기록이 기기ID로 남아 누락되는 것 방지)
  const ids = identityIds();
  if (!ids.length) return false;
  const v = (advancedDays != null && Number.isFinite(Number(advancedDays))) ? Number(Number(advancedDays).toFixed(2)) : 0;
  const filter = ids.length > 1 ? `client_id=in.(${ids.join(',')})` : `client_id=eq.${ids[0]}`;
  try {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?${filter}`, {
      method: 'PATCH', headers: headers({ prefer: 'return=minimal' }),
      body: JSON.stringify({ advanced_days: v })
    });
    return res.ok;
  } catch { return false; }
}

export async function fetchTopScores(limit = 10, ageBand) {
  try {
    const band = ageBand ? `&age_band=eq.${ageBand}` : '';
    const sel = `select=client_id,nickname,fire_score,age_band,earliest_age${band}`;
    // 1순위: 빠른 파이어 → 같으면 실제 저축으로 더 당긴 사람(advanced_days) → 생존점수
    const urlAdv = `${SUPABASE_URL}/rest/v1/${TABLE}?${sel}&order=earliest_age.asc.nullslast,advanced_days.desc,fire_score.desc&limit=${limit}`;
    let res = await fetch(urlAdv, { method: 'GET', headers: headers() });
    if (!res.ok) {
      // advanced_days 컬럼 마이그레이션 전이면 옛 정렬로 폴백
      const urlOld = `${SUPABASE_URL}/rest/v1/${TABLE}?${sel}&order=earliest_age.asc.nullslast,fire_score.desc&limit=${limit}`;
      res = await fetch(urlOld, { method: 'GET', headers: headers() });
    }
    if (!res.ok) return [];
    return await res.json();
  } catch {
    return [];
  }
}

export async function fetchAggregates(ageBand) {
  try {
    const opts = { method: 'GET', headers: headers({ prefer: 'count=exact', range: '0-1999' }) };
    const band = ageBand ? `&age_band=eq.${ageBand}` : '';
    const res = await fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?select=earliest_age,age_band,fire_score${band}`, opts);
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

// 내 주변 순위 — 바로 위(더 빨리 파이어) / 바로 아래
export async function fetchNeighbors(earliestAge, ageBand, exactAge) {
  if (earliestAge == null || !Number.isFinite(Number(earliestAge))) return null;
  try {
    const mine = Math.round(Number(earliestAge));
    // exactAge가 주어지면 같은 나이(current_age) 기준, 아니면 기존처럼 연령대(age_band) 기준 — 하위호환.
    const band = (exactAge != null && Number.isFinite(Number(exactAge)))
      ? `&current_age=eq.${Math.round(Number(exactAge))}`
      : (ageBand ? `&age_band=eq.${ageBand}` : '');
    const sel = 'select=client_id,nickname,earliest_age,age_band';
    const opts = { method: 'GET', headers: headers() };
    const countOpts = { method: 'GET', headers: headers({ prefer: 'count=exact', range: '0-0' }) };
    const [aboveRes, belowRes, sameRes] = await Promise.all([
      fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?${sel}&earliest_age=lt.${mine}${band}&order=earliest_age.desc&limit=3`, opts),
      fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?${sel}&earliest_age=gt.${mine}${band}&order=earliest_age.asc&limit=3`, opts),
      fetch(`${SUPABASE_URL}/rest/v1/${TABLE}?select=id&earliest_age=eq.${mine}${band}`, countOpts)
    ]);
    const above = aboveRes.ok ? await aboveRes.json() : [];
    const below = belowRes.ok ? await belowRes.json() : [];
    const same = sameRes.ok ? countFromRange(sameRes) : 0; // 나와 같은 파이어나이 인원(동점)
    return { above: above.reverse(), below, same };
  } catch {
    return null;
  }
}

const POLL_TABLE = 'firemap_poll_votes';

export async function votePoll(pollKey, choice) {
  const cid = identityId();
  try {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/${POLL_TABLE}?on_conflict=poll_key,client_id`, {
      method: 'POST',
      headers: headers({ prefer: 'return=minimal,resolution=merge-duplicates' }),
      body: JSON.stringify({ poll_key: pollKey, choice, client_id: cid })
    });
    return res.ok;
  } catch {
    return false;
  }
}

export async function fetchPollResults(pollKey, choices) {
  try {
    const opts = { method: 'GET', headers: headers({ prefer: 'count=exact', range: '0-0' }) };
    const counts = {};
    let total = 0;
    await Promise.all(choices.map(async (c) => {
      const url = `${SUPABASE_URL}/rest/v1/${POLL_TABLE}?select=id&poll_key=eq.${encodeURIComponent(pollKey)}&choice=eq.${encodeURIComponent(c)}`;
      const res = await fetch(url, opts);
      const n = res.ok ? countFromRange(res) : 0;
      counts[c] = n;
      total += n;
    }));
    return { counts, total };
  } catch {
    return null;
  }
}
