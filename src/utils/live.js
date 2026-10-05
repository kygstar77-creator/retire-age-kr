import { identityId } from './identity.js';
import { SUPABASE_URL, SUPABASE_KEY } from './supabaseClient.js';
// 실시간 접속(프레즈던) + 익명 이벤트 로깅 — 개인정보 없이 기기ID·이벤트명·익명 속성만

const H = { apikey: SUPABASE_KEY, authorization: `Bearer ${SUPABASE_KEY}`, 'content-type': 'application/json' };

function nick() { try { return localStorage.getItem('fm_nickname') || ''; } catch { return ''; } }

// 로컬·미리보기 호스트(127.0.0.1·localhost·*.pages.dev 등)에서는 기록하지 않는다 — 9/30 원값 451세션 중 352가 테스트라 실측을 덮음(성장 담당 요청 10/1).
// 테스트가 이벤트를 봐야 할 때만 localStorage fm_events_on=1로 켠다(그래도 host 표시는 붙는다).
function localHost() {
  try {
    const h = (window.location.hostname || '').toLowerCase();
    return !h || h === 'localhost' || h === '127.0.0.1' || h === '[::1]' || h === '::1' || h.endsWith('.localhost') || h.endsWith('.test') || h.endsWith('.pages.dev') || /^(10|192\.168|172\.(1[6-9]|2\d|3[01]))\./.test(h);
  } catch { return false; }
}
function eventsOff() {
  if (!localHost()) return false;
  try { return localStorage.getItem('fm_events_on') !== '1'; } catch { return true; }
}

// 접속 중임을 알림(하트비트)
export function presencePing() {
  if (eventsOff()) return;
  const cid = identityId();
  if (!cid) return;
  try {
    fetch(`${SUPABASE_URL}/rest/v1/rpc/fm_presence_ping`, { method: 'POST', headers: H, body: JSON.stringify({ p_client: cid, p_nick: nick() || null }) }).catch(() => {});
  } catch { /* ignore */ }
}

// 현재 접속자 수 + 최근 닉네임
export async function fetchLivePresence() {
  try {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/fm_live_presence`, { method: 'POST', headers: H, body: JSON.stringify({}) });
    if (!res.ok) return null;
    const rows = await res.json();
    const r = rows && rows[0];
    return r ? { online: r.online || 0, names: r.names || [] } : { online: 0, names: [] };
  } catch { return null; }
}

// 최근 절약 기록(배너 활동 표시용)
// 지금까지 계산한 총 인원(누적 통계)
export async function fetchTotalCalc() {
  try {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/firemap_scores?select=id`, { headers: { ...H, prefer: 'count=exact', range: '0-0' } });
    const cr = res.headers.get('content-range') || '';
    const t = cr.split('/')[1];
    return t && t !== '*' ? Number(t) : 0;
  } catch { return 0; }
}

// 내부 점검 방문 표시 — ?fm_internal=1 로 한 번 들어온 기기는 이후 모든 이벤트에 internal:1(성장 담당 요청 9/30).
// firemap.kr 밖(localhost·pages.dev 미리보기)에서 난 이벤트엔 host를 남긴다. 개인정보 없는 값만.
function auditProps() {
  const extra = {};
  try {
    if (new URLSearchParams(window.location.search || '').get('fm_internal') === '1') localStorage.setItem('fm_internal', '1');
    if (localStorage.getItem('fm_internal') === '1') extra.internal = 1;
  } catch { /* ignore */ }
  try {
    const host = window.location.hostname || '';
    if (host && host !== 'firemap.kr' && host !== 'www.firemap.kr') extra.host = host.slice(0, 80);
  } catch { /* ignore */ }
  return extra;
}

// 실험군 a/b — client_id 문자열 해시(FNV-1a 32비트)의 홀짝으로 반반(10/5 [지시] X-CP-1·X-HOME-1, 근거 behavior/2026-10-02-coupang-audit.md 5장).
// 같은 기기는 늘 같은 군. 화면은 아직 군별로 다르지 않다(측정만 먼저) — 군별 화면이 생기면 이 함수만 쓴다.
export function abArm(cid) {
  const s = String(cid || '');
  if (!s) return null;
  let h = 0x811c9dc5;
  for (let i = 0; i < s.length; i += 1) { h ^= s.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; }
  return (h & 1) ? 'b' : 'a';
}

// 익명 이벤트 기록(append-only). 개인정보·금액 원본 없이 행동 이벤트만. 모든 이벤트에 실험군 ab를 붙인다.
// keepalive: 페이지를 떠나는 순간(home_leave) 보낸 요청도 끊기지 않게.
export function logEvent(event, props) {
  if (eventsOff()) return;
  try {
    const cid = identityId();
    const extra = auditProps();
    const ab = abArm(cid);
    if (ab) extra.ab = ab;
    const merged = Object.keys(extra).length ? { ...(props || {}), ...extra } : (props || null);
    fetch(`${SUPABASE_URL}/rest/v1/firemap_events`, {
      method: 'POST',
      keepalive: true,
      headers: { ...H, prefer: 'return=minimal' },
      body: JSON.stringify({ client_id: cid, event: String(event).slice(0, 80), props: merged })
    }).catch(() => {});
  } catch { /* ignore */ }
}
