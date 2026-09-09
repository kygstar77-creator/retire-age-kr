// 플랫폼 추상화 1벌 — 웹 구현. 앱(Capacitor) 단계에서 이 파일의 구현만 플러그인으로 바꾼다.
// 화면은 navigator.share / Notification / window.open 을 직접 부르지 않고 여기만 쓴다.
export function isNative() {
  try { return !!(window.Capacitor && window.Capacitor.isNativePlatform && window.Capacitor.isNativePlatform()); } catch { return false; }
}

export function platform() {
  try { if (window.Capacitor && window.Capacitor.getPlatform) return window.Capacitor.getPlatform(); } catch { /* ignore */ }
  const ua = navigator.userAgent || '';
  if (/iPhone|iPad|iPod/i.test(ua)) return 'ios-web';
  if (/Android/i.test(ua)) return 'android-web';
  return 'web';
}

// 공유: 네이티브 시트 → 클립보드 폴백. 반환 { ok, method }
export async function share({ title, text, url }) {
  if (navigator.share) {
    try { await navigator.share({ title, text, url }); return { ok: true, method: 'share' }; }
    catch (e) { if (e && e.name === 'AbortError') return { ok: false, method: 'abort' }; }
  }
  try { await navigator.clipboard.writeText(url ? `${text || ''}\n${url}`.trim() : text); return { ok: true, method: 'clipboard' }; }
  catch { return { ok: false, method: 'none' }; }
}

export function openExternal(url) {
  try { window.open(url, '_blank', 'noopener,noreferrer'); return true; } catch { return false; }
}

export function haptic(kind = 'light') {
  try { if (navigator.vibrate) navigator.vibrate(kind === 'heavy' ? 30 : 12); } catch { /* ignore */ }
}

// 위젯 스냅샷 전달 — 웹은 localStorage(fm_widget)만. 앱은 App Group / SharedPreferences 브리지로 교체.
export function widgetSync(state) {
  try { localStorage.setItem('fm_widget', JSON.stringify(state)); } catch { /* ignore */ }
}

// 보상형 광고 — 웹은 항상 '없음'. 앱 단계(AdMob)에서만 구현. 부가 콘텐츠에만 쓴다(App Store 3.1.1·AdMob 정책).
export async function showRewarded() { return { ok: false, reason: 'web' }; }
