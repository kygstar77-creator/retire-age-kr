/* 파이어맵 서비스워커 — 웹푸시(파이어 시계) 전용.
   주의: fetch 캐싱은 일부러 안 함(오프라인 캐시로 인한 흰 화면/구버전 고착 방지). 푸시 표시·클릭만 담당. */
self.addEventListener('install', () => { self.skipWaiting(); });
self.addEventListener('activate', (event) => { event.waitUntil(self.clients.claim()); });

self.addEventListener('push', (event) => {
  let data = {};
  try { data = event.data ? event.data.json() : {}; } catch { data = {}; }
  const title = data.title || '파이어맵';
  const options = {
    body: data.body || '오늘의 파이어 시계를 확인해보세요',
    icon: data.icon || '/icon-192.png',
    badge: data.badge || '/icon-192.png',
    tag: data.tag || 'fire-clock',
    renotify: true,
    data: { url: data.url || 'https://firemap.kr/' }
  };
  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  const url = (event.notification.data && event.notification.data.url) || 'https://firemap.kr/';
  event.waitUntil((async () => {
    const all = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
    for (const c of all) {
      if (c.url.includes('firemap.kr') && 'focus' in c) return c.focus();
    }
    if (self.clients.openWindow) return self.clients.openWindow(url);
    return undefined;
  })());
});
