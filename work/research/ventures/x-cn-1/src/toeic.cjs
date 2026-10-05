/* X-CN-1 2편 토익 '오늘 기준 다음 할 일 한 줄' — 브라우저와 빌드(node)가 같은 파일을 쓴다(기준 하나).
 * 한능검(nextline.cjs)과 같은 카드 틀(stamp·k·b·d·subh·subs), 같은 예술가 조건(도장 같은 줄·빌드가 찍음·24시간 넘으면 공식 링크).
 * 토익만 다른 점: 회차 번호가 원문에 없어 시험일로 부른다. 접수 창(정기접수·특별추가)이 여러 회차에 동시에 열려 있어
 * 맨 위 줄은 '지금 열린 창 중 가장 먼저 닫히는 것'. 보조 상자 = 원문 "차기 시험 접수 마감 후 성적이 발표됩니다"를 날짜로 푼 것
 * (compare.md beat-1st ①): 다가오는 시험의 성적발표 전에 닫히는 정기접수와, 발표 뒤 가장 먼저 닫히는 접수.
 * 시각은 모두 한국 시각(KST). */
(function (root) {
  'use strict';
  var DOW = ['일', '월', '화', '수', '목', '금', '토'];
  var DAY = 864e5;

  function t(s) { return Date.parse(s.length === 10 ? s + 'T00:00:00+09:00' : s + ':00+09:00'); }
  function kst(ms) { var d = new Date(ms + 9 * 36e5); return { m: d.getUTCMonth() + 1, d: d.getUTCDate(), w: d.getUTCDay(), h: d.getUTCHours(), mi: d.getUTCMinutes() }; }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function md(ms) { var k = kst(ms); return k.m + '/' + k.d + '(' + DOW[k.w] + ')'; }
  function hm(ms) { var k = kst(ms); return pad(k.h) + ':' + pad(k.mi); }
  function dayNo(ms) { return Math.floor((ms + 9 * 36e5) / DAY); }
  function rel(ms, now) {
    var n = dayNo(ms) - dayNo(now);
    return n === 0 ? '오늘' : n === 1 ? '내일' : n > 1 ? n + '일 뒤' : '';
  }
  function ex(r) { return md(t(r.exam)) + ' 시험'; }

  function windows(F) {
    var w = [];
    F.rounds.forEach(function (r) {
      w.push({ r: r, kind: '정기접수', s: t(r.apply[0]), e: t(r.apply[1]) });
      w.push({ r: r, kind: '특별추가', s: t(r.extra[0]), e: t(r.extra[1]) });
    });
    return w;
  }

  // 반환: {state, main, after, stamp, k, b, d, subh, subs}  state: open | upcoming | done | stale
  function nextLine(F, verifiedAt, now) {
    var v = verifiedAt ? Date.parse(verifiedAt) : 0, vk = kst(v);
    var stamp = md(now) + ' 기준 · ' + F.org + ' 원문 ' + (!v ? '--:--' : (dayNo(v) === dayNo(now) ? '' : vk.m + '/' + vk.d + ' ') + hm(v)) + ' 대조';
    if (!verifiedAt || now - v > DAY) {
      return { state: 'stale', main: '공식 일정 확인하기', after: '', stamp: '', subh: '', subs: [], href: F.source_url };
    }
    var w = windows(F);
    var open = w.filter(function (x) { return x.s <= now && now < x.e; }).sort(function (a, b) { return a.e - b.e; });
    var next = w.filter(function (x) { return x.s > now; }).sort(function (a, b) { return a.s - b.s; })[0];
    var sp = subParts(F, now);
    var r = { state: '', main: '', after: '', stamp: stamp, subh: sp ? sp.h : '', subs: sp ? sp.items : [] };
    if (open.length) {
      var o = open[0], rr = rel(o.e, now), o2 = open[1];
      r.state = 'open';
      r.main = ex(o.r) + ' ' + o.kind + ' 중 · ' + md(o.e) + ' ' + hm(o.e) + ' 마감' + (rr ? '(' + rr + ')' : '');
      r.after = o2 ? '놓치면 다음: ' + ex(o2.r) + ' ' + o2.kind + ' ' + md(o2.e) + ' ' + hm(o2.e) + ' 마감' : '';
      r.k = ex(o.r) + ' ' + o.kind + ' 중 · 마감' + (rr ? ' ' + rr : ''); r.b = md(o.e) + ' ' + hm(o.e); r.d = r.after;
    } else if (next) {
      var nr = rel(next.s, now);
      r.state = 'upcoming';
      r.main = '다음: ' + ex(next.r) + ' ' + next.kind + ' ' + md(next.s) + ' ' + hm(next.s) + (nr ? '(' + nr + ')' : '');
      r.k = '다음: ' + ex(next.r) + ' ' + next.kind + (nr ? ' · ' + nr : ''); r.b = md(next.s) + ' ' + hm(next.s); r.d = '';
    } else {
      r.state = 'done';
      r.main = '사실표의 접수 일정 모두 마감됨';
      r.after = '다음 일정은 ' + F.org + ' 시험일정을 확인하세요';
      r.k = ''; r.b = r.main; r.d = r.after;
    }
    return r;
  }

  // 시험을 아직 안 본(또는 성적을 기다리는) 가장 가까운 회차 기준: 성적발표 전에 닫히는 정기접수 / 발표 뒤 가장 먼저 닫히는 접수
  function subParts(F, now) {
    var rs = F.rounds.slice().sort(function (a, b) { return t(a.exam) - t(b.exam); });
    for (var i = 0; i < rs.length; i++) {
      var r = rs[i], res = t(r.result);
      if (res <= now) continue;
      var items = ['성적발표 ' + md(res) + ' ' + hm(res)];
      var before = rs.filter(function (x) { var e = t(x.apply[1]); return x !== r && now < e && e < res; });
      if (before.length) {
        items.push('발표 전 정기접수 마감: ' + before.map(function (x) { return ex(x) + '(' + md(t(x.apply[1])) + ' ' + hm(t(x.apply[1])) + ')'; }).join(', '));
      }
      var after = windows(F).filter(function (x) { return x.r !== r && t(x.r.exam) > t(r.exam) && x.e > res; })
        .sort(function (a, b) { return t(a.r.exam) - t(b.r.exam) || a.e - b.e; })[0];
      if (after) items.push('발표 뒤 가장 빠른 접수: ' + ex(after.r) + ' ' + after.kind + ' ' + md(after.e) + ' ' + hm(after.e) + ' 마감');
      return { h: md(t(r.exam)) + (t(r.exam) < now ? ' 시험을 봤다면' : ' 시험을 본다면'), items: items };
    }
    return null;
  }

  var api = { nextLine: nextLine, md: md, hm: hm, t: t };
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.NextLine = api;
})(this);
