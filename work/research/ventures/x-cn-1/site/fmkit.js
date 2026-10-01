/* fmkit.js (uk-pay 복사본, noStore) — 브라우저 저장소·쿠키 0, 페이지 열 때마다 임시 id. brief 9장 1(영국 PECR).
 * 원본: retire-age-kr public/kit/fmkit.js (firemap-venture-builder, 2026-10-01)
 * 빌드 없이 <script src="/kit/fmkit.js" defer></script> 한 줄로 쓴다. 의존성 0.
 *
 * 1) 측정: 파이어맵과 같은 firemap_events 표(파이어맵 Supabase)에 익명 이벤트를 남긴다.
 *    - props.site(사이트 이름)·lang·path가 모든 이벤트에 붙는다. 파이어맵 앱 이벤트와 site로 가른다.
 *    - ?fm_internal=1 로 한 번 들어온 기기는 internal:1 (src/utils/live.js와 같은 규칙).
 *    - utm_*·ref(리퍼러 호스트)는 session_start에만 붙는다. 금액·이름 같은 입력 원본은 절대 넣지 않는다.
 * 2) 결과 공유 카드: 1080×1080 PNG를 canvas로 그려 Web Share(파일) → 링크 공유 → 링크 복사 순서로 내보낸다.
 *
 * 쓰는 법:
 *   FMKit.init({ site: 'salary-en', lang: 'en', accent: '#0a6b52' }); // session_start 1회, accent는 사이트 색(필수)
 *   FMKit.log('calc_submit', { bucket: '50-100k' });          // 행동 이벤트(구간값만)
 *   FMKit.share({ title, big, sub, brand, url, text });       // 결과 공유(share_open/share_done 자동 기록)
 */
(function () {
  'use strict';
  var SB_URL = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
  var SB_KEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');
  var ctx = { site: 'unknown', lang: document.documentElement.lang || 'ko' };
  var started = false;

  // noStore: 저장소를 전혀 쓰지 않는다.
  var tmpId = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : Date.now() + '-' + Math.random().toString(16).slice(2);
  function cid() { return tmpId; }
  function qs() { try { return new URLSearchParams(location.search || ''); } catch (e) { return { get: function () { return null; } }; } }
  function audit() {
    var x = {};
    if (qs().get('fm_internal') === '1') x.internal = 1;
    var h = location.hostname || '';
    if (h && h !== 'firemap.kr' && h !== 'www.firemap.kr') x.host = h.slice(0, 80);
    return x;
  }

  function log(event, props) {
    try {
      var p = { site: ctx.site, lang: ctx.lang, path: location.pathname.slice(0, 120) };
      var k;
      for (k in (props || {})) if (Object.prototype.hasOwnProperty.call(props, k)) p[k] = props[k];
      var a = audit();
      for (k in a) p[k] = a[k];
      var body = JSON.stringify({ client_id: cid(), event: String(event).slice(0, 80), props: p });
      fetch(SB_URL + '/rest/v1/firemap_events', {
        method: 'POST',
        keepalive: true,
        headers: { apikey: SB_KEY, authorization: 'Bearer ' + SB_KEY, 'content-type': 'application/json', prefer: 'return=minimal' },
        body: body
      }).catch(function () {});
    } catch (e) { /* 측정 실패가 화면을 막지 않는다 */ }
  }

  function init(opts) {
    opts = opts || {};
    if (opts.site) ctx.site = String(opts.site).slice(0, 40);
    if (opts.lang) ctx.lang = String(opts.lang).slice(0, 8);
    if (opts.accent) ctx.accent = String(opts.accent).slice(0, 20);
    if (started) return;
    started = true;
    var q = qs(), p = {};
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content'].forEach(function (k) { var v = q.get(k); if (v) p[k] = v.slice(0, 60); });
    try { if (document.referrer) { var r = new URL(document.referrer); if (r.hostname !== location.hostname) p.ref = r.hostname.slice(0, 80); } } catch (e) { /* ignore */ }
    p.w = Math.round(window.innerWidth || document.documentElement.clientWidth || (screen && screen.width) || 0);
    log('session_start', p);
  }

  // ── 결과 공유 카드 ──────────────────────────────────────────
  // 색은 파이어맵 디자인 규칙(색 4개)을 기본값으로, 사이트마다 accent만 바꾼다.
  function wrap(g, text, maxW) {
    var words = String(text || '').split(/(\s+)/), lines = [], cur = '';
    for (var i = 0; i < words.length; i++) {
      var t = cur + words[i];
      if (g.measureText(t).width > maxW && cur.trim()) { lines.push(cur.trim()); cur = words[i]; } else cur = t;
    }
    if (cur.trim()) lines.push(cur.trim());
    return lines;
  }
  function fit(g, text, weight, start, maxW, family) {
    var s = start;
    do { g.font = weight + ' ' + s + 'px ' + family; s -= 4; } while (g.measureText(text).width > maxW && s > 40);
  }
  // 디자인 검수(kit-review 08:1x) 반영: 묶음 세로 가운데 · 숫자 최대 180px · accent는 사이트마다 필수.
  function card(o) {
    var S = 1080, c = document.createElement('canvas');
    c.width = S; c.height = S;
    var g = c.getContext('2d');
    var fam = o.font || '"Pretendard", "Apple SD Gothic Neo", "Noto Sans KR", system-ui, sans-serif';
    // accent 기본값을 파이어맵 주황으로 두지 않는다(신사업 = 별도 정체성). 없으면 무채색 + 콘솔 경고.
    var accent = o.accent || ctx.accent;
    if (!accent) { accent = '#f2f3f5'; try { console.warn('FMKit.card: accent missing — pass the site colour'); } catch (e) { /* ignore */ } }
    g.fillStyle = '#18191d'; g.fillRect(0, 0, S, S);
    g.fillStyle = accent; g.fillRect(0, 0, S, 16);
    g.textBaseline = 'top';
    var big = String(o.big || '');
    g.font = '600 44px ' + fam;
    var tl = wrap(g, o.title, S - 160).slice(0, 3);
    g.font = '400 38px ' + fam;
    var sl = wrap(g, o.sub, S - 160).slice(0, 4);
    fit(g, big, '700', 180, S - 160, fam);
    var bigFont = g.font, bigSize = parseInt(/(\d+)px/.exec(bigFont)[1], 10);
    var gap = 40, h = tl.length * 60 + gap + Math.round(bigSize * 1.2) + gap + sl.length * 54;
    var y = Math.max(96, Math.round((S - h) / 2 - 40));
    g.fillStyle = '#f2f3f5'; g.font = '600 44px ' + fam;
    tl.forEach(function (l) { g.fillText(l, 80, y); y += 60; });
    y += gap;
    g.fillStyle = accent; g.font = bigFont;
    g.fillText(big, 80, y);
    y += Math.round(bigSize * 1.2) + gap;
    g.fillStyle = '#b0b3ba'; g.font = '400 38px ' + fam;
    sl.forEach(function (l) { g.fillText(l, 80, y); y += 54; });
    g.fillStyle = '#f2f3f5'; g.font = '700 40px ' + fam;
    g.fillText(o.brand || location.hostname, 80, S - 130);
    g.fillStyle = '#8b8e96'; g.font = '400 30px ' + fam;
    g.fillText((o.url || location.href).replace(/^https?:\/\//, '').replace(/[?#].*$/, '').slice(0, 60), 80, S - 80);
    return c;
  }
  // 화면 큰 숫자 맞춤(kit-review 1): 칸보다 넓으면 4px씩 줄인다. 최소 24px.
  function fitText(el, min) {
    if (!el) return;
    el.style.fontSize = '';
    var s = parseFloat(getComputedStyle(el).fontSize) || 40;
    while (el.scrollWidth > el.clientWidth && s > (min || 24)) { s -= 4; el.style.fontSize = s + 'px'; }
  }
  function toBlob(c) { return new Promise(function (res) { c.toBlob ? c.toBlob(res, 'image/png') : res(null); }); }

  function share(o) {
    o = o || {};
    var url = o.url || (location.origin + location.pathname);
    var sep = url.indexOf('?') < 0 ? '?' : '&';
    var shareUrl = url + sep + 'utm_source=share&utm_medium=' + encodeURIComponent(ctx.site);
    log('share_open', o.clock ? { kind: o.kind || 'result', clock: 1 } : { kind: o.kind || 'result' });
    var done = function (method) { log('share_done', { method: method, kind: o.kind || 'result' }); return method; };
    return toBlob(card(o)).then(function (blob) {
      var file = null;
      try { if (blob && window.File) file = new File([blob], (ctx.site || 'result') + '.png', { type: 'image/png' }); } catch (e) { file = null; }
      var data = { title: o.title || document.title, text: o.text || '', url: shareUrl };
      if (file && navigator.canShare && navigator.canShare({ files: [file] })) {
        return navigator.share({ files: [file], title: data.title, text: (data.text ? data.text + '\n' : '') + shareUrl })
          .then(function () { return done('share_file'); }, function () { return 'cancel'; });
      }
      if (navigator.share) return navigator.share(data).then(function () { return done('share_link'); }, function () { return 'cancel'; });
      var copy = navigator.clipboard ? navigator.clipboard.writeText((data.text ? data.text + ' ' : '') + shareUrl) : Promise.reject();
      return copy.then(function () { return done('copy'); }, function () {
        if (blob) { var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = file ? file.name : 'result.png'; a.click(); return done('download'); }
        return 'fail';
      });
    });
  }

  window.FMKit = { init: init, log: log, share: share, card: card, fitText: fitText };
})();
