// PWA 설치 프롬프트 캡처(beforeinstallprompt) — 앱 로드 시 일찍 등록
let deferred = null;
const listeners = new Set();
function emit() { listeners.forEach((fn) => { try { fn(); } catch { /* ignore */ } }); }
if (typeof window !== 'undefined') {
  window.addEventListener('beforeinstallprompt', (e) => { e.preventDefault(); deferred = e; emit(); });
  window.addEventListener('appinstalled', () => { deferred = null; emit(); });
}
export function installAvailable() { return !!deferred; }
export function onInstallChange(fn) { listeners.add(fn); return () => listeners.delete(fn); }
export async function promptInstall() {
  if (!deferred) return null;
  deferred.prompt();
  let outcome = 'unknown';
  try { const r = await deferred.userChoice; outcome = r && r.outcome ? r.outcome : 'unknown'; } catch { /* ignore */ }
  deferred = null; emit();
  return outcome;
}
