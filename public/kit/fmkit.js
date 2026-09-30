/* fmkit.js — 신사업 새 사이트 공용 부품 (firemap-venture-builder, 2026-10-01)
 * 빌드 없이 <script src="/kit/fmkit.js" defer></script> 한 줄로 쓴다. 의존성 0.
 *
 * 1) 측정: 파이어맵과 같은 firemap_events 표(파이어맵 Supabase)에 익명 이벤트를 남긴다.
 *    - props.site(사이트 이름)·lang·path가 모든 이벤트에 붙는다. 파이어맵 앱 이벤트와 site로 가른다.
 *    - ?fm_internal=1 로 한 번 들어온 기기는 internal:1 (src/utils/live.js와 같은 규칙).
 *    - utm_*·ref(리퍼러 호스트)는 session_start에만 붙는다. 금액·이름 같은 입력 원본은 절대 넣지 않는다.
 * 2) 결과 공유 카드: 1080×1080 PNG를 canvas로 그려 Web Share(파일) → 링크 공유 → 링크 복사 순서로 내보낸다.
 *
 * 쓰는 법:
 *   FMKit.init({ site: 'salary-en', lang: 'en' });           // session_start 1회
 *   FMKit.log('calc_submit', { bucket: '50-100k' });          // 행동 이벤트(구간값만)
 *   FMKit.share({ title, big, sub, brand, url, text });       // 결과 공유(share_open/share_done 자동 기록)
 */
(function () {
  'use strict';
  var SB_URL = ['https://cvhskxdwqubmshdgkzhj', 'supabase', 'co'].join('.');
  var SB_KEY = ['sb', 'publishable', 'uhbAVqCA8JrJNXqaAcft9g', 'yYtwgct9'].join('_');
  var CID = 'fm_cid';
  var ctx = { site: 'unknown', lang: document.documentElement.lang || 'ko' };
  var started = false;

  function ls(k, v) {
    try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { /* 사생활 모드 */ }
    return null;
  }
  function cid() {
    var id = ls(CID);
    if (!id) {
      id = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : Date.now() + '-' + Math.random().toString(16).slice(2);
      ls(CID, id);
    }
    return id || 'anon';
  }
  function qs() { try { return new URLSearchParams(location.search || ''); } catch (e) { return { get: function () { return null; } }; } }
  function audit() {
    var x = {};
    if (qs().get('fm_internal') === '1') ls('fm_internal', '1');
    if (ls('fm_internal') === '1') x.internal = 1;
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
  function card(o) {
    var S = 1080, c = document.createElement('canvas');
    c.width = S; c.height = S;
    var g = c.getContext('2d');
    var fam = '"Pretendard", "Apple SD Gothic Neo", "Noto Sans KR", system-ui, sans-serif';
    var accent = o.accent || '#ff5a00';
    g.fillStyle = '#18191d'; g.fillRect(0, 0, S, S);
    g.fillStyle = accent; g.fillRect(0, 0, S, 16);
    g.textBaseline = 'top';
    g.fillStyle = '#f2f3f5'; g.font = '600 44px ' + fam;
    var y = 120;
    wrap(g, o.title, S - 160).slice(0, 3).forEach(function (l) { g.fillText(l, 80, y); y += 60; });
    y += 40;
    g.fillStyle = accent;
    fit(g, String(o.big || ''), '700', 150, S - 160, fam);
    g.fillText(String(o.big || ''), 80, y);
    y += 200;
    g.fillStyle = '#b0b3ba'; g.font = '400 38px ' + fam;
    wrap(g, o.sub, S - 160).slice(0, 4).forEach(function (l) { g.fillText(l, 80, y); y += 54; });
    g.fillStyle = '#f2f3f5'; g.font = '700 40px ' + fam;
    g.fillText(o.brand || location.hostname, 80, S - 130);
    g.fillStyle = '#8b8e96'; g.font = '400 30px ' + fam;
    g.fillText((o.url || location.href).replace(/^https?:\/\//, '').replace(/[?#].*$/, '').slice(0, 60), 80, S - 80);
    return c;
  }
  function toBlob(c) { return new Promise(function (res) { c.toBlob ? c.toBlob(res, 'image/png') : res(null); }); }

  function share(o) {
    o = o || {};
    var url = o.url || (location.origin + location.pathname);
    var sep = url.indexOf('?') < 0 ? '?' : '&';
    var shareUrl = url + sep + 'utm_source=share&utm_medium=' + encodeURIComponent(ctx.site);
    log('share_open', { kind: o.kind || 'result' });
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

  window.FMKit = { init: init, log: log, share: share, card: card };
})();
