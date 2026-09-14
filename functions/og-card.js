// 공유 카드(남색 카카오 스타일) 공통 SVG 빌더.
// /og 동적 생성(functions/og.js)과 정적 og-image(work/fix-branding-og.mjs)가 함께 써서
// 카카오·다른 앱·웹 링크 어디서 공유하든 같은 남색 카드가 나오게 한다.
const COMMA = (n) => String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
// 텍스트 폭 추정 후 카드 폭을 넘치면 폰트 크기 자동 축소(auto-fit). 한글/전각≈1.0em, 라틴·기호≈0.56em, 공백≈0.32em.
function fitFont(text, base, maxWidth, min) {
  let units = 0;
  for (const ch of String(text)) {
    const c = ch.codePointAt(0);
    if (ch === ' ') units += 0.32;
    else if (c >= 0x1100) units += 1.0;
    else units += 0.56;
  }
  const est = units * base;
  return est <= maxWidth ? base : Math.max(min, Math.round(base * maxWidth / est));
}
const FLAME = '<svg x="497" y="92" width="30" height="60" viewBox="188 84 136 276"><path d="M256 84 C 232 150, 188 172, 188 256 C 188 322, 218 360, 256 360 C 294 360, 324 322, 324 256 C 324 212, 300 188, 286 162 C 282 192, 268 204, 252 210 C 268 166, 262 116, 256 84 Z" fill="#ff5a00"/><path d="M256 250 C 246 276, 232 286, 232 312 C 232 336, 242 352, 256 352 C 270 352, 280 336, 280 312 C 280 292, 270 280, 264 268 C 262 282, 258 286, 252 290 C 258 274, 258 262, 256 250 Z" fill="#fdba74"/></svg>';

// opts: { mode: 'rank'|'generic'|'save'|'firetype', ea, pos, tot, runway, tname, nick, cities, font }
export function buildCardSvg(opts = {}) {
  const font = opts.font || 'Noto Sans CJK KR';
  const mode = opts.mode || 'rank';
  const header = `<rect width="1200" height="600" fill="#18224d"/>
${FLAME}
<text x="537" y="138" font-family="${font}" font-weight="700" font-size="40" fill="#ffffff">파이어맵</text>`;

  let body;
  if (mode === 'save') {
    body = `<text x="600" y="216" font-family="${font}" font-weight="400" font-size="34" fill="#9aa4d4" text-anchor="middle">절약으로 파이어 앞당기기</text>
<text x="600" y="322" font-family="${font}" font-weight="700" font-size="78" fill="#ffffff" text-anchor="middle">하루 아낀 돈이</text>
<text x="600" y="416" font-family="${font}" font-weight="700" font-size="78" fill="#ffffff" text-anchor="middle"><tspan fill="#ff5a00">파이어</tspan>를 당겨요</text>`;
  } else if (mode === 'generic') {
    body = `<text x="600" y="216" font-family="${font}" font-weight="400" font-size="34" fill="#9aa4d4" text-anchor="middle">또래 중 내 파이어 등수도 1분 만에</text>
<text x="600" y="322" font-family="${font}" font-weight="700" font-size="80" fill="#ffffff" text-anchor="middle">나는 몇 살에</text>
<text x="600" y="416" font-family="${font}" font-weight="700" font-size="80" fill="#ffffff" text-anchor="middle"><tspan fill="#ff5a00">파이어</tspan>할 수 있을까?</text>`;
  } else if (mode === 'firetype') {
    const tname = (opts.tname || '').trim() || '파이어족';
    const nick = (opts.nick || '').trim();
    const cities = (opts.cities || '').trim();
    const citiesText = `추천 도시 · ${cities}`;
    const tSize = fitFont(tname, 84, 1040, 46);       // 제목: 좌우 ~80px 여백 확보, 길면 자동 축소
    const nSize = fitFont(`“${nick}”`, 40, 1060, 26); // 닉네임
    const cSize = fitFont(citiesText, 34, 1100, 22);  // 추천 도시 줄(3개가 길어도 안 잘리게)
    body = `<text x="600" y="206" font-family="${font}" font-weight="400" font-size="34" fill="#9aa4d4" text-anchor="middle">나의 파이어 유형은</text>
<text x="600" y="312" font-family="${font}" font-weight="700" font-size="${tSize}" fill="#ffffff" text-anchor="middle">${tname}</text>
${nick ? `<text x="600" y="372" font-family="${font}" font-weight="700" font-size="${nSize}" fill="#ff8a4c" text-anchor="middle">“${nick}”</text>` : ''}
${cities ? `<text x="600" y="448" font-family="${font}" font-weight="600" font-size="${cSize}" fill="#9aa4d4" text-anchor="middle">${citiesText}</text>` : ''}`;
  } else {
    // rank — 사용자별 또래 상위 %·등수·파이어 나이
    const ea = Number(opts.ea) || 0;
    const pos = Number(opts.pos) || 0;
    const tot = Math.max(1, Number(opts.tot) || 1);
    const runway = (opts.runway && opts.runway !== '—') ? String(opts.runway) : '';
    const p = Math.max(1, Math.min(99, Math.round((pos / tot) * 100)));
    const parts = [];
    if (ea > 0) parts.push(ea + '세 파이어 가능');
    if (runway) parts.push(runway.indexOf('이상') >= 0 ? runway + ' 버팀' : runway + '까지 버팀');
    const mid = parts.join(' · ');
    body = `<text x="600" y="208" font-family="${font}" font-weight="400" font-size="34" fill="#9aa4d4" text-anchor="middle">파이어 랭킹 · 또래 상위</text>
<text x="600" y="358" font-family="${font}" font-weight="700" font-size="150" fill="#ff5a00" text-anchor="middle">${p}%</text>
<text x="600" y="418" font-family="${font}" font-weight="700" font-size="40" fill="#ffffff" text-anchor="middle">전체 <tspan fill="#ff8a4c">${COMMA(tot)}명</tspan> 중 <tspan fill="#ff8a4c">${COMMA(pos)}등</tspan></text>
<text x="600" y="470" font-family="${font}" font-weight="600" font-size="30" fill="#9aa4d4" text-anchor="middle">${mid}</text>`;
  }

  const cta = `<text x="600" y="540" font-family="${font}" font-weight="700" font-size="30" fill="#ffffff" text-anchor="middle">나도 1분 만에 확인  →  <tspan fill="#ff8a4c">firemap.kr</tspan></text>`;
  return `<svg width="1200" height="600" viewBox="0 0 1200 600" xmlns="http://www.w3.org/2000/svg">
${header}
${body}
${cta}
</svg>`;
}

// 인증 카드(1080×1350, 카페·인스타 세로) — 배당 투자자 모임 제목 공식 + Reddit 댓글 6종(숫자·기간·가정)
// 자산 곡선용 점 — 엔진 rows(financialAsset)를 0~1로 정규화. 앱 화면·미리보기·공유 이미지가 같은 함수를 쓴다.
export function seriesFromRows(rows, fireAge) {
  const pts = (rows || []).map((r) => ({ age: r.age, v: Math.max(0, r.financialAsset || 0) }));
  if (pts.length < 2) return null;
  const max = Math.max(...pts.map((p) => p.v), 1);
  const a0 = pts[0].age; const a1 = pts[pts.length - 1].age;
  const out = pts.map((p) => ({ x: (p.age - a0) / Math.max(1, a1 - a0), y: p.v / max }));
  const fx = fireAge ? Math.min(1, Math.max(0, (fireAge - a0) / Math.max(1, a1 - a0))) : null;
  return { pts: out, fireX: fx, a0, a1 };
}
// 곡선 SVG 조각 — box {x,y,w,h}
function curveSvg(series, box, opts = {}) {
  if (!series || !series.pts || series.pts.length < 2) return '';
  const { x, y, w, h } = box;
  const P = (p) => `${(x + p.x * w).toFixed(1)} ${(y + h - p.y * h).toFixed(1)}`;
  const line = series.pts.map((p, i) => (i ? 'L' : 'M') + P(p)).join(' ');
  const area = `${line} L${(x + w).toFixed(1)} ${(y + h).toFixed(1)} L${x} ${(y + h).toFixed(1)} Z`;
  const fireLine = series.fireX != null ? `<line x1="${(x + series.fireX * w).toFixed(1)}" y1="${y}" x2="${(x + series.fireX * w).toFixed(1)}" y2="${y + h}" stroke="#ffffff" stroke-opacity="0.35" stroke-width="${opts.thin ? 2 : 3}" stroke-dasharray="8 8"/>` : '';
  const dot = series.fireX != null ? (() => { const p = series.pts.reduce((b, q) => (Math.abs(q.x - series.fireX) < Math.abs(b.x - series.fireX) ? q : b)); return `<circle cx="${(x + p.x * w).toFixed(1)}" cy="${(y + h - p.y * h).toFixed(1)}" r="${opts.thin ? 8 : 11}" fill="#ff5a00" stroke="#18191d" stroke-width="4"/>`; })() : '';
  return `<path d="${area}" fill="#ff5a00" fill-opacity="0.16"/><path d="${line}" fill="none" stroke="#ff5a00" stroke-width="${opts.thin ? 5 : 7}" stroke-linejoin="round" stroke-linecap="round"/>${fireLine}${dot}`;
}
function certText(opts) {
  const esc = (v) => String(v == null ? '' : v).replace(/[<>&"]/g, '').slice(0, 40);
  const ea = Number(opts.ea) || 0; const tgt = Number(opts.target) || 0;
  const gap = ea && tgt ? tgt - ea : null;
  const big = ea ? `${ea}세` : '아직';
  const line1 = !ea ? '파이어 준비 중' : gap == null ? '파이어 가능 나이' : gap > 0 ? `목표보다 ${gap}년 빨라요` : gap < 0 ? `목표보다 ${-gap}년 늦어요` : '목표와 같아요';
  // 태어난 해는 앱이 묻지 않는다(연도-나이 추정은 한 해 틀릴 수 있어 뺐다). 입력한 현재 나이를 그대로 적는다.
  const cur = Number(opts.cur) || 0;
  const title = `${cur ? `현재 ${cur}세` : `${esc(opts.year)}년생`} · ${esc(opts.round) || 1}회차`;
  const stats = [[`${ea || tgt}세 때 자산`, esc(opts.need)], ['현재 자산', esc(opts.asset)], ['월 저축액', esc(opts.save)]];
  const assume = `파이어 후 월 생활비 ${esc(opts.cost)} · 수익률 ${esc(opts.ret)}% · 물가 ${esc(opts.inf)}% · 연금 ${esc(opts.pen)}세~`;
  return { esc, ea, tgt, big, line1, title, stats, assume };
}
const LOGO = (x, y, w, h) => `<svg x="${x}" y="${y}" width="${w}" height="${h}" viewBox="188 84 136 276"><path d="M256 84 C 232 150, 188 172, 188 256 C 188 322, 218 360, 256 360 C 294 360, 324 322, 324 256 C 324 212, 300 188, 286 162 C 282 192, 268 204, 252 210 C 268 166, 262 116, 256 84 Z" fill="#ff5a00"/><path d="M256 250 C 246 276, 232 286, 232 312 C 232 336, 242 352, 256 352 C 270 352, 280 336, 280 312 C 280 292, 270 280, 264 268 C 262 282, 258 286, 252 290 C 258 274, 258 262, 256 250 Z" fill="#fdba74"/></svg>`;

// 세로판 1080×1350 (인스타·카페 게시판)
export function buildCertSvg(opts = {}) {
  const font = opts.font || 'Pretendard';
  const t = certText(opts);
  const statsSvg = t.stats.map(([k, v], i) => {
    const x = 80 + i * 320;
    return `${i ? `<line x1="${x - 20}" y1="1010" x2="${x - 20}" y2="1090" stroke="#ffffff" stroke-opacity="0.14" stroke-width="2"/>` : ''}
<text x="${x}" y="1030" font-family="${font}" font-weight="600" font-size="26" fill="#9aa0a8">${k}</text>
<text x="${x}" y="1084" font-family="${font}" font-weight="700" font-size="44" fill="#ffffff">${v}</text>`;
  }).join('\n');
  return `<svg width="1080" height="1350" viewBox="0 0 1080 1350" xmlns="http://www.w3.org/2000/svg">
<rect width="1080" height="1350" rx="0" fill="#18191d"/>
${LOGO(80, 84, 40, 80)}
<text x="134" y="140" font-family="${font}" font-weight="700" font-size="40" fill="#ffffff">파이어맵</text>
<text x="1000" y="140" font-family="${font}" font-weight="600" font-size="30" fill="#9aa0a8" text-anchor="end">${t.title}</text>
<text x="80" y="290" font-family="${font}" font-weight="600" font-size="34" fill="#9aa0a8">파이어 가능 나이</text>
<text x="80" y="480" font-family="${font}" font-weight="700" font-size="200" fill="#ff5a00">${t.big}</text>
<text x="80" y="560" font-family="${font}" font-weight="700" font-size="46" fill="#ffffff">${t.line1}</text>
${curveSvg(opts.series, { x: 80, y: 640, w: 920, h: 300 })}
<line x1="80" y1="980" x2="1000" y2="980" stroke="#ffffff" stroke-opacity="0.14" stroke-width="2"/>
${statsSvg}
<text x="80" y="1170" font-family="${font}" font-weight="500" font-size="26" fill="#9aa0a8">${t.assume}</text>
<text x="80" y="1270" font-family="${font}" font-weight="600" font-size="28" fill="#9aa0a8">계산: firemap.kr</text>
<text x="1000" y="1270" font-family="${font}" font-weight="700" font-size="32" fill="#ff5a00" text-anchor="end">firemap.kr</text>
</svg>`;
}

// 가로판 1200×630 (카카오톡·링크 미리보기). 내용은 세로판과 같다.
export function buildCertWideSvg(opts = {}) {
  const font = opts.font || 'Pretendard';
  const t = certText(opts);
  const statsSvg = t.stats.map(([k, v], i) => {
    const y = 300 + i * 96;
    return `<text x="700" y="${y}" font-family="${font}" font-weight="600" font-size="22" fill="#9aa0a8">${k}</text>
<text x="1130" y="${y}" font-family="${font}" font-weight="700" font-size="36" fill="#ffffff" text-anchor="end">${v}</text>
<line x1="700" y1="${y + 26}" x2="1130" y2="${y + 26}" stroke="#ffffff" stroke-opacity="0.12" stroke-width="2"/>`;
  }).join('\n');
  return `<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
<rect width="1200" height="630" fill="#18191d"/>
${LOGO(70, 56, 30, 60)}
<text x="110" y="98" font-family="${font}" font-weight="700" font-size="30" fill="#ffffff">파이어맵</text>
<text x="1130" y="98" font-family="${font}" font-weight="600" font-size="24" fill="#9aa0a8" text-anchor="end">${t.title}</text>
<text x="70" y="196" font-family="${font}" font-weight="600" font-size="26" fill="#9aa0a8">파이어 가능 나이</text>
<text x="70" y="346" font-family="${font}" font-weight="700" font-size="160" fill="#ff5a00">${t.big}</text>
<text x="70" y="404" font-family="${font}" font-weight="700" font-size="36" fill="#ffffff">${t.line1}</text>
${curveSvg(opts.series, { x: 70, y: 430, w: 560, h: 120 }, { thin: true })}
${statsSvg}
<text x="70" y="590" font-family="${font}" font-weight="500" font-size="20" fill="#9aa0a8">${t.assume}</text>
<text x="1130" y="590" font-family="${font}" font-weight="700" font-size="26" fill="#ff5a00" text-anchor="end">firemap.kr</text>
</svg>`;
}

// 카페 글에 붙이는 대표 이미지 — 제목 한 줄과 숫자 3줄. 네이버 검색 결과에 썸네일로 걸린다.
// 글자는 og-fonts-pd 서브셋에 들어 있어야 그려진다(work/gen-og-fonts.py가 cafePosts.js도 훑는다).
export function buildPostSvg(opts = {}) {
  const font = opts.font || 'Pretendard';
  const esc = (v) => String(v == null ? '' : v).replace(/[<>&"]/g, '').slice(0, 44);
  const title = esc(opts.title);
  const lines = (opts.lines || []).slice(0, 3).map(esc).filter(Boolean);
  const ts = fitFont(title, 54, 1060, 34);
  const rows = lines.map((ln, i) => {
    const [k, v] = ln.split('|');
    const y = 380 + i * 74;
    return v == null
      ? `<text x="70" y="${y}" font-family="${font}" font-weight="600" font-size="30" fill="#d6d9de">${k}</text>`
      : `<text x="70" y="${y}" font-family="${font}" font-weight="600" font-size="30" fill="#9aa0a8">${k}</text>
<text x="1130" y="${y}" font-family="${font}" font-weight="700" font-size="40" fill="#ffffff" text-anchor="end">${v}</text>
<line x1="70" y1="${y + 24}" x2="1130" y2="${y + 24}" stroke="#ffffff" stroke-opacity="0.12" stroke-width="2"/>`;
  }).join('\n');
  return `<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
<rect width="1200" height="630" fill="#18191d"/>
${LOGO(70, 56, 30, 60)}
<text x="110" y="98" font-family="${font}" font-weight="700" font-size="30" fill="#ffffff">파이어맵</text>
<text x="70" y="232" font-family="${font}" font-weight="700" font-size="${ts}" fill="#ff5a00">${title}</text>
<line x1="70" y1="290" x2="1130" y2="290" stroke="#ffffff" stroke-opacity="0.14" stroke-width="3"/>
${rows}
<text x="1130" y="590" font-family="${font}" font-weight="700" font-size="26" fill="#ff5a00" text-anchor="end">firemap.kr</text>
</svg>`;
}
