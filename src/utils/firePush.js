// 파이어 시계 — 웹푸시 구독 유틸. 로그인 무관(익명 client_id로 식별), 매일 1회 'D-day' 알림.
import { identityId, account } from './identity.js';

const SUPABASE_URL = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
const SUPABASE_KEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');
// VAPID 공개키(서버 비밀키와 한 쌍). 공개키는 클라이언트 노출이 정상.
const VAPID_PUBLIC = 'BJYJgOTmlTx9LcLWBex3RJZAicBp6D6Y8RJ3_cn4uKhDy6yFQp23uBagGUeZqcHHJTlXo8tJZp6t7HdI9eOTo44';

function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
  const raw = atob(base64);
  const out = new Uint8Array(raw.length);
  for (let i = 0; i < raw.length; i += 1) out[i] = raw.charCodeAt(i);
  return out;
}

export function isIOSDevice() {
  try { return /iphone|ipad|ipod/i.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1); }
  catch { return false; }
}

export function isStandalone() {
  try { return (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) || window.navigator.standalone === true; }
  catch { return false; }
}

// 이 기기에서 웹푸시가 실제로 가능한지(iOS는 홈화면 추가 PWA에서만 가능)
export function pushSupported() {
  try {
    if (!('serviceWorker' in navigator) || !('PushManager' in window) || !('Notification' in window)) return false;
    if (isIOSDevice() && !isStandalone()) return false; // iOS는 홈화면 추가 후에만
    return true;
  } catch { return false; }
}

export function notifPermission() {
  try { return Notification.permission; } catch { return 'default'; }
}

async function registerSW() {
  if (!('serviceWorker' in navigator)) return null;
  try {
    const existing = await navigator.serviceWorker.getRegistration('/');
    if (existing) return existing;
    return await navigator.serviceWorker.register('/sw.js', { scope: '/' });
  } catch { return null; }
}

export async function currentSubscription() {
  try {
    const reg = await navigator.serviceWorker.getRegistration();
    if (!reg) return null;
    return await reg.pushManager.getSubscription();
  } catch { return null; }
}

async function saveSub(sub, meta) {
  const json = sub.toJSON();
  let cid = null; try { cid = identityId(); } catch { /* ignore */ }
  let acc = null; try { acc = account(); } catch { /* ignore */ }
  let tz = 'Asia/Seoul'; try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || 'Asia/Seoul'; } catch { /* ignore */ }
  const body = {
    endpoint: sub.endpoint,
    p256dh: json.keys && json.keys.p256dh,
    auth: json.keys && json.keys.auth,
    client_id: cid || null,
    user_id: (acc && acc.userId) ? acc.userId : null,
    target_fire_date: meta.targetFireDate || null,
    earliest_age: meta.earliestAge ?? null,
    current_age: meta.currentAge ?? null,
    tz,
    active: true,
    updated_at: new Date().toISOString()
  };
  try {
    const res = await fetch(`${SUPABASE_URL}/rest/v1/firemap_push_subs?on_conflict=endpoint`, {
      method: 'POST',
      headers: { apikey: SUPABASE_KEY, authorization: `Bearer ${SUPABASE_KEY}`, 'content-type': 'application/json', prefer: 'resolution=merge-duplicates,return=minimal' },
      body: JSON.stringify(body)
    });
    return res.ok;
  } catch { return false; }
}

// 구독 시작: (iOS 대비) 권한을 클릭 제스처 직후 '가장 먼저' 요청 → SW 등록 → 구독 → 저장.
// meta={targetFireDate, earliestAge, currentAge}
export async function subscribeFireClock(meta = {}) {
  if (!('serviceWorker' in navigator) || !('PushManager' in window) || !('Notification' in window)) {
    return { ok: false, reason: isIOSDevice() ? 'ios-install' : 'unsupported' };
  }
  if (isIOSDevice() && !isStandalone()) return { ok: false, reason: 'ios-install' };

  // 1) 권한 먼저(awaits 전에 — iOS Safari 제스처 보존)
  let perm = notifPermission();
  if (perm === 'default') { try { perm = await Notification.requestPermission(); } catch { perm = 'denied'; } }
  if (perm !== 'granted') return { ok: false, reason: 'denied' };

  // 2) 서비스워커 등록
  const reg = await registerSW();
  if (!reg) return { ok: false, reason: 'sw' };
  try { await navigator.serviceWorker.ready; } catch { /* ignore */ }

  // 3) 푸시 구독
  let sub = null;
  try { sub = await reg.pushManager.getSubscription(); } catch { /* ignore */ }
  if (!sub) {
    try {
      sub = await reg.pushManager.subscribe({ userVisibleOnly: true, applicationServerKey: urlBase64ToUint8Array(VAPID_PUBLIC) });
    } catch (e) {
      return { ok: false, reason: 'subscribe', detail: String((e && (e.message || e.name)) || e) };
    }
  }

  // 4) 서버 저장
  const saved = await saveSub(sub, meta);
  if (!saved) return { ok: false, reason: 'save' };
  return { ok: true };
}

// 저장된 목표일 등 메타만 갱신(재계산 후 호출). 구독이 없으면 무시.
export async function refreshFireClockMeta(meta = {}) {
  try {
    const sub = await currentSubscription();
    if (!sub) return false;
    return await saveSub(sub, meta);
  } catch { return false; }
}

export async function unsubscribeFireClock() {
  try {
    const sub = await currentSubscription();
    if (!sub) return true;
    try {
      await fetch(`${SUPABASE_URL}/rest/v1/firemap_push_subs?endpoint=eq.${encodeURIComponent(sub.endpoint)}`, {
        method: 'PATCH',
        headers: { apikey: SUPABASE_KEY, authorization: `Bearer ${SUPABASE_KEY}`, 'content-type': 'application/json', prefer: 'return=minimal' },
        body: JSON.stringify({ active: false, updated_at: new Date().toISOString() })
      });
    } catch { /* ignore */ }
    await sub.unsubscribe();
    return true;
  } catch { return false; }
}

// 시뮬레이션 → 목표 파이어 날짜(YYYY-MM-DD). 가장 이른 파이어 나이 기준.
export function targetFireDateFrom(simulation) {
  try {
    const earliest = simulation && simulation.earliestRetirementAge;
    const cur = simulation && simulation.inputs && Number(simulation.inputs.currentAge);
    if (!earliest || !cur) return null;
    const years = Math.max(0, earliest - cur);
    const d = new Date(Date.now() + years * 365.25 * 86400000);
    return d.toISOString().slice(0, 10);
  } catch { return null; }
}
