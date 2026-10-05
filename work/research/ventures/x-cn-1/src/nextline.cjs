/* X-CN-1 '오늘 기준 다음 할 일 한 줄' — 브라우저와 빌드(node)가 같은 파일을 쓴다(기준 하나).
 * 예술가 통과 조건(art/2026-10-01-1445.md 0-1): ① 기준일·원문 대조 시각 도장은 같은 줄·같은 크기
 * ② 대조 시각은 빌드 스크립트가 원문과 사실표를 비교한 시각(사람 0) ③ 24시간 넘으면 그 줄만 '공식 일정 확인하기' 링크로 물러난다.
 * 예술가 제안 R: 접수가 끝나고 다음 접수 전이면 '놓쳤다면' 줄로 바뀐다.
 * 시각은 모두 한국 시각(KST). 사용자 기기 시간대와 상관없다. */
(function (root) {
  'use strict';
  var DOW = ['일', '월', '화', '수', '목', '금', '토'];
  var DAY = 864e5;

  function t(s) { return Date.parse(s.length === 10 ? s + 'T00:00:00+09:00' : s + ':00+09:00'); }
  function kst(ms) { var d = new Date(ms + 9 * 36e5); return { y: d.getUTCFullYear(), m: d.getUTCMonth() + 1, d: d.getUTCDate(), w: d.getUTCDay(), h: d.getUTCHours(), mi: d.getUTCMinutes() }; }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function md(ms) { var k = kst(ms); return k.m + '/' + k.d + '(' + DOW[k.w] + ')'; }
  function hm(ms) { var k = kst(ms); return pad(k.h) + ':' + pad(k.mi); }
  function dayNo(ms) { return Math.floor((ms + 9 * 36e5) / DAY); }
  function rel(ms, now) {
    var n = dayNo(ms) - dayNo(now);
    return n === 0 ? '오늘' : n === 1 ? '내일' : n > 1 ? n + '일 뒤' : '';
  }

  function windows(F) {
    var w = [];
    F.rounds.forEach(function (r) {
      w.push({ no: r.no, kind: '원서접수', s: t(r.apply[0]), e: t(r.apply[1]) });
      w.push({ no: r.no, kind: '취소좌석 접수', s: t(r.cancel_seat[0]), e: t(r.cancel_seat[1]) });
    });
    return w.sort(function (a, b) { return a.s - b.s; });
  }

  // 반환: {state, main, after, stamp, sub}
  //  state: open | missed | upcoming | done | stale
  function nextLine(F, verifiedAt, now) {
    // 대조가 어제였으면 날짜를 붙인다(안 붙이면 다음 날 아침에 '원문 15:45 대조'가 아직 안 온 오늘 오후로 읽힌다).
    var v = verifiedAt ? Date.parse(verifiedAt) : 0, vk = kst(v);
    var stamp = md(now) + ' 기준 · ' + F.org + ' 원문 ' + (!v ? '--:--' : (dayNo(v) === dayNo(now) ? '' : vk.m + '/' + vk.d + ' ') + hm(v)) + ' 대조';
    if (!verifiedAt || now - Date.parse(verifiedAt) > DAY) {
      return { state: 'stale', main: '공식 일정 확인하기', after: '', stamp: '', sub: '', href: F.source_url };
    }
    var w = windows(F), open = null, next = null, last = null;
    w.forEach(function (x) {
      if (x.s <= now && now < x.e) open = open || x;
      else if (x.s > now) next = next || x;
      else last = x;
    });
    var nextTxt = next ? '제' + next.no + '회 ' + next.kind + ' ' + md(next.s) + ' ' + hm(next.s) : '';
    // 채점 10/2: 카드는 작은 머리(k) + 큰 글자 1줄(b) + 설명 1줄(d). 글자는 main·after와 같은 조각(새 문장 0)
    // 채점 10/2 v3: 큰 줄은 날짜·시각 하나만, 'n일 뒤'는 머리(k) 줄로, 이미 마감된 일은 카드에서 뺀다
    var nk = next ? '제' + next.no + '회 ' + next.kind + (rel(next.s, now) ? ' · ' + rel(next.s, now) : '') : '', nb = next ? md(next.s) + ' ' + hm(next.s) : '';
    var sp = subParts(F, now);
    var r = { state: '', main: '', after: '', stamp: stamp, sub: sp ? sp.h + ': ' + sp.items.join(' · ') : '', subh: sp ? sp.h : '', subs: sp ? sp.items : [] };
    if (open) {
      var rr = rel(open.e, now);
      r.state = 'open';
      r.main = '제' + open.no + '회 ' + open.kind + ' 중 · ' + md(open.e) + ' ' + hm(open.e) + ' 마감' + (rr ? '(' + rr + ')' : '');
      r.after = nextTxt ? '놓치면 다음: ' + nextTxt : '';
      r.k = '제' + open.no + '회 ' + open.kind + ' 중 · 마감' + (rr ? ' ' + rr : ''); r.b = md(open.e) + ' ' + hm(open.e); r.d = r.after;
    } else if (last && next) {
      r.state = 'missed';
      r.main = '제' + last.no + '회 ' + last.kind + ' ' + md(last.e) + ' ' + hm(last.e) + ' 마감됨';
      r.after = '다음: ' + nextTxt + (rel(next.s, now) ? '(' + rel(next.s, now) + ')' : '');
      r.k = '다음: ' + nk; r.b = nb; r.d = '';
    } else if (next) {
      r.state = 'upcoming';
      r.main = '다음: ' + nextTxt + (rel(next.s, now) ? '(' + rel(next.s, now) + ')' : '');
      r.k = '다음: ' + nk; r.b = nb; r.d = '';
    } else {
      r.state = 'done';
      r.main = '2026년 접수 일정 모두 마감됨';
      r.after = '다음 해 일정은 ' + F.org + ' 공지를 확인하세요';
      r.k = ''; r.b = r.main; r.d = r.after;
    }
    return r;
  }

  // 이미 접수한 사람용 보조 줄: 시험이 아직 안 지난 가장 가까운 회차
  // beat-1st 10/2: 접수 취소 환불 구간(공식 표 '접수 취소 기간 및 취소시 환불안내')을 맨 앞에 — 100% 환불이 끝나는 시각을 놓치지 않게.
  function subParts(F, now) {
    for (var i = 0; i < F.rounds.length; i++) {
      var r = F.rounds[i], ex = t(r.exam);
      if (ex + DAY <= now) continue;
      if (t(r.apply[0]) > now) return null;
      var parts = [];
      if (r.refund100 && now < t(r.refund100[1])) {
        var rr = rel(t(r.refund100[1]), now);
        parts.push('접수 취소 시 100% 환불 ' + md(t(r.refund100[1])) + ' ' + hm(t(r.refund100[1])) + '까지' + (rr ? '(' + rr + ')' : ''));
      } else if (r.refund50 && now < t(r.refund50[1])) {
        parts.push('접수 취소 시 50% 환불 ' + (now < t(r.refund50[0]) ? md(t(r.refund50[0])) + ' ' + hm(t(r.refund50[0])) + ' ~ ' : '')
          + md(t(r.refund50[1])) + ' ' + hm(t(r.refund50[1])) + (now < t(r.refund50[0]) ? '' : '까지'));
      }
      if (t(r.ticket) > now) parts.push('수험표 출력 ' + md(t(r.ticket)) + ' ' + hm(t(r.ticket)) + '부터');
      parts.push('시험 ' + md(ex));
      return { h: '제' + r.no + '회 접수했다면', items: parts };
    }
    return null;
  }

  var api = { nextLine: nextLine, md: md, hm: hm, t: t };
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.NextLine = api;
})(this);
