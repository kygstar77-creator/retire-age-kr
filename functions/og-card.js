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
// opts: { year, family, ea, target, need(억 문자열), asset(억 문자열|'비공개'), save(만 문자열|'비공개'), cost, ret, inf, pen, round, font }
export function buildCertSvg(opts = {}) {
  const font = opts.font || 'Noto Sans CJK KR';
  const esc = (v) => String(v == null ? '' : v).replace(/[<>&"]/g, '').slice(0, 40);
  const title = `${esc(opts.year)}년생 ${esc(opts.family)} · ${esc(opts.round) || 1}회차`;
  const ea = Number(opts.ea) || 0;
  const big = ea ? `${ea}세` : '아직';
  const line1 = ea ? `${ea}세에 파이어 가능` : '파이어 준비 중';
  const rows = [
    ['필요 자산', esc(opts.need)], ['지금 자산', esc(opts.asset)], ['월 저축', esc(opts.save)], ['파이어 후 생활비', esc(opts.cost)],
    ['목표 나이', `${Number(opts.target) || 0}세`], ['가정', `수익률 ${esc(opts.ret)}% · 물가 ${esc(opts.inf)}% · 연금 ${esc(opts.pen)}세~`]
  ];
  const rowsSvg = rows.map(([k, v], i) => {
    const y = 700 + i * 92;
    return `<rect x="80" y="${y - 54}" width="920" height="78" rx="18" fill="rgba(255,255,255,0.06)"/>
<text x="112" y="${y}" font-family="${font}" font-weight="600" font-size="30" fill="#9aa4d4">${k}</text>
<text x="968" y="${y}" font-family="${font}" font-weight="700" font-size="${i === 5 ? 26 : 36}" fill="#ffffff" text-anchor="end">${v}</text>`;
  }).join('\n');
  return `<svg width="1080" height="1350" viewBox="0 0 1080 1350" xmlns="http://www.w3.org/2000/svg">
<rect width="1080" height="1350" fill="#18224d"/>
<rect x="0" y="0" width="1080" height="14" fill="#ff5a00"/>
<svg x="80" y="80" width="44" height="88" viewBox="188 84 136 276"><path d="M256 84 C 232 150, 188 172, 188 256 C 188 322, 218 360, 256 360 C 294 360, 324 322, 324 256 C 324 212, 300 188, 286 162 C 282 192, 268 204, 252 210 C 268 166, 262 116, 256 84 Z" fill="#ff5a00"/><path d="M256 250 C 246 276, 232 286, 232 312 C 232 336, 242 352, 256 352 C 270 352, 280 336, 280 312 C 280 292, 270 280, 264 268 C 262 282, 258 286, 252 290 C 258 274, 258 262, 256 250 Z" fill="#fdba74"/></svg>
<text x="140" y="140" font-family="${font}" font-weight="700" font-size="44" fill="#ffffff">파이어맵 인증 카드</text>
<text x="80" y="250" font-family="${font}" font-weight="600" font-size="36" fill="#9aa4d4">${title}</text>
<text x="80" y="440" font-family="${font}" font-weight="700" font-size="180" fill="#ff5a00">${big}</text>
<text x="80" y="520" font-family="${font}" font-weight="700" font-size="48" fill="#ffffff">${line1}</text>
${rowsSvg}
<text x="80" y="1290" font-family="${font}" font-weight="600" font-size="28" fill="#9aa4d4">참고용 계산 · 검증 firemap.kr</text>
<text x="1000" y="1290" font-family="${font}" font-weight="700" font-size="30" fill="#ff8a4c" text-anchor="end">firemap.kr</text>
</svg>`;
}
